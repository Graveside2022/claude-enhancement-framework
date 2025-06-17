#!/usr/bin/env python3
"""
Reports Organization System - Design Document
Created for Christian's CLAUDE improvement project

This system creates a clean organizational structure for all generated files
with automated directory management, timestamped categorization, and maintenance.
"""

import os
import shutil
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import hashlib

class ReportsOrganizationSystem:
    """
    Comprehensive file organization system for CLAUDE project reports
    """
    
    def __init__(self, base_path: str = None):
        """Initialize the reports organization system"""
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.reports_root = self.base_path / "reports"
        self.config_file = self.reports_root / "organization_config.json"
        
        # Report categories with their purposes
        self.report_categories = {
            "handoff": {
                "description": "Session handoff and continuity files",
                "retention_days": 90,
                "examples": ["HANDOFF_SUMMARY.md", "NEXT_SESSION_HANDOFF_PROMPT.md"]
            },
            "backup": {
                "description": "Backup verification and status reports",
                "retention_days": 30,
                "examples": ["backup_verification.json", "backup_status.md"]
            },
            "session": {
                "description": "Session state and continuity tracking",
                "retention_days": 60,
                "examples": ["SESSION_CONTINUITY.md", "session_state.json"]
            },
            "error": {
                "description": "Error analysis and learning records",
                "retention_days": 180,
                "examples": ["LEARNED_CORRECTIONS.md", "error_analysis.json"]
            },
            "analysis": {
                "description": "Code and project analysis reports",
                "retention_days": 45,
                "examples": ["dependency_analysis.md", "code_review.json"]
            },
            "monitoring": {
                "description": "System monitoring and health checks",
                "retention_days": 30,
                "examples": ["timing_compliance.json", "resource_usage.md"]
            },
            "completion": {
                "description": "Task and project completion reports",
                "retention_days": 120,
                "examples": ["task_completion.md", "project_status.json"]
            }
        }
        
        # File naming patterns
        self.naming_patterns = {
            "timestamp_format": "%Y-%m-%d_%H-%M-%S",
            "date_format": "%Y-%m-%d",
            "prefixes": {
                "report": "RPT",
                "backup": "BKP", 
                "session": "SES",
                "handoff": "HND",
                "error": "ERR",
                "analysis": "ANL",
                "monitoring": "MON",
                "completion": "CMP"
            }
        }

    def initialize_directory_structure(self) -> Dict[str, str]:
        """
        Create the complete reports directory structure
        Returns: Dictionary of created directories
        """
        created_dirs = {}
        
        # Create main reports directory
        self.reports_root.mkdir(exist_ok=True)
        created_dirs["reports_root"] = str(self.reports_root)
        
        # Create date-based structure for current date
        current_date = datetime.now().strftime(self.naming_patterns["date_format"])
        date_dir = self.reports_root / current_date
        date_dir.mkdir(exist_ok=True)
        created_dirs["current_date"] = str(date_dir)
        
        # Create category subdirectories
        for category, config in self.report_categories.items():
            category_dir = date_dir / category
            category_dir.mkdir(exist_ok=True)
            created_dirs[f"category_{category}"] = str(category_dir)
            
            # Create README for each category
            readme_path = category_dir / "README.md"
            if not readme_path.exists():
                self._create_category_readme(readme_path, category, config)
        
        # Create archive directory for old reports
        archive_dir = self.reports_root / "archive"
        archive_dir.mkdir(exist_ok=True)
        created_dirs["archive"] = str(archive_dir)
        
        # Create index file
        self._create_master_index()
        
        return created_dirs

    def generate_file_path(self, category: str, filename: str, 
                          custom_date: datetime = None) -> Path:
        """
        Generate standardized file path with timestamp
        
        Args:
            category: Report category (handoff, backup, session, etc.)
            filename: Base filename without timestamp
            custom_date: Optional custom date (defaults to now)
            
        Returns:
            Complete file path with timestamp
        """
        if category not in self.report_categories:
            raise ValueError(f"Unknown category: {category}. "
                           f"Valid categories: {list(self.report_categories.keys())}")
        
        # Use custom date or current date
        date_obj = custom_date or datetime.now()
        date_str = date_obj.strftime(self.naming_patterns["date_format"])
        timestamp = date_obj.strftime(self.naming_patterns["timestamp_format"])
        
        # Get category prefix
        prefix = self.naming_patterns["prefixes"].get(category, "RPT")
        
        # Create timestamped filename
        name_parts = filename.split(".")
        if len(name_parts) > 1:
            base_name = ".".join(name_parts[:-1])
            extension = name_parts[-1]
            timestamped_name = f"{prefix}_{timestamp}_{base_name}.{extension}"
        else:
            timestamped_name = f"{prefix}_{timestamp}_{filename}"
        
        # Build complete path
        category_dir = self.reports_root / date_str / category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        return category_dir / timestamped_name

    def move_file_to_reports(self, source_path: Path, category: str, 
                           preserve_original: bool = False) -> Path:
        """
        Move or copy file to appropriate reports directory
        
        Args:
            source_path: Path to source file
            category: Target category
            preserve_original: If True, copy instead of move
            
        Returns:
            New file path in reports directory
        """
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")
        
        # Generate target path
        target_path = self.generate_file_path(category, source_path.name)
        
        # Move or copy file
        if preserve_original:
            shutil.copy2(source_path, target_path)
        else:
            shutil.move(str(source_path), target_path)
        
        # Update index
        self._update_file_index(target_path, category, source_path)
        
        return target_path

    def create_report_file(self, category: str, filename: str, 
                          content: str, metadata: Dict = None) -> Path:
        """
        Create new report file with content and metadata
        
        Args:
            category: Report category
            filename: Base filename
            content: File content
            metadata: Optional metadata dictionary
            
        Returns:
            Path to created file
        """
        # Generate file path
        file_path = self.generate_file_path(category, filename)
        
        # Add metadata header if provided
        if metadata:
            metadata_header = self._generate_metadata_header(metadata)
            content = metadata_header + "\n" + content
        
        # Write content
        file_path.write_text(content, encoding='utf-8')
        
        # Update index
        self._update_file_index(file_path, category, metadata=metadata)
        
        return file_path

    def cleanup_old_reports(self, dry_run: bool = False) -> Dict[str, List[str]]:
        """
        Clean up old reports based on retention policies
        
        Args:
            dry_run: If True, only report what would be deleted
            
        Returns:
            Dictionary of deleted files by category
        """
        deleted_files = {category: [] for category in self.report_categories}
        current_date = datetime.now()
        
        # Process each category
        for category, config in self.report_categories.items():
            retention_days = config["retention_days"]
            cutoff_date = current_date - timedelta(days=retention_days)
            
            # Find old files
            for date_dir in self.reports_root.iterdir():
                if not date_dir.is_dir() or date_dir.name == "archive":
                    continue
                
                try:
                    dir_date = datetime.strptime(date_dir.name, 
                                               self.naming_patterns["date_format"])
                    if dir_date < cutoff_date:
                        category_dir = date_dir / category
                        if category_dir.exists():
                            for file_path in category_dir.iterdir():
                                if file_path.is_file():
                                    if not dry_run:
                                        # Move to archive before deletion
                                        self._archive_file(file_path, category)
                                        file_path.unlink()
                                    deleted_files[category].append(str(file_path))
                except ValueError:
                    # Skip directories with invalid date format
                    continue
        
        return deleted_files

    def get_report_statistics(self) -> Dict[str, any]:
        """
        Generate statistics about reports organization
        
        Returns:
            Dictionary with comprehensive statistics
        """
        stats = {
            "total_files": 0,
            "categories": {},
            "date_ranges": {"earliest": None, "latest": None},
            "disk_usage": 0,
            "recent_activity": []
        }
        
        # Collect statistics
        for date_dir in self.reports_root.iterdir():
            if not date_dir.is_dir() or date_dir.name == "archive":
                continue
            
            try:
                dir_date = datetime.strptime(date_dir.name, 
                                           self.naming_patterns["date_format"])
                # Update date ranges
                if not stats["date_ranges"]["earliest"] or dir_date < stats["date_ranges"]["earliest"]:
                    stats["date_ranges"]["earliest"] = dir_date
                if not stats["date_ranges"]["latest"] or dir_date > stats["date_ranges"]["latest"]:
                    stats["date_ranges"]["latest"] = dir_date
                
            except ValueError:
                continue
            
            # Process category statistics
            for category in self.report_categories:
                category_dir = date_dir / category
                if category_dir.exists():
                    if category not in stats["categories"]:
                        stats["categories"][category] = {
                            "file_count": 0,
                            "total_size": 0,
                            "latest_file": None
                        }
                    
                    for file_path in category_dir.iterdir():
                        if file_path.is_file():
                            file_size = file_path.stat().st_size
                            file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                            
                            stats["total_files"] += 1
                            stats["categories"][category]["file_count"] += 1
                            stats["categories"][category]["total_size"] += file_size
                            stats["disk_usage"] += file_size
                            
                            if (not stats["categories"][category]["latest_file"] or 
                                file_mtime > stats["categories"][category]["latest_file"]["date"]):
                                stats["categories"][category]["latest_file"] = {
                                    "path": str(file_path),
                                    "date": file_mtime
                                }
        
        return stats

    def _create_category_readme(self, readme_path: Path, category: str, config: Dict):
        """Create README file for category directory"""
        content = f"""# {category.title()} Reports

## Purpose
{config['description']}

## Retention Policy
Files in this category are retained for {config['retention_days']} days.

## File Examples
{chr(10).join(f'- {example}' for example in config['examples'])}

## Naming Convention
Files follow the pattern: {self.naming_patterns['prefixes'].get(category, 'RPT')}_YYYY-MM-DD_HH-MM-SS_filename.ext

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
User: Christian
"""
        readme_path.write_text(content, encoding='utf-8')

    def _create_master_index(self):
        """Create master index file for reports directory"""
        index_path = self.reports_root / "INDEX.md"
        content = f"""# Reports Directory Index

## Organization Structure
This directory contains organized reports for Christian's CLAUDE improvement project.

## Categories
{chr(10).join(f'- **{cat}**: {config["description"]} (Retention: {config["retention_days"]} days)' 
              for cat, config in self.report_categories.items())}

## Directory Structure
```
reports/
├── YYYY-MM-DD/          # Date-based directories
│   ├── handoff/         # Session handoff files
│   ├── backup/          # Backup verification files
│   ├── session/         # Session state files
│   ├── error/           # Error learning files
│   ├── analysis/        # Analysis reports
│   ├── monitoring/      # System monitoring
│   └── completion/      # Task completion reports
├── archive/             # Archived old reports
└── INDEX.md            # This file

```

## File Naming Convention
- Format: PREFIX_YYYY-MM-DD_HH-MM-SS_filename.ext
- Prefixes: {', '.join(f'{k}={v}' for k, v in self.naming_patterns['prefixes'].items())}

## Maintenance
- Automatic cleanup based on retention policies
- Files moved to archive before deletion
- Statistics and monitoring available

Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
User: Christian
"""
        index_path.write_text(content, encoding='utf-8')

    def _generate_metadata_header(self, metadata: Dict) -> str:
        """Generate metadata header for report files"""
        lines = ["---"]
        lines.append(f"generated: {datetime.now().isoformat()}")
        lines.append("user: Christian")
        
        for key, value in metadata.items():
            lines.append(f"{key}: {value}")
        
        lines.append("---")
        return "\n".join(lines)

    def _update_file_index(self, file_path: Path, category: str, 
                          source_path: Path = None, metadata: Dict = None):
        """Update file index with new entry"""
        index_file = self.reports_root / "file_index.json"
        
        # Load existing index
        if index_file.exists():
            with open(index_file, 'r') as f:
                index_data = json.load(f)
        else:
            index_data = {"files": [], "last_updated": None}
        
        # Add new entry
        entry = {
            "path": str(file_path.relative_to(self.reports_root)),
            "category": category,
            "created": datetime.now().isoformat(),
            "size": file_path.stat().st_size,
            "checksum": self._calculate_checksum(file_path)
        }
        
        if source_path:
            entry["source_path"] = str(source_path)
        
        if metadata:
            entry["metadata"] = metadata
        
        index_data["files"].append(entry)
        index_data["last_updated"] = datetime.now().isoformat()
        
        # Save updated index
        with open(index_file, 'w') as f:
            json.dump(index_data, f, indent=2)

    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA-256 checksum of file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    def _archive_file(self, file_path: Path, category: str):
        """Move file to archive directory"""
        archive_dir = self.reports_root / "archive" / category
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Create unique archived filename
        timestamp = datetime.now().strftime(self.naming_patterns["timestamp_format"])
        archived_name = f"ARCHIVED_{timestamp}_{file_path.name}"
        archive_path = archive_dir / archived_name
        
        shutil.move(str(file_path), archive_path)


def demo_usage():
    """
    Demonstration of the Reports Organization System
    """
    print("=== Reports Organization System Demo ===")
    print("User: Christian")
    print()
    
    # Initialize system
    org_system = ReportsOrganizationSystem()
    
    # Create directory structure
    print("1. Creating directory structure...")
    created_dirs = org_system.initialize_directory_structure()
    for purpose, path in created_dirs.items():
        print(f"   ✓ {purpose}: {path}")
    
    print()
    
    # Generate sample file paths
    print("2. Sample file path generation:")
    sample_files = [
        ("handoff", "session_handoff.md"),
        ("backup", "backup_verification.json"),
        ("session", "session_state.md"),
        ("error", "error_analysis.json"),
        ("analysis", "dependency_report.md")
    ]
    
    for category, filename in sample_files:
        path = org_system.generate_file_path(category, filename)
        print(f"   {category}: {path}")
    
    print()
    
    # Create sample report
    print("3. Creating sample report...")
    sample_content = """# Sample Handoff Report

## Session Summary
- Task: Reports organization system design
- Status: Complete
- Next steps: Implementation testing

## Files Modified
- reports_organization_system.py: New comprehensive system

## Notes
System ready for deployment and testing.
"""
    
    sample_metadata = {
        "session_id": "demo_001",
        "task_type": "system_design",
        "priority": "high"
    }
    
    sample_file = org_system.create_report_file(
        "handoff", 
        "demo_handoff.md", 
        sample_content, 
        sample_metadata
    )
    print(f"   ✓ Created: {sample_file}")
    
    print()
    
    # Generate statistics
    print("4. System statistics:")
    stats = org_system.get_report_statistics()
    print(f"   Total files: {stats['total_files']}")
    print(f"   Disk usage: {stats['disk_usage']} bytes")
    print(f"   Categories: {len(stats['categories'])}")
    
    print()
    print("=== Demo Complete ===")


if __name__ == "__main__":
    demo_usage()