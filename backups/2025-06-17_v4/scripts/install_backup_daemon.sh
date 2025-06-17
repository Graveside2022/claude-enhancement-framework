#!/bin/bash
# Installation script for 120-minute backup daemon
# Created for: Christian
# Purpose: Install automatic backup enforcement as system service

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$PROJECT_ROOT/scripts"

echo "🔧 Installing 120-minute backup daemon for Christian's CLAUDE project"
echo "Project root: $PROJECT_ROOT"
echo ""

# Detect operating system
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
    SERVICE_TYPE="launchd"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
    SERVICE_TYPE="systemd"
else
    OS="Other"
    SERVICE_TYPE="manual"
fi

echo "Operating System: $OS"
echo "Service Type: $SERVICE_TYPE"
echo ""

# Function to install on macOS using launchd
install_macos() {
    local plist_file="$SCRIPTS_DIR/com.christian.claude.backup.plist"
    local target_dir="$HOME/Library/LaunchAgents"
    local target_file="$target_dir/com.christian.claude.backup.plist"
    
    echo "📦 Installing macOS launchd service..."
    
    # Create LaunchAgents directory if it doesn't exist
    mkdir -p "$target_dir"
    
    # Copy plist file
    cp "$plist_file" "$target_file"
    echo "✓ Copied plist to $target_file"
    
    # Load the service
    launchctl unload "$target_file" 2>/dev/null || true  # Unload if already loaded
    launchctl load "$target_file"
    echo "✓ Loaded service with launchctl"
    
    # Start the service
    launchctl start com.christian.claude.backup
    echo "✓ Started backup daemon service"
    
    echo ""
    echo "📋 macOS Service Management Commands:"
    echo "  Start:   launchctl start com.christian.claude.backup"
    echo "  Stop:    launchctl stop com.christian.claude.backup"
    echo "  Status:  launchctl list | grep claude.backup"
    echo "  Logs:    tail -f $PROJECT_ROOT/backup_daemon.log"
}

# Function to install on Linux using systemd
install_linux() {
    local service_file="$SCRIPTS_DIR/claude-backup-daemon.service"
    local target_file="$HOME/.config/systemd/user/claude-backup-daemon.service"
    
    echo "📦 Installing Linux systemd user service..."
    
    # Create systemd user directory if it doesn't exist
    mkdir -p "$HOME/.config/systemd/user"
    
    # Copy service file
    cp "$service_file" "$target_file"
    echo "✓ Copied service file to $target_file"
    
    # Reload systemd and enable service
    systemctl --user daemon-reload
    systemctl --user enable claude-backup-daemon.service
    echo "✓ Enabled service with systemd"
    
    # Start the service
    systemctl --user start claude-backup-daemon.service
    echo "✓ Started backup daemon service"
    
    echo ""
    echo "📋 Linux Service Management Commands:"
    echo "  Start:   systemctl --user start claude-backup-daemon.service"
    echo "  Stop:    systemctl --user stop claude-backup-daemon.service"
    echo "  Status:  systemctl --user status claude-backup-daemon.service"
    echo "  Logs:    journalctl --user -u claude-backup-daemon.service -f"
}

# Function to install manual startup
install_manual() {
    echo "📦 Setting up manual startup option..."
    
    # Create startup script if it doesn't exist
    if [ ! -f "$SCRIPTS_DIR/start_backup_daemon.sh" ]; then
        echo "❌ Startup script not found: $SCRIPTS_DIR/start_backup_daemon.sh"
        exit 1
    fi
    
    echo "✓ Manual startup script available: $SCRIPTS_DIR/start_backup_daemon.sh"
    
    echo ""
    echo "📋 Manual Management Commands:"
    echo "  Start:   $SCRIPTS_DIR/start_backup_daemon.sh start"
    echo "  Stop:    $SCRIPTS_DIR/start_backup_daemon.sh stop"
    echo "  Status:  $SCRIPTS_DIR/start_backup_daemon.sh status"
    echo "  Test:    $SCRIPTS_DIR/start_backup_daemon.sh test"
}

# Function to test installation
test_installation() {
    echo "🧪 Testing backup daemon installation..."
    
    # Wait a moment for service to start
    sleep 3
    
    # Test backup functionality
    if python3 "$SCRIPTS_DIR/backup_daemon.py" --test --project-root "$PROJECT_ROOT"; then
        echo "✅ Backup functionality test passed"
    else
        echo "❌ Backup functionality test failed"
        return 1
    fi
    
    # Check service status
    case "$SERVICE_TYPE" in
        launchd)
            if launchctl list | grep -q "claude.backup"; then
                echo "✅ macOS service is running"
            else
                echo "❌ macOS service is not running"
                return 1
            fi
            ;;
        systemd)
            if systemctl --user is-active --quiet claude-backup-daemon.service; then
                echo "✅ Linux service is running"
            else
                echo "❌ Linux service is not running"
                return 1
            fi
            ;;
        manual)
            echo "ℹ️ Manual installation - use start_backup_daemon.sh to manage"
            ;;
    esac
}

# Function to show post-install information
show_post_install_info() {
    echo ""
    echo "🎉 120-minute backup daemon installation complete!"
    echo ""
    echo "📊 System Configuration:"
    echo "  Project: CLAUDE Improvement (Christian)"
    echo "  Backup Interval: 120 minutes (2 hours)"
    echo "  Check Interval: 5 minutes"
    echo "  Service Type: $SERVICE_TYPE"
    echo "  Auto-start: Enabled"
    echo ""
    echo "📝 Log Files:"
    echo "  Daemon Log: $PROJECT_ROOT/backup_daemon.log"
    echo "  Backup Log: $PROJECT_ROOT/backups/backup_log.txt"
    echo ""
    echo "🔧 Configuration Files:"
    echo "  Backup Integration: $SCRIPTS_DIR/backup_integration.py"
    echo "  Daemon Script: $SCRIPTS_DIR/backup_daemon.py"
    echo "  Management Script: $SCRIPTS_DIR/start_backup_daemon.sh"
    echo ""
    echo "⚠️ Important Notes:"
    echo "  - Backup enforcement is now automatic every 120 minutes"
    echo "  - System will create backups even when user is not actively working"
    echo "  - All backup procedures follow CLAUDE.md specifications exactly"
    echo "  - File integrity verification is performed on every backup"
    echo ""
    echo "📋 Quick Commands:"
    case "$SERVICE_TYPE" in
        launchd)
            echo "  Check Status: launchctl list | grep claude.backup"
            echo "  View Logs: tail -f $PROJECT_ROOT/backup_daemon.log"
            ;;
        systemd)
            echo "  Check Status: systemctl --user status claude-backup-daemon.service"
            echo "  View Logs: journalctl --user -u claude-backup-daemon.service -f"
            ;;
        manual)
            echo "  Check Status: $SCRIPTS_DIR/start_backup_daemon.sh status"
            echo "  View Logs: tail -f $PROJECT_ROOT/backup_daemon.log"
            ;;
    esac
}

# Main installation process
main() {
    # Check prerequisites
    if ! command -v python3 >/dev/null 2>&1; then
        echo "❌ Python 3 is required but not installed"
        exit 1
    fi
    
    # Install based on operating system
    case "$SERVICE_TYPE" in
        launchd)
            install_macos
            ;;
        systemd)
            install_linux
            ;;
        manual)
            install_manual
            ;;
    esac
    
    # Test installation
    if test_installation; then
        show_post_install_info
        echo "✅ Installation successful!"
    else
        echo "❌ Installation test failed"
        exit 1
    fi
}

# Run installation if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi