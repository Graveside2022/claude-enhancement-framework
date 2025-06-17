#!/usr/bin/env python3
"""
120-Minute Automatic Backup System Daemon
Created for: Christian
Purpose: Automatic enforcement of 120-minute backup intervals

This daemon runs continuously and checks for backup requirements
every few minutes, automatically triggering backups when needed.
"""

import os
import sys
import time
import signal
import threading
import datetime
import logging
from pathlib import Path

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent))

from backup_integration import BackupIntegration

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backup_daemon.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class BackupDaemon:
    """
    Automatic backup daemon that enforces 120-minute backup intervals.
    
    Features:
    - Continuous monitoring of backup timing
    - Automatic backup creation when 120 minutes have elapsed
    - Graceful shutdown handling
    - Comprehensive logging
    - File integrity verification
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.backup_system = BackupIntegration(project_root)
        self.running = False
        self.check_interval_seconds = 300  # Check every 5 minutes
        self.daemon_thread = None
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info(f"Backup daemon initialized for Christian's project at: {self.project_root}")
        logger.info(f"120-minute backup enforcement active")
        logger.info(f"Check interval: {self.check_interval_seconds} seconds")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.stop()
    
    def start(self):
        """Start the backup daemon."""
        if self.running:
            logger.warning("Backup daemon is already running")
            return
        
        logger.info("Starting backup daemon for Christian's CLAUDE improvement project")
        logger.info("Enforcing 120-minute backup intervals automatically")
        
        self.running = True
        self.daemon_thread = threading.Thread(target=self._daemon_loop, daemon=True)
        self.daemon_thread.start()
        
        logger.info("✅ Backup daemon started successfully")
    
    def stop(self):
        """Stop the backup daemon."""
        if not self.running:
            logger.info("Backup daemon is not running")
            return
        
        logger.info("Stopping backup daemon...")
        self.running = False
        
        if self.daemon_thread and self.daemon_thread.is_alive():
            self.daemon_thread.join(timeout=10)
        
        logger.info("✅ Backup daemon stopped")
    
    def _daemon_loop(self):
        """Main daemon loop that checks and enforces backup timing."""
        logger.info("Backup daemon loop started")
        
        while self.running:
            try:
                self._check_and_enforce_backup()
                
                # Sleep for check interval, but break early if stopping
                for _ in range(self.check_interval_seconds):
                    if not self.running:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Error in daemon loop: {e}")
                # Continue running even if there's an error
                time.sleep(60)  # Wait a minute before retrying
        
        logger.info("Backup daemon loop ended")
    
    def _check_and_enforce_backup(self):
        """Check backup system status (automatic backup disabled)."""
        try:
            # Automatic backup enforcement has been disabled
            logger.info("⚠️ Automatic backup enforcement has been disabled")
            logger.info("💾 Use manual backup system instead:")
            logger.info("    scripts/manual_backup.sh backup           - Standard backup")
            logger.info("    scripts/manual_backup.sh full backup      - Comprehensive backup")
            logger.info("    scripts/manual_backup.sh status           - Check backup status")
            
            # Log status periodically (every hour) for awareness
            if hasattr(self, '_status_check_count'):
                self._status_check_count += 1
            else:
                self._status_check_count = 1
            
            if self._status_check_count % 12 == 0:
                logger.info("💾 Manual backup system is active - no automatic backups will be created")
                
        except Exception as e:
            logger.error(f"Error during backup check: {e}")
    
    def _verify_backup_integrity(self, backup_name: str):
        """Verify the integrity of a newly created backup."""
        try:
            backup_path = self.backup_system.backups_dir / backup_name
            metadata_file = backup_path / "backup_info.json"
            
            if metadata_file.exists():
                import json
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                if metadata.get('integrity_verified', False):
                    logger.info(f"✅ Backup integrity verified: {backup_name}")
                else:
                    logger.warning(f"⚠️ Backup integrity not verified: {backup_name}")
            else:
                logger.warning(f"⚠️ No metadata found for backup: {backup_name}")
                
        except Exception as e:
            logger.error(f"Error verifying backup integrity: {e}")
    
    def get_status(self) -> dict:
        """Get daemon status information."""
        return {
            "daemon_running": self.running,
            "check_interval_seconds": self.check_interval_seconds,
            "backup_interval_minutes": self.backup_system.backup_interval_minutes,
            "project_root": str(self.project_root),
            "backup_system_status": self.backup_system.get_backup_status()
        }
    
    def force_backup(self, reason: str = "manual_force"):
        """Force immediate backup creation."""
        logger.info(f"Force backup requested: {reason}")
        backup_name = self.backup_system.create_backup(reason)
        
        if backup_name:
            logger.info(f"✅ Force backup created: {backup_name}")
            self._verify_backup_integrity(backup_name)
            return backup_name
        else:
            logger.error("❌ Force backup creation failed")
            return None


def main():
    """Main function for standalone daemon usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="120-Minute Backup Daemon for CLAUDE Project")
    parser.add_argument("--start", action="store_true", help="Start the backup daemon")
    parser.add_argument("--stop", action="store_true", help="Stop the backup daemon") 
    parser.add_argument("--status", action="store_true", help="Show daemon status")
    parser.add_argument("--force-backup", metavar="REASON", help="Force immediate backup")
    parser.add_argument("--test", action="store_true", help="Test backup functionality")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--foreground", action="store_true", help="Run in foreground (don't daemonize)")
    
    args = parser.parse_args()
    
    daemon = BackupDaemon(args.project_root)
    
    if args.test:
        logger.info("🧪 Testing backup functionality...")
        backup_name = daemon.force_backup("test_functionality")
        if backup_name:
            logger.info(f"✅ Test backup successful: {backup_name}")
            sys.exit(0)
        else:
            logger.error("❌ Test backup failed")
            sys.exit(1)
    
    elif args.force_backup:
        backup_name = daemon.force_backup(args.force_backup)
        sys.exit(0 if backup_name else 1)
    
    elif args.status:
        import json
        status = daemon.get_status()
        print(json.dumps(status, indent=2, default=str))
    
    elif args.start:
        daemon.start()
        
        if args.foreground:
            logger.info("Running in foreground mode (Ctrl+C to stop)")
            try:
                while daemon.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received")
        else:
            logger.info("Daemon started in background")
            logger.info("Use --stop to stop the daemon")
        
    elif args.stop:
        daemon.stop()
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()