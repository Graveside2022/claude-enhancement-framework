# Claude Enhancement Framework - Troubleshooting Guide

## Table of Contents
1. [Installation and Setup Issues](#installation-and-setup-issues)
2. [Framework Initialization Problems](#framework-initialization-problems)
3. [Pattern Deployment Issues](#pattern-deployment-issues)
4. [Platform-Specific Troubleshooting](#platform-specific-troubleshooting)
5. [Frequently Asked Questions (FAQ)](#frequently-asked-questions-faq)
6. [Diagnostic Commands](#diagnostic-commands)
7. [Validation Steps](#validation-steps)

---

## Installation and Setup Issues

### Issue: Permission Denied During Installation
**Symptoms:**
- `Permission denied` errors when running setup script
- Cannot create directories or files

**Solutions:**
```bash
# Option 1: Run with appropriate permissions
sudo ./setup

# Option 2: Change ownership of target directory
sudo chown -R $USER:$USER ~/.claude/

# Option 3: Use user-specific installation
./setup --user-only
```

### Issue: Python Path Not Found
**Symptoms:**
- `python: command not found`
- Import errors for claude_enhancer module

**Solutions:**
```bash
# Check Python installation
which python3
python3 --version

# Add to PATH if needed
export PATH="/usr/local/bin/python3:$PATH"

# Install using specific Python version
python3 -m pip install -e .
```

### Issue: Dependencies Not Installing
**Symptoms:**
- Module import errors
- Missing required packages

**Solutions:**
```bash
# Install dependencies manually
pip install -r requirements.txt

# Or install with development dependencies
pip install -e ".[dev]"

# Check for conflicting versions
pip list | grep claude
```

---

## Framework Initialization Problems

### Issue: CLAUDE.md Not Found
**Symptoms:**
- Framework fails to initialize
- "Configuration file not found" errors

**Solutions:**
1. **Check file location:**
   ```bash
   ls -la ~/.claude/CLAUDE.md
   ls -la ./CLAUDE.md
   ```

2. **Create minimal configuration:**
   ```bash
   ./setup --init-config
   ```

3. **Manual configuration creation:**
   ```bash
   mkdir -p ~/.claude
   cp templates/CLAUDE_template.md ~/.claude/CLAUDE.md
   ```

### Issue: Pattern Directory Not Created
**Symptoms:**
- No patterns/ directory found
- Pattern loading failures

**Solutions:**
```bash
# Create pattern structure manually
mkdir -p patterns/{generation,refactoring,bug_fixes,architecture,security}

# Or run structure initialization
python -c "from claude_enhancer.core.enhancer import ClaudeEnhancer; ClaudeEnhancer().init_project_structure()"
```

### Issue: Memory Files Missing
**Symptoms:**
- No SESSION_CONTINUITY.md found
- Memory persistence not working

**Solutions:**
```bash
# Initialize memory structure
mkdir -p memory
cp claude_enhancer/memory/*.md memory/

# Or use framework initialization
python -c "
from claude_enhancer.deployment.pattern_deployer import PatternDeployer
deployer = PatternDeployer()
deployer.setup_memory_structure()
"
```

---

## Pattern Deployment Issues

### Issue: Pattern Validation Failures
**Symptoms:**
- "Pattern validation failed" errors
- Patterns not being applied

**Solutions:**
1. **Check pattern syntax:**
   ```bash
   python patterns/validate_patterns.py
   ```

2. **Validate specific pattern:**
   ```python
   from claude_enhancer.deployment.pattern_deployer import PatternDeployer
   deployer = PatternDeployer()
   result = deployer.validate_pattern("patterns/generation/your_pattern.md")
   print(result)
   ```

3. **Fix common validation issues:**
   - Ensure proper YAML frontmatter
   - Check required fields: name, type, description
   - Validate code block syntax

### Issue: Pattern Not Found During Deployment
**Symptoms:**
- "Pattern file not found" errors
- Deployment script fails

**Solutions:**
```bash
# Check pattern file exists
ls -la patterns/generation/your_pattern.md

# Verify pattern structure
find patterns/ -name "*.md" -type f

# Check pattern registry
python -c "
from claude_enhancer.deployment.pattern_deployer import PatternDeployer
deployer = PatternDeployer()
patterns = deployer.list_available_patterns()
print(patterns)
"
```

### Issue: Cross-Project Deployment Failures
**Symptoms:**
- Patterns not copying to target projects
- Permission errors during deployment

**Solutions:**
```bash
# Check target directory permissions
ls -ld /path/to/target/project/

# Run deployment with verbose output
python examples/pattern_deployment_example.py --verbose

# Manual pattern copying
cp -r patterns/ /path/to/target/project/patterns/
```

---

## Platform-Specific Troubleshooting

### macOS Issues

#### Issue: Gatekeeper Blocking Execution
**Solutions:**
```bash
# Remove quarantine attribute
xattr -d com.apple.quarantine setup

# Or allow in System Preferences > Security & Privacy
```

#### Issue: PATH Issues with Homebrew Python
**Solutions:**
```bash
# Add to ~/.zshrc or ~/.bash_profile
export PATH="/opt/homebrew/bin:$PATH"

# Or use specific Python path
/opt/homebrew/bin/python3 -m pip install -e .
```

### Linux Issues

#### Issue: Missing Build Tools
**Solutions:**
```bash
# Ubuntu/Debian
sudo apt-get install build-essential python3-dev

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel

# Arch Linux
sudo pacman -S base-devel python3
```

#### Issue: SELinux Restrictions
**Solutions:**
```bash
# Check SELinux status
sestatus

# Temporarily disable if needed
sudo setenforce 0

# Or create appropriate SELinux policy
```

### Windows Issues

#### Issue: PowerShell Execution Policy
**Solutions:**
```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Issue: Path Length Limitations
**Solutions:**
- Enable long path support in Windows 10/11
- Use shorter directory names
- Install in root directory (C:\claude-enhancer)

---

## Frequently Asked Questions (FAQ)

### Q: How do I verify the framework is properly installed?
**A:** Run the validation commands:
```bash
python -c "import claude_enhancer; print('Framework imported successfully')"
./setup --verify
```

### Q: Can I use this framework with existing Claude projects?
**A:** Yes, the framework is designed to integrate with existing projects:
```bash
cd /path/to/existing/project
python /path/to/claude-enhancement-framework/examples/pattern_deployment_example.py
```

### Q: How do I update patterns after deployment?
**A:** Patterns can be updated and redeployed:
```bash
# Update patterns in framework
git pull  # if using git

# Redeploy to projects
python examples/pattern_deployment_example.py --update
```

### Q: What's the difference between global and project-specific patterns?
**A:** 
- **Global patterns**: Stored in framework, apply to all projects
- **Project-specific patterns**: Stored in project/patterns/, override global ones

### Q: How do I create custom patterns?
**A:** Follow the pattern template structure:
```bash
cp templates/pattern_template.md patterns/generation/my_pattern.md
# Edit the pattern with your specific requirements
```

### Q: Can I disable certain patterns?
**A:** Yes, use pattern configuration:
```python
from claude_enhancer.core.enhancer import ClaudeEnhancer
enhancer = ClaudeEnhancer()
enhancer.disable_pattern("pattern_name")
```

### Q: How do I backup my patterns before updates?
**A:** 
```bash
# Create backup
cp -r patterns/ patterns_backup_$(date +%Y%m%d)/

# Or use the built-in backup
python -c "
from claude_enhancer.deployment.pattern_deployer import PatternDeployer
PatternDeployer().backup_patterns()
"
```

---

## Diagnostic Commands

### Framework Health Check
```bash
# Comprehensive system check
python -c "
from claude_enhancer.core.enhancer import ClaudeEnhancer
enhancer = ClaudeEnhancer()
enhancer.run_diagnostics()
"
```

### Pattern Validation
```bash
# Validate all patterns
python patterns/validate_patterns.py --all

# Validate specific pattern type
python patterns/validate_patterns.py --type generation
```

### Configuration Check
```bash
# Check configuration files
python -c "
from claude_enhancer.core.config import Config
config = Config()
config.validate()
print('Configuration valid')
"
```

### Memory System Check
```bash
# Check memory file integrity
python -c "
from claude_enhancer.deployment.pattern_deployer import PatternDeployer
deployer = PatternDeployer()
status = deployer.check_memory_system()
print(f'Memory system status: {status}')
"
```

### Deployment Status
```bash
# Check deployment status
python -c "
from claude_enhancer.deployment.pattern_deployer import PatternDeployer
deployer = PatternDeployer()
status = deployer.get_deployment_status()
for project, info in status.items():
    print(f'{project}: {info}')
"
```

---

## Validation Steps

### 1. Pre-Installation Validation
```bash
# Check system requirements
python3 --version  # Should be 3.8+
pip --version
git --version  # Optional but recommended
```

### 2. Post-Installation Validation
```bash
# Test import
python -c "import claude_enhancer; print('✓ Framework installed')"

# Test configuration
python -c "
from claude_enhancer.core.config import Config
config = Config()
print('✓ Configuration loaded')
"

# Test pattern loading
python -c "
from claude_enhancer.deployment.pattern_deployer import PatternDeployer
deployer = PatternDeployer()
patterns = deployer.list_available_patterns()
print(f'✓ Found {len(patterns)} patterns')
"
```

### 3. Pattern Deployment Validation
```bash
# Test pattern deployment
python examples/pattern_deployment_example.py --dry-run

# Verify pattern files exist
ls -la patterns/generation/
ls -la patterns/refactoring/
ls -la patterns/bug_fixes/
ls -la patterns/architecture/
```

### 4. Memory System Validation
```bash
# Check memory templates
ls -la claude_enhancer/memory/

# Test memory initialization
python -c "
from claude_enhancer.deployment.pattern_deployer import PatternDeployer
deployer = PatternDeployer()
deployer.setup_memory_structure()
print('✓ Memory system initialized')
"
```

### 5. Integration Validation
```bash
# Test with sample project
mkdir -p test_project
cd test_project
python ../examples/pattern_deployment_example.py
ls -la patterns/  # Should contain deployed patterns
ls -la memory/    # Should contain memory templates
```

---

## Getting Help

If you continue to experience issues:

1. **Check the logs:**
   ```bash
   tail -f ~/.claude/logs/enhancer.log
   ```

2. **Enable debug mode:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

3. **Create a minimal test case:**
   ```bash
   mkdir debug_test
   cd debug_test
   python -c "
   from claude_enhancer.core.enhancer import ClaudeEnhancer
   enhancer = ClaudeEnhancer()
   enhancer.init_project_structure()
   "
   ```

4. **Report issues with:**
   - Python version
   - Operating system
   - Full error message
   - Steps to reproduce

Remember: Most issues are related to file permissions, Python path configuration, or missing dependencies. Double-check these basics before diving into complex solutions.