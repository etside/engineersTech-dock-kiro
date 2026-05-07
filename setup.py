#!/usr/bin/env python3
"""
Kiro Dock Setup Wizard
Interactive configuration for dock positioning and asset paths
"""

import json
import os
import sys
from pathlib import Path

CONFIG_FILE = Path.home() / ".config" / "kiro-dock" / "config.json"
ASSETS_DIR = Path.home() / ".local" / "share" / "kiro-dock" / "assets"

DEFAULT_CONFIG = {
    "position": "bottom",  # bottom, top, center, top-left, top-right
    "animation_speed": "normal",  # slow, normal, fast
    "custom_assets_dir": None,
    "assets": {
        "walk_sheet": "sheet2.png",
        "idle_sheet": "anims.png",
        "fallback_icon": "icon.png"
    },
    "auto_start": False
}

POSITIONS = {
    "1": ("bottom", "Bottom of screen (default)"),
    "2": ("top", "Top of screen"),
    "3": ("center", "Center of screen"),
    "4": ("top-left", "Top-left corner"),
    "5": ("top-right", "Top-right corner"),
}

SPEEDS = {
    "1": ("slow", "Slow (2x slower)"),
    "2": ("normal", "Normal"),
    "3": ("fast", "Fast (1.5x faster)"),
}


def print_header():
    print("\n" + "=" * 60)
    print("  🚀 KIRO DOCK - Setup Wizard")
    print("=" * 60 + "\n")


def print_section(title):
    print(f"\n📋 {title}")
    print("-" * 60)


def get_position():
    print_section("Step 1: Choose Dock Position")
    print("\nWhere would you like the dock to appear on your screen?\n")
    
    for key, (pos, desc) in POSITIONS.items():
        print(f"  [{key}] {desc}")
    
    while True:
        choice = input("\nEnter choice (1-5): ").strip()
        if choice in POSITIONS:
            return POSITIONS[choice][0]
        print("❌ Invalid choice. Please enter 1-5.")


def get_animation_speed():
    print_section("Step 2: Choose Animation Speed")
    print("\nHow fast should the dock animate?\n")
    
    for key, (speed, desc) in SPEEDS.items():
        print(f"  [{key}] {desc}")
    
    while True:
        choice = input("\nEnter choice (1-3): ").strip()
        if choice in SPEEDS:
            return SPEEDS[choice][0]
        print("❌ Invalid choice. Please enter 1-3.")


def get_custom_assets():
    print_section("Step 3: Custom Assets (Optional)")
    print("\nYou can use custom animation sprites and icons.")
    print("Leave blank to use default assets.\n")
    
    custom_dir = input("Enter path to custom assets directory (or press Enter to skip): ").strip()
    
    if custom_dir:
        custom_path = Path(custom_dir).expanduser()
        if not custom_path.exists():
            print(f"❌ Directory not found: {custom_dir}")
            return None
        if not custom_path.is_dir():
            print(f"❌ Not a directory: {custom_dir}")
            return None
        return str(custom_path)
    
    return None


def get_auto_start():
    print_section("Step 4: Auto-start Configuration")
    print("\nWould you like Kiro Dock to start automatically on login?\n")
    
    while True:
        choice = input("Auto-start on login? (y/n): ").strip().lower()
        if choice in ('y', 'yes'):
            return True
        elif choice in ('n', 'no'):
            return False
        print("❌ Please enter 'y' or 'n'.")


def verify_kiro_cli():
    print_section("Step 5: Verify Kiro CLI Installation")
    
    kiro_path = Path.home() / ".local" / "bin" / "kiro-cli"
    
    if kiro_path.exists():
        print(f"✅ Kiro CLI found at: {kiro_path}")
        return True
    else:
        print(f"⚠️  Kiro CLI not found at: {kiro_path}")
        print("\n📖 Installation instructions:")
        print("   Visit: https://kiro.dev")
        print("   Then run: kiro install")
        print("\nContinuing without Kiro CLI may limit functionality.")
        
        while True:
            choice = input("\nContinue setup anyway? (y/n): ").strip().lower()
            if choice in ('y', 'yes'):
                return False
            elif choice in ('n', 'no'):
                print("❌ Setup cancelled.")
                sys.exit(1)


def save_config(config):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"\n✅ Configuration saved to: {CONFIG_FILE}")


def print_summary(config):
    print_section("Configuration Summary")
    print(f"\n  Position:          {config['position']}")
    print(f"  Animation Speed:   {config['animation_speed']}")
    print(f"  Custom Assets:     {config['custom_assets_dir'] or 'None (using defaults)'}")
    print(f"  Auto-start:        {'Enabled' if config['auto_start'] else 'Disabled'}")


def load_existing_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Failed to load existing config: {e}")
    return None


def main():
    print_header()
    
    existing = load_existing_config()
    if existing:
        print("Found existing configuration.\n")
        choice = input("Would you like to reconfigure? (y/n): ").strip().lower()
        if choice not in ('y', 'yes'):
            print("✅ Using existing configuration.")
            print_summary(existing)
            return
    
    # Run setup wizard
    verify_kiro_cli()
    
    position = get_position()
    speed = get_animation_speed()
    custom_assets = get_custom_assets()
    auto_start = get_auto_start()
    
    # Build config
    config = DEFAULT_CONFIG.copy()
    config["position"] = position
    config["animation_speed"] = speed
    config["custom_assets_dir"] = custom_assets
    config["auto_start"] = auto_start
    
    # Save config
    save_config(config)
    print_summary(config)
    
    print("\n" + "=" * 60)
    print("✅ Setup complete! Launch with:")
    print("   kiro-dock")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
