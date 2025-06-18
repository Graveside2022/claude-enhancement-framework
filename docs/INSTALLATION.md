# Claude Enhancement Framework - Installation Guide

## Overview

The Claude Enhancement Framework brings **98.5% boot improvement** (649.1ms → 6.6ms), **pattern-first development**, and **automated learning systems** to any project with a simple installation process.

Transform your Claude experience in under 2 minutes with optimized performance, intelligent pattern matching, and cross-session memory.

## System Requirements

### Minimum Requirements
- **Python 3.8+** (Python 3.9+ recommended)
- **Git** (for version control and pattern deployment)
- **Claude Code access** (Anthropic's CLI interface)
- **Disk Space**: 50MB free space for framework and patterns

### Supported Platforms
- **macOS** (10.14+, native support)
- **Linux** (Ubuntu 18.04+, CentOS 7+, Debian 10+)
- **Windows** (Windows 10+ with WSL2 recommended)

### Performance Requirements
- **RAM**: 512MB available (framework uses ~10MB at runtime)
- **CPU**: Any modern processor (framework startup: <10ms)
- **Network**: Internet connection for initial framework download

## Quick Installation

### One-Command Setup
```bash
git clone https://github.com/your-username/claude-enhancement-framework.git
cd claude-enhancement-framework
./setup
```

This will:
1. ✅ Detect your system automatically
2. ✅ Configure global Claude optimization
3. ✅ Deploy 19 battle-tested patterns
4. ✅ Initialize memory systems
5. ✅ Validate installation with benchmarks

## Step-by-Step Installation

### Step 1: Download Framework
```bash
# Clone the repository
git clone https://github.com/your-username/claude-enhancement-framework.git
cd claude-enhancement-framework

# Verify download
ls -la
# Should show: setup, claude_enhancer/, patterns/, templates/, etc.
```

### Step 2: Check System Compatibility
```bash
# Manual system check (optional)
python3 --version  # Should be 3.8+
git --version      # Should be present
which claude       # Should find Claude Code CLI
```

### Step 3: Run Interactive Setup
```bash
./setup
```

### Step 4: Follow Interactive Prompts

The setup script will guide you through:

```
🔍 Checking system requirements...
✅ Python 3.9.7 on Darwin

🎯 Claude Enhancement Framework Configuration
==================================================

Username [christian]: christian
Project name [claude-enhancement-framework]: my-project

📦 Deployment Options:
1. Global only (deploy to ~/.claude/)
2. Project only (deploy to current directory)  
3. Both global and project (recommended)

Choose deployment [3]: 3

⚡ Performance Configuration:
Session continuity lines [750]: 750
Cache hit rate target [0.90]: 0.90
```

### Step 5: Verify Installation
```bash
# Check global deployment
ls ~/.claude/
# Should show: CLAUDE.md, LEARNED_CORRECTIONS.md, etc.

# Check project deployment (if selected)
ls ./
# Should show: CLAUDE.md, SESSION_CONTINUITY.md, memory/, patterns/, etc.
```

## Installation Options

### Global Deployment
Installs framework to `~/.claude/` for system-wide Claude optimization.

**Files Created:**
- `~/.claude/CLAUDE.md` - Core optimization rules
- `~/.claude/LEARNED_CORRECTIONS.md` - Error prevention patterns
- `~/.claude/PYTHON_LEARNINGS.md` - Python-specific patterns
- `~/.claude/INFRASTRUCTURE_LEARNINGS.md` - System architecture patterns
- `~/.claude/PROJECT_SPECIFIC_LEARNINGS.md` - Project-specific learning

### Project Deployment
Installs framework to current directory for project-specific optimization.

**Directory Structure Created:**
```
project-root/
├── CLAUDE.md                    # Project-specific configuration
├── SESSION_CONTINUITY.md        # Session memory
├── memory/
│   ├── learning_archive.md      # Successful patterns
│   ├── error_patterns.md        # Error prevention
│   └── side_effects_log.md      # Unintended consequences
├── patterns/                    # Pattern library (19 patterns)
│   ├── architecture/
│   ├── generation/
│   ├── refactoring/
│   ├── bug_fixes/
│   └── security/
├── tests/                       # Testing directory
└── scripts/                     # Utility scripts
```

### Hybrid Deployment (Recommended)
Combines global and project deployment for maximum optimization.

## Platform-Specific Instructions

### macOS Installation

```bash
# Standard installation
git clone https://github.com/your-username/claude-enhancement-framework.git
cd claude-enhancement-framework
./setup

# For Homebrew users
brew install python3 git  # If not already installed
./setup
```

**macOS-Specific Notes:**
- Uses native macOS paths (`~/Library/Application Support/claude/`)
- Integrates with Terminal and iTerm2
- Supports Apple Silicon (M1/M2) processors

### Linux Installation

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip git
git clone https://github.com/your-username/claude-enhancement-framework.git
cd claude-enhancement-framework
./setup

# CentOS/RHEL/Fedora
sudo yum install python3 python3-pip git  # CentOS 7
# OR
sudo dnf install python3 python3-pip git  # CentOS 8+/Fedora
git clone https://github.com/your-username/claude-enhancement-framework.git
cd claude-enhancement-framework  
./setup
```

**Linux-Specific Notes:**
- Uses XDG Base Directory Specification
- Supports both systemd and init systems
- Works with multiple Python installations

### Windows (WSL) Installation

**Prerequisites:**
```powershell
# Install WSL2 (run in PowerShell as Administrator)
wsl --install -d Ubuntu

# Restart computer, then continue in WSL terminal
```

**In WSL Terminal:**
```bash
# Update package list
sudo apt update
sudo apt install python3 python3-pip git

# Install framework
git clone https://github.com/your-username/claude-enhancement-framework.git
cd claude-enhancement-framework
./setup
```

**Windows-Specific Notes:**
- WSL2 is strongly recommended over native Windows
- Framework paths adapt to WSL environment
- Cross-platform file access handled automatically

## Configuration Options

### Performance Tuning

```bash
# During setup, customize these options:
Session continuity lines [750]: 1000      # More context retention
Cache hit rate target [0.90]: 0.95       # Higher cache efficiency
```

**Performance Options:**
- **Session Lines**: 500-2000 (default: 750)
- **Cache Target**: 0.80-0.98 (default: 0.90)
- **Boot Timeout**: 5-30ms (default: 6.6ms)

### Memory Configuration

```bash
# Advanced configuration (post-installation)
# Edit ~/.claude/CLAUDE.md or project-specific CLAUDE.md

# Memory system settings
MEMORY_AUTO_LEARNING=true          # Auto-capture patterns
MEMORY_RETENTION_HOURS=8           # Session persistence
MEMORY_MAX_ENTRIES=1000            # Pattern limit
```

### Pattern Selection

```bash
# Deploy specific pattern categories
./setup --patterns=architecture,generation,refactoring

# Deploy specific patterns
./setup --patterns=boot_sequence_optimization,error_learning_deferred_loading
```

## Post-Installation Setup

### Verify Installation

```bash
# Check framework version
python3 -c "from claude_enhancer import ClaudeEnhancer; print(ClaudeEnhancer().version)"
# Should output: 1.0.0

# Verify global configuration
cat ~/.claude/CLAUDE.md | head -5
# Should show framework header

# Test pattern deployment (if project deployment was selected)
ls patterns/ | wc -l
# Should show 19+ pattern files
```

### Performance Validation

```bash
# Run benchmark test
cd claude-enhancement-framework
python3 -c "
from claude_enhancer import ClaudeEnhancer
import time

start = time.time()
enhancer = ClaudeEnhancer()
enhancer.initialize_framework()
boot_time = time.time() - start

print(f'Boot time: {boot_time*1000:.1f}ms')
if boot_time < 0.0066:
    print('✅ Performance target achieved!')
else:
    print('⚠️  Performance optimization in progress...')
"
```

### First Use Setup

**For Claude Code CLI:**
```bash
# Restart Claude Code to load global configuration
claude --version

# Test framework integration (in project directory)
claude "boot"
# Should activate 3-agent boot context with optimized loading
```

## Troubleshooting

### Common Installation Issues

#### Issue: Python Version Error
```bash
❌ Python 3.8+ required. Current version: 3.7.x
```

**Solution:**
```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt update
sudo apt install python3.9

# Update alternatives
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
```

#### Issue: Permission Denied
```bash
❌ Permission denied: ~/.claude/
```

**Solution:**
```bash
# Fix directory permissions
chmod 755 ~
mkdir -p ~/.claude
chmod 755 ~/.claude

# Re-run setup
./setup
```

#### Issue: Git Clone Failed
```bash
❌ Failed to clone repository
```

**Solution:**
```bash
# Check internet connection
ping github.com

# Try HTTPS instead of SSH
git clone https://github.com/your-username/claude-enhancement-framework.git

# Or download ZIP file
wget https://github.com/your-username/claude-enhancement-framework/archive/main.zip
unzip main.zip
cd claude-enhancement-framework-main
```

#### Issue: Framework Import Error
```bash
❌ Failed to import Claude Enhancement Framework
```

**Solution:**
```bash
# Check Python path
python3 -c "import sys; print(sys.path)"

# Add framework to Python path manually
export PYTHONPATH="$PYTHONPATH:$(pwd)"
./setup

# Or install in development mode
pip3 install -e .
```

### Platform-Specific Issues

#### macOS: Gatekeeper Warning
```bash
# If setup script is blocked by Gatekeeper
xattr -d com.apple.quarantine ./setup
./setup
```

#### Linux: Python3 Not Found
```bash
# Create symlink if python3 command doesn't exist
sudo ln -s /usr/bin/python3.x /usr/bin/python3
```

#### WSL: File Permission Issues
```bash
# Fix Windows/WSL file permissions
sudo chmod +x ./setup
./setup
```

### Performance Issues

#### Slow Boot Times (>50ms)
```bash
# Check system load
top

# Reduce session lines
# Edit ~/.claude/CLAUDE.md
# Set: SESSION_CONTINUITY_LINES=500

# Clear pattern cache
rm -rf ~/.claude/.pattern_cache
```

#### Low Cache Hit Rate (<80%)
```bash
# Increase cache target
# Edit configuration during setup or post-installation
# Set: CACHE_HIT_TARGET=0.85

# Verify memory settings
cat ~/.claude/CLAUDE.md | grep -i cache
```

### Recovery Options

#### Reset to Factory Settings
```bash
# Remove all framework files
rm -rf ~/.claude/CLAUDE.md
rm -rf ~/.claude/LEARNED_CORRECTIONS.md
rm -rf ~/.claude/*LEARNINGS.md

# Remove project files
rm -rf CLAUDE.md SESSION_CONTINUITY.md memory/ patterns/

# Re-run setup
./setup
```

#### Backup Current Configuration
```bash
# Before major changes, backup configuration
mkdir ~/claude-framework-backup
cp -r ~/.claude/* ~/claude-framework-backup/
cp CLAUDE.md SESSION_CONTINUITY.md ~/claude-framework-backup/ 2>/dev/null || true
```

## Advanced Configuration

### Custom Pattern Development

```bash
# Add custom patterns to framework
mkdir -p patterns/custom/
cp my-pattern.md patterns/custom/

# Re-deploy patterns
python3 -c "
from claude_enhancer import ClaudeEnhancer
enhancer = ClaudeEnhancer()
enhancer.deploy_patterns(categories=['custom'])
"
```

### Multi-Project Setup

```bash
# Configure framework for multiple projects
for project in project1 project2 project3; do
    cd $project
    ~/claude-enhancement-framework/setup --project-only
    cd ..
done
```

### Environment Integration

```bash
# Add to shell profile (.bashrc, .zshrc, etc.)
export CLAUDE_FRAMEWORK_HOME=~/claude-enhancement-framework
export PYTHONPATH="$PYTHONPATH:$CLAUDE_FRAMEWORK_HOME"

# Add custom aliases
alias claude-boot="claude 'boot'"
alias claude-patterns="ls $CLAUDE_FRAMEWORK_HOME/patterns/"
```

## Uninstallation

### Complete Removal
```bash
# Remove global configuration
rm -rf ~/.claude/

# Remove project-specific files
rm -f CLAUDE.md SESSION_CONTINUITY.md
rm -rf memory/ patterns/ scripts/ tests/

# Remove framework directory
rm -rf ~/claude-enhancement-framework/
```

### Selective Removal
```bash
# Keep global config, remove project files only
rm -f CLAUDE.md SESSION_CONTINUITY.md
rm -rf memory/ patterns/

# Keep patterns, remove configuration only
rm -f ~/.claude/CLAUDE.md
rm -f CLAUDE.md SESSION_CONTINUITY.md
```

## Getting Help

### Documentation Resources
- **Framework Guide**: [README.md](../README.md)
- **Pattern Reference**: [PATTERNS.md](PATTERNS.md)
- **Configuration Options**: [CONFIGURATION.md](CONFIGURATION.md)  
- **Performance Benchmarks**: [BENCHMARKS.md](BENCHMARKS.md)

### Support Channels
- **GitHub Issues**: Report bugs and feature requests
- **Discussions**: Community support and patterns sharing
- **Wiki**: Extended documentation and examples

### Diagnostic Information

When reporting issues, include:

```bash
# Generate diagnostic report
python3 -c "
from claude_enhancer import ClaudeEnhancer
import platform
import sys

enhancer = ClaudeEnhancer()
status = enhancer.get_framework_status()

print('=== Claude Enhancement Framework Diagnostics ===')
print(f'Framework Version: {status[\"version\"]}')
print(f'Python Version: {sys.version}')
print(f'Platform: {platform.platform()}')
print(f'Initialized: {status[\"initialized\"]}')
print(f'Global Deployed: {status[\"global_deployed\"]}')
print(f'Project Deployed: {status[\"project_deployed\"]}')
print(f'Boot Time: {status[\"boot_metrics\"].get(\"boot_time\", \"N/A\")}ms')
print(f'Global Claude Dir: {status[\"global_claude_dir\"]}')
print(f'Project Root: {status[\"project_root\"]}')
"
```

---

## Quick Reference

### Essential Commands
```bash
# Install framework
./setup

# Global + project deployment (recommended)
./setup --global --project

# Project-only deployment
./setup --project-only

# Custom configuration
./setup --session-lines=1000 --cache-target=0.95

# Verify installation
python3 -c "from claude_enhancer import ClaudeEnhancer; print('✅ Framework ready!')"

# Check status
claude "boot"  # Should show optimized 3-agent boot context
```

### File Locations
- **Global Config**: `~/.claude/CLAUDE.md`
- **Project Config**: `./CLAUDE.md`
- **Session Memory**: `./SESSION_CONTINUITY.md`
- **Patterns**: `./patterns/` (19 patterns across 5 categories)
- **Memory System**: `./memory/` (learning_archive, error_patterns, side_effects_log)

**Installation complete! Your Claude experience is now optimized with 98.5% boot improvement and intelligent pattern systems.**