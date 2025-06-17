#!/usr/bin/env python3
"""
Automated File Management System
Continuous automation for file organization, cleanup, and maintenance

This system provides automated triggers, scheduled maintenance, and intelligent
file management for the reports organization system.
"""

import os
import time
import json
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set, Optional, Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from reports_organization_system import ReportsOrganizationSystem
from reports_integration import ReportsIntegration

class FileChangeHandler(FileSystemEventHandler):
    """
    File system event handler for automatic file organization
    """
    
    def __init__(self, management_system):
        """Initialize file change handler"""
        self.management_system = management_system
        self.processing_files = set()  # Prevent recursive processing
        
    def on_created(self, event):
        """Handle file creation events"""
        if not event.is_directory:
            self._process_file_event("created", Path(event.src_path))
    
    def on_modified(self, event):
        """Handle file modification events"""
        if not event.is_directory:
            self._process_file_event("modified", Path(event.src_path))
    
    def on_moved(self, event):
        """Handle file move events"""
        if not event.is_directory:
            self._process_file_event("moved", Path(event.dest_path))
    
    def _process_file_event(self, event_type: str, file_path: Path):
        """Process file system events"""
        # Avoid processing the same file repeatedly
        if str(file_path) in self.processing_files:
            return
            
        try:
            self.processing_files.add(str(file_path))
            self.management_system.process_file_change(event_type, file_path)
        finally:
            self.processing_files.discard(str(file_path))


class AutomatedFileManagement:
    """
    Comprehensive automated file management system
    """
    
    def __init__(self, base_path: str = None):
        """Initialize automated file management"""
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.org_system = ReportsOrganizationSystem(base_path)
        self.integration = ReportsIntegration(base_path)
        
        # Management configuration
        self.config = self._load_management_config()
        
        # File monitoring
        self.observer = None
        self.file_handler = FileChangeHandler(self)
        
        # Scheduled tasks
        self.scheduled_tasks = []
        self.task_threads = []
        self.running = False
        
        # File categorization rules
        self.categorization_rules = self._load_categorization_rules()
        
        # Maintenance statistics
        self.stats = {
            "files_processed": 0,
            "files_organized": 0,
            "cleanup_operations": 0,
            "errors": 0,
            "last_maintenance": None
        }

    def _load_management_config(self) -> Dict:
        """Load automated management configuration"""
        config_path = self.base_path / "automated_management_config.json"
        
        default_config = {
            "monitoring": {
                "enabled": True,
                "watch_directories": [
                    ".",
                    "backups",
                    "memory",
                    "docs"
                ],
                "exclude_patterns": [
                    "*.tmp",
                    "*.log",
                    ".git/*",
                    "reports/*"  # Don't monitor reports directory to avoid recursion
                ]
            },
            "auto_organization": {
                "enabled": True,
                "immediate_processing": True,
                "batch_processing_interval": 300,  # 5 minutes
                "max_batch_size": 50
            },
            "scheduled_maintenance": {
                "enabled": True,
                "cleanup_interval": 3600,  # 1 hour
                "statistics_interval": 1800,  # 30 minutes
                "health_check_interval": 900  # 15 minutes
            },
            "cleanup_policies": {
                "temp_files_age_hours": 24,
                "log_files_age_days": 7,
                "backup_retention_days": 30,
                "archive_threshold_days": 90
            }
        }
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                user_config = json.load(f)
            # Deep merge with defaults
            default_config.update(user_config)
        else:
            # Create default config
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
        
        return default_config

    def _load_categorization_rules(self) -> Dict[str, Dict]:
        """Load file categorization rules"""
        rules_path = self.base_path / "categorization_rules.json"
        
        default_rules = {
            "handoff": {
                "filename_patterns": [
                    "*handoff*",
                    "*HANDOFF*",
                    "*session_end*",
                    "*continuity*"
                ],
                "content_patterns": [
                    "HANDOFF SUMMARY",
                    "Session End",
                    "Next Session"
                ],
                "extensions": [".md", ".txt"]
            },
            "backup": {
                "filename_patterns": [
                    "*backup*",
                    "*BACKUP*",
                    "backup_*",
                    "*verification*"
                ],
                "content_patterns": [
                    "Backup Created",
                    "backup_info",
                    "verification"
                ],
                "extensions": [".json", ".txt", ".md"]
            },
            "session": {
                "filename_patterns": [
                    "*session*",
                    "*SESSION*",
                    "TODO.md",
                    "*continuity*"
                ],
                "content_patterns": [
                    "SESSION CONTINUITY",
                    "Current Status",
                    "TODO.md"
                ],
                "extensions": [".md", ".txt", ".json"]
            },
            "error": {
                "filename_patterns": [
                    "*error*",
                    "*ERROR*",
                    "*learned*",
                    "*LEARNED*",
                    "*correction*"
                ],
                "content_patterns": [
                    "LEARNED_CORRECTIONS",
                    "Error Analysis",
                    "error_patterns"
                ],
                "extensions": [".md", ".txt", ".json"]
            },
            "analysis": {
                "filename_patterns": [
                    "*analysis*",
                    "*ANALYSIS*",
                    "*report*",
                    "*dependency*"
                ],
                "content_patterns": [
                    "Analysis Report",
                    "Dependency",
                    "Code Review"
                ],
                "extensions": [".md", ".txt", ".json"]
            },
            "monitoring": {
                "filename_patterns": [
                    "*monitoring*",
                    "*health*",
                    "*status*",
                    "*metrics*"
                ],
                "content_patterns": [
                    "System Health",
                    "Monitoring",
                    "Performance"
                ],
                "extensions": [".json", ".md", ".txt"]
            }
        }
        
        if rules_path.exists():
            with open(rules_path, 'r') as f:
                user_rules = json.load(f)
            default_rules.update(user_rules)
        else:
            with open(rules_path, 'w') as f:
                json.dump(default_rules, f, indent=2)
        
        return default_rules

    def start_monitoring(self):
        """Start file system monitoring"""
        if not self.config["monitoring"]["enabled"]:
            return
        
        self.running = True
        
        # Set up file system observer
        self.observer = Observer()
        
        # Watch specified directories
        for watch_dir in self.config["monitoring"]["watch_directories"]:
            dir_path = self.base_path / watch_dir
            if dir_path.exists():
                self.observer.schedule(
                    self.file_handler,
                    str(dir_path),
                    recursive=True
                )
        
        # Start observer
        self.observer.start()
        
        # Start scheduled tasks
        self._start_scheduled_tasks()
        
        print(f"[{datetime.now()}] File monitoring started for Christian's project")

    def stop_monitoring(self):
        """Stop file system monitoring"""
        self.running = False
        
        # Stop file system observer
        if self.observer:
            self.observer.stop()
            self.observer.join()
        
        # Stop scheduled tasks
        for thread in self.task_threads:
            if thread.is_alive():
                thread.join(timeout=5)  # Wait max 5 seconds
        
        print(f"[{datetime.now()}] File monitoring stopped")

    def process_file_change(self, event_type: str, file_path: Path):
        """Process file system change events"""
        try:
            # Skip excluded files
            if self._is_excluded_file(file_path):
                return
            
            # Skip if file doesn't exist (might be temporary)
            if not file_path.exists():
                return
            
            # Categorize and organize file
            category = self._categorize_file(file_path)
            if category:
                self._organize_file(file_path, category, event_type)
                self.stats["files_organized"] += 1
            
            self.stats["files_processed"] += 1
            
        except Exception as e:
            self.stats["errors"] += 1
            self._log_error(f"Error processing {file_path}: {str(e)}")

    def _categorize_file(self, file_path: Path) -> Optional[str]:
        """Categorize file based on rules"""
        filename = file_path.name.lower()
        
        # Try to read file content for content-based categorization
        try:
            if file_path.suffix in ['.md', '.txt'] and file_path.stat().st_size < 1024 * 1024:  # Max 1MB
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(1000).lower()  # First 1000 chars
            else:
                content = ""
        except:
            content = ""
        
        # Check each category's rules
        for category, rules in self.categorization_rules.items():
            # Check filename patterns
            for pattern in rules.get("filename_patterns", []):
                if self._matches_pattern(filename, pattern.lower()):
                    return category
            
            # Check content patterns
            if content:
                for pattern in rules.get("content_patterns", []):
                    if pattern.lower() in content:
                        return category
            
            # Check extensions
            if file_path.suffix in rules.get("extensions", []):
                # Additional heuristics for extension-based categorization
                if "backup" in filename and category == "backup":
                    return category
                elif "session" in filename and category == "session":
                    return category
        
        return None

    def _organize_file(self, file_path: Path, category: str, event_type: str):
        """Organize file into appropriate reports category"""
        try:
            # Create metadata
            metadata = {
                "original_path": str(file_path),
                "event_type": event_type,
                "auto_organized": True,
                "categorization_confidence": "automatic"
            }
            
            # Move file to reports organization
            new_path = self.org_system.move_file_to_reports(
                file_path,
                category,
                preserve_original=False
            )
            
            print(f"[{datetime.now()}] Organized {file_path.name} → {category} category")
            
        except Exception as e:
            self._log_error(f"Failed to organize {file_path}: {str(e)}")

    def _is_excluded_file(self, file_path: Path) -> bool:
        """Check if file should be excluded from processing"""
        filename = file_path.name.lower()
        
        # Check exclude patterns
        for pattern in self.config["monitoring"]["exclude_patterns"]:
            if self._matches_pattern(str(file_path).lower(), pattern.lower()):
                return True
        
        # Skip temporary files
        if filename.endswith(('.tmp', '.temp', '.swp', '.bak')):
            return True
        
        # Skip hidden files (except specific ones we care about)
        if filename.startswith('.') and filename not in ['.project_context']:
            return True
        
        return False

    def _matches_pattern(self, text: str, pattern: str) -> bool:
        """Simple pattern matching with wildcards"""
        if '*' not in pattern:
            return pattern in text
        
        # Simple wildcard matching
        parts = pattern.split('*')
        pos = 0
        for part in parts:
            if part:
                pos = text.find(part, pos)
                if pos == -1:
                    return False
                pos += len(part)
        return True

    def _start_scheduled_tasks(self):
        """Start scheduled maintenance tasks"""
        if not self.config["scheduled_maintenance"]["enabled"]:
            return
        
        # Cleanup task
        cleanup_thread = threading.Thread(
            target=self._scheduled_cleanup,
            daemon=True
        )
        cleanup_thread.start()
        self.task_threads.append(cleanup_thread)
        
        # Statistics task
        stats_thread = threading.Thread(
            target=self._scheduled_statistics,
            daemon=True
        )
        stats_thread.start()
        self.task_threads.append(stats_thread)
        
        # Health check task
        health_thread = threading.Thread(
            target=self._scheduled_health_check,
            daemon=True
        )
        health_thread.start()
        self.task_threads.append(health_thread)

    def _scheduled_cleanup(self):
        """Scheduled cleanup operations"""
        interval = self.config["scheduled_maintenance"]["cleanup_interval"]
        
        while self.running:
            try:
                time.sleep(interval)
                if not self.running:
                    break
                
                self._perform_cleanup()
                self.stats["cleanup_operations"] += 1
                
            except Exception as e:
                self._log_error(f"Scheduled cleanup error: {str(e)}")

    def _scheduled_statistics(self):
        """Scheduled statistics generation"""
        interval = self.config["scheduled_maintenance"]["statistics_interval"]
        
        while self.running:
            try:
                time.sleep(interval)
                if not self.running:
                    break
                
                self._generate_statistics_report()
                
            except Exception as e:
                self._log_error(f"Statistics generation error: {str(e)}")

    def _scheduled_health_check(self):
        """Scheduled system health checks"""
        interval = self.config["scheduled_maintenance"]["health_check_interval"]
        
        while self.running:
            try:
                time.sleep(interval)
                if not self.running:
                    break
                
                self._perform_health_check()
                
            except Exception as e:
                self._log_error(f"Health check error: {str(e)}")

    def _perform_cleanup(self):
        """Perform cleanup operations"""
        cleanup_policies = self.config["cleanup_policies"]
        
        # Clean up temporary files
        temp_age = timedelta(hours=cleanup_policies["temp_files_age_hours"])
        self._cleanup_old_files("*.tmp", temp_age)
        
        # Clean up old log files
        log_age = timedelta(days=cleanup_policies["log_files_age_days"])
        self._cleanup_old_files("*.log", log_age)
        
        # Clean up old reports (using organization system's cleanup)
        self.org_system.cleanup_old_reports()
        
        print(f"[{datetime.now()}] Cleanup completed")

    def _cleanup_old_files(self, pattern: str, max_age: timedelta):
        """Clean up old files matching pattern"""
        cutoff_time = datetime.now() - max_age
        
        for file_path in self.base_path.glob(pattern):
            if file_path.is_file():
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_time:
                    try:
                        file_path.unlink()
                        print(f"[{datetime.now()}] Cleaned up old file: {file_path}")
                    except Exception as e:
                        self._log_error(f"Failed to clean up {file_path}: {str(e)}")

    def _generate_statistics_report(self):
        """Generate system statistics report"""
        try:
            stats_content = f"""# Automated File Management Statistics

## Current Statistics
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**User:** Christian

### Processing Statistics
- Files Processed: {self.stats['files_processed']}
- Files Organized: {self.stats['files_organized']}
- Cleanup Operations: {self.stats['cleanup_operations']}
- Errors: {self.stats['errors']}
- Last Maintenance: {self.stats['last_maintenance']}

### Organization Statistics
{self._get_organization_stats()}

### System Health
- Monitoring Status: {'Active' if self.running else 'Stopped'}
- Observer Status: {'Running' if self.observer and self.observer.is_alive() else 'Stopped'}
- Task Threads: {len([t for t in self.task_threads if t.is_alive()])} active

### Performance Metrics
- Success Rate: {((self.stats['files_processed'] - self.stats['errors']) / max(self.stats['files_processed'], 1) * 100):.1f}%
- Organization Rate: {(self.stats['files_organized'] / max(self.stats['files_processed'], 1) * 100):.1f}%

---
*Generated by Automated File Management System*
"""
            
            # Create statistics report
            self.org_system.create_report_file(
                "monitoring",
                "file_management_stats.md",
                stats_content,
                {
                    "report_type": "statistics",
                    "files_processed": self.stats['files_processed'],
                    "files_organized": self.stats['files_organized'],
                    "errors": self.stats['errors']
                }
            )
            
        except Exception as e:
            self._log_error(f"Statistics report generation failed: {str(e)}")

    def _perform_health_check(self):
        """Perform system health check"""
        try:
            health_status = {
                "timestamp": datetime.now().isoformat(),
                "monitoring_active": self.running,
                "observer_status": self.observer.is_alive() if self.observer else False,
                "active_threads": len([t for t in self.task_threads if t.is_alive()]),
                "error_rate": self.stats["errors"] / max(self.stats["files_processed"], 1),
                "reports_directory_accessible": self.org_system.reports_root.exists(),
                "disk_space_available": self._check_disk_space()
            }
            
            # Create health check report if issues found
            issues = []
            if not health_status["monitoring_active"]:
                issues.append("Monitoring not active")
            if not health_status["observer_status"]:
                issues.append("File observer not running")
            if health_status["error_rate"] > 0.1:
                issues.append(f"High error rate: {health_status['error_rate']:.2%}")
            if not health_status["reports_directory_accessible"]:
                issues.append("Reports directory not accessible")
            
            if issues:
                self._create_health_alert(health_status, issues)
            
        except Exception as e:
            self._log_error(f"Health check failed: {str(e)}")

    def _get_organization_stats(self) -> str:
        """Get organization system statistics"""
        try:
            stats = self.org_system.get_report_statistics()
            return f"""- Total Reports: {stats['total_files']}
- Active Categories: {len(stats['categories'])}
- Disk Usage: {stats['disk_usage']} bytes"""
        except:
            return "- Statistics unavailable"

    def _check_disk_space(self) -> bool:
        """Check available disk space"""
        try:
            stat = os.statvfs(self.base_path)
            available_bytes = stat.f_bavail * stat.f_frsize
            return available_bytes > 100 * 1024 * 1024  # 100MB minimum
        except:
            return True  # Assume OK if check fails

    def _create_health_alert(self, health_status: Dict, issues: List[str]):
        """Create health alert report"""
        alert_content = f"""# System Health Alert

## Alert Summary
Health check detected issues requiring attention.

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**User:** Christian  
**Severity:** Warning

## Issues Detected
{chr(10).join(f'- {issue}' for issue in issues)}

## System Status
{chr(10).join(f'- {key}: {value}' for key, value in health_status.items())}

## Recommended Actions
1. Review system logs for errors
2. Restart monitoring if stopped
3. Check disk space and permissions
4. Verify configuration files

---
*Generated by Automated File Management System*
"""
        
        self.org_system.create_report_file(
            "monitoring",
            "health_alert.md",
            alert_content,
            {
                "alert_type": "health_check",
                "severity": "warning",
                "issues_count": len(issues)
            }
        )

    def _log_error(self, message: str):
        """Log error message"""
        error_log = self.base_path / "automated_management_errors.log"
        with open(error_log, 'a') as f:
            f.write(f"[{datetime.now()}] {message}\n")


def main():
    """
    Main function for automated file management
    """
    print("=== Automated File Management System ===")
    print("User: Christian")
    print()
    
    # Initialize management system
    manager = AutomatedFileManagement()
    
    try:
        # Start monitoring
        print("Starting file monitoring...")
        manager.start_monitoring()
        
        print("File management system is now running.")
        print("Press Ctrl+C to stop monitoring.")
        
        # Keep running until interrupted
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping file management system...")
        manager.stop_monitoring()
        print("File management system stopped.")


if __name__ == "__main__":
    main()