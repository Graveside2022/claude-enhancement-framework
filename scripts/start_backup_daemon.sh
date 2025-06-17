#!/bin/bash
# Startup script for 120-minute backup daemon
# Created for: Christian
# Purpose: Automatic startup of backup enforcement system

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DAEMON_SCRIPT="$PROJECT_ROOT/scripts/backup_daemon.py"
PID_FILE="$PROJECT_ROOT/backup_daemon.pid"
LOG_FILE="$PROJECT_ROOT/backup_daemon.log"

echo "🚀 Starting 120-minute backup daemon for Christian's CLAUDE project"
echo "Project root: $PROJECT_ROOT"
echo "Daemon script: $DAEMON_SCRIPT"
echo "PID file: $PID_FILE"
echo "Log file: $LOG_FILE"

# Function to check if daemon is running
is_daemon_running() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0  # Running
        else
            rm -f "$PID_FILE"  # Clean up stale PID file
            return 1  # Not running
        fi
    fi
    return 1  # Not running
}

# Function to start daemon
start_daemon() {
    if is_daemon_running; then
        echo "⚠️ Backup daemon is already running (PID: $(cat "$PID_FILE"))"
        return 1
    fi
    
    echo "Starting backup daemon..."
    cd "$PROJECT_ROOT"
    
    # Start daemon in background
    nohup python3 "$DAEMON_SCRIPT" --start --foreground > "$LOG_FILE" 2>&1 &
    local daemon_pid=$!
    
    # Save PID
    echo "$daemon_pid" > "$PID_FILE"
    
    # Wait a moment to see if it started successfully
    sleep 2
    
    if is_daemon_running; then
        echo "✅ Backup daemon started successfully (PID: $daemon_pid)"
        echo "📝 Logs: $LOG_FILE"
        echo "⏰ 120-minute backup enforcement active"
        return 0
    else
        echo "❌ Failed to start backup daemon"
        rm -f "$PID_FILE"
        return 1
    fi
}

# Function to stop daemon
stop_daemon() {
    if ! is_daemon_running; then
        echo "⚠️ Backup daemon is not running"
        return 1
    fi
    
    local pid=$(cat "$PID_FILE")
    echo "Stopping backup daemon (PID: $pid)..."
    
    # Send SIGTERM for graceful shutdown
    kill -TERM "$pid"
    
    # Wait for graceful shutdown
    local count=0
    while [ $count -lt 10 ] && ps -p "$pid" > /dev/null 2>&1; do
        sleep 1
        count=$((count + 1))
    done
    
    # Force kill if still running
    if ps -p "$pid" > /dev/null 2>&1; then
        echo "Force killing daemon..."
        kill -KILL "$pid"
        sleep 1
    fi
    
    rm -f "$PID_FILE"
    echo "✅ Backup daemon stopped"
}

# Function to check daemon status
status_daemon() {
    echo "🔍 Checking backup daemon status..."
    
    if is_daemon_running; then
        local pid=$(cat "$PID_FILE")
        echo "✅ Backup daemon is running (PID: $pid)"
        
        # Show recent log entries
        if [ -f "$LOG_FILE" ]; then
            echo ""
            echo "📝 Recent log entries:"
            tail -n 5 "$LOG_FILE"
        fi
        
        # Show backup system status
        echo ""
        echo "📊 Backup system status:"
        python3 "$DAEMON_SCRIPT" --status --project-root "$PROJECT_ROOT"
    else
        echo "❌ Backup daemon is not running"
    fi
}

# Function to test backup functionality
test_backup() {
    echo "🧪 Testing backup functionality..."
    cd "$PROJECT_ROOT"
    python3 "$DAEMON_SCRIPT" --test --project-root "$PROJECT_ROOT"
}

# Main execution
case "${1:-status}" in
    start)
        start_daemon
        ;;
    stop)
        stop_daemon
        ;;
    restart)
        echo "🔄 Restarting backup daemon..."
        stop_daemon
        sleep 2
        start_daemon
        ;;
    status)
        status_daemon
        ;;
    test)
        test_backup
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|test}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the 120-minute backup daemon"
        echo "  stop    - Stop the backup daemon"
        echo "  restart - Restart the backup daemon"
        echo "  status  - Show daemon and backup system status"
        echo "  test    - Test backup functionality"
        echo ""
        echo "120-minute backup enforcement for Christian's CLAUDE project"
        exit 1
        ;;
esac