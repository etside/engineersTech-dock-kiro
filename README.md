# 🚀 Kiro Dock — Advanced Desktop Agent

> An animated, interactive desktop dock powered by **Kiro CLI**. Walk, chat, and customize! 

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

- **🎬 Animated Desktop Agent** — Walks and idles smoothly across your screen
- **📍 Configurable Position** — Choose bottom, top, center, top-left, or top-right placement
- **💬 Built-in Chat** — Click to open Kiro CLI chat popup with real-time streaming
- **🎨 Custom Assets** — Use your own sprites, animations, and icons
- **⚡ Adjustable Speed** — Control animation speed (slow, normal, fast)
- **🎵 Tray Integration** — Synchronized tray icon with walking animation
- **🖱️ Draggable** — Move the agent and popup anywhere on screen
- **✅ Auto-login** — Optional auto-start on login

---

## 📋 System Requirements

- **OS:** Linux with X11 or Wayland (with XWayland)
- **Python:** 3.10 or later
- **Desktop:** GNOME, KDE, XFCE, or any X11-compatible environment

### Required Dependencies

```
PyQt6>=6.7.1
Pillow>=10.4.0
```

### Optional Dependencies

- **Kiro CLI** — For AI chat functionality ([Installation Guide](https://kiro.dev))

---

## 🛠️ Installation Guide

### Step 1: Clone or Download Repository

```bash
# Using Git
git clone https://github.com/yourusername/engineersTech-dock-kiro.git
cd engineersTech-dock-kiro

# Or download and extract ZIP
unzip engineersTech-dock-kiro.zip
cd engineersTech-dock-kiro
```

### Step 2: Install Dependencies

```bash
# Option A: Using Virtual Environment (Recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# Option B: System-wide Installation
sudo apt install python3-pyqt6 python3-pil  # Debian/Ubuntu
# Or use your package manager
```

### Step 3: Install Kiro CLI (Required for Chat)

```bash
# Visit https://kiro.dev for detailed instructions
# Typical installation:
kiro install

# Verify installation
kiro whoami
```

### Step 4: Run the Installer

```bash
# Make installer executable
chmod +x install.sh

# Run installation
./install.sh
```

This will:
- Copy application files to `~/.local/share/kiro-dock/`
- Create launcher scripts in `~/.local/bin/`
- Register desktop entry for app launcher
- Create configuration directory

### Step 5: Configure the Dock

```bash
# Launch setup wizard
kiro-dock-setup
```

**Configuration Options:**

1. **Choose Dock Position**
   - Bottom (default) — Walks at screen bottom
   - Top — Walks at screen top
   - Center — Stationary in center
   - Top-left — Fixed in top-left corner
   - Top-right — Fixed in top-right corner

2. **Animation Speed**
   - Slow (2x slower)
   - Normal (default)
   - Fast (1.5x faster)

3. **Custom Assets** (Optional)
   - Provide path to custom sprite/animation directory
   - Leave blank for default assets

4. **Auto-start**
   - Enable automatic startup on login

5. **Verify Kiro CLI**
   - Check if Kiro CLI is properly installed

---

## 🚀 Running the Dock

### Start Immediately

```bash
kiro-dock
```

### Start in Background

```bash
kiro-dock &
```

### Run with Virtual Environment

```bash
source ~/.local/share/kiro-dock/.venv/bin/activate
python ~/.local/share/kiro-dock/main.py
```

### Start with DISPLAY Variable (Headless)

```bash
DISPLAY=:0 kiro-dock &
```

### Launch from Application Menu

Find "Kiro Dock" in your system application launcher.

---

## 📦 Custom Assets & Animations

### Asset Directory Structure

Create a custom assets directory with the following structure:

```
my-assets/
├── sheet2.png       # Walk animation sprite sheet
├── anims.png        # Idle animation sprite sheet
├── sprite.png       # Fallback static sprite
└── icon.png         # Application icon
```

### Sprite Sheet Specifications

#### Walk Sheet (sheet2.png)
- **Grid:** 3 columns × 2 rows
- **Frame Size:** 150×220 pixels
- **Format:** PNG with transparency
- **Coordinates:**
  - Frame 1: x=80, y=168
  - Frame 2: x=224, y=168
  - Frame 3: x=366, y=168
  - Frame 4: x=80, y=419
  - Frame 5: x=224, y=419
  - Frame 6: x=366, y=419

#### Idle Sheet (anims.png)
- **Grid:** 3 columns × 2 rows
- **Frame Size:** 150×220 pixels
- **Format:** PNG with transparency

#### Fallback Sprite (sprite.png)
- **Size:** Any (will be scaled to 100×100px)
- **Format:** PNG with transparency

#### Icon (icon.png)
- **Size:** 256×256 pixels recommended
- **Format:** PNG

### Using Custom Assets

1. Create custom assets directory:
   ```bash
   mkdir -p ~/custom-dock-assets
   # Add your PNG files to this directory
   ```

2. Run setup wizard and provide the path when prompted:
   ```bash
   kiro-dock-setup
   # When asked for custom assets, enter: ~/custom-dock-assets
   ```

3. Restart the dock:
   ```bash
   kiro-dock
   ```

---

## 🎮 Usage & Controls

### Mouse Controls

| Action | Effect |
|--------|--------|
| **Left-Click** | Open Kiro chat popup |
| **Drag** | Move agent anywhere (temp) |
| **Double-Click** | Same as single click |

### Right-Click Menu (Tray Icon)

- **Chat** — Open chat popup
- **Speed** — Adjust animation speed
  - Slow
  - Normal
  - Fast
- **Exit** — Close the dock

### Keyboard Shortcuts (Chat Popup)

| Shortcut | Effect |
|----------|--------|
| **Enter** | Send message |
| **Ctrl+C** | Close popup |
| **Esc** | Close popup |

### Configuration Changes

To reconfigure the dock:

```bash
kiro-dock-setup
```

Configuration is saved to: `~/.config/kiro-dock/config.json`

---

## ⚙️ Configuration File

Location: `~/.config/kiro-dock/config.json`

Example:
```json
{
  "position": "bottom",
  "animation_speed": "normal",
  "custom_assets_dir": null,
  "assets": {
    "walk_sheet": "sheet2.png",
    "idle_sheet": "anims.png",
    "fallback_icon": "icon.png"
  },
  "auto_start": false
}
```

### Configuration Options

| Setting | Values | Default | Description |
|---------|--------|---------|-------------|
| `position` | bottom, top, center, top-left, top-right | bottom | Dock position |
| `animation_speed` | slow, normal, fast | normal | Animation speed |
| `custom_assets_dir` | path or null | null | Custom assets directory |
| `auto_start` | true/false | false | Auto-start on login |

---

## 🔧 Troubleshooting

### Issue: "kiro-cli not found"

**Solution:**
```bash
# Install Kiro CLI
kiro install

# Or manually set path in ~/.config/kiro-dock/config.json
# Ensure ~/.local/bin/kiro-cli exists
which kiro-cli
```

### Issue: No Animation or Black Screen

**Solution:**
```bash
# Check asset files exist
ls -la ~/.local/share/kiro-dock/*.png

# Use emoji fallback (🤖 will appear)
# Or provide custom assets via kiro-dock-setup
```

### Issue: Window Not Appearing

**Solution:**
```bash
# Check DISPLAY variable
echo $DISPLAY

# Run with explicit display
DISPLAY=:0 kiro-dock

# Check for running instances
ps aux | grep kiro-dock
```

### Issue: Chat Not Working

**Solution:**
```bash
# Verify Kiro CLI authentication
kiro whoami

# Login to Kiro
kiro login

# Check Kiro is accessible
~/.local/bin/kiro-cli chat --no-interactive "Hello"
```

### Issue: High CPU Usage

**Solution:**
```bash
# Reduce animation speed
kiro-dock-setup  # Choose "Slow"

# Close unused popup windows
```

### Issue: Permission Denied on install.sh

**Solution:**
```bash
chmod +x install.sh
./install.sh
```

---

## 🔌 Kiro CLI Integration

### Authentication

The dock requires Kiro CLI authentication for chat functionality:

```bash
# Login to Kiro
kiro login

# Verify login status
kiro whoami

# If not authenticated, login prompt appears in dock
```

### Chat Functionality

- **First Use:** Click the agent to open chat popup
- **Auth Banner:** Shows if not logged in
- **Real-time Streaming:** Responses stream character by character
- **Progress Bar:** Shows AI response generation progress

### Kiro CLI Reference

For more info about Kiro CLI:
- Website: https://kiro.dev
- Documentation: https://kiro.dev/docs
- GitHub: https://github.com/kiro-dev/cli

---

## 🚀 Deployment & Distribution

### Prepare for GitHub

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Kiro Dock v1.0"
   git remote add origin https://github.com/yourusername/engineersTech-dock-kiro.git
   git push -u origin main
   ```

2. **Create Release**
   - Go to GitHub repository
   - Click "Releases" → "Create a new release"
   - Tag: `v1.0.0`
   - Include release notes and assets

### Share as AUR Package (Arch Linux)

See [AUR Submission Guide](https://wiki.archlinux.org/title/AUR_submission_guidelines)

### Create Snap Package

```bash
snapcraft
# Follow snapcraft.yaml configuration
```

### Create AppImage

Use [AppImageKit](https://appimage.org/) to create portable AppImage

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Support & Issues

- **Report Bugs:** [GitHub Issues](https://github.com/yourusername/engineersTech-dock-kiro/issues)
- **Suggestions:** [GitHub Discussions](https://github.com/yourusername/engineersTech-dock-kiro/discussions)
- **Documentation:** See [Docs](DOCS.md)

---

## 🎨 Credits

- **Kiro CLI:** AI-powered CLI by [Kiro](https://kiro.dev)
- **PyQt6:** Python bindings for Qt
- **Pillow:** Python Imaging Library

---

## 📚 Additional Resources For full version contact, engineerstechbd.com

- [PyQt6 Documentation](https://doc.qt.io/qtforpython-6/)
- [Linux Desktop Integration](https://specifications.freedesktop.org/)
- [Creating Custom Sprites](https://docs.aseprite.org/)

---

**Happy docking! 🚀**
```
