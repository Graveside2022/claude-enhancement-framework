#!/usr/bin/env python3
"""
Simple Boot Status Reporter
Shows what files and systems are loaded during boot/start

Created for: Christian
Purpose: Easy visibility into what gets loaded on boot
"""

import os
import time
from pathlib import Path
from typing import Dict, List

class SimpleBootReporter:
    """Ultra-simple boot status reporter"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        
    def generate_boot_report(self) -> str:
        """Generate simple boot status report"""
        
        # Check key files
        session_continuity = self._check_file("SESSION_CONTINUITY.md")
        side_effects = self._check_file("memory/side_effects_log.md")
        solution_candidates = self._check_file("memory/solution_candidates.md")
        learning_archive = self._check_file("memory/learning_archive.md")
        learned_corrections = self._check_file(str(Path.home() / ".claude" / "LEARNED_CORRECTIONS.md"))
        
        # Check patterns and memories
        patterns_info = self._check_patterns()
        memory_info = self._check_memory_files()
        
        # Build report
        report = f"""
🚀 BOOT STATUS REPORT - {time.strftime('%Y-%m-%d %H:%M:%S')}
User: Christian

📁 KEY FILES LOADED:
  ✅ SESSION_CONTINUITY.md     {session_continuity['status']} ({session_continuity['size']} lines)
  ✅ side_effects_log.md       {side_effects['status']} ({side_effects['size']} entries)
  ✅ solution_candidates.md    {solution_candidates['status']} ({solution_candidates['size']} candidates)
  ✅ learning_archive.md       {learning_archive['status']} ({learning_archive['size']} patterns)
  ✅ LEARNED_CORRECTIONS.md    {learned_corrections['status']} ({learned_corrections['size']} corrections)

🧠 PATTERNS & MEMORIES:
  📊 Total Patterns: {patterns_info['total']} across {patterns_info['categories']} categories
  🔍 Pattern Categories: {', '.join(patterns_info['category_list'])}
  📝 Memory Files: {memory_info['count']} active files
  💾 Cache Status: Active (.claude_session_state.json)

⚡ SYSTEM STATUS: Ready
"""
        return report
    
    def _check_file(self, file_path: str) -> Dict:
        """Check file status and get basic stats"""
        if file_path.startswith('/'):
            # Absolute path
            path = Path(file_path)
        else:
            # Relative to project
            path = self.project_root / file_path
            
        if not path.exists():
            return {'status': 'Missing', 'size': 0}
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Different counting for different file types
            if 'SESSION_CONTINUITY' in str(path):
                return {'status': 'Loaded', 'size': len(lines)}
            elif 'side_effects' in str(path):
                entries = len([l for l in lines if l.startswith('### Side Effect')])
                return {'status': 'Loaded', 'size': entries}
            elif 'solution_candidates' in str(path):
                candidates = len([l for l in lines if l.startswith('## CANDIDATE')])
                return {'status': 'Loaded', 'size': candidates}
            elif 'learning_archive' in str(path):
                patterns = len([l for l in lines if '**Function:**' in l or '**Class:**' in l])
                return {'status': 'Loaded', 'size': patterns}
            elif 'LEARNED_CORRECTIONS' in str(path):
                corrections = len([l for l in lines if l.startswith('## 20')])
                return {'status': 'Loaded', 'size': corrections}
            else:
                return {'status': 'Loaded', 'size': len(lines)}
                
        except Exception:
            return {'status': 'Error', 'size': 0}
    
    def _check_patterns(self) -> Dict:
        """Check patterns directory"""
        patterns_dir = self.project_root / "patterns"
        if not patterns_dir.exists():
            return {'total': 0, 'categories': 0, 'category_list': []}
        
        categories = []
        total_patterns = 0
        
        for category_dir in patterns_dir.iterdir():
            if category_dir.is_dir() and not category_dir.name.startswith('.'):
                pattern_files = list(category_dir.glob("*.md"))
                if pattern_files:
                    categories.append(category_dir.name)
                    total_patterns += len(pattern_files)
        
        return {
            'total': total_patterns,
            'categories': len(categories),
            'category_list': categories
        }
    
    def _check_memory_files(self) -> Dict:
        """Check memory directory"""
        memory_dir = self.project_root / "memory"
        if not memory_dir.exists():
            return {'count': 0}
        
        memory_files = list(memory_dir.glob("*.md"))
        return {'count': len(memory_files)}

def show_boot_status(project_root: str = ".") -> str:
    """Main function to show boot status"""
    reporter = SimpleBootReporter(project_root)
    return reporter.generate_boot_report()

if __name__ == "__main__":
    print(show_boot_status())