#!/usr/bin/env python3
"""
SESSION_CONTINUITY.md Archival Tool

Optimizes SESSION_CONTINUITY.md for fast boot operations by archiving
verbose logs and maintaining only essential context.

Usage:
    python3 archive_session_continuity.py [--dry-run] [--target-lines=250]
"""

import os
import re
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple

class SessionContinuityArchiver:
    def __init__(self, project_root: str, target_lines: int = 750):
        self.project_root = Path(project_root)
        self.session_file = self.project_root / "SESSION_CONTINUITY.md"
        self.archive_root = self.project_root / "logs" / "session_continuity"
        self.target_lines = target_lines
        self.current_date = datetime.now()
        
        # Ensure archive structure exists
        self.setup_archive_structure()
        
    def setup_archive_structure(self):
        """Create archive directory structure if it doesn't exist"""
        year_month = self.current_date.strftime("%Y-%m")
        archive_month_dir = self.archive_root / year_month
        archive_month_dir.mkdir(parents=True, exist_ok=True)
        
        # Create index file if it doesn't exist
        index_file = self.archive_root / "archive_index.md"
        if not index_file.exists():
            index_file.write_text(self._create_index_template())
            
        # Create search database if it doesn't exist
        search_file = self.archive_root / "quick_search.json"
        if not search_file.exists():
            search_file.write_text(json.dumps({"sessions": {}, "last_updated": str(self.current_date)}))

    def _create_index_template(self) -> str:
        """Create template for archive index"""
        return f"""# SESSION_CONTINUITY Archive Index

## Quick Access
- **Most Recent Archive**: {self.current_date.strftime('%Y-%m-%d')}
- **Total Sessions Archived**: 0
- **Last Updated**: {self.current_date.isoformat()}

## Recent Sessions (Last 30 Days)
*Archive entries will appear here automatically*

## Search Tips
- Use `./scripts/search_session_archive.sh "keyword"` for content search
- Use `./scripts/restore_session_context.sh YYYY-MM-DD` to restore specific session
- Check `quick_search.json` for machine-readable index

## Archive Structure
```
logs/session_continuity/
├── YYYY-MM/
│   ├── session_YYYY-MM-DD_HH-MM-SS.md (session summaries)
│   ├── integration_logs_YYYY-MM-DD.md (verbose script outputs)
│   └── task_details_YYYY-MM-DD.md (implementation details)
├── archive_index.md (this file)
└── quick_search.json (search database)
```
"""

    def analyze_current_file(self) -> Dict:
        """Analyze the current SESSION_CONTINUITY.md file structure"""
        if not self.session_file.exists():
            return {"error": "SESSION_CONTINUITY.md not found"}
            
        content = self.session_file.read_text()
        lines = content.split('\n')
        total_lines = len(lines)
        
        analysis = {
            "total_lines": total_lines,
            "exceeds_target": total_lines > self.target_lines,
            "sections": self._identify_sections(lines),
            "archival_candidates": [],
            "keep_active": []
        }
        
        # Categorize content
        current_section = None
        section_start = 0
        
        for i, line in enumerate(lines):
            if line.startswith('## '):
                if current_section:
                    section_lines = i - section_start
                    analysis["sections"][current_section]["lines"] = section_lines
                    analysis["sections"][current_section]["content"] = lines[section_start:i]
                    
                    # Determine if section should be archived
                    if self._should_archive_section(current_section, section_lines):
                        analysis["archival_candidates"].append(current_section)
                    else:
                        analysis["keep_active"].append(current_section)
                
                current_section = line.strip('# ')
                section_start = i
                analysis["sections"][current_section] = {"start_line": i}
        
        # Handle last section
        if current_section:
            section_lines = len(lines) - section_start
            analysis["sections"][current_section]["lines"] = section_lines
            analysis["sections"][current_section]["content"] = lines[section_start:]
            
            if self._should_archive_section(current_section, section_lines):
                analysis["archival_candidates"].append(current_section)
            else:
                analysis["keep_active"].append(current_section)
                
        return analysis

    def _identify_sections(self, lines: List[str]) -> Dict:
        """Identify major sections in the file"""
        sections = {}
        for line in lines:
            if line.startswith('## '):
                section_name = line.strip('# ')
                sections[section_name] = {"type": self._classify_section(section_name)}
        return sections

    def _classify_section(self, section_name: str) -> str:
        """Classify section type for archival decisions"""
        section_lower = section_name.lower()
        
        if "implementation update" in section_lower or "2025-" in section_name:
            return "session_summary"
        elif "project claude.md integration" in section_lower:
            return "integration_log"
        elif "checkpoint" in section_lower:
            return "checkpoint"
        elif any(word in section_lower for word in ["task", "completed", "✅"]):
            return "task_detail"
        elif "critical context" in section_lower or "summary" in section_lower:
            return "critical_context"
        elif "optimization" in section_lower or "enhancement" in section_lower:
            return "configuration_change"
        else:
            return "general"

    def _should_archive_section(self, section_name: str, line_count: int) -> bool:
        """Determine if a section should be archived based on criteria"""
        section_type = self._classify_section(section_name)
        section_lower = section_name.lower()
        
        # Always archive verbose integration logs  
        if section_type == "integration_log" or "project claude.md integration" in section_lower:
            return True
            
        # Archive completed implementation updates from previous days
        if section_type == "session_summary" and self._is_section_old(section_name):
            return True
            
        # Archive all checkpoint entries
        if section_type == "checkpoint" or "checkpoint" in section_lower:
            return True
            
        # Archive completed tasks (marked with ✅ COMPLETED)
        if "✅ completed" in section_lower or "completed!" in section_lower:
            return True
            
        # Archive large task continuations from previous sessions
        if ("continuation from" in section_lower or "task" in section_lower) and line_count > 30:
            return True
            
        # Archive implementation summaries over 40 lines (keep in archive for reference)
        if ("implementation" in section_lower or "optimization" in section_lower) and line_count > 40:
            return True
            
        # Archive file organization logs (one-time events)
        if "file organization" in section_lower or "enforcement implementation" in section_lower:
            return True
            
        # Archive pattern loading optimizations (completed fixes)
        if "pattern loading optimization" in section_lower:
            return True
            
        # Keep only the most recent critical context - archive older ones
        if "critical context" in section_lower and self._is_section_old(section_name):
            return True
            
        # Archive configuration enhancement logs (keep the result, not the process)
        if "configuration enhancement" in section_lower and line_count > 20:
            return True
            
        # Archive large learned corrections updates (keep summary, not details)
        if "learned corrections" in section_lower and line_count > 15:
            return True
            
        return False

    def _is_section_old(self, section_name: str) -> bool:
        """Check if section is from previous sessions (older than 1 day)"""
        # Extract date from section name if present (various formats)
        date_patterns = [
            r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
            r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)',  # ISO format
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, section_name)
            if matches:
                try:
                    # Handle ISO format vs simple date
                    date_str = matches[0]
                    if 'T' in date_str:
                        section_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    else:
                        section_date = datetime.strptime(date_str, '%Y-%m-%d')
                        
                    # Consider old if more than 1 day old
                    age_hours = (self.current_date - section_date.replace(tzinfo=None)).total_seconds() / 3600
                    return age_hours > 24
                except (ValueError, AttributeError):
                    continue
                
        # Special keywords that indicate old sections
        section_lower = section_name.lower()
        old_indicators = [
            "previous session", "critical context from", "continuation from",
            "handoff", "checkpoint", "completed", "summary of session"
        ]
        
        for indicator in old_indicators:
            if indicator in section_lower:
                return True
                
        return False

    def archive_content(self, dry_run: bool = False) -> Dict:
        """Perform the actual archival operation"""
        if dry_run:
            print("🧪 DRY RUN MODE - No files will be modified")
            
        # Create backup first
        backup_path = self._create_backup()
        print(f"📦 Backup created: {backup_path}")
        
        # Analyze current file
        analysis = self.analyze_current_file()
        if "error" in analysis:
            return analysis
            
        print(f"📊 Current file: {analysis['total_lines']} lines (target: {self.target_lines})")
        print(f"📤 Sections to archive: {len(analysis['archival_candidates'])}")
        print(f"📌 Sections to keep: {len(analysis['keep_active'])}")
        
        if analysis['total_lines'] <= self.target_lines:
            print("✅ File is already within target size - no archival needed")
            return {"status": "no_action_needed", "current_size": analysis['total_lines']}
        
        if not dry_run:
            # Perform archival
            archived_content = self._extract_archival_content(analysis)
            self._save_archived_content(archived_content)
            self._create_optimized_file(analysis)
            self._update_search_index(archived_content)
            
        # Calculate results
        estimated_new_size = self._estimate_optimized_size(analysis)
        result = {
            "status": "completed" if not dry_run else "dry_run",
            "original_size": analysis['total_lines'],
            "estimated_new_size": estimated_new_size,
            "reduction": analysis['total_lines'] - estimated_new_size,
            "backup_path": str(backup_path),
            "archived_sections": analysis['archival_candidates']
        }
        
        if not dry_run:
            print(f"✅ Archival complete! Reduced from {analysis['total_lines']} to ~{estimated_new_size} lines")
        else:
            print(f"📋 Would reduce from {analysis['total_lines']} to ~{estimated_new_size} lines")
            
        return result

    def _create_backup(self) -> Path:
        """Create timestamped backup of current file"""
        timestamp = self.current_date.strftime("%Y%m%d_%H%M%S")
        backup_dir = self.project_root / "backups" / f"session_continuity_{timestamp}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        backup_file = backup_dir / "SESSION_CONTINUITY.md"
        shutil.copy2(self.session_file, backup_file)
        
        # Create backup metadata
        metadata = {
            "timestamp": self.current_date.isoformat(),
            "original_size": len(self.session_file.read_text().split('\n')),
            "backup_reason": "pre_archival"
        }
        
        metadata_file = backup_dir / "backup_metadata.json"
        metadata_file.write_text(json.dumps(metadata, indent=2))
        
        return backup_file

    def _extract_archival_content(self, analysis: Dict) -> Dict:
        """Extract content that should be archived"""
        archived = {
            "session_summaries": [],
            "integration_logs": [],
            "task_details": [],
            "checkpoints": []
        }
        
        for section_name in analysis['archival_candidates']:
            section_data = analysis['sections'][section_name]
            section_type = section_data.get('type', self._classify_section(section_name))
            content = '\n'.join(section_data['content'])
            
            entry = {
                "section_name": section_name,
                "timestamp": self.current_date.isoformat(),
                "content": content,
                "line_count": section_data['lines']
            }
            
            if section_type == "session_summary":
                archived["session_summaries"].append(entry)
            elif section_type == "integration_log":
                archived["integration_logs"].append(entry)
            elif section_type == "task_detail":
                archived["task_details"].append(entry)
            elif section_type == "checkpoint":
                archived["checkpoints"].append(entry)
                
        return archived

    def _save_archived_content(self, archived_content: Dict):
        """Save archived content to appropriate files"""
        timestamp = self.current_date.strftime("%Y-%m-%d_%H-%M-%S")
        date_str = self.current_date.strftime("%Y-%m-%d")
        year_month = self.current_date.strftime("%Y-%m")
        archive_dir = self.archive_root / year_month
        
        # Save session summaries
        if archived_content["session_summaries"]:
            session_file = archive_dir / f"session_{timestamp}.md"
            content = self._format_archived_sessions(archived_content["session_summaries"])
            session_file.write_text(content)
            
        # Save integration logs
        if archived_content["integration_logs"]:
            integration_file = archive_dir / f"integration_logs_{date_str}.md"
            content = self._format_archived_integration_logs(archived_content["integration_logs"])
            if integration_file.exists():
                content = integration_file.read_text() + "\n\n" + content
            integration_file.write_text(content)
            
        # Save task details
        if archived_content["task_details"]:
            task_file = archive_dir / f"task_details_{date_str}.md"
            content = self._format_archived_task_details(archived_content["task_details"])
            if task_file.exists():
                content = task_file.read_text() + "\n\n" + content
            task_file.write_text(content)

    def _format_archived_sessions(self, sessions: List[Dict]) -> str:
        """Format session summaries for archive"""
        content = f"# Archived Session Summaries - {self.current_date.strftime('%Y-%m-%d')}\n\n"
        content += f"Archived from SESSION_CONTINUITY.md at {self.current_date.isoformat()}\n\n"
        
        for session in sessions:
            content += f"## {session['section_name']}\n"
            content += f"*Archived: {session['timestamp']} | Lines: {session['line_count']}*\n\n"
            content += session['content'] + "\n\n"
            content += "---\n\n"
            
        return content

    def _format_archived_integration_logs(self, logs: List[Dict]) -> str:
        """Format integration logs for archive"""
        content = f"# Archived Integration Logs - {self.current_date.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for log in logs:
            content += f"## {log['section_name']}\n"
            content += f"*Lines: {log['line_count']} | Archived: {log['timestamp']}*\n\n"
            # Condense verbose logs to summary
            content += self._condense_integration_log(log['content']) + "\n\n"
            
        return content

    def _format_archived_task_details(self, tasks: List[Dict]) -> str:
        """Format task details for archive"""
        content = f"# Archived Task Details - {self.current_date.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for task in tasks:
            content += f"## {task['section_name']}\n"
            content += f"*Lines: {task['line_count']} | Archived: {task['timestamp']}*\n\n"
            content += task['content'] + "\n\n"
            content += "---\n\n"
            
        return content

    def _condense_integration_log(self, content: str) -> str:
        """Condense verbose integration logs to summary lines"""
        lines = content.split('\n')
        summary_lines = []
        
        for line in lines:
            # Keep key result lines, skip verbose process lines
            if any(marker in line for marker in ['✅', '❌', '⚠️', 'Status:', 'Results:']):
                summary_lines.append(line)
            elif line.startswith('## ') or line.startswith('### '):
                summary_lines.append(line)
                
        if not summary_lines:
            # If no key markers found, create a basic summary
            return f"Integration completed at {self.current_date.strftime('%Y-%m-%d %H:%M:%S')}"
            
        return '\n'.join(summary_lines)

    def _create_optimized_file(self, analysis: Dict):
        """Create the optimized SESSION_CONTINUITY.md file"""
        optimized_content = []
        
        # Add header
        optimized_content.append("# SESSION CONTINUITY LOG - CLAUDE Improvement Project")
        optimized_content.append("User: Christian")
        optimized_content.append("Project: Automatic learning file loading on session start implementation")
        optimized_content.append("")
        
        # Add archive reference
        optimized_content.append("## Archive Information")
        optimized_content.append(f"Previous sessions archived: {self.current_date.strftime('%Y-%m-%d %H:%M:%S')}")
        optimized_content.append("📁 **Archive Location**: `logs/session_continuity/`")
        optimized_content.append("🔍 **Search Archives**: `./scripts/search_session_archive.sh \"keyword\"`")
        optimized_content.append("♻️ **Restore Session**: `./scripts/restore_session_context.sh YYYY-MM-DD`")
        optimized_content.append("")
        
        # Keep only active sections
        for section_name in analysis['keep_active']:
            section_data = analysis['sections'][section_name]
            optimized_content.extend(section_data['content'])
            optimized_content.append("")
            
        # Add current session marker
        optimized_content.append(f"## Current Session - {self.current_date.strftime('%Y-%m-%d %H:%M:%S')}")
        optimized_content.append("*Session active - ready for new updates*")
        optimized_content.append("")
        
        # Write optimized file
        self.session_file.write_text('\n'.join(optimized_content))

    def _update_search_index(self, archived_content: Dict):
        """Update the search index with archived content"""
        search_file = self.archive_root / "quick_search.json"
        
        try:
            search_data = json.loads(search_file.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            search_data = {"sessions": {}, "last_updated": ""}
            
        # Add new entries to search index
        session_key = self.current_date.strftime("%Y-%m-%d_%H-%M-%S")
        search_data["sessions"][session_key] = {
            "timestamp": self.current_date.isoformat(),
            "archived_sections": len(archived_content["session_summaries"]) + 
                               len(archived_content["integration_logs"]) + 
                               len(archived_content["task_details"]),
            "files": []
        }
        
        # Record archive files created
        year_month = self.current_date.strftime("%Y-%m")
        if archived_content["session_summaries"]:
            search_data["sessions"][session_key]["files"].append(f"{year_month}/session_{session_key}.md")
        if archived_content["integration_logs"]:
            search_data["sessions"][session_key]["files"].append(f"{year_month}/integration_logs_{self.current_date.strftime('%Y-%m-%d')}.md")
        if archived_content["task_details"]:
            search_data["sessions"][session_key]["files"].append(f"{year_month}/task_details_{self.current_date.strftime('%Y-%m-%d')}.md")
            
        search_data["last_updated"] = self.current_date.isoformat()
        search_file.write_text(json.dumps(search_data, indent=2))

    def _estimate_optimized_size(self, analysis: Dict) -> int:
        """Estimate the size of the optimized file"""
        keep_lines = sum(analysis['sections'][section]['lines'] 
                        for section in analysis['keep_active'])
        # Add overhead for headers and archive references
        return keep_lines + 20

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Archive SESSION_CONTINUITY.md for optimal boot performance")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be archived without making changes")
    parser.add_argument("--target-lines", type=int, default=750, help="Target file size in lines (default: 750)")
    parser.add_argument("--project-root", default="/Users/scarmatrix/Project/CLAUDE_improvement", help="Project root directory")
    
    args = parser.parse_args()
    
    archiver = SessionContinuityArchiver(args.project_root, args.target_lines)
    result = archiver.archive_content(dry_run=args.dry_run)
    
    print("\n📋 Archival Summary:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()