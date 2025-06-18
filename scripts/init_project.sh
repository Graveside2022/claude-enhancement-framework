#!/bin/bash
# CLAUDE Improvement Project Initialization Script
# Purpose: Set up a new CLAUDE improvement project with standard structure
# Usage: ./init_project.sh [project_name]
# Requirements: bash, standard Unix utilities

set -e  # Exit on error

# Installation timing and metrics
INSTALL_START_TIME=$(date +%s)
FILES_CREATED=0
DIRECTORIES_CREATED=0
VERIFICATION_FAILURES=0
CREATED_PATHS=()

# Error handling function
handle_error() {
    local exit_code=$?
    local line_number=$1
    echo ""
    echo "✗ Error: Installation failed at line $line_number (exit code: $exit_code)"
    echo "✗ Error: Unable to complete project initialization"
    echo "💡 Suggestion: Check file permissions and disk space"
    exit $exit_code
}

# Set up error trap
trap 'handle_error $LINENO' ERR

PROJECT_NAME="${1:-CLAUDE_improvement}"
echo "🚀 Initializing CLAUDE improvement project: $PROJECT_NAME"
echo "📁 Target directory: $PROJECT_NAME"

# Create directory structure
echo ""
echo "📂 Creating directory structure..."
total_dirs=5
dirs_created=0

for dir in patterns memory scripts tests docs; do
    if [ ! -d "$PROJECT_NAME/$dir" ]; then
        mkdir -p "$PROJECT_NAME/$dir"
        ((dirs_created++))
        echo "✓ Created $dir/ (${dirs_created}/${total_dirs})"
    else
        echo "- Directory $dir/ already exists"
    fi
done

echo "✅ Directory structure complete (${dirs_created} directories created)"

# Create initial files
echo ""
echo "📄 Installing project-specific files..."
total_files=3
files_created=0

# Create README
if [ ! -f "$PROJECT_NAME/README.md" ]; then
    cat > "$PROJECT_NAME/README.md" << 'EOF'
# CLAUDE Improvement Project

## Project Purpose
This project systematically captures and implements improvements for Claude's operational effectiveness.

## Directory Structure
- patterns/: Successful interaction patterns
- memory/: Persistent memory storage
- scripts/: Automation tools
- tests/: Validation tests
- docs/: Documentation

Created: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian
EOF
    ((files_created++))
    echo "✓ Created README.md (${files_created}/${total_files})"
else
    echo "- File README.md already exists"
fi

# Create SESSION_CONTINUITY template
if [ ! -f "$PROJECT_NAME/memory/SESSION_CONTINUITY.md" ]; then
    cat > "$PROJECT_NAME/memory/SESSION_CONTINUITY.md" << 'EOF'
# SESSION CONTINUITY
Created: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian

## Current Status
- Task: [Current task]
- Progress: [Progress made]
- Next step: [Immediate next action]

## Environment Info
- OS: [Operating system]
- Project Path: [Path]

## Files Modified
- [List files]

## What Worked
- [Successful approaches]

## What Didn't Work
- [Failed attempts]

## Key Decisions
- [Technical choices]
EOF
    ((files_created++))
    echo "✓ Created memory/SESSION_CONTINUITY.md (${files_created}/${total_files})"
else
    echo "- File memory/SESSION_CONTINUITY.md already exists"
fi

# Create .gitkeep files
echo "📌 Creating .gitkeep placeholder files..."
gitkeep_dirs=(patterns scripts tests docs)
gitkeep_created=0

for dir in "${gitkeep_dirs[@]}"; do
    if [ ! -f "$PROJECT_NAME/$dir/.gitkeep" ]; then
        touch "$PROJECT_NAME/$dir/.gitkeep"
        ((gitkeep_created++))
        echo "✓ Created $dir/.gitkeep"
    else
        echo "- File $dir/.gitkeep already exists"
    fi
done

if [ ! -f "$PROJECT_NAME/memory/.gitkeep" ]; then
    touch "$PROJECT_NAME/memory/.gitkeep"
    ((gitkeep_created++))
    echo "✓ Created memory/.gitkeep"
else
    echo "- File memory/.gitkeep already exists"
fi

((files_created++))
echo "✓ Placeholder files complete (${files_created}/${total_files})"

echo ""
echo "✅ Project-specific files installed successfully"

# Comprehensive installation summary
show_initialization_summary() {
    INSTALL_END_TIME=$(date +%s)
    INSTALL_DURATION=$((INSTALL_END_TIME - INSTALL_START_TIME))
    
    echo ""
    echo "╔════════════════════════════════════════════════════════════════════════════════╗"
    echo "║                   PROJECT INITIALIZATION SUMMARY                              ║"
    echo "╠════════════════════════════════════════════════════════════════════════════════╣"
    echo "║ Project: $PROJECT_NAME                                                        ║"
    echo "║ Component: CLAUDE Improvement Project Structure                               ║"
    echo "║ Initialization Date: $(date +'%Y-%m-%d %H:%M:%S %Z')                                  ║"
    echo "║ Initialization Duration: ${INSTALL_DURATION}s                                         ║"
    echo "╚════════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    
    echo "📊 INITIALIZATION METRICS"
    echo "├─ Directories Created: ${dirs_created}/${total_dirs}"
    echo "├─ Files Created: ${files_created}/${total_files}"
    echo "├─ Placeholder Files: ${gitkeep_created}"
    echo "├─ Total Components: $((dirs_created + files_created + gitkeep_created))"
    echo "└─ Success Rate: $(( (dirs_created + files_created) > 0 ? ((dirs_created + files_created) * 100) / (total_dirs + total_files) : 0 ))%"
    echo ""
    
    echo "📁 PROJECT STRUCTURE CREATED"
    if [ -d "$PROJECT_NAME" ]; then
        echo "├─ Project Root: $(pwd)/$PROJECT_NAME"
        echo "├─ Core Directories:"
        for dir in patterns memory scripts tests docs; do
            if [ -d "$PROJECT_NAME/$dir" ]; then
                echo "│  ├─ $dir/ (ready for use)"
            else
                echo "│  ├─ $dir/ (⚠️ missing)"
            fi
        done
        echo "├─ Configuration Files:"
        echo "│  ├─ README.md (project documentation)"
        echo "│  └─ memory/SESSION_CONTINUITY.md (session tracking)"
        echo "└─ Placeholder Files: .gitkeep files in each directory"
    fi
    echo ""
    
    echo "📋 PROJECT COMPONENTS"
    echo "├─ patterns/    - Successful interaction patterns"
    echo "├─ memory/      - Persistent memory storage"
    echo "├─ scripts/     - Automation tools"
    echo "├─ tests/       - Validation tests"
    echo "└─ docs/        - Documentation"
    echo ""
    
    echo "🚀 NEXT STEPS & USAGE INSTRUCTIONS"
    echo "1. Navigate to your project:"
    echo "   └─ cd $PROJECT_NAME"
    echo ""
    echo "2. Initialize version control:"
    echo "   ├─ git init"
    echo "   ├─ git add ."
    echo "   └─ git commit -m \"Initial project structure\""
    echo ""
    echo "3. Start working:"
    echo "   ├─ Edit memory/SESSION_CONTINUITY.md for your session"
    echo "   ├─ Add patterns to patterns/ directory"
    echo "   └─ Create scripts in scripts/ directory"
    echo ""
    echo "4. Directory contents:"
    ls -la "$PROJECT_NAME"
    echo ""
    
    if [ $((dirs_created + files_created)) -eq $((total_dirs + total_files)) ]; then
        echo "✅ INITIALIZATION COMPLETED SUCCESSFULLY"
        echo "   All components created and verified. Project ready for use."
    else
        echo "⚠️ INITIALIZATION COMPLETED WITH WARNINGS"
        echo "   Some components may need manual verification. Check structure above."
    fi
    echo ""
}

show_initialization_summary