#!/usr/bin/env python3
"""
Session Information Formatter for Claude
Parses SESSION_CONTINUITY.md and formats session information for easy Claude consumption.
"""

import os
import sys
import re
import json
from datetime import datetime, timedelta
from pathlib import Path

class SessionRestoreFormatter:
    def __init__(self, project_root=None):
        """Initialize the session restore formatter."""
        if project_root is None:
            # Try to find project root by looking for CLAUDE.md or SESSION_CONTINUITY.md
            current_dir = Path(__file__).parent.parent
            if (current_dir / "SESSION_CONTINUITY.md").exists():
                project_root = current_dir
            else:
                project_root = Path.cwd()
        
        self.project_root = Path(project_root)
        self.session_file = self.project_root / "SESSION_CONTINUITY.md"
        
    def parse_session_continuity(self):
        """Parse SESSION_CONTINUITY.md file for recent context."""
        if not self.session_file.exists():
            return {
                'error': f"SESSION_CONTINUITY.md not found at {self.session_file}",
                'project_status': 'unknown',
                'recent_activities': [],
                'file_age': 'file_missing'
            }
        
        try:
            with open(self.session_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Get file age
            file_stat = self.session_file.stat()
            file_age = datetime.now() - datetime.fromtimestamp(file_stat.st_mtime)
            
            # Parse content sections
            parsed_data = {
                'file_age_minutes': round(file_age.total_seconds() / 60, 1),
                'file_age_human': self._format_time_ago(file_age),
                'project_info': self._extract_project_info(content),
                'current_status': self._extract_current_status(content),
                'recent_activities': self._extract_recent_activities(content),
                'critical_learnings': self._extract_critical_learnings(content),
                'system_status': self._extract_system_status(content),
                'agent_preferences': self._extract_agent_preferences(content),
                'backup_info': self._extract_backup_info(content)
            }
            
            return parsed_data
            
        except Exception as e:
            return {
                'error': f"Error parsing SESSION_CONTINUITY.md: {str(e)}",
                'project_status': 'parse_error',
                'recent_activities': [],
                'file_age': 'unknown'
            }
    
    def _extract_project_info(self, content):
        """Extract basic project information."""
        info = {}
        
        # Extract user and project from header
        lines = content.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            if line.startswith('User:'):
                info['user'] = line.replace('User:', '').strip()
            elif line.startswith('Project:'):
                info['project'] = line.replace('Project:', '').strip()
        
        return info
    
    def _extract_current_status(self, content):
        """Extract the most recent status/activity."""
        # Look for the most recent "Current Session" entry
        current_session_pattern = r'## Current Session - (.+?)\n\*(.+?)\*'
        matches = re.findall(current_session_pattern, content, re.DOTALL)
        
        if matches:
            latest_timestamp, latest_activity = matches[-1]
            return {
                'timestamp': latest_timestamp.strip(),
                'activity': latest_activity.strip()
            }
        
        # Fallback to looking for recent completed activities
        completed_pattern = r'## (.+?) COMPLETE ✅ - (.+?)\n'
        completed_matches = re.findall(completed_pattern, content)
        
        if completed_matches:
            latest_task, timestamp = completed_matches[-1]
            return {
                'timestamp': timestamp.strip(),
                'activity': f"{latest_task} completed"
            }
        
        return {'timestamp': 'unknown', 'activity': 'No recent activity found'}
    
    def _extract_recent_activities(self, content):
        """Extract recent activities and completed tasks."""
        activities = []
        
        # Find all completed tasks
        completed_pattern = r'## (.+?) COMPLETE ✅ - (.+?)\n### 🎯 (.+?)\n\*\*(.+?)\*\*'
        matches = re.findall(completed_pattern, content, re.DOTALL)
        
        for task_name, timestamp, mission, description in matches[-5:]:  # Last 5 activities
            activities.append({
                'type': 'completed_task',
                'task': task_name.strip(),
                'timestamp': timestamp.strip(),
                'mission': mission.strip(),
                'description': description.strip()[:200] + '...' if len(description.strip()) > 200 else description.strip()
            })
        
        # Find critical learnings
        learning_pattern = r'## CRITICAL LEARNING: (.+?)\n- \*\*Error\*\*: (.+?)\n- \*\*Impact\*\*: (.+?)\n'
        learning_matches = re.findall(learning_pattern, content)
        
        for learning_title, error, impact in learning_matches[-3:]:  # Last 3 learnings
            activities.append({
                'type': 'critical_learning',
                'title': learning_title.strip(),
                'error': error.strip(),
                'impact': impact.strip()
            })
        
        return activities
    
    def _extract_critical_learnings(self, content):
        """Extract critical learning entries."""
        learnings = []
        learning_pattern = r'## CRITICAL LEARNING: (.+?)\n((?:- \*\*[^:]+\*\*: .+?\n)+)'
        matches = re.findall(learning_pattern, content, re.MULTILINE)
        
        for title, details in matches:
            learning_data = {'title': title.strip(), 'details': {}}
            
            # Parse detail lines
            detail_lines = details.split('\n')
            for line in detail_lines:
                if line.strip() and '**' in line:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        key = parts[0].replace('- **', '').replace('**', '').strip().lower()
                        value = parts[1].strip()
                        learning_data['details'][key] = value
            
            learnings.append(learning_data)
        
        return learnings
    
    def _extract_system_status(self, content):
        """Extract system status and performance metrics."""
        status = {}
        
        # Look for performance metrics
        performance_patterns = [
            (r'(\d+(?:\.\d+)?)% (.+?) improvement', 'improvements'),
            (r'✅ \*\*(.+?)\*\*: (.+?)(?=\n|$)', 'achievements'),
            (r'- \*\*(.+?)\*\*: (.+?)(?=\n|$)', 'metrics')
        ]
        
        for pattern, category in performance_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                status[category] = matches[-10:]  # Last 10 matches
        
        return status
    
    def _extract_agent_preferences(self, content):
        """Extract agent configuration preferences."""
        agent_section = re.search(r'### 🧠 CHRISTIAN\'S PERMANENT AGENT EXECUTION RULE(.+?)(?=##|\Z)', content, re.DOTALL)
        
        if agent_section:
            section_text = agent_section.group(1)
            return {
                'rule_found': True,
                'simple_tasks': '5 agents minimum (parallel execution)',
                'complex_tasks': '10 agents minimum (parallel execution)',
                'sequential_agents': 'NEVER use - explicitly forbidden',
                'boot_integration': 'Automatically loaded on every session start'
            }
        
        # Look for other agent configurations
        agent_configs = re.findall(r'- \*\*(.+? Context)\*\*: (\d+) agents', content)
        if agent_configs:
            return {
                'rule_found': False,
                'configurations': agent_configs
            }
        
        return {'rule_found': False, 'configurations': []}
    
    def _extract_backup_info(self, content):
        """Extract backup system information."""
        backup_info = {}
        
        # Look for backup status
        backup_patterns = [
            (r'- Last backup: (.+)', 'last_backup'),
            (r'- Minutes since backup: (.+)', 'minutes_since_backup'),
            (r'- Total backups: (\d+)', 'total_backups'),
            (r'- Backup system: (.+)', 'backup_system_status')
        ]
        
        for pattern, key in backup_patterns:
            match = re.search(pattern, content)
            if match:
                backup_info[key] = match.group(1).strip()
        
        return backup_info
    
    def _format_time_ago(self, time_delta):
        """Format timedelta as human-readable string."""
        total_seconds = int(time_delta.total_seconds())
        
        if total_seconds < 60:
            return f"{total_seconds} seconds ago"
        elif total_seconds < 3600:
            minutes = total_seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif total_seconds < 86400:
            hours = total_seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            days = total_seconds // 86400
            return f"{days} day{'s' if days != 1 else ''} ago"
    
    def format_for_claude(self, data):
        """Format parsed data for easy Claude consumption."""
        if 'error' in data:
            return f"""# SESSION RESTORE ERROR
            
❌ **Error**: {data['error']}

Please check if SESSION_CONTINUITY.md exists and is readable.
"""
        
        output = []
        output.append("# SESSION CONTEXT RESTORE")
        output.append("")
        
        # Project Information
        if data.get('project_info'):
            output.append("## 📁 PROJECT INFORMATION")
            if 'user' in data['project_info']:
                output.append(f"**User**: {data['project_info']['user']}")
            if 'project' in data['project_info']:
                output.append(f"**Project**: {data['project_info']['project']}")
            output.append("")
        
        # File Age and Freshness
        output.append("## ⏰ SESSION FRESHNESS")
        output.append(f"**File Age**: {data.get('file_age_human', 'unknown')}")
        output.append(f"**Minutes**: {data.get('file_age_minutes', 'unknown')}")
        
        age_minutes = data.get('file_age_minutes', 0)
        if age_minutes < 30:
            output.append("✅ **Status**: Fresh (< 30 minutes)")
        elif age_minutes < 120:
            output.append("⚠️ **Status**: Recent (< 2 hours)")
        else:
            output.append("🔄 **Status**: Stale (> 2 hours)")
        output.append("")
        
        # Current Status
        if data.get('current_status'):
            output.append("## 🎯 CURRENT STATUS")
            output.append(f"**Latest Activity**: {data['current_status'].get('activity', 'unknown')}")
            output.append(f"**Timestamp**: {data['current_status'].get('timestamp', 'unknown')}")
            output.append("")
        
        # Recent Activities
        if data.get('recent_activities'):
            output.append("## 📋 RECENT ACTIVITIES")
            for activity in data['recent_activities'][-5:]:  # Last 5 activities
                if activity['type'] == 'completed_task':
                    output.append(f"### ✅ {activity['task']}")
                    output.append(f"**Mission**: {activity['mission']}")
                    output.append(f"**Time**: {activity['timestamp']}")
                    output.append(f"**Description**: {activity['description']}")
                elif activity['type'] == 'critical_learning':
                    output.append(f"### 🧠 LEARNING: {activity['title']}")
                    output.append(f"**Error**: {activity['error']}")
                    output.append(f"**Impact**: {activity['impact']}")
                output.append("")
        
        # Agent Preferences
        if data.get('agent_preferences', {}).get('rule_found'):
            output.append("## 🤖 AGENT EXECUTION PREFERENCES")
            prefs = data['agent_preferences']
            output.append(f"**Simple Tasks**: {prefs.get('simple_tasks', 'unknown')}")
            output.append(f"**Complex Tasks**: {prefs.get('complex_tasks', 'unknown')}")
            output.append(f"**Sequential Agents**: {prefs.get('sequential_agents', 'unknown')}")
            output.append(f"**Boot Integration**: {prefs.get('boot_integration', 'unknown')}")
            output.append("")
        
        # System Status
        if data.get('system_status'):
            status = data['system_status']
            if status.get('achievements'):
                output.append("## 🚀 SYSTEM ACHIEVEMENTS")
                for achievement, result in status['achievements'][-5:]:
                    output.append(f"**{achievement}**: {result}")
                output.append("")
        
        # Backup Information
        if data.get('backup_info'):
            backup = data['backup_info']
            output.append("## 💾 BACKUP STATUS")
            for key, value in backup.items():
                formatted_key = key.replace('_', ' ').title()
                output.append(f"**{formatted_key}**: {value}")
            output.append("")
        
        # Critical Learnings
        if data.get('critical_learnings'):
            output.append("## 🧠 CRITICAL LEARNINGS")
            for learning in data['critical_learnings'][-3:]:  # Last 3 learnings
                output.append(f"### {learning['title']}")
                for key, value in learning['details'].items():
                    formatted_key = key.replace('_', ' ').title()
                    output.append(f"**{formatted_key}**: {value}")
                output.append("")
        
        return '\n'.join(output)
    
    def generate_json_summary(self, data):
        """Generate JSON summary for programmatic use."""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'file_age_minutes': data.get('file_age_minutes'),
            'is_fresh': data.get('file_age_minutes', 999) < 30,
            'current_activity': data.get('current_status', {}).get('activity'),
            'user': data.get('project_info', {}).get('user'),
            'project': data.get('project_info', {}).get('project'),
            'recent_tasks_count': len([a for a in data.get('recent_activities', []) if a['type'] == 'completed_task']),
            'critical_learnings_count': len(data.get('critical_learnings', [])),
            'agent_preferences_configured': data.get('agent_preferences', {}).get('rule_found', False),
            'backup_status': data.get('backup_info', {})
        }
        return summary

def main():
    """Main execution function."""
    # Parse command line arguments
    project_root = None
    output_format = 'text'  # default to text
    
    for i, arg in enumerate(sys.argv[1:]):
        if arg == '--project-root' and i + 1 < len(sys.argv) - 1:
            project_root = sys.argv[i + 2]
        elif arg == '--json':
            output_format = 'json'
        elif arg == '--help':
            print("""
Session Restore Formatter for Claude

Usage:
    python session_restore.py [options]
    
Options:
    --project-root PATH    Specify project root directory
    --json                 Output in JSON format instead of formatted text
    --help                 Show this help message
    
Examples:
    python session_restore.py
    python session_restore.py --project-root /path/to/project
    python session_restore.py --json
""")
            return
    
    # Initialize formatter and parse session
    formatter = SessionRestoreFormatter(project_root)
    data = formatter.parse_session_continuity()
    
    # Output results
    if output_format == 'json':
        summary = formatter.generate_json_summary(data)
        print(json.dumps(summary, indent=2))
    else:
        formatted_output = formatter.format_for_claude(data)
        print(formatted_output)

if __name__ == '__main__':
    main()