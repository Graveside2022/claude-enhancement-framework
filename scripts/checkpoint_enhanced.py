#!/usr/bin/env python3
"""
Enhanced Checkpoint Script for SESSION_CONTINUITY.md
Supports three checkpoint modes:
1. Document only (default)
2. Document + git stash
3. Document + git commit

Usage:
    python3 checkpoint_enhanced.py [message]              # Document only
    python3 checkpoint_enhanced.py --stash [message]      # Document + git stash
    python3 checkpoint_enhanced.py --commit [message]     # Document + git commit
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path


class CheckpointManager:
    def __init__(self, project_root=None):
        """Initialize the checkpoint manager."""
        self.project_root = Path(project_root) if project_root else Path(__file__).parent.parent.resolve()
        self.session_file = self.project_root / "SESSION_CONTINUITY.md"
        self.backup_dir = self.project_root / "backups"
        
    def run_command(self, cmd, capture_output=True, check=True):
        """Run a shell command safely."""
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                shell=True,
                capture_output=capture_output,
                text=True,
                check=check
            )
            return result.stdout.strip() if capture_output else None
        except subprocess.CalledProcessError as e:
            if capture_output:
                raise Exception(f"Command failed: {cmd}\nError: {e.stderr}")
            else:
                raise Exception(f"Command failed: {cmd}")
    
    def get_git_status(self):
        """Get comprehensive git repository status."""
        try:
            # Check if we're in a git repository
            self.run_command("git rev-parse --is-inside-work-tree", capture_output=True)
            
            status_info = {
                "is_git_repo": True,
                "current_branch": None,
                "modified_files": [],
                "staged_files": [],
                "untracked_files": [],
                "total_changes": 0,
                "is_clean": False,
                "last_commit": None
            }
            
            # Get current branch
            try:
                status_info["current_branch"] = self.run_command("git branch --show-current")
            except:
                status_info["current_branch"] = "unknown"
            
            # Get git status
            try:
                status_output = self.run_command("git status --porcelain")
                if status_output:
                    lines = status_output.split('\n')
                    for line in lines:
                        if not line.strip():
                            continue
                        status_code = line[:2]
                        filename = line[3:]
                        
                        if status_code[0] in ['A', 'M', 'D', 'R', 'C']:
                            status_info["staged_files"].append(f"{status_code[0]} {filename}")
                        if status_code[1] in ['M', 'D', '?']:
                            if status_code[1] == '?':
                                status_info["untracked_files"].append(filename)
                            else:
                                status_info["modified_files"].append(f"{status_code[1]} {filename}")
                    
                    status_info["total_changes"] = len(lines)
                    status_info["is_clean"] = False
                else:
                    status_info["is_clean"] = True
            except:
                pass
            
            # Get last commit info
            try:
                status_info["last_commit"] = self.run_command("git log -1 --format='%h - %s (%ar)'")
            except:
                status_info["last_commit"] = "No commits found"
            
            return status_info
            
        except:
            return {
                "is_git_repo": False,
                "error": "Not a git repository or git not available"
            }
    
    def get_project_status(self):
        """Get comprehensive project status."""
        status = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "readable_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "git": self.get_git_status(),
            "todo_tasks": 0,
            "project_files": {
                "session_continuity": self.session_file.exists(),
                "claude_md": (self.project_root / "CLAUDE.md").exists(),
                "todo_md": (self.project_root / "TODO.md").exists()
            }
        }
        
        # Count TODO tasks
        todo_file = self.project_root / "TODO.md"
        if todo_file.exists():
            try:
                with open(todo_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    status["todo_tasks"] = content.count('- [ ]')
            except:
                status["todo_tasks"] = 0
        
        return status
    
    def create_checkpoint_entry(self, message, checkpoint_type="document"):
        """Create a checkpoint entry for SESSION_CONTINUITY.md."""
        project_status = self.get_project_status()
        
        # Generate checkpoint header
        timestamp_iso = project_status["timestamp"]
        readable_time = project_status["readable_time"]
        
        # Format checkpoint type
        type_emoji = {
            "document": "📝",
            "stash": "💾",
            "commit": "💾"
        }
        
        # Build git status summary
        git_info = project_status["git"]
        if git_info["is_git_repo"]:
            git_summary = f"**Branch**: {git_info['current_branch']}\n"
            git_summary += f"**Status**: {'Clean' if git_info['is_clean'] else f'{git_info['total_changes']} changes'}\n"
            
            if not git_info["is_clean"]:
                if git_info["staged_files"]:
                    git_summary += f"**Staged**: {len(git_info['staged_files'])} files\n"
                if git_info["modified_files"]:
                    git_summary += f"**Modified**: {len(git_info['modified_files'])} files\n"
                if git_info["untracked_files"]:
                    git_summary += f"**Untracked**: {len(git_info['untracked_files'])} files\n"
            
            if git_info["last_commit"]:
                git_summary += f"**Last Commit**: {git_info['last_commit']}\n"
        else:
            git_summary = "**Git**: Not a repository\n"
        
        # Create checkpoint entry
        checkpoint_entry = f"""## CHECKPOINT - {timestamp_iso}

### {type_emoji.get(checkpoint_type, '📍')} CHECKPOINT: {message}
**Type**: {checkpoint_type.upper()}  
**Timestamp**: {readable_time}  
{git_summary}**TODO Tasks**: {project_status['todo_tasks']} pending  
**Session Status**: Active checkpoint by Christian  

"""
        
        return checkpoint_entry
    
    def update_session_continuity(self, checkpoint_entry):
        """Update SESSION_CONTINUITY.md with checkpoint entry."""
        if not self.session_file.exists():
            # Create basic SESSION_CONTINUITY.md structure
            initial_content = f"""# SESSION CONTINUITY - CLAUDE IMPROVEMENT PROJECT

## Current Session Status
- Project: CLAUDE_improvement
- Owner: Christian
- Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Session History

"""
            with open(self.session_file, 'w', encoding='utf-8') as f:
                f.write(initial_content)
        
        # Read current content
        with open(self.session_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Insert checkpoint after "## Session History" or "## Current Session Status"
        lines = content.split('\n')
        new_lines = []
        inserted = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            
            # Insert after Session History header
            if line.strip() == "## Session History" and not inserted:
                new_lines.append("")
                new_lines.extend(checkpoint_entry.strip().split('\n'))
                new_lines.append("")
                inserted = True
            # Fallback: Insert after Current Session Status section
            elif "## Current Session Status" in line and not inserted:
                # Look for the end of this section
                j = i + 1
                while j < len(lines) and not lines[j].startswith("##"):
                    new_lines.append(lines[j])
                    j += 1
                
                new_lines.append("")
                new_lines.extend(checkpoint_entry.strip().split('\n'))
                new_lines.append("")
                
                # Add remaining lines
                new_lines.extend(lines[j:])
                inserted = True
                break
        
        # If we couldn't insert, append at the end
        if not inserted:
            new_lines.append("")
            new_lines.extend(checkpoint_entry.strip().split('\n'))
        
        # Write updated content
        with open(self.session_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
    
    def create_git_stash(self, message):
        """Create a git stash with the checkpoint message."""
        try:
            git_status = self.get_git_status()
            if not git_status["is_git_repo"]:
                raise Exception("Not a git repository")
            
            if git_status["is_clean"]:
                print("⚠️  No changes to stash (working directory is clean)")
                return None
            
            stash_message = f"checkpoint: {message}"
            self.run_command(f'git stash push -m "{stash_message}"', capture_output=False)
            
            # Get stash info
            stash_list = self.run_command("git stash list --oneline | head -1")
            return stash_list
            
        except Exception as e:
            raise Exception(f"Failed to create git stash: {str(e)}")
    
    def create_git_commit(self, message):
        """Create a git commit with all changes."""
        try:
            git_status = self.get_git_status()
            if not git_status["is_git_repo"]:
                raise Exception("Not a git repository")
            
            if git_status["is_clean"]:
                print("⚠️  No changes to commit (working directory is clean)")
                return None
            
            # Add all changes
            self.run_command("git add -A", capture_output=False)
            
            commit_message = f"""checkpoint: {message}

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"""
            
            # Create commit
            self.run_command(f'git commit -m "{commit_message}"', capture_output=False)
            
            # Get commit info
            commit_info = self.run_command("git log -1 --format='%h - %s'")
            return commit_info
            
        except Exception as e:
            raise Exception(f"Failed to create git commit: {str(e)}")
    
    def execute_checkpoint(self, mode, message):
        """Execute checkpoint based on mode."""
        print(f"🔄 Creating {mode} checkpoint: {message}")
        
        # Always create documentation checkpoint
        checkpoint_entry = self.create_checkpoint_entry(message, mode)
        self.update_session_continuity(checkpoint_entry)
        
        git_result = None
        
        # Execute git operations based on mode
        if mode == "stash":
            try:
                git_result = self.create_git_stash(message)
                if git_result:
                    print(f"💾 Git stash created: {git_result}")
            except Exception as e:
                print(f"❌ Git stash failed: {str(e)}")
                return False
                
        elif mode == "commit":
            try:
                git_result = self.create_git_commit(message)
                if git_result:
                    print(f"💾 Git commit created: {git_result}")
            except Exception as e:
                print(f"❌ Git commit failed: {str(e)}")
                return False
        
        # Success summary
        print(f"✅ Checkpoint completed successfully")
        print(f"📝 Documentation updated in SESSION_CONTINUITY.md")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if git_result:
            print(f"🔄 Git operation: {git_result}")
        
        return True


def main():
    """Main function to handle command line arguments and execute checkpoint."""
    parser = argparse.ArgumentParser(
        description="Enhanced Checkpoint Script for SESSION_CONTINUITY.md",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Work in progress"                    # Document only checkpoint
  %(prog)s --stash "Temporary save"              # Document + git stash
  %(prog)s --commit "Feature complete"           # Document + git commit
        """
    )
    
    parser.add_argument(
        "message",
        nargs="?",
        default="Manual checkpoint",
        help="Checkpoint message (default: 'Manual checkpoint')"
    )
    
    parser.add_argument(
        "--stash",
        action="store_true",
        help="Create checkpoint with git stash"
    )
    
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Create checkpoint with git commit"
    )
    
    parser.add_argument(
        "--project-root",
        help="Project root directory (default: auto-detect)"
    )
    
    args = parser.parse_args()
    
    # Determine checkpoint mode
    if args.stash and args.commit:
        print("❌ Error: Cannot use both --stash and --commit options")
        sys.exit(1)
    elif args.stash:
        mode = "stash"
    elif args.commit:
        mode = "commit"
    else:
        mode = "document"
    
    # Initialize checkpoint manager
    try:
        checkpoint_manager = CheckpointManager(args.project_root)
        
        # Verify project directory exists
        if not checkpoint_manager.project_root.exists():
            print(f"❌ Error: Project directory not found: {checkpoint_manager.project_root}")
            sys.exit(1)
        
        # Execute checkpoint
        success = checkpoint_manager.execute_checkpoint(mode, args.message)
        
        if not success:
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()