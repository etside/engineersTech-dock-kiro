import sys, os, re, subprocess, time, random, json
from pathlib import Path
from PyQt6.QtGui import QPixmap, QTransform, QIcon
from PyQt6.QtCore import Qt, QTimer, QRect, QPoint, pyqtSignal, QThread, QObject
from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QSystemTrayIcon, QMenu,
                              QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
                              QScrollArea, QFrame, QProgressBar)

KIRO = os.path.expanduser("~/.local/bin/kiro-cli")
BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = Path.home() / ".config" / "kiro-dock" / "config.json"

# Default configuration
DEFAULT_CONFIG = {
    "position": "bottom",
    "animation_speed": "normal",
    "custom_assets_dir": None,
    "assets": {
        "walk_sheet": "sheet2.png",
        "idle_sheet": "anims.png",
        "fallback_icon": "icon.png"
    }
}

def load_config():
    """Load configuration from file or return defaults"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load config: {e}")
    return DEFAULT_CONFIG

CONFIG = load_config()

_ANSI = re.compile(r'\x1b\[[0-9;?]*[A-Za-z]|\x1b\].*?(?:\x07|\x1b\\)')
_NOISE = re.compile(
    r'^\s*$'                          # blank
    r'|▸\s*Credits'                   # credits/time line
    r'|^\s*>\s*$'                     # bare prompt marker
    r'|\x1b\[\?25[lh]'               # cursor show/hide
    r'|\x1b\[1G'                      # carriage return escape
)

def _clean(line):
    """Strip ANSI and return None if the line is noise."""
    s = _ANSI.sub('', line).strip()
    # strip leading "> " prompt prefix kiro adds
    s = re.sub(r'^>\s+', '', s)
    return None if not s or _NOISE.search(line) else s


def _is_authed():
    try:
        r = subprocess.run([KIRO, "whoami"], capture_output=True, text=True, timeout=5)
        return r.returncode == 0 and "Logged in" in r.stdout
    except Exception:
        return False


def screen_size():
    s = QApplication.primaryScreen()
    return s.geometry().width(), s.availableGeometry().bottom() + 1


def get_animation_speed_multiplier(speed):
    """Convert speed config to velocity multiplier"""
    speeds = {"slow": 15.0, "normal": 30.0, "fast": 60.0}
    return speeds.get(speed, 30.0)


def get_initial_position(position, width, height):
    """Calculate initial position based on config"""
    sw, sh = screen_size()
    
    if position == "bottom":
        return 0.0, float(sh - height)
    elif position == "top":
        return 0.0, 0.0
    elif position == "center":
        return float((sw - width) // 2), float((sh - height) // 2)
    elif position == "top-left":
        return 0.0, 0.0
    elif position == "top-right":
        return float(sw - width), 0.0
    else:  # default to bottom
        return 0.0, float(sh - height)


def get_asset_path(filename):
    """Load asset from custom directory or fallback to BASE"""
    custom_dir = CONFIG.get("custom_assets_dir")
    
    if custom_dir and os.path.exists(custom_dir):
        custom_path = os.path.join(custom_dir, filename)
        if os.path.exists(custom_path):
            return custom_path
    
    # Fallback to BASE directory
    return os.path.join(BASE, filename)


# ── Background Kiro worker ───────────────────────────────────────────────────
class KiroWorker(QObject):
    line_out = pyqtSignal(str)
    progress = pyqtSignal(int)
    done     = pyqtSignal(int)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        self.progress.emit(5)
        try:
            proc = subprocess.Popen(
                [KIRO, "chat", "--no-interactive", self.prompt],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )
            n = 0
            for raw in proc.stdout:
                self.line_out.emit(raw.rstrip("\n"))
                n += 1
                self.progress.emit(min(90, 5 + n * 3))
            proc.wait()
            self.progress.emit(100)
            self.done.emit(proc.returncode)
        except FileNotFoundError:
            self.line_out.emit(f"⚠  kiro-cli not found at {KIRO}")
            self.done.emit(1)
        except Exception as e:
            self.line_out.emit(f"Error: {e}")
            self.done.emit(1)


# ── Chat popup ───────────────────────────────────────────────────────────────
class ChatPopup(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.Tool |
                            Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedWidth(360)
        self._dp = None
        self._thread = None
        self._build()

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet("QFrame#card{background:rgba(10,10,16,240);border-radius:20px;"
                           "border:1px solid rgba(255,255,255,0.08);}")
        v = QVBoxLayout(card)
        v.setContentsMargins(14, 12, 14, 12)
        v.setSpacing(8)

        # header
        hdr = QHBoxLayout()
        dot = QLabel("⬤"); dot.setStyleSheet("color:#a78bfa;font-size:9px;")
        ttl = QLabel("Kiro"); ttl.setStyleSheet("color:#e2e8f0;font-weight:700;font-size:14px;")
        xb  = QPushButton("✕"); xb.setFixedSize(22, 22)
        xb.setStyleSheet("QPushButton{background:rgba(255,255,255,0.07);color:#555;"
                         "border-radius:11px;border:none;font-size:11px;}"
                         "QPushButton:hover{background:rgba(220,50,50,0.6);color:white;}")
        xb.clicked.connect(self.hide)
        hdr.addWidget(dot); hdr.addWidget(ttl); hdr.addStretch(); hdr.addWidget(xb)
        v.addLayout(hdr)

        # auth banner (shown only when not logged in)
        self._auth_banner = QFrame()
        self._auth_banner.setStyleSheet(
            "QFrame{background:rgba(124,58,237,0.18);border-radius:10px;"
            "border:1px solid rgba(124,58,237,0.4);}")
        ab = QVBoxLayout(self._auth_banner)
        ab.setContentsMargins(10, 8, 10, 8); ab.setSpacing(6)
        ab.addWidget(QLabel("⚠  Not logged in to Kiro",
                            styleSheet="color:#c4b5fd;font-size:12px;"))
        login_btn = QPushButton("Login with Kiro CLI")
        login_btn.setStyleSheet(
            "QPushButton{background:#7c3aed;color:white;border-radius:10px;"
            "border:none;padding:6px 12px;font-size:12px;}"
            "QPushButton:hover{background:#6d28d9;}")
        login_btn.clicked.connect(self._do_login)
        ab.addWidget(login_btn)
        v.addWidget(self._auth_banner)
        self._auth_banner.setVisible(not _is_authed())

        # scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(240)
        self.scroll.setStyleSheet("QScrollArea{border:none;background:transparent;}"
                                  "QScrollBar:vertical{width:3px;background:transparent;}"
                                  "QScrollBar::handle:vertical{background:rgba(255,255,255,0.15);"
                                  "border-radius:2px;}")
        self.msg_w = QWidget(); self.msg_w.setStyleSheet("background:transparent;")
        self.msg_l = QVBoxLayout(self.msg_w)
        self.msg_l.setContentsMargins(0, 0, 0, 0); self.msg_l.setSpacing(6)
        self.msg_l.addStretch()
        self.scroll.setWidget(self.msg_w)
        v.addWidget(self.scroll)

        # progress bar
        self.bar = QProgressBar()
        self.bar.setFixedHeight(3); self.bar.setTextVisible(False)
        self.bar.setRange(0, 100); self.bar.setValue(0)
        self.bar.setStyleSheet("QProgressBar{background:rgba(255,255,255,0.06);"
                               "border-radius:2px;border:none;}"
                               "QProgressBar::chunk{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,"
                               "stop:0 #7c3aed,stop:1 #a78bfa);border-radius:2px;}")
        self.bar.hide(); v.addWidget(self.bar)

        # input
        row = QHBoxLayout()
        self.inp = QLineEdit(); self.inp.setPlaceholderText("Ask Kiro…")
        self.inp.setStyleSheet("QLineEdit{background:rgba(255,255,255,0.07);"
                               "border:1px solid rgba(255,255,255,0.10);border-radius:14px;"
                               "color:white;padding:8px 14px;font-size:13px;}"
                               "QLineEdit:focus{border-color:#7c3aed;}")
        self.inp.returnPressed.connect(self.send)
        btn = QPushButton("↑"); btn.setFixedSize(34, 34)
        btn.setStyleSheet("QPushButton{background:#7c3aed;color:white;border-radius:17px;"
                          "border:none;font-size:17px;font-weight:bold;}"
                          "QPushButton:hover{background:#6d28d9;}")
        btn.clicked.connect(self.send)
        row.addWidget(self.inp); row.addWidget(btn)
        v.addLayout(row)
        outer.addWidget(card)

    def _scroll_bottom(self):
        QTimer.singleShot(30, lambda: self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()))

    def _bubble(self, text, role):
        b = QLabel(text); b.setWordWrap(True)
        b.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        if role == "user":
            b.setStyleSheet("background:#7c3aed;color:white;border-radius:12px;"
                            "padding:8px 12px;font-size:12px;")
            b.setAlignment(Qt.AlignmentFlag.AlignRight)
        elif role == "ai":
            b.setStyleSheet("background:rgba(255,255,255,0.07);color:#e2e8f0;"
                            "border-radius:12px;padding:8px 12px;font-size:12px;")
        else:
            b.setStyleSheet("color:#475569;font-size:11px;padding:2px 4px;")
            b.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg_l.insertWidget(self.msg_l.count() - 1, b)
        self._scroll_bottom()
        return b

    def _do_login(self):
        """Open a terminal for kiro-cli login, then recheck auth."""
        for term in ("gnome-terminal", "xterm", "konsole", "xfce4-terminal"):
            if subprocess.run(["which", term], capture_output=True).returncode == 0:
                subprocess.Popen([term, "--", KIRO, "login"])
                break
        # recheck after 10 s
        QTimer.singleShot(10000, lambda: self._auth_banner.setVisible(not _is_authed()))

    def send(self):
        text = self.inp.text().strip()
        if not text or (self._thread and self._thread.isRunning()):
            return
        self.inp.clear()
        self._bubble(text, "user")
        self.bar.setValue(0); self.bar.show()
        self._rb = self._bubble("…", "ai")
        self._lines = []

        self._thread = QThread()
        self._worker = KiroWorker(text)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.line_out.connect(self._on_line)
        self._worker.progress.connect(self.bar.setValue)
        self._worker.done.connect(self._on_done)
        self._worker.done.connect(self._thread.quit)
        self._thread.start()

    def _on_line(self, line):
        s = _clean(line)
        if s:
            self._lines.append(s)
            self._rb.setText("\n".join(self._lines[-30:]))
            self._scroll_bottom()

    def _on_done(self, code):
        self.bar.hide()
        self._bubble("✓ Done" if code == 0 else f"✗ Exited ({code})", "sys")

    def show_near(self, ax, ay, sprite_w=100):
        sw, _ = screen_size()
        # centre popup over sprite head
        x = int(ax) + sprite_w // 2 - self.width() // 2
        x = max(0, min(x, sw - self.width() - 4))
        # place bottom of popup 4px above sprite top (ay = sprite top-left y)
        y = int(ay) - self.height() - 4
        if y < 0:  # not enough room above — go below sprite
            y = int(ay) + sprite_w + 4
        self.move(x, y); self.show(); self.raise_()
        self.inp.setFocus()

    # draggable
    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._dp = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self._dp and e.buttons() == Qt.MouseButton.LeftButton:
            self.move(e.globalPosition().toPoint() - self._dp)

    def mouseReleaseEvent(self, e):
        self._dp = None


# ── Draggable sprite ─────────────────────────────────────────────────────────
class DesktopAgent(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.Tool |
                            Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)

        SZ = 100
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("background:transparent;")
        self.label.setMouseTracking(True)
        self.label.setCursor(Qt.CursorShape.OpenHandCursor)
        # Route ALL mouse events through the label (it's the visible surface)
        self.label.mousePressEvent   = self._press
        self.label.mouseMoveEvent    = self._move
        self.label.mouseReleaseEvent = self._release

        T = QTransform().scale(-1, 1)

        def load_sheet(path, cxs, cys, w, h):
            px = QPixmap(path); r, l = [], []
            for cy in cys:
                for cx in cxs:
                    f = px.copy(QRect(cx-w//2, cy-h//2, w, h)).scaledToHeight(
                        SZ, Qt.TransformationMode.SmoothTransformation)
                    r.append(f)
                    l.append(f.transformed(T, Qt.TransformationMode.SmoothTransformation))
            return r, l

        s2 = get_asset_path('sheet2.png')
        sp = get_asset_path('sprite.png')
        an = get_asset_path('anims.png')
        ic = get_asset_path('icon.png')

        self.fr = self.fl = self.ir = self.il = []
        self.icon_path = ""
        self._last_px = None

        if os.path.exists(s2):
            self.icon_path = s2
            self.fr, self.fl = load_sheet(s2, [80,224,366], [168,419], 150, 220)
        elif os.path.exists(sp):
            self.icon_path = sp
            px = QPixmap(sp).scaledToHeight(SZ, Qt.TransformationMode.SmoothTransformation)
            self.fr = [px]; self.fl = [px.transformed(T, Qt.TransformationMode.SmoothTransformation)]

        if os.path.exists(an):
            self.ir, self.il = load_sheet(an, [80,231,375], [172,430], 150, 220)

        if self.fr:
            self._show(self.fr[0])
            self.aw, self.ah = self.fr[0].width(), self.fr[0].height()
        else:
            self.aw = self.ah = SZ
            self.label.setText("🤖")
            self.label.setStyleSheet("background:transparent;font-size:40px;")

        self.label.resize(self.aw, self.ah)
        self.resize(self.aw, self.ah)

        sw, sb = screen_size()
        self.sw = sw
        # Use configured position instead of hardcoded bottom
        self.ax, self.ay = get_initial_position(CONFIG.get("position", "bottom"), self.aw, self.ah)
        self.move(int(self.ax), int(self.ay))

        # walk state - use speed from config
        self.dir = 1
        self.vel = get_animation_speed_multiplier(CONFIG.get("animation_speed", "normal"))
        self.last_t = time.time()
        self.state = 'WALKING'; self.st = 0.0; self.sd = random.uniform(3, 8)
        self.cf = 0; self.at = 0.0
        self.bo = 0.0; self.bu = True

        # drag state
        self._drag = False; self._ds = QPoint(); self._do = QPoint()

        self.popup = ChatPopup()

        self._walk_timer = QTimer(self); self._walk_timer.timeout.connect(self._tick)
        self._walk_timer.start(16)
        QTimer(self, timeout=self._env_check, interval=500).start()

        self._setup_tray()
        self._config_pos = CONFIG.get("position", "bottom")  # Track configured position

    def paintEvent(self, e):
        pass  # fully transparent — label handles all drawing

    def _show(self, px):
        if px is self._last_px:
            return
        self._last_px = px
        self.label.setPixmap(px)

    def _setup_tray(self):
        def px_to_icon(px):
            return QIcon(px.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation))
        self._tray_icons_r = [px_to_icon(p) for p in self.fr] if self.fr else []
        self._tray_icons_l = [px_to_icon(p) for p in self.fl] if self.fl else []
        fallback = self._tray_icons_r[0] if self._tray_icons_r else QIcon()
        self.tray = QSystemTrayIcon(fallback, self)
        self.tray.setToolTip("Kiro Dock")
        m = QMenu()
        m.addAction("Chat", lambda: self.popup.show_near(self.ax, self.ay, self.aw))
        m.addSeparator()
        sm = m.addMenu("Speed")
        sm.addAction("Slow",   lambda: setattr(self, 'vel', 15.0))
        sm.addAction("Normal", lambda: setattr(self, 'vel', 30.0))
        sm.addAction("Fast",   lambda: setattr(self, 'vel', 60.0))
        m.addSeparator()
        m.addAction("Exit", QApplication.quit)
        self.tray.setContextMenu(m); self.tray.show()

    def _env_check(self):
        self.sw, sb = screen_size()
        if not self._drag:
            # Snap back to configured position if user hasn't dragged it
            target_x, target_y = get_initial_position(self._config_pos, self.aw, self.ah)
            if abs(self.ax - target_x) < 5 and abs(self.ay - target_y) < 5:
                self.ax = target_x
                self.ay = target_y

    # ── drag ────────────────────────────────────────────────────────────────
    def _press(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag = True
            self._ds   = e.globalPosition().toPoint()
            self._do   = self.pos()
            self.label.setCursor(Qt.CursorShape.ClosedHandCursor)
            self._walk_timer.stop()

    def _move(self, e):
        if self._drag:
            delta = e.globalPosition().toPoint() - self._ds
            p = self._do + delta
            self.ax = float(p.x())
            self.ay = float(p.y())
            self.move(p)

    def _release(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            moved = (e.globalPosition().toPoint() - self._ds).manhattanLength()
            self._drag = False
            self.label.setCursor(Qt.CursorShape.OpenHandCursor)
            self._walk_timer.start(16)
            if moved < 6:
                self.popup.show_near(self.ax, self.ay, self.aw)

    # ── animation tick ───────────────────────────────────────────────────────
    def _tick(self):
        now = time.time(); dt = min(now - self.last_t, 0.1); self.last_t = now
        self.st += dt

        if self.st >= self.sd:
            self.st = 0.0
            if self.state == 'WALKING':
                self.state = 'IDLE'; self.sd = random.uniform(2, 6)
                fl = self.ir if self.dir == 1 else self.il
                if not fl: fl = self.fr if self.dir == 1 else self.fl
                if fl: self._show(fl[random.randint(0, len(fl)-1)])
            else:
                self.state = 'WALKING'; self.sd = random.uniform(4, 10)

        flipped = False
        if self.state == 'WALKING':
            self.ax += self.vel * self.dir * dt
            if len(self.fr) > 1:
                self.at += dt
                if self.at >= 0.15:
                    self.at = 0.0; self.cf = (self.cf + 1) % len(self.fr)
            if self.bu:
                self.bo += 10 * dt
                if self.bo >= 3: self.bu = False
            else:
                self.bo -= 10 * dt
                if self.bo <= 0: self.bu = True
        else:
            if self.bo > 0: self.bo = max(0.0, self.bo - 10 * dt)

        # Constrain movement based on position
        pos = self._config_pos
        if pos == "center" or pos == "top":
            # Vertical constraints for center/top positions - can't move vertically
            pass
        elif pos == "top-left" or pos == "top-right":
            # Fixed position modes - don't move
            pass
        else:
            # Bottom position (default) - allow horizontal movement
            if self.ax <= 0:
                self.ax = 0; self.dir = 1; flipped = True
            elif self.ax >= self.sw - self.aw:
                self.ax = self.sw - self.aw; self.dir = -1; flipped = True

        if self.fr and (self.state == 'WALKING' or flipped):
            fl = self.fr if self.dir == 1 else self.fl
            self._show(fl[self.cf % len(fl)])
            # sync tray icon to current walk frame
            ti = self._tray_icons_r if self.dir == 1 else self._tray_icons_l
            if ti:
                self.tray.setIcon(ti[self.cf % len(ti)])

        self.move(int(self.ax), int(self.ay - self.bo))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    agent = DesktopAgent()
    agent.show()
    sys.exit(app.exec())
