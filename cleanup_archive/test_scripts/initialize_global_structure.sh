#\!/bin/bash
echo "🔧 Initializing global structure for Christian..."

# Create essential directories if they don't exist
echo "📁 Creating directories..."
mkdir -p "$HOME/.claude/backups"
mkdir -p "$HOME/.claude/.claude"

# Initialize backup system markers
if [ \! -f "$HOME/.claude/backups/.last_scheduled_backup" ]; then
    echo "⏰ Initializing backup system..."
    touch "$HOME/.claude/backups/.last_scheduled_backup"
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Backup system initialized for Christian" >> "$HOME/.claude/backups/backup_log.txt"
fi

# Create TODO.md if it doesn't exist
if [ \! -f "$HOME/.claude/TODO.md" ]; then
    echo "📝 Creating TODO.md..."
    cat > "$HOME/.claude/TODO.md" << EOT
# TODO.md - Development Pipeline
Created: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian

## PROJECT TYPE
[To be determined from initial scan]

## CURRENT SPRINT
- [ ] Initial setup complete

## COMPLETED THIS SESSION
- [x] Created TODO.md
- [x] Initialized global structure

## BACKLOG
- [ ] Define initial tasks based on project type
EOT
fi

# Create LEARNED_CORRECTIONS.md if it doesn't exist
if [ \! -f "$HOME/.claude/LEARNED_CORRECTIONS.md" ]; then
    echo "🧠 Creating LEARNED_CORRECTIONS.md..."
    cat > "$HOME/.claude/LEARNED_CORRECTIONS.md" << EOT
# LEARNED CORRECTIONS LOG
User: Christian
Initialized: $(date -u +%Y-%m-%dT%H:%M:%SZ)

This file tracks errors identified and corrections learned to prevent recurrence.

## FORMAT
Each entry includes:
- Date/Time
- Error Context
- Analysis Results
- Prevention Procedures
- Validation Checkpoints

---
EOT
fi

# Create domain-specific learning files if they don't exist
echo "📚 Creating domain-specific learning files..."
if [ \! -f "$HOME/.claude/PYTHON_LEARNINGS.md" ]; then
    cat > "$HOME/.claude/PYTHON_LEARNINGS.md" << EOT
# PYTHON LEARNINGS
User: Christian
Initialized: $(date -u +%Y-%m-%dT%H:%M:%SZ)

Domain-specific learnings for Python development.

---
EOT
fi

if [ \! -f "$HOME/.claude/INFRASTRUCTURE_LEARNINGS.md" ]; then
    cat > "$HOME/.claude/INFRASTRUCTURE_LEARNINGS.md" << EOT
# INFRASTRUCTURE LEARNINGS
User: Christian
Initialized: $(date -u +%Y-%m-%dT%H:%M:%SZ)

Domain-specific learnings for infrastructure and deployment.

---
EOT
fi

if [ \! -f "$HOME/.claude/PROJECT_SPECIFIC_LEARNINGS.md" ]; then
    cat > "$HOME/.claude/PROJECT_SPECIFIC_LEARNINGS.md" << EOT
# PROJECT SPECIFIC LEARNINGS
User: Christian
Initialized: $(date -u +%Y-%m-%dT%H:%M:%SZ)

Learnings specific to individual projects.

---
EOT
fi

# Create .project_context if it doesn't exist
if [ \! -f "$HOME/.claude/.project_context" ]; then
    echo "🎯 Creating .project_context..."
    echo "# Project Context - $(date -u +%Y-%m-%d)" > "$HOME/.claude/.project_context"
    echo "User: Christian" >> "$HOME/.claude/.project_context"
    echo "Initialized: Auto-initialization on session start" >> "$HOME/.claude/.project_context"
fi

# Ensure backup log exists
if [ \! -f "$HOME/.claude/backups/backup_log.txt" ]; then
    echo "📋 Creating backup log..."
    echo "# Backup Log - Started $(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$HOME/.claude/backups/backup_log.txt"
    echo "User: Christian" >> "$HOME/.claude/backups/backup_log.txt"
    echo "---" >> "$HOME/.claude/backups/backup_log.txt"
fi

echo "✅ Global structure initialization complete\!"
