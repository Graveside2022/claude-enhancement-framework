#!/bin/bash
# SESSION_CONTINUITY Archive Summary Tool
# Usage: ./summarize_archive.sh [timeframe] [--format=json|markdown]

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
    echo "Usage: $0 [timeframe] [--format=json|markdown]"
    echo ""
    echo "Examples:"
    echo "  $0                           # Show all archive summary"
    echo "  $0 week                      # Show last week's archives"
    echo "  $0 month                     # Show last month's archives"
    echo "  $0 2025-06                   # Show specific month's archives"
    echo "  $0 --format=json             # Output in JSON format"
    echo ""
    echo "Timeframe options:"
    echo "  all     - All archived sessions (default)"
    echo "  week    - Last 7 days"
    echo "  month   - Last 30 days"
    echo "  YYYY-MM - Specific month (e.g., 2025-06)"
    echo ""
    exit 1
}

# Function to get file stats
get_file_stats() {
    local file="$1"
    local lines=$(wc -l < "$file" 2>/dev/null || echo "0")
    local size=$(stat -f%z "$file" 2>/dev/null || echo "0")
    local modified=$(stat -f%m "$file" 2>/dev/null || echo "0")
    
    echo "$lines $size $modified"
}

# Function to analyze archive content
analyze_archives() {
    local timeframe="$1"
    local current_date=$(date +%s)
    local cutoff_date=0
    
    # Calculate cutoff date based on timeframe
    case "$timeframe" in
        "week")
            cutoff_date=$((current_date - 7*24*3600))
            ;;
        "month")
            cutoff_date=$((current_date - 30*24*3600))
            ;;
        "all")
            cutoff_date=0
            ;;
        [0-9][0-9][0-9][0-9]-[0-9][0-9])
            # Specific month - no cutoff, filter by path
            cutoff_date=0
            ;;
        *)
            echo -e "${RED}❌ Invalid timeframe: $timeframe${NC}"
            usage
            ;;
    esac
    
    # Initialize counters
    local total_files=0
    local total_lines=0
    local total_size=0
    local session_files=0
    local integration_files=0
    local task_files=0
    local oldest_file=""
    local newest_file=""
    local oldest_timestamp=9999999999
    local newest_timestamp=0
    
    declare -A monthly_stats
    
    # Scan archive directory
    if [ ! -d "$ARCHIVE_ROOT" ]; then
        echo "No archives found"
        return 1
    fi
    
    # Find all archive files
    while IFS= read -r -d '' file; do
        # Skip index and search files
        if [[ "$file" == *"archive_index.md" ]] || [[ "$file" == *"quick_search.json" ]]; then
            continue
        fi
        
        # Filter by specific month if requested
        if [[ "$timeframe" =~ ^[0-9]{4}-[0-9]{2}$ ]]; then
            if [[ "$file" != *"$timeframe"* ]]; then
                continue
            fi
        fi
        
        # Get file stats
        local stats=($(get_file_stats "$file"))
        local file_lines=${stats[0]}
        local file_size=${stats[1]}
        local file_modified=${stats[2]}
        
        # Apply time filter
        if [ $cutoff_date -gt 0 ] && [ $file_modified -lt $cutoff_date ]; then
            continue
        fi
        
        # Update counters
        total_files=$((total_files + 1))
        total_lines=$((total_lines + file_lines))
        total_size=$((total_size + file_size))
        
        # Categorize files
        if [[ "$file" == *"session_"* ]]; then
            session_files=$((session_files + 1))
        elif [[ "$file" == *"integration_"* ]]; then
            integration_files=$((integration_files + 1))
        elif [[ "$file" == *"task_"* ]]; then
            task_files=$((task_files + 1))
        fi
        
        # Track oldest and newest
        if [ $file_modified -lt $oldest_timestamp ]; then
            oldest_timestamp=$file_modified
            oldest_file="$file"
        fi
        if [ $file_modified -gt $newest_timestamp ]; then
            newest_timestamp=$file_modified
            newest_file="$file"
        fi
        
        # Monthly stats
        local month_key=$(echo "$file" | grep -o '[0-9]\{4\}-[0-9]\{2\}' | head -1)
        if [ -n "$month_key" ]; then
            monthly_stats["$month_key"]=$((${monthly_stats["$month_key"]:-0} + 1))
        fi
        
    done < <(find "$ARCHIVE_ROOT" -name "*.md" -type f -print0)
    
    # Prepare results
    local human_size=$(numfmt --to=iec --suffix=B $total_size 2>/dev/null || echo "${total_size}B")
    local oldest_date=""
    local newest_date=""
    
    if [ $oldest_timestamp -ne 9999999999 ]; then
        oldest_date=$(date -r $oldest_timestamp '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo "unknown")
    fi
    if [ $newest_timestamp -ne 0 ]; then
        newest_date=$(date -r $newest_timestamp '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo "unknown")
    fi
    
    # Output results
    cat << EOF
{
    "timeframe": "$timeframe",
    "generated_at": "$(date -Iseconds)",
    "summary": {
        "total_files": $total_files,
        "total_lines": $total_lines,
        "total_size_bytes": $total_size,
        "total_size_human": "$human_size"
    },
    "file_types": {
        "session_summaries": $session_files,
        "integration_logs": $integration_files,
        "task_details": $task_files
    },
    "date_range": {
        "oldest_file": "$(basename "$oldest_file")",
        "oldest_date": "$oldest_date",
        "newest_file": "$(basename "$newest_file")",
        "newest_date": "$newest_date"
    },
    "monthly_distribution": {
EOF

    # Add monthly stats
    local first=true
    for month in $(printf '%s\n' "${!monthly_stats[@]}" | sort); do
        if [ "$first" = true ]; then
            first=false
        else
            echo ","
        fi
        echo -n "        \"$month\": ${monthly_stats[$month]}"
    done
    
    cat << EOF

    }
}
EOF
}

# Function to format output as markdown
format_markdown() {
    local json_data="$1"
    
    echo "# SESSION_CONTINUITY Archive Summary"
    echo ""
    echo "**Generated**: $(echo "$json_data" | jq -r '.generated_at')"
    echo "**Timeframe**: $(echo "$json_data" | jq -r '.timeframe')"
    echo ""
    
    echo "## Overview"
    echo ""
    local total_files=$(echo "$json_data" | jq -r '.summary.total_files')
    local total_lines=$(echo "$json_data" | jq -r '.summary.total_lines')
    local total_size=$(echo "$json_data" | jq -r '.summary.total_size_human')
    
    echo "- **Total Files**: $total_files"
    echo "- **Total Lines**: $total_lines"
    echo "- **Total Size**: $total_size"
    echo ""
    
    echo "## File Types"
    echo ""
    local session_files=$(echo "$json_data" | jq -r '.file_types.session_summaries')
    local integration_files=$(echo "$json_data" | jq -r '.file_types.integration_logs')
    local task_files=$(echo "$json_data" | jq -r '.file_types.task_details')
    
    echo "- **Session Summaries**: $session_files files"
    echo "- **Integration Logs**: $integration_files files"
    echo "- **Task Details**: $task_files files"
    echo ""
    
    echo "## Date Range"
    echo ""
    local oldest_file=$(echo "$json_data" | jq -r '.date_range.oldest_file')
    local oldest_date=$(echo "$json_data" | jq -r '.date_range.oldest_date')
    local newest_file=$(echo "$json_data" | jq -r '.date_range.newest_file')
    local newest_date=$(echo "$json_data" | jq -r '.date_range.newest_date')
    
    echo "- **Oldest Archive**: $oldest_file ($oldest_date)"
    echo "- **Newest Archive**: $newest_file ($newest_date)"
    echo ""
    
    echo "## Monthly Distribution"
    echo ""
    echo "$json_data" | jq -r '.monthly_distribution | to_entries[] | "- **\(.key)**: \(.value) files"'
    echo ""
    
    echo "## Quick Actions"
    echo ""
    echo "- **Search Archives**: \`./scripts/search_session_archive.sh \"keyword\"\`"
    echo "- **Restore Session**: \`./scripts/restore_session_context.sh YYYY-MM-DD\`"
    echo "- **Browse Archives**: \`ls logs/session_continuity/\`"
}

# Main execution
main() {
    local timeframe="all"
    local format="markdown"
    
    # Parse arguments
    for arg in "$@"; do
        case $arg in
            --format=*)
                format="${arg#*=}"
                ;;
            --help|-h)
                usage
                ;;
            *)
                if [[ "$arg" != --* ]]; then
                    timeframe="$arg"
                fi
                ;;
        esac
    done
    
    # Validate format
    if [[ "$format" != "json" && "$format" != "markdown" ]]; then
        echo -e "${RED}❌ Invalid format: $format${NC}"
        echo "Supported formats: json, markdown"
        exit 1
    fi
    
    # Check if archive exists
    if [ ! -d "$ARCHIVE_ROOT" ]; then
        echo -e "${RED}❌ Archive directory not found: $ARCHIVE_ROOT${NC}"
        echo "Run the archival tool first: python3 scripts/archive_session_continuity.py"
        exit 1
    fi
    
    # Analyze archives
    local json_result=$(analyze_archives "$timeframe")
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to analyze archives${NC}"
        exit 1
    fi
    
    # Output in requested format
    case "$format" in
        "json")
            echo "$json_result" | jq .
            ;;
        "markdown")
            format_markdown "$json_result"
            ;;
    esac
}

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}⚠️ jq not found. JSON parsing may be limited.${NC}"
    echo "Install jq for better formatting: brew install jq"
fi

# Run main function
main "$@"