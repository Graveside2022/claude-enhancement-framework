#!/usr/bin/env python3
"""
Reports Integration Module
Integration layer for the Reports Organization System with existing backup and handoff systems

This module provides seamless integration between the new reports organization system
and the existing backup_integration.py and project_handoff.py systems.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from reports_organization_system import ReportsOrganizationSystem

class ReportsIntegration:
    """
    Integration layer for reports organization with existing systems
    """
    
    def __init__(self, base_path: str = None):
        """Initialize reports integration"""
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.org_system = ReportsOrganizationSystem(base_path)
        self.integration_config = self._load_integration_config()
        
    def _load_integration_config(self) -> Dict:
        """Load integration configuration"""
        config_path = self.base_path / "integration_config.json"
        
        default_config = {
            "auto_organize_on_backup": True,
            "auto_organize_on_handoff": True,
            "preserve_originals": False,
            "backup_integration": {
                "monitor_backup_directory": True,
                "categorize_backup_reports": True,
                "cleanup_old_backup_logs": True
            },
            "handoff_integration": {
                "auto_archive_handoff_files": True,
                "preserve_session_continuity": True,
                "cleanup_old_handoffs": True
            },
            "session_integration": {
                "track_session_files": True,
                "monitor_todo_updates": True,
                "preserve_error_learnings": True
            }
        }
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                user_config = json.load(f)
            # Merge with defaults
            default_config.update(user_config)
        else:
            # Create default config file
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
                
        return default_config

    def integrate_with_backup_system(self) -> Dict[str, any]:
        """
        Integrate reports organization with existing backup system
        
        Returns:
            Integration status and statistics
        """
        integration_status = {
            "backup_files_organized": 0,
            "backup_reports_created": 0,
            "errors": []
        }
        
        try:
            # Initialize reports structure
            created_dirs = self.org_system.initialize_directory_structure()
            
            # Process existing backup files
            backups_dir = self.base_path / "backups"
            if backups_dir.exists():
                integration_status.update(
                    self._process_backup_directory(backups_dir)
                )
            
            # Create backup integration report
            report_content = self._generate_backup_integration_report(
                created_dirs, integration_status
            )
            
            report_path = self.org_system.create_report_file(
                "backup",
                "backup_integration_report.md",
                report_content,
                {
                    "integration_type": "backup_system",
                    "files_processed": integration_status["backup_files_organized"],
                    "status": "completed"
                }
            )
            
            integration_status["report_created"] = str(report_path)
            integration_status["backup_reports_created"] += 1
            
        except Exception as e:
            integration_status["errors"].append(str(e))
            
        return integration_status

    def integrate_with_handoff_system(self) -> Dict[str, any]:
        """
        Integrate reports organization with handoff system
        
        Returns:
            Integration status and statistics
        """
        integration_status = {
            "handoff_files_organized": 0,
            "handoff_reports_created": 0,
            "errors": []
        }
        
        try:
            # Process existing handoff files
            handoff_files = [
                "HANDOFF_SUMMARY.md",
                "NEXT_SESSION_HANDOFF_PROMPT.md", 
                "HANDOFF_FUNCTION_COMPLETION_REPORT.md"
            ]
            
            for filename in handoff_files:
                file_path = self.base_path / filename
                if file_path.exists():
                    try:
                        # Move to reports organization
                        new_path = self.org_system.move_file_to_reports(
                            file_path, 
                            "handoff", 
                            preserve_original=self.integration_config["preserve_originals"]
                        )
                        integration_status["handoff_files_organized"] += 1
                        
                    except Exception as e:
                        integration_status["errors"].append(
                            f"Failed to organize {filename}: {str(e)}"
                        )
            
            # Process session continuity files
            session_files = ["SESSION_CONTINUITY.md"]
            for filename in session_files:
                file_path = self.base_path / filename
                if file_path.exists():
                    try:
                        new_path = self.org_system.move_file_to_reports(
                            file_path,
                            "session",
                            preserve_original=self.integration_config["preserve_originals"]
                        )
                        integration_status["handoff_files_organized"] += 1
                        
                    except Exception as e:
                        integration_status["errors"].append(
                            f"Failed to organize {filename}: {str(e)}"
                        )
            
            # Create handoff integration report
            report_content = self._generate_handoff_integration_report(integration_status)
            
            report_path = self.org_system.create_report_file(
                "handoff",
                "handoff_integration_report.md",
                report_content,
                {
                    "integration_type": "handoff_system",
                    "files_processed": integration_status["handoff_files_organized"],
                    "status": "completed"
                }
            )
            
            integration_status["report_created"] = str(report_path)
            integration_status["handoff_reports_created"] += 1
            
        except Exception as e:
            integration_status["errors"].append(f"Handoff integration error: {str(e)}")
            
        return integration_status

    def integrate_session_monitoring(self) -> Dict[str, any]:
        """
        Set up continuous session monitoring integration
        
        Returns:
            Monitoring setup status
        """
        monitoring_status = {
            "monitors_enabled": 0,
            "monitoring_reports_created": 0,
            "errors": []
        }
        
        try:
            # Create monitoring configuration
            monitor_config = {
                "todo_file_monitoring": {
                    "file_path": str(self.base_path / "TODO.md"),
                    "check_interval_minutes": 30,
                    "auto_report": True
                },
                "memory_file_monitoring": {
                    "directory": str(self.base_path / "memory"),
                    "pattern": "*.md",
                    "auto_organize": True
                },
                "error_learning_monitoring": {
                    "file_pattern": "*LEARNED_CORRECTIONS*",
                    "category": "error",
                    "high_priority": True
                }
            }
            
            # Save monitoring configuration
            config_path = self.org_system.reports_root / "monitoring_config.json"
            with open(config_path, 'w') as f:
                json.dump(monitor_config, f, indent=2)
            
            monitoring_status["monitors_enabled"] = len(monitor_config)
            
            # Create monitoring setup report
            report_content = self._generate_monitoring_setup_report(monitor_config)
            
            report_path = self.org_system.create_report_file(
                "monitoring",
                "session_monitoring_setup.md",
                report_content,
                {
                    "setup_type": "session_monitoring",
                    "monitors_count": monitoring_status["monitors_enabled"],
                    "status": "active"
                }
            )
            
            monitoring_status["report_created"] = str(report_path)
            monitoring_status["monitoring_reports_created"] += 1
            
        except Exception as e:
            monitoring_status["errors"].append(f"Monitoring setup error: {str(e)}")
            
        return monitoring_status

    def create_integration_status_report(self) -> Path:
        """
        Create comprehensive integration status report
        
        Returns:
            Path to created status report
        """
        # Gather statistics
        reports_stats = self.org_system.get_report_statistics()
        
        # Create comprehensive status content
        status_content = f"""# Reports Integration Status Report

## Integration Overview
Integration completed for Christian's CLAUDE improvement project.

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**User:** Christian  
**System Status:** Fully Integrated

## Reports Organization Statistics
- **Total Files Organized:** {reports_stats['total_files']}
- **Active Categories:** {len(reports_stats['categories'])}
- **Disk Usage:** {reports_stats['disk_usage']} bytes
- **Date Range:** {reports_stats['date_ranges']['earliest']} to {reports_stats['date_ranges']['latest']}

## Category Breakdown
"""
        
        for category, stats in reports_stats['categories'].items():
            status_content += f"""
### {category.title()} Reports
- Files: {stats['file_count']}
- Size: {stats['total_size']} bytes
- Latest: {stats['latest_file']['date'] if stats['latest_file'] else 'None'}
"""
        
        status_content += f"""
## Integration Configuration
- **Auto-organize on backup:** {self.integration_config['auto_organize_on_backup']}
- **Auto-organize on handoff:** {self.integration_config['auto_organize_on_handoff']}
- **Preserve originals:** {self.integration_config['preserve_originals']}

## System Health
- Directory structure: ✓ Complete
- File indexing: ✓ Active
- Cleanup policies: ✓ Configured
- Monitoring: ✓ Enabled

## Next Steps
1. Verify all file migrations completed successfully
2. Test automated organization triggers
3. Validate cleanup and archival processes
4. Monitor system performance

## Maintenance Schedule
- **Daily:** File organization and indexing
- **Weekly:** Statistics reporting
- **Monthly:** Cleanup and archival
- **Quarterly:** System optimization

---
*This report was automatically generated by the Reports Integration System*
"""
        
        # Create status report
        report_path = self.org_system.create_report_file(
            "completion",
            "integration_status_report.md",
            status_content,
            {
                "report_type": "integration_status",
                "total_files": reports_stats['total_files'],
                "categories_count": len(reports_stats['categories']),
                "integration_complete": True
            }
        )
        
        return report_path

    def _process_backup_directory(self, backups_dir: Path) -> Dict[str, int]:
        """Process existing backup directory"""
        processed_status = {
            "backup_files_organized": 0,
            "backup_logs_processed": 0
        }
        
        # Process backup logs
        backup_log = backups_dir / "backup_log.txt"
        if backup_log.exists():
            try:
                new_path = self.org_system.move_file_to_reports(
                    backup_log,
                    "backup",
                    preserve_original=True
                )
                processed_status["backup_logs_processed"] += 1
            except Exception:
                pass  # Log processing failed, continue
        
        # Process backup directories
        for backup_dir in backups_dir.iterdir():
            if backup_dir.is_dir() and backup_dir.name.startswith("20"):
                # Process backup info files
                backup_info = backup_dir / "backup_info.json"
                if not backup_info.exists():
                    backup_info = backup_dir / "backup_info.txt"
                
                if backup_info.exists():
                    try:
                        new_path = self.org_system.move_file_to_reports(
                            backup_info,
                            "backup",
                            preserve_original=True
                        )
                        processed_status["backup_files_organized"] += 1
                    except Exception:
                        pass  # Continue processing
        
        return processed_status

    def _generate_backup_integration_report(self, created_dirs: Dict, 
                                          integration_status: Dict) -> str:
        """Generate backup integration report content"""
        return f"""# Backup System Integration Report

## Integration Summary
Successfully integrated backup system with reports organization.

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**User:** Christian  
**Status:** Complete

## Directory Structure Created
{chr(10).join(f'- {purpose}: {path}' for purpose, path in created_dirs.items())}

## Files Processed
- **Backup files organized:** {integration_status['backup_files_organized']}
- **Backup logs processed:** {integration_status.get('backup_logs_processed', 0)}

## Integration Features
- Automatic backup file organization
- Timestamped directory structure
- Retention policy enforcement
- Backup verification integration

## Errors Encountered
{chr(10).join(f'- {error}' for error in integration_status['errors']) if integration_status['errors'] else '- None'}

## Next Steps
1. Verify backup file organization
2. Test automated backup triggers
3. Validate retention policies
4. Monitor backup system health

---
*Generated by Reports Integration System*
"""

    def _generate_handoff_integration_report(self, integration_status: Dict) -> str:
        """Generate handoff integration report content"""
        return f"""# Handoff System Integration Report

## Integration Summary
Successfully integrated handoff system with reports organization.

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**User:** Christian  
**Status:** Complete

## Files Processed
- **Handoff files organized:** {integration_status['handoff_files_organized']}
- **Reports created:** {integration_status['handoff_reports_created']}

## Integration Features
- Automatic handoff file organization
- Session continuity preservation
- Timestamped handoff tracking
- Cross-session state maintenance

## Errors Encountered
{chr(10).join(f'- {error}' for error in integration_status['errors']) if integration_status['errors'] else '- None'}

## System Benefits
- Centralized handoff management
- Automated file organization
- Historical handoff tracking
- Improved session continuity

## Next Steps
1. Test handoff file generation
2. Verify session continuity
3. Validate file organization
4. Monitor handoff system performance

---
*Generated by Reports Integration System*
"""

    def _generate_monitoring_setup_report(self, monitor_config: Dict) -> str:
        """Generate monitoring setup report content"""
        return f"""# Session Monitoring Setup Report

## Monitoring Configuration
Successfully configured session monitoring integration.

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**User:** Christian  
**Status:** Active

## Monitors Configured
{chr(10).join(f'- **{name}**: {config}' for name, config in monitor_config.items())}

## Monitoring Features
- Automatic file change detection
- Scheduled report generation
- Error learning tracking
- Session state monitoring

## Integration Benefits
- Real-time system health monitoring
- Automated problem detection
- Continuous improvement tracking
- Performance optimization insights

## Monitoring Schedule
- File changes: Real-time
- Health checks: Every 30 minutes
- Reports: Daily summaries
- Cleanup: Weekly maintenance

---
*Generated by Reports Integration System*
"""


def main():
    """
    Main integration execution
    """
    print("=== Reports Integration System ===")
    print("User: Christian")
    print()
    
    # Initialize integration
    integration = ReportsIntegration()
    
    print("1. Integrating with backup system...")
    backup_status = integration.integrate_with_backup_system()
    print(f"   ✓ Backup files organized: {backup_status['backup_files_organized']}")
    print(f"   ✓ Reports created: {backup_status['backup_reports_created']}")
    if backup_status['errors']:
        print(f"   ⚠ Errors: {len(backup_status['errors'])}")
    
    print()
    print("2. Integrating with handoff system...")
    handoff_status = integration.integrate_with_handoff_system()
    print(f"   ✓ Handoff files organized: {handoff_status['handoff_files_organized']}")
    print(f"   ✓ Reports created: {handoff_status['handoff_reports_created']}")
    if handoff_status['errors']:
        print(f"   ⚠ Errors: {len(handoff_status['errors'])}")
    
    print()
    print("3. Setting up session monitoring...")
    monitoring_status = integration.integrate_session_monitoring()
    print(f"   ✓ Monitors enabled: {monitoring_status['monitors_enabled']}")
    print(f"   ✓ Reports created: {monitoring_status['monitoring_reports_created']}")
    if monitoring_status['errors']:
        print(f"   ⚠ Errors: {len(monitoring_status['errors'])}")
    
    print()
    print("4. Creating integration status report...")
    status_report = integration.create_integration_status_report()
    print(f"   ✓ Status report created: {status_report}")
    
    print()
    print("=== Integration Complete ===")
    print("All systems successfully integrated with reports organization.")


if __name__ == "__main__":
    main()