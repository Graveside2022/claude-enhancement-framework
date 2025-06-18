#!/bin/bash
# Function Extraction Script for CLAUDE.md Migration
# User: Christian
# Purpose: Safely extract bash functions from CLAUDE.md to organized scripts

set -euo pipefail

echo "=== CLAUDE.md Function Extraction Script ==="
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "User: Christian"
echo ""

# Configuration
CLAUDE_MD="CLAUDE.md"
SCRIPTS_DIR="scripts"
BACKUP_FILE="CLAUDE.md.pre_migration_$(date +%Y%m%d_%H%M%S)"

# Create backup
echo "Creating backup: $BACKUP_FILE"
cp "$CLAUDE_MD" "backups/$BACKUP_FILE"

# Create directory structure
echo "Creating script directory structure..."
mkdir -p "$SCRIPTS_DIR"/{core,learning,backup,handoff,reports,utils}

# Function to extract a bash function from CLAUDE.md
extract_function() {
    local func_name="$1"
    local start_line="$2"
    local output_file="$3"
    local category="$4"
    
    echo "  Extracting $func_name (line $start_line) to $output_file"
    
    # Find the function and extract until the closing brace
    awk -v func="$func_name" -v start="$start_line" '
        NR >= start && $0 ~ "^" func "\\(\\) {" { found=1 }
        found {
            print
            if ($0 ~ /^}$/ && brace_count == 0) {
                exit
            }
            # Track brace depth
            gsub(/[^{]/, "", open_braces); brace_count += length($0) - length(open_braces)
            gsub(/[^}]/, "", close_braces); brace_count -= length($0) - length(close_braces)
        }
    ' "$CLAUDE_MD" > temp_func.sh
    
    # Add to output file with header if new file
    if [ ! -f "$output_file" ]; then
        cat > "$output_file" << EOF
#!/bin/bash
# $category Functions for CLAUDE Improvement Project
# User: Christian
# Extracted from CLAUDE.md on $(date -u +%Y-%m-%dT%H:%M:%SZ)

EOF
    fi
    
    # Add function with source comment
    echo -e "\n# Function: $func_name (originally at line $start_line)" >> "$output_file"
    cat temp_func.sh >> "$output_file"
    echo "" >> "$output_file"
    
    rm temp_func.sh
}

# Extract Core System Functions
echo "Extracting Core System Functions..."
extract_function "initialize_global_structure" 238 "$SCRIPTS_DIR/core/system_functions.sh" "Core System"
extract_function "whats_next" 3492 "$SCRIPTS_DIR/core/system_functions.sh" "Core System"
extract_function "detect_whats_next_request" 3506 "$SCRIPTS_DIR/core/system_functions.sh" "Core System"
extract_function "find_project_root" 1136 "$SCRIPTS_DIR/core/project_detection.sh" "Project Detection"

# Extract Learning Functions
echo "Extracting Learning Functions..."
extract_function "load_learning_files" 549 "$SCRIPTS_DIR/learning/learning_loader.sh" "Learning Loader"
extract_function "load_file_organization_enforcement" 605 "$SCRIPTS_DIR/learning/file_organization.sh" "File Organization"
extract_function "organize_misplaced_files" 643 "$SCRIPTS_DIR/learning/file_organization.sh" "File Organization"

# Extract Backup Functions
echo "Extracting Backup Functions..."
extract_function "check_scheduled_backup" 830 "$SCRIPTS_DIR/backup/backup_system.sh" "Backup System"
extract_function "create_backup" 848 "$SCRIPTS_DIR/backup/backup_system.sh" "Backup System"
extract_function "check_context_backup" 916 "$SCRIPTS_DIR/backup/backup_system.sh" "Backup System"
extract_function "create_project_backup" 2187 "$SCRIPTS_DIR/backup/backup_system.sh" "Backup System"
extract_function "check_timing_rules" 2121 "$SCRIPTS_DIR/backup/timing_rules.sh" "Timing Rules"

# Extract Handoff Functions
echo "Extracting Handoff Functions..."
# Note: generate_handoff_files appears twice, we'll use the first occurrence
extract_function "generate_handoff_files" 928 "$SCRIPTS_DIR/handoff/handoff_core.sh" "Handoff Core"
extract_function "detect_handoff_triggers" 2363 "$SCRIPTS_DIR/handoff/trigger_detection.sh" "Trigger Detection"
extract_function "execute_trigger_protocol" 2413 "$SCRIPTS_DIR/handoff/trigger_detection.sh" "Trigger Detection"
extract_function "execute_checkpoint_protocol" 2453 "$SCRIPTS_DIR/handoff/session_protocols.sh" "Session Protocols"
extract_function "execute_handoff_protocol" 2553 "$SCRIPTS_DIR/handoff/session_protocols.sh" "Session Protocols"
extract_function "execute_context_limit_protocol" 2628 "$SCRIPTS_DIR/handoff/session_protocols.sh" "Session Protocols"
extract_function "validate_handoff_completeness" 2705 "$SCRIPTS_DIR/handoff/handoff_core.sh" "Handoff Core"
extract_function "check_all_handoff_functions" 2823 "$SCRIPTS_DIR/handoff/handoff_core.sh" "Handoff Core"
extract_function "generate_session_end_protocol" 2232 "$SCRIPTS_DIR/handoff/session_protocols.sh" "Session Protocols"

# Extract Reports Functions
echo "Extracting Reports Functions..."
extract_function "initialize_reports_structure" 2913 "$SCRIPTS_DIR/reports/reports_organization.sh" "Reports Organization"
extract_function "get_timestamped_report_path" 2995 "$SCRIPTS_DIR/reports/reports_organization.sh" "Reports Organization"
extract_function "cleanup_old_reports" 3040 "$SCRIPTS_DIR/reports/reports_organization.sh" "Reports Organization"
extract_function "categorize_report" 3112 "$SCRIPTS_DIR/reports/reports_organization.sh" "Reports Organization"
extract_function "generate_organized_report" 3144 "$SCRIPTS_DIR/reports/reports_organization.sh" "Reports Organization"
extract_function "update_existing_reports_to_use_organization" 3202 "$SCRIPTS_DIR/reports/reports_organization.sh" "Reports Organization"

# Extract Project Initialization
echo "Extracting Project Initialization Functions..."
extract_function "initialize_complete_project_template" 3319 "$SCRIPTS_DIR/utils/project_initialization.sh" "Project Initialization"

# Create the sourcing helper
echo "Creating sourcing helper..."
cat > "$SCRIPTS_DIR/utils/sourcing_helper.sh" << 'EOF'
#!/bin/bash
# Sourcing Helper for CLAUDE Functions
# User: Christian
# Purpose: Load all extracted CLAUDE functions

# Get the scripts directory
CLAUDE_SCRIPTS_DIR="$(dirname "${BASH_SOURCE[0]}")/.."

# Function to load all CLAUDE functions
load_all_claude_functions() {
    local load_count=0
    
    echo "Loading CLAUDE functions for Christian..."
    
    # Core functions
    if [ -f "$CLAUDE_SCRIPTS_DIR/core/system_functions.sh" ]; then
        source "$CLAUDE_SCRIPTS_DIR/core/system_functions.sh"
        ((load_count++))
    fi
    
    if [ -f "$CLAUDE_SCRIPTS_DIR/core/project_detection.sh" ]; then
        source "$CLAUDE_SCRIPTS_DIR/core/project_detection.sh"
        ((load_count++))
    fi
    
    # Learning functions
    if [ -f "$CLAUDE_SCRIPTS_DIR/learning/learning_loader.sh" ]; then
        source "$CLAUDE_SCRIPTS_DIR/learning/learning_loader.sh"
        ((load_count++))
    fi
    
    if [ -f "$CLAUDE_SCRIPTS_DIR/learning/file_organization.sh" ]; then
        source "$CLAUDE_SCRIPTS_DIR/learning/file_organization.sh"
        ((load_count++))
    fi
    
    # Backup functions
    if [ -f "$CLAUDE_SCRIPTS_DIR/backup/backup_system.sh" ]; then
        source "$CLAUDE_SCRIPTS_DIR/backup/backup_system.sh"
        ((load_count++))
    fi
    
    if [ -f "$CLAUDE_SCRIPTS_DIR/backup/timing_rules.sh" ]; then
        source "$CLAUDE_SCRIPTS_DIR/backup/timing_rules.sh"
        ((load_count++))
    fi
    
    # Handoff functions
    if [ -f "$CLAUDE_SCRIPTS_DIR/handoff/handoff_core.sh" ]; then
        source "$CLAUDE_SCRIPTS_DIR/handoff/handoff_core.sh"
        ((load_count++))
    fi
    
    if [ -f "$CLAUDE_SCRIPTS_DIR/handoff/trigger_detection.sh" ]; then
        source "$CLAUDE_SCRIPTS_DIR/handoff/trigger_detection.sh"
        ((load_count++))
    fi
    
    if [ -f "$CLAUDE_SCRIPTS_DIR/handoff/session_protocols.sh" ]; then
        source "$CLAUDE_SCRIPTS_DIR/handoff/session_protocols.sh"
        ((load_count++))
    fi
    
    # Reports functions
    if [ -f "$CLAUDE_SCRIPTS_DIR/reports/reports_organization.sh" ]; then
        source "$CLAUDE_SCRIPTS_DIR/reports/reports_organization.sh"
        ((load_count++))
    fi
    
    # Utils functions
    if [ -f "$CLAUDE_SCRIPTS_DIR/utils/project_initialization.sh" ]; then
        source "$CLAUDE_SCRIPTS_DIR/utils/project_initialization.sh"
        ((load_count++))
    fi
    
    echo "✓ Loaded $load_count CLAUDE function files"
    return 0
}

# Auto-load if sourced
if [ "${BASH_SOURCE[0]}" != "${0}" ]; then
    load_all_claude_functions
fi
EOF

# Make all scripts executable
echo "Making scripts executable..."
find "$SCRIPTS_DIR" -name "*.sh" -exec chmod +x {} \;

# Create extraction summary
cat > "$SCRIPTS_DIR/EXTRACTION_SUMMARY.md" << EOF
# Function Extraction Summary
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian

## Extracted Functions

### Core System Functions (scripts/core/)
- initialize_global_structure() - system_functions.sh
- whats_next() - system_functions.sh
- detect_whats_next_request() - system_functions.sh
- find_project_root() - project_detection.sh

### Learning Functions (scripts/learning/)
- load_learning_files() - learning_loader.sh
- load_file_organization_enforcement() - file_organization.sh
- organize_misplaced_files() - file_organization.sh

### Backup Functions (scripts/backup/)
- check_scheduled_backup() - backup_system.sh
- create_backup() - backup_system.sh
- check_context_backup() - backup_system.sh
- create_project_backup() - backup_system.sh
- check_timing_rules() - timing_rules.sh

### Handoff Functions (scripts/handoff/)
- generate_handoff_files() - handoff_core.sh
- detect_handoff_triggers() - trigger_detection.sh
- execute_trigger_protocol() - trigger_detection.sh
- execute_checkpoint_protocol() - session_protocols.sh
- execute_handoff_protocol() - session_protocols.sh
- execute_context_limit_protocol() - session_protocols.sh
- validate_handoff_completeness() - handoff_core.sh
- check_all_handoff_functions() - handoff_core.sh
- generate_session_end_protocol() - session_protocols.sh

### Reports Functions (scripts/reports/)
- initialize_reports_structure() - reports_organization.sh
- get_timestamped_report_path() - reports_organization.sh
- cleanup_old_reports() - reports_organization.sh
- categorize_report() - reports_organization.sh
- generate_organized_report() - reports_organization.sh
- update_existing_reports_to_use_organization() - reports_organization.sh

### Project Functions (scripts/utils/)
- initialize_complete_project_template() - project_initialization.sh

## Usage
To load all functions:
\`\`\`bash
source scripts/utils/sourcing_helper.sh
\`\`\`

## Backup
Original CLAUDE.md backed up to: backups/$BACKUP_FILE
EOF

echo ""
echo "✅ Function extraction complete!"
echo "📁 Functions extracted to: $SCRIPTS_DIR/"
echo "📊 Summary: $SCRIPTS_DIR/EXTRACTION_SUMMARY.md"
echo "💾 Backup: backups/$BACKUP_FILE"