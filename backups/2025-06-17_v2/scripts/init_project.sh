#!/bin/bash
# CLAUDE Improvement Project Initialization Script
# Purpose: Set up a new CLAUDE improvement project with standard structure
# Usage: ./init_project.sh [project_name]
# Requirements: bash, standard Unix utilities

set -e  # Exit on error

PROJECT_NAME="${1:-CLAUDE_improvement}"
echo "Initializing CLAUDE improvement project: $PROJECT_NAME"

# Create directory structure
echo "Creating directory structure..."
mkdir -p "$PROJECT_NAME"/{patterns,memory,scripts,tests,docs}

# Create initial files
echo "Creating initial files..."

# Create README
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

# Create SESSION_CONTINUITY template
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

# Create .gitkeep files
touch "$PROJECT_NAME"/{patterns,scripts,tests,docs}/.gitkeep

echo "Project structure created successfully!"
echo "Directory contents:"
ls -la "$PROJECT_NAME"