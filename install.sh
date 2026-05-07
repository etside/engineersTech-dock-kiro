#!/usr/bin/env bash
set -e

INSTALL_DIR="$HOME/.local/share/kiro-dock"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
DESKTOP_DIR="$HOME/.local/share/applications"
CONFIG_DIR="$HOME/.config/kiro-dock"
SRC="$(cd "$(dirname "$0")" && pwd)"

echo "Installing Kiro Dock..."

mkdir -p "$INSTALL_DIR" "$ICON_DIR" "$DESKTOP_DIR" "$CONFIG_DIR"

# copy app files
cp "$SRC/main.py" "$INSTALL_DIR/"
cp "$SRC/setup.py" "$INSTALL_DIR/"
for f in sheet2.png anims.png sprite.png icon.png; do
    [ -f "$SRC/$f" ] && cp "$SRC/$f" "$INSTALL_DIR/"
done

# install icon
[ -f "$SRC/icon.png" ] && cp "$SRC/icon.png" "$ICON_DIR/kiro-dock.png"

# write launcher script
cat > "$INSTALL_DIR/kiro-dock" <<'EOF'
#!/usr/bin/env bash
cd "$INSTALL_DIR"
exec python3 "$INSTALL_DIR/main.py" "$@"
EOF
chmod +x "$INSTALL_DIR/kiro-dock"
ln -sf "$INSTALL_DIR/kiro-dock" "$HOME/.local/bin/kiro-dock"

# write setup script launcher
cat > "$INSTALL_DIR/kiro-dock-setup" <<'EOF'
#!/usr/bin/env bash
cd "$INSTALL_DIR"
exec python3 "$INSTALL_DIR/setup.py" "$@"
EOF
chmod +x "$INSTALL_DIR/kiro-dock-setup"
ln -sf "$INSTALL_DIR/kiro-dock-setup" "$HOME/.local/bin/kiro-dock-setup"

# write .desktop file
cat > "$DESKTOP_DIR/kiro-dock.desktop" <<EOF
[Desktop Entry]
Name=Kiro Dock
Comment=Animated Kiro desktop agent
Exec=$INSTALL_DIR/kiro-dock
Icon=kiro-dock
Type=Application
Categories=Utility;Development;
StartupNotify=false
X-GNOME-Autostart-enabled=false
EOF

# update icon cache
gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true

echo ""
echo "✅ Installation complete!"
echo ""
echo "📋 NEXT STEPS:"
echo "1. Run configuration wizard:"
echo "   kiro-dock-setup"
echo ""
echo "2. Launch the dock:"
echo "   kiro-dock"
echo ""
echo "📚 For more help, see: README.md"

