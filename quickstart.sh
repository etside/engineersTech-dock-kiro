#!/usr/bin/env bash
#
# Quick-start script for Kiro Dock
# Handles installation, setup, and initial launch
#

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COLOR_BLUE='\033[0;34m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${COLOR_BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${COLOR_GREEN}✓${NC} $1"
}

log_warn() {
    echo -e "${COLOR_YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${COLOR_RED}✗${NC} $1"
}

print_header() {
    echo ""
    echo "╔════════════════════════════════════╗"
    echo "║   🚀 Kiro Dock Quick Start v1.0   ║"
    echo "╚════════════════════════════════════╝"
    echo ""
}

check_python() {
    log_info "Checking Python installation..."
    
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 not found!"
        log_warn "Please install Python 3.10 or later"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    log_success "Python $PYTHON_VERSION found"
}

check_dependencies() {
    log_info "Checking system dependencies..."
    
    # Check for required commands
    for cmd in git pip3; do
        if ! command -v "$cmd" &> /dev/null; then
            log_warn "$cmd not found (optional)"
        fi
    done
    
    log_success "Dependency check complete"
}

install_app() {
    log_info "Installing Kiro Dock..."
    
    if [ ! -f "$SCRIPT_DIR/install.sh" ]; then
        log_error "install.sh not found!"
        exit 1
    fi
    
    cd "$SCRIPT_DIR"
    chmod +x install.sh
    ./install.sh
    
    log_success "Installation complete"
}

run_setup() {
    log_info "Running setup wizard..."
    echo ""
    
    python3 "$HOME/.local/share/kiro-dock/setup.py"
    
    log_success "Setup complete"
}

launch_app() {
    echo ""
    log_info "Ready to launch!"
    
    read -p "$(echo -e ${COLOR_BLUE}?)$(echo -e ${NC}) Launch Kiro Dock now? (y/n) " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Launching Kiro Dock..."
        kiro-dock &
        log_success "Kiro Dock launched! (PID: $!)"
        echo ""
        log_info "Tip: Right-click the tray icon for options"
    else
        log_info "To launch later, run: kiro-dock"
    fi
}

main() {
    print_header
    
    check_python
    check_dependencies
    install_app
    run_setup
    launch_app
    
    echo ""
    log_success "All done! Enjoy your dock! 🎉"
    echo ""
}

main "$@"
