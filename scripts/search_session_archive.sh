#!/bin/bash
# SESSION_CONTINUITY Archive Search Tool
# Usage: ./search_session_archive.sh "keyword" [date_range]

set -e

PROJECT_ROOT="/Users/scarmatrix/Project/CLAUDE_improvement"
ARCHIVE_ROOT="$PROJECT_ROOT/logs/session_continuity"
SEARCH_DB="$ARCHIVE_ROOT/quick_search.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print usage
usage() {
    echo "Usage: $0 \"keyword\" [date_range]"
    echo ""
    echo "Examples:"
    echo "  $0 \"parallel agents\"              # Search for 'parallel agents' in all archives"
    echo "  $0 \"optimization\" 2025-06        # Search in June 2025 archives"
    echo "  $0 \"task completion\" 2025-06-16  # Search in specific date"
    echo ""
    echo "Date range formats:"
    echo "  YYYY-MM     (e.g., 2025-06)"
    echo "  YYYY-MM-DD  (e.g., 2025-06-16)"
    echo ""
    exit 1
}

# Check if archive exists
if [ ! -d "$ARCHIVE_ROOT" ]; then
    echo -e "${RED}❌ Archive directory not found: $ARCHIVE_ROOT${NC}"
    echo "Run the archival tool first: python3 scripts/archive_session_continuity.py"
    exit 1
fi

# Check arguments
if [ $# -lt 1 ]; then
    usage
fi

KEYWORD="$1"
DATE_RANGE="${2:-}"

echo -e "${BLUE}🔍 Searching SESSION_CONTINUITY archives...${NC}"
echo -e "Keyword: ${GREEN}$KEYWORD${NC}"
[ -n "$DATE_RANGE" ] && echo -e "Date range: ${GREEN}$DATE_RANGE${NC}"
echo ""

# Initialize results
RESULTS_FOUND=0
TEMP_RESULTS=$(mktemp)

# Function to search in a file and format results
search_file() {
    local file="$1"
    local relative_path=$(echo "$file" | sed "s|$ARCHIVE_ROOT/||")
    
    # Use ripgrep if available, otherwise grep
    if command -v rg &> /dev/null; then
        SEARCH_RESULTS=$(rg -i -n -C 2 "$KEYWORD" "$file" 2>/dev/null || true)
    else
        SEARCH_RESULTS=$(grep -i -n -C 2 "$KEYWORD" "$file" 2>/dev/null || true)
    fi
    
    if [ -n "$SEARCH_RESULTS" ]; then
        echo -e "${YELLOW}📄 $relative_path${NC}" >> "$TEMP_RESULTS"
        echo "$SEARCH_RESULTS" | sed 's/^/  /' >> "$TEMP_RESULTS"
        echo "" >> "$TEMP_RESULTS"
        return 0
    fi
    return 1
}

# Search in archive files
if [ -n "$DATE_RANGE" ]; then
    # Search in specific date range
    if [[ "$DATE_RANGE" =~ ^[0-9]{4}-[0-9]{2}$ ]]; then
        # Search in specific month
        SEARCH_DIR="$ARCHIVE_ROOT/$DATE_RANGE"
    elif [[ "$DATE_RANGE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        # Search in specific date files
        YEAR_MONTH=$(echo "$DATE_RANGE" | cut -d'-' -f1,2)
        SEARCH_DIR="$ARCHIVE_ROOT/$YEAR_MONTH"
        # Filter files by date
        DATE_FILTER="$DATE_RANGE"
    else
        echo -e "${RED}❌ Invalid date format: $DATE_RANGE${NC}"
        usage
    fi
    
    if [ ! -d "$SEARCH_DIR" ]; then
        echo -e "${RED}❌ No archives found for date range: $DATE_RANGE${NC}"
        exit 1
    fi
    
    echo -e "Searching in: ${BLUE}$SEARCH_DIR${NC}"
    
    # Search files in the directory
    find "$SEARCH_DIR" -name "*.md" -type f | while read -r file; do
        # Apply date filter if specified
        if [ -n "$DATE_FILTER" ]; then
            if [[ "$file" != *"$DATE_FILTER"* ]]; then
                continue
            fi
        fi
        
        if search_file "$file"; then
            RESULTS_FOUND=$((RESULTS_FOUND + 1))
        fi
    done
else
    # Search in all archives
    echo -e "Searching in: ${BLUE}All archives${NC}"
    
    find "$ARCHIVE_ROOT" -name "*.md" -type f | while read -r file; do
        # Skip the index file
        if [[ "$file" == *"archive_index.md" ]]; then
            continue
        fi
        
        if search_file "$file"; then
            RESULTS_FOUND=$((RESULTS_FOUND + 1))
        fi
    done
fi

# Display results
if [ -s "$TEMP_RESULTS" ]; then
    echo -e "${GREEN}✅ Search Results:${NC}"
    echo ""
    cat "$TEMP_RESULTS"
    
    # Count number of files with matches
    FILE_COUNT=$(grep -c "📄" "$TEMP_RESULTS" 2>/dev/null || echo "0")
    echo -e "${GREEN}📊 Found matches in $FILE_COUNT file(s)${NC}"
else
    echo -e "${YELLOW}⚠️ No matches found for: $KEYWORD${NC}"
    
    if [ -n "$DATE_RANGE" ]; then
        echo "Try searching without date range or check available dates:"
        echo "  ls $ARCHIVE_ROOT/"
    fi
fi

# Cleanup
rm -f "$TEMP_RESULTS"

# Show quick navigation tips
echo ""
echo -e "${BLUE}💡 Quick Tips:${NC}"
echo "  View full file:    cat logs/session_continuity/YYYY-MM/filename.md"
echo "  Restore context:   ./scripts/restore_session_context.sh YYYY-MM-DD"
echo "  Browse archive:    ls logs/session_continuity/"