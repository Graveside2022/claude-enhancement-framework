#!/bin/bash
# SESSION_CONTINUITY Context Restoration Tool
# Usage: ./restore_session_context.sh YYYY-MM-DD [--append|--replace]

set -e

PROJECT_ROOT="/Users/scarmatrix/Project/CLAUDE_improvement"
ARCHIVE_ROOT="$PROJECT_ROOT/logs/session_continuity"
SESSION_FILE="$PROJECT_ROOT/SESSION_CONTINUITY.md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print usage
usage() {
    echo "Usage: $0 YYYY-MM-DD [--append|--replace]"
    echo ""
    echo "Examples:"
    echo "  $0 2025-06-16                    # Show archived session from June 16, 2025"
    echo "  $0 2025-06-16 --append          # Append archived session to current file"
    echo "  $0 2025-06-16 --replace         # Replace current file with archived session"
    echo ""
    echo "Available operations:"
    echo "  (default)  Display archived content without modifying current file"
    echo "  --append   Add archived content to the end of current SESSION_CONTINUITY.md"
    echo "  --replace  Replace current file with archived content (creates backup first)"
    echo ""
    exit 1
}

# Function to find archived files for a date
find_archived_files() {
    local target_date="$1"
    local year_month=$(echo "$target_date" | cut -d'-' -f1,2)
    local archive_dir="$ARCHIVE_ROOT/$year_month"
    
    if [ ! -d "$archive_dir" ]; then
        echo -e "${RED}❌ No archives found for $target_date${NC}"
        echo "Available archive months:"
        ls -1 "$ARCHIVE_ROOT" 2>/dev/null | grep -E '^[0-9]{4}-[0-9]{2}$' || echo "  (no archives found)"
        return 1
    fi
    
    # Find files matching the date
    local files=($(find "$archive_dir" -name "*$target_date*" -type f | sort))
    
    if [ ${#files[@]} -eq 0 ]; then
        echo -e "${RED}❌ No archived files found for $target_date${NC}"
        echo "Available dates in $year_month:"
        ls -1 "$archive_dir" | grep -o '[0-9]{4}-[0-9]{2}-[0-9]{2}' | sort -u || echo "  (no files found)"
        return 1
    fi
    
    echo "${files[@]}"
}

# Function to create backup
create_backup() {
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local backup_dir="$PROJECT_ROOT/backups/session_restore_$timestamp"
    
    mkdir -p "$backup_dir"
    cp "$SESSION_FILE" "$backup_dir/SESSION_CONTINUITY.md"
    
    echo "$backup_dir/SESSION_CONTINUITY.md"
}

# Function to display archived content
display_archived_content() {
    local files=("$@")
    
    echo -e "${GREEN}📋 Archived Session Content:${NC}"
    echo "==============================================="
    
    for file in "${files[@]}"; do
        local relative_path=$(echo "$file" | sed "s|$ARCHIVE_ROOT/||")
        echo -e "${BLUE}📄 $relative_path${NC}"
        echo "-----------------------------------------------"
        cat "$file"
        echo ""
        echo "==============================================="
    done
}

# Function to append archived content
append_archived_content() {
    local files=("$@")
    local target_date="$1"
    
    echo -e "${YELLOW}📝 Appending archived content to SESSION_CONTINUITY.md...${NC}"
    
    # Add separator in current file
    echo "" >> "$SESSION_FILE"
    echo "## RESTORED FROM ARCHIVE - $(date '+%Y-%m-%d %H:%M:%S')" >> "$SESSION_FILE"
    echo "**Source**: Archived session from $target_date" >> "$SESSION_FILE"
    echo "**Restoration method**: Append to current session" >> "$SESSION_FILE"
    echo "" >> "$SESSION_FILE"
    
    # Append each archived file
    for file in "${files[@]}"; do
        local relative_path=$(echo "$file" | sed "s|$ARCHIVE_ROOT/||")
        echo "### Restored from: $relative_path" >> "$SESSION_FILE"
        echo "" >> "$SESSION_FILE"
        cat "$file" >> "$SESSION_FILE"
        echo "" >> "$SESSION_FILE"
        echo "---" >> "$SESSION_FILE"
        echo "" >> "$SESSION_FILE"
    done
    
    echo -e "${GREEN}✅ Archived content appended successfully${NC}"
}

# Function to replace with archived content
replace_with_archived_content() {
    local files=("$@")
    local target_date="$1"
    
    echo -e "${YELLOW}🔄 Replacing SESSION_CONTINUITY.md with archived content...${NC}"
    
    # Create backup first
    local backup_path=$(create_backup)
    echo -e "${BLUE}📦 Backup created: $backup_path${NC}"
    
    # Create new file header
    cat > "$SESSION_FILE" << EOF
# SESSION CONTINUITY LOG - CLAUDE Improvement Project
User: Christian
Project: Automatic learning file loading on session start implementation

## RESTORED FROM ARCHIVE - $(date '+%Y-%m-%d %H:%M:%S')
**Source**: Archived session from $target_date
**Restoration method**: Full replacement (backup created)
**Backup location**: $backup_path

EOF
    
    # Add each archived file
    for file in "${files[@]}"; do
        local relative_path=$(echo "$file" | sed "s|$ARCHIVE_ROOT/||")
        echo "## Restored from: $relative_path" >> "$SESSION_FILE"
        echo "" >> "$SESSION_FILE"
        cat "$file" >> "$SESSION_FILE"
        echo "" >> "$SESSION_FILE"
    done
    
    echo -e "${GREEN}✅ SESSION_CONTINUITY.md replaced successfully${NC}"
    echo -e "${BLUE}📦 Original backed up to: $backup_path${NC}"
}

# Main execution
main() {
    # Check if archive exists
    if [ ! -d "$ARCHIVE_ROOT" ]; then
        echo -e "${RED}❌ Archive directory not found: $ARCHIVE_ROOT${NC}"
        echo "Run the archival tool first: python3 scripts/archive_session_continuity.py"
        exit 1
    fi
    
    # Parse arguments
    if [ $# -lt 1 ]; then
        usage
    fi
    
    local target_date="$1"
    local operation="${2:-display}"
    
    # Validate date format
    if [[ ! "$target_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        echo -e "${RED}❌ Invalid date format: $target_date${NC}"
        echo "Expected format: YYYY-MM-DD (e.g., 2025-06-16)"
        exit 1
    fi
    
    # Find archived files
    local files_result=$(find_archived_files "$target_date")
    if [ $? -ne 0 ]; then
        exit 1
    fi
    
    # Convert to array
    local files=($files_result)
    
    echo -e "${GREEN}📁 Found ${#files[@]} archived file(s) for $target_date:${NC}"
    for file in "${files[@]}"; do
        local relative_path=$(echo "$file" | sed "s|$ARCHIVE_ROOT/||")
        echo "  📄 $relative_path"
    done
    echo ""
    
    # Execute operation
    case "$operation" in
        "display"|"--display")
            display_archived_content "${files[@]}"
            ;;
        "--append")
            append_archived_content "$target_date" "${files[@]}"
            ;;
        "--replace")
            read -p "⚠️  This will replace the current SESSION_CONTINUITY.md file. Continue? (y/N): " confirm
            if [[ "$confirm" =~ ^[Yy]$ ]]; then
                replace_with_archived_content "$target_date" "${files[@]}"
            else
                echo "Operation cancelled."
                exit 0
            fi
            ;;
        *)
            echo -e "${RED}❌ Unknown operation: $operation${NC}"
            usage
            ;;
    esac
}

# Run main function
main "$@"