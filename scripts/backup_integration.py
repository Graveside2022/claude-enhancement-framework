#!/usr/bin/env python3
# CLAUDE Improvement Project - Backup System Integration
# Purpose: Connect project handoff with backup system for continuous data preservation
# Usage: Used by handoff and continuity systems
# Requirements: python3, standard library modules

import os
import json
import shutil
import hashlib
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BackupIntegration:
    """
    Backup system integration for CLAUDE project handoff system.
    Handles backup creation, verification, cleanup, and integrity checks.
    
    User: Christian
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.backups_dir = self.project_root / "backups"
        self.marker_file = self.backups_dir / ".last_scheduled_backup"
        self.log_file = self.backups_dir / "backup_log.txt"
        self.backup_interval_minutes = 120
        
        # Critical files that must be backed up
        self.critical_files = [
            "TODO.md",
            "CLAUDE.md", 
            "SESSION_CONTINUITY.md",
            "HANDOFF_SUMMARY.md",
            "NEXT_SESSION_HANDOFF_PROMPT.md",
            ".project_context",
            "LEARNED_CORRECTIONS.md"
        ]
        
        # Ensure backup directory exists
        self.backups_dir.mkdir(exist_ok=True)
        
        logger.info(f"Backup integration initialized for Christian's project at: {self.project_root}")

    def check_backup_due(self) -> bool:
        """
        Check if backup is due based on 30-minute interval.
        
        Returns:
            bool: True if backup is needed, False otherwise
        """
        if not self.marker_file.exists():
            logger.info("No backup marker found - backup required")
            return True
            
        try:
            last_backup_time = datetime.datetime.fromtimestamp(
                self.marker_file.stat().st_mtime
            )
            current_time = datetime.datetime.now()
            minutes_since_backup = (current_time - last_backup_time).total_seconds() / 60
            
            backup_due = minutes_since_backup >= self.backup_interval_minutes
            
            if backup_due:
                logger.info(f"Backup due: {minutes_since_backup:.1f} minutes since last backup (120-minute threshold)")
            else:
                logger.info(f"Backup not due: {minutes_since_backup:.1f} minutes since last backup (120-minute threshold)")
                
            return backup_due
            
        except Exception as e:
            logger.warning(f"Error checking backup time: {e} - assuming backup needed")
            return True

    def create_backup(self, reason: str = "routine") -> Optional[str]:
        """
        Create a versioned backup of critical project files.
        
        Args:
            reason: Reason for backup creation
            
        Returns:
            str: Backup directory name if successful, None if failed
        """
        try:
            # Generate backup directory name
            date_stamp = datetime.datetime.now().strftime("%Y-%m-%d")
            version = self._get_next_version(date_stamp)
            backup_name = f"{date_stamp}_v{version}"
            backup_path = self.backups_dir / backup_name
            
            # Create backup directory
            backup_path.mkdir(exist_ok=True)
            
            logger.info(f"Creating backup: {backup_name} (reason: {reason})")
            
            # Copy critical files
            files_backed_up = []
            for file_name in self.critical_files:
                source_file = self.project_root / file_name
                if source_file.exists():
                    dest_file = backup_path / file_name
                    # Create subdirectories if needed
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_file, dest_file)
                    files_backed_up.append(file_name)
                    logger.debug(f"Backed up: {file_name}")
            
            # Copy memory directory if it exists
            memory_dir = self.project_root / "memory"
            if memory_dir.exists():
                dest_memory = backup_path / "memory"
                shutil.copytree(memory_dir, dest_memory, dirs_exist_ok=True)
                files_backed_up.append("memory/")
                logger.debug("Backed up memory directory")
            
            # Create backup metadata
            metadata = self._create_backup_metadata(backup_name, reason, files_backed_up)
            metadata_file = backup_path / "backup_info.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, default=str)
            
            # Verify backup integrity
            if self._verify_backup_integrity(backup_path):
                # Update marker file
                self.marker_file.touch()
                
                # Log backup creation
                self._log_backup_creation(backup_name, reason, len(files_backed_up))
                
                # Cleanup old backups
                self._cleanup_old_backups()
                
                logger.info(f"✓ Backup created successfully: {backup_name}")
                return backup_name
            else:
                logger.error(f"Backup verification failed: {backup_name}")
                # Remove failed backup
                shutil.rmtree(backup_path, ignore_errors=True)
                return None
                
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return None

    def _get_next_version(self, date_stamp: str) -> int:
        """Get the next version number for a given date."""
        version = 1
        while (self.backups_dir / f"{date_stamp}_v{version}").exists():
            version += 1
        return version

    def _create_backup_metadata(self, backup_name: str, reason: str, files_backed_up: List[str]) -> Dict:
        """Create metadata for the backup."""
        # Get git status if available
        git_status = "No git repository"
        try:
            import subprocess
            result = subprocess.run(
                ["git", "status", "--short"], 
                cwd=self.project_root,
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0:
                uncommitted_changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
                git_status = f"{uncommitted_changes} uncommitted changes"
        except Exception:
            pass
        
        return {
            "backup_created": datetime.datetime.now(),
            "user": "Christian",
            "reason": reason,
            "version": backup_name,
            "project_state": {
                "files_in_root": len(list(self.project_root.glob("*"))),
                "todo_lines": self._count_file_lines("TODO.md"),
                "git_status": git_status
            },
            "files_backed_up": files_backed_up,
            "integrity_verified": False  # Will be updated after verification
        }

    def _count_file_lines(self, filename: str) -> int:
        """Count lines in a file."""
        try:
            file_path = self.project_root / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return len(f.readlines())
        except Exception:
            pass
        return 0

    def _verify_backup_integrity(self, backup_path: Path) -> bool:
        """
        Verify backup integrity through file comparisons and checksums.
        
        Args:
            backup_path: Path to the backup directory
            
        Returns:
            bool: True if backup is valid, False otherwise
        """
        try:
            verification_results = []
            
            for file_name in self.critical_files:
                source_file = self.project_root / file_name
                backup_file = backup_path / file_name
                
                if source_file.exists() and backup_file.exists():
                    # Compare file sizes
                    source_size = source_file.stat().st_size
                    backup_size = backup_file.stat().st_size
                    
                    if source_size != backup_size:
                        logger.error(f"Size mismatch for {file_name}: {source_size} vs {backup_size}")
                        verification_results.append(False)
                        continue
                    
                    # Compare checksums for critical files
                    if source_size > 0:  # Only check non-empty files
                        source_hash = self._calculate_file_hash(source_file)
                        backup_hash = self._calculate_file_hash(backup_file)
                        
                        if source_hash != backup_hash:
                            logger.error(f"Checksum mismatch for {file_name}")
                            verification_results.append(False)
                            continue
                    
                    verification_results.append(True)
                    logger.debug(f"Verified: {file_name}")
                elif source_file.exists():
                    logger.error(f"Missing backup file: {file_name}")
                    verification_results.append(False)
            
            # Update metadata with verification status
            metadata_file = backup_path / "backup_info.json"
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                metadata["integrity_verified"] = all(verification_results)
                metadata["verification_timestamp"] = datetime.datetime.now()
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2, default=str)
            
            success = all(verification_results) and len(verification_results) > 0
            
            if success:
                logger.info("✓ Backup integrity verification passed")
            else:
                logger.error("✗ Backup integrity verification failed")
                
            return success
            
        except Exception as e:
            logger.error(f"Backup verification error: {e}")
            return False

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file."""
        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {file_path}: {e}")
            return ""

    def _log_backup_creation(self, backup_name: str, reason: str, file_count: int):
        """Log backup creation to backup_log.txt."""
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            log_entry = f"[{timestamp}] {backup_name} - {reason} ({file_count} files)\n"
            
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                
        except Exception as e:
            logger.error(f"Failed to write backup log: {e}")

    def _cleanup_old_backups(self, retention_days: int = 30):
        """
        Clean up backups older than retention period.
        
        Args:
            retention_days: Number of days to retain backups
        """
        try:
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=retention_days)
            
            for backup_dir in self.backups_dir.iterdir():
                if backup_dir.is_dir() and backup_dir.name.startswith("20"):
                    # Check if backup is older than retention period
                    backup_time = datetime.datetime.fromtimestamp(backup_dir.stat().st_mtime)
                    
                    if backup_time < cutoff_date:
                        logger.info(f"Removing old backup: {backup_dir.name}")
                        shutil.rmtree(backup_dir, ignore_errors=True)
                        
        except Exception as e:
            logger.error(f"Error during backup cleanup: {e}")

    def ensure_backup_before_handoff(self) -> bool:
        """
        Ensure backup is created before handoff operations.
        Always creates backup regardless of timer to preserve handoff state.
        
        Returns:
            bool: True if backup successful, False otherwise
        """
        logger.info("Creating pre-handoff backup for Christian's project")
        backup_name = self.create_backup("pre_handoff")
        return backup_name is not None

    def get_backup_status(self) -> Dict:
        """
        Get current backup system status.
        
        Returns:
            dict: Status information
        """
        try:
            status = {
                "backup_system_active": True,
                "backups_directory": str(self.backups_dir),
                "last_backup": "Never",
                "minutes_since_backup": float('inf'),
                "backup_due": True,
                "total_backups": 0,
                "oldest_backup": None,
                "newest_backup": None
            }
            
            if self.marker_file.exists():
                last_backup_time = datetime.datetime.fromtimestamp(
                    self.marker_file.stat().st_mtime
                )
                status["last_backup"] = last_backup_time.isoformat()
                status["minutes_since_backup"] = (
                    datetime.datetime.now() - last_backup_time
                ).total_seconds() / 60
                status["backup_due"] = status["minutes_since_backup"] >= self.backup_interval_minutes
            
            # Count backups
            backup_dirs = [d for d in self.backups_dir.iterdir() if d.is_dir() and d.name.startswith("20")]
            status["total_backups"] = len(backup_dirs)
            
            if backup_dirs:
                backup_dirs.sort(key=lambda x: x.stat().st_mtime)
                status["oldest_backup"] = backup_dirs[0].name
                status["newest_backup"] = backup_dirs[-1].name
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting backup status: {e}")
            return {"backup_system_active": False, "error": str(e)}

    def list_recent_backups(self, limit: int = 10) -> List[Dict]:
        """
        List recent backups with metadata.
        
        Args:
            limit: Maximum number of backups to return
            
        Returns:
            list: List of backup information
        """
        try:
            backups = []
            backup_dirs = [d for d in self.backups_dir.iterdir() if d.is_dir() and d.name.startswith("20")]
            backup_dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            for backup_dir in backup_dirs[:limit]:
                info = {
                    "name": backup_dir.name,
                    "created": datetime.datetime.fromtimestamp(backup_dir.stat().st_mtime).isoformat(),
                    "size_mb": self._get_directory_size(backup_dir) / (1024 * 1024)
                }
                
                # Load metadata if available
                metadata_file = backup_dir / "backup_info.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                        info.update({
                            "reason": metadata.get("reason", "unknown"),
                            "files_count": len(metadata.get("files_backed_up", [])),
                            "verified": metadata.get("integrity_verified", False)
                        })
                    except Exception:
                        pass
                        
                backups.append(info)
                
            return backups
            
        except Exception as e:
            logger.error(f"Error listing backups: {e}")
            return []

    def _get_directory_size(self, path: Path) -> int:
        """Calculate total size of directory in bytes."""
        total = 0
        try:
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    total += file_path.stat().st_size
        except Exception:
            pass
        return total


def main():
    """Main function for standalone usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="CLAUDE Backup Integration System")
    parser.add_argument("--check", action="store_true", help="Check if backup is due")
    parser.add_argument("--create", metavar="REASON", help="Create backup with reason")
    parser.add_argument("--status", action="store_true", help="Show backup status")
    parser.add_argument("--list", action="store_true", help="List recent backups")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    
    args = parser.parse_args()
    
    backup_system = BackupIntegration(args.project_root)
    
    if args.check:
        due = backup_system.check_backup_due()
        print(f"Backup due: {due}")
        exit(0 if due else 1)
    elif args.create:
        result = backup_system.create_backup(args.create)
        if result:
            print(f"Backup created: {result}")
        else:
            print("Backup creation failed")
            exit(1)
    elif args.status:
        status = backup_system.get_backup_status()
        print(json.dumps(status, indent=2, default=str))
    elif args.list:
        backups = backup_system.list_recent_backups()
        print(json.dumps(backups, indent=2, default=str))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()