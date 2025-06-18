#!/bin/bash
# Auto-Archive SESSION_CONTINUITY.md Integration Script
# Can be called from CLAUDE.md boot sequence for automatic archival

set -e

PROJECT_ROOT="/Users/scarmatrix/Project/CLAUDE_improvement"
SESSION_FILE="$PROJECT_ROOT/SESSION_CONTINUITY.md"
ARCHIVAL_SCRIPT="$PROJECT_ROOT/scripts/archive_session_continuity.py"
TARGET_LINES=750

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if archival is needed
check_archival_needed() {
    if [ ! -f "$SESSION_FILE" ]; then
        echo -e "${YELLOW}⚠️ SESSION_CONTINUITY.md not found - no archival needed${NC}"
        return 1
    fi
    
    local current_lines=$(wc -l < "$SESSION_FILE" 2>/dev/null || echo "0")
    
    if [ "$current_lines" -le "$TARGET_LINES" ]; then
        echo -e "${GREEN}✅ SESSION_CONTINUITY.md is optimal ($current_lines lines ≤ $TARGET_LINES target)${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}📊 SESSION_CONTINUITY.md needs archival ($current_lines lines > $TARGET_LINES target)${NC}"
    return 0
}

# Function to perform archival
perform_archival() {
    echo -e "${BLUE}🗂️ Starting automatic archival...${NC}"
    
    if [ ! -f "$ARCHIVAL_SCRIPT" ]; then
        echo -e "${RED}❌ Archival script not found: $ARCHIVAL_SCRIPT${NC}"
        return 1
    fi
    
    # Run archival with timeout to prevent hanging
    if timeout 120 python3 "$ARCHIVAL_SCRIPT" 2>/dev/null; then
        local new_size=$(wc -l < "$SESSION_FILE" 2>/dev/null || echo "unknown")
        echo -e "${GREEN}✅ Archival completed - optimized to $new_size lines${NC}"
        return 0
    else
        echo -e "${RED}❌ Archival failed or timed out${NC}"
        return 1
    fi
}

# Function to show archive status
show_archive_status() {
    local current_lines=$(wc -l < "$SESSION_FILE" 2>/dev/null || echo "0")
    local archive_count=0
    
    if [ -d "$PROJECT_ROOT/logs/session_continuity" ]; then
        archive_count=$(find "$PROJECT_ROOT/logs/session_continuity" -name "*.md" -type f | grep -v "archive_index.md" | wc -l 2>/dev/null || echo "0")
    fi
    
    echo -e "${BLUE}📊 Archive Status:${NC}"
    echo -e "   Current file size: ${GREEN}$current_lines lines${NC}"
    echo -e "   Target size: ${GREEN}$TARGET_LINES lines${NC}"
    echo -e "   Archived sessions: ${GREEN}$archive_count files${NC}"
    
    if [ "$current_lines" -le "$TARGET_LINES" ]; then
        echo -e "   Status: ${GREEN}✅ Optimal${NC}"
    else
        echo -e "   Status: ${YELLOW}⚠️ Needs archival${NC}"
    fi
}

# Main execution
main() {
    local mode="${1:-auto}"
    
    case "$mode" in
        "check")
            show_archive_status
            check_archival_needed
            ;;
        "force")
            echo -e "${YELLOW}🔄 Forcing archival (as requested)...${NC}"
            perform_archival
            show_archive_status
            ;;
        "auto")
            if check_archival_needed; then
                perform_archival
            fi
            show_archive_status
            ;;
        "status")
            show_archive_status
            ;;
        *)
            echo "Usage: $0 [auto|check|force|status]"
            echo ""
            echo "Modes:"
            echo "  auto   - Archive only if needed (default)"
            echo "  check  - Check if archival is needed without doing it"
            echo "  force  - Force archival regardless of size"
            echo "  status - Show current archive status"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"