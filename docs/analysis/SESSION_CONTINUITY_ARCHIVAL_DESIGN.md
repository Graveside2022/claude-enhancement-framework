# SESSION_CONTINUITY.md Archival System Design

## Overview
A lightweight, efficient archival system that reduces boot overhead while maintaining full historical access when needed.

## Architecture

### 1. File Structure
```
memory/
├── SESSION_CONTINUITY.md          # Current active session (< 2KB)
├── archives/
│   ├── daily/
│   │   ├── 2025-06-17.md        # Today's archive (compressed)
│   │   ├── 2025-06-16.md        # Yesterday's archive
│   │   └── ...
│   ├── weekly/
│   │   ├── 2025-W25.md          # Week 25 archive
│   │   ├── 2025-W24.md          # Week 24 archive
│   │   └── ...
│   ├── monthly/
│   │   ├── 2025-06.md           # June archive
│   │   ├── 2025-05.md           # May archive
│   │   └── ...
│   └── index.json                # Archive metadata index
```

### 2. Active Session File (SESSION_CONTINUITY.md)
- **Size limit**: 2KB maximum
- **Content**: Only last 24 hours of activity
- **Structure**: Most recent entries first
- **Auto-archival**: Triggered when size > 2KB or age > 24 hours

### 3. Archive Strategy

#### Daily Archives (memory/archives/daily/)
- **Retention**: 7 days
- **Format**: Compressed markdown with timestamp headers
- **Naming**: YYYY-MM-DD.md
- **Content**: Full day's session data
- **Compression**: gzip compression after 24 hours

#### Weekly Archives (memory/archives/weekly/)
- **Retention**: 4 weeks
- **Format**: Aggregated daily archives
- **Naming**: YYYY-W##.md (ISO week number)
- **Content**: Summarized key events + full critical data
- **Compression**: Higher compression ratio

#### Monthly Archives (memory/archives/monthly/)
- **Retention**: 12 months
- **Format**: High-level summaries only
- **Naming**: YYYY-MM.md
- **Content**: Major milestones and critical learnings
- **Compression**: Maximum compression

### 4. Archive Index (archives/index.json)
```json
{
  "last_archive": "2025-06-17T14:30:00Z",
  "active_session_size": 1834,
  "archives": {
    "daily": {
      "2025-06-17": {
        "size": 15420,
        "compressed_size": 3204,
        "entries": 45,
        "key_events": ["boot_optimization", "archive_system_design"]
      }
    },
    "weekly": {
      "2025-W25": {
        "size": 89320,
        "compressed_size": 12450,
        "days_included": 7,
        "major_achievements": ["project_detection_fix", "learning_file_loading"]
      }
    }
  }
}
```

## Implementation Components

### 1. Archival Functions (to add to CLAUDE.md)

```bash
# Function: Archive old session data
archive_session_data() {
    local MEMORY_DIR="${PROJECT_ROOT:-$(pwd)}/memory"
    local ARCHIVE_DIR="$MEMORY_DIR/archives"
    local TODAY=$(date +%Y-%m-%d)
    local CURRENT_SIZE=$(wc -c < "$MEMORY_DIR/SESSION_CONTINUITY.md" 2>/dev/null || echo 0)
    
    # Skip if file is small and recent
    if [[ $CURRENT_SIZE -lt 2048 ]]; then
        return 0
    fi
    
    # Create archive structure
    mkdir -p "$ARCHIVE_DIR/daily" "$ARCHIVE_DIR/weekly" "$ARCHIVE_DIR/monthly"
    
    # Archive entries older than 24 hours
    awk -v cutoff="$(date -d '24 hours ago' +%Y-%m-%dT%H:%M:%S)" '
        BEGIN { archive = ""; current = "" }
        /^## .* - [0-9]{4}-[0-9]{2}-[0-9]{2}T/ {
            if (match($0, /[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}/)) {
                timestamp = substr($0, RSTART, RLENGTH)
                if (timestamp < cutoff) {
                    archive = archive $0 "\n"
                } else {
                    current = current $0 "\n"
                }
                mode = (timestamp < cutoff) ? "archive" : "current"
            }
        }
        !/^## .* - [0-9]{4}-[0-9]{2}-[0-9]{2}T/ {
            if (mode == "archive") {
                archive = archive $0 "\n"
            } else {
                current = current $0 "\n"
            }
        }
        END {
            print archive > "'$ARCHIVE_DIR'/daily/'$TODAY'.tmp"
            print current > "'$MEMORY_DIR'/SESSION_CONTINUITY.tmp"
        }
    ' "$MEMORY_DIR/SESSION_CONTINUITY.md"
    
    # Append to daily archive and update current
    if [[ -f "$ARCHIVE_DIR/daily/$TODAY.tmp" ]]; then
        cat "$ARCHIVE_DIR/daily/$TODAY.tmp" >> "$ARCHIVE_DIR/daily/$TODAY.md"
        rm "$ARCHIVE_DIR/daily/$TODAY.tmp"
    fi
    
    if [[ -f "$MEMORY_DIR/SESSION_CONTINUITY.tmp" ]]; then
        mv "$MEMORY_DIR/SESSION_CONTINUITY.tmp" "$MEMORY_DIR/SESSION_CONTINUITY.md"
    fi
    
    # Compress old daily archives
    find "$ARCHIVE_DIR/daily" -name "*.md" -mtime +1 -exec gzip {} \;
    
    # Update index
    update_archive_index
}

# Function: Retrieve archived data on-demand
retrieve_archive() {
    local QUERY="$1"
    local MEMORY_DIR="${PROJECT_ROOT:-$(pwd)}/memory"
    local ARCHIVE_DIR="$MEMORY_DIR/archives"
    
    echo "🔍 Searching archives for: $QUERY"
    
    # Search in daily archives first (most recent)
    for archive in $(ls -r "$ARCHIVE_DIR/daily/"*.{md,gz} 2>/dev/null); do
        if [[ $archive == *.gz ]]; then
            zgrep -l "$QUERY" "$archive" && echo "Found in: $archive"
        else
            grep -l "$QUERY" "$archive" && echo "Found in: $archive"
        fi
    done
    
    # Then weekly
    for archive in $(ls -r "$ARCHIVE_DIR/weekly/"*.{md,gz} 2>/dev/null); do
        if [[ $archive == *.gz ]]; then
            zgrep -l "$QUERY" "$archive" && echo "Found in: $archive"
        else
            grep -l "$QUERY" "$archive" && echo "Found in: $archive"
        fi
    done
}

# Function: Update archive index
update_archive_index() {
    local MEMORY_DIR="${PROJECT_ROOT:-$(pwd)}/memory"
    local ARCHIVE_DIR="$MEMORY_DIR/archives"
    local INDEX="$ARCHIVE_DIR/index.json"
    
    # Create index.json with archive metadata
    python3 -c "
import os
import json
import gzip
from datetime import datetime

archive_dir = '$ARCHIVE_DIR'
index_data = {
    'last_archive': datetime.now().isoformat() + 'Z',
    'active_session_size': os.path.getsize('$MEMORY_DIR/SESSION_CONTINUITY.md') if os.path.exists('$MEMORY_DIR/SESSION_CONTINUITY.md') else 0,
    'archives': {
        'daily': {},
        'weekly': {},
        'monthly': {}
    }
}

# Process daily archives
daily_dir = os.path.join(archive_dir, 'daily')
if os.path.exists(daily_dir):
    for file in os.listdir(daily_dir):
        if file.endswith('.md') or file.endswith('.md.gz'):
            date_key = file.replace('.md.gz', '').replace('.md', '')
            file_path = os.path.join(daily_dir, file)
            
            if file.endswith('.gz'):
                with gzip.open(file_path, 'rt') as f:
                    content = f.read()
                    size = len(content)
            else:
                size = os.path.getsize(file_path)
            
            index_data['archives']['daily'][date_key] = {
                'size': size,
                'compressed': file.endswith('.gz'),
                'last_modified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
            }

with open('$INDEX', 'w') as f:
    json.dump(index_data, f, indent=2)
"
}

# Function: Clean old archives
cleanup_old_archives() {
    local ARCHIVE_DIR="${PROJECT_ROOT:-$(pwd)}/memory/archives"
    
    echo "🧹 Cleaning old archives..."
    
    # Remove daily archives older than 7 days
    find "$ARCHIVE_DIR/daily" -name "*.md*" -mtime +7 -delete
    
    # Remove weekly archives older than 28 days
    find "$ARCHIVE_DIR/weekly" -name "*.md*" -mtime +28 -delete
    
    # Remove monthly archives older than 365 days
    find "$ARCHIVE_DIR/monthly" -name "*.md*" -mtime +365 -delete
    
    # Update index after cleanup
    update_archive_index
}

# Function: Create weekly rollup
create_weekly_rollup() {
    local ARCHIVE_DIR="${PROJECT_ROOT:-$(pwd)}/memory/archives"
    local WEEK=$(date +%Y-W%V)
    
    echo "📦 Creating weekly rollup for $WEEK..."
    
    # Aggregate daily archives from past week
    python3 -c "
import os
import gzip
from datetime import datetime, timedelta

archive_dir = '$ARCHIVE_DIR'
week = '$WEEK'
weekly_file = os.path.join(archive_dir, 'weekly', f'{week}.md')

# Find daily archives from past week
daily_dir = os.path.join(archive_dir, 'daily')
week_data = []

for i in range(7):
    date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
    
    # Check for both compressed and uncompressed
    for ext in ['.md', '.md.gz']:
        file_path = os.path.join(daily_dir, date + ext)
        if os.path.exists(file_path):
            if ext == '.md.gz':
                with gzip.open(file_path, 'rt') as f:
                    week_data.append(f'### {date}\\n{f.read()}')
            else:
                with open(file_path, 'r') as f:
                    week_data.append(f'### {date}\\n{f.read()}')
            break

# Write weekly rollup
os.makedirs(os.path.dirname(weekly_file), exist_ok=True)
with open(weekly_file, 'w') as f:
    f.write(f'# Weekly Archive: {week}\\n\\n')
    f.write('\\n\\n'.join(reversed(week_data)))
"
}
```

### 2. Boot Sequence Integration

```bash
# Modified boot check with archival
check_session_continuity() {
    local MEMORY_DIR="${PROJECT_ROOT:-$(pwd)}/memory"
    local SESSION_FILE="$MEMORY_DIR/SESSION_CONTINUITY.md"
    
    if [[ -f "$SESSION_FILE" ]]; then
        local LAST_UPDATE=$(stat -f %m "$SESSION_FILE" 2>/dev/null || stat -c %Y "$SESSION_FILE" 2>/dev/null || echo 0)
        local CURRENT_TIME=$(date +%s)
        local TIME_DIFF=$((CURRENT_TIME - LAST_UPDATE))
        
        # Archive if needed (runs in background)
        (archive_session_data &)
        
        # If session is recent, skip full initialization
        if [[ $TIME_DIFF -lt 7200 ]]; then  # 2 hours
            echo "✓ Recent session found ($(($TIME_DIFF / 60)) minutes old)"
            return 0
        fi
    fi
    
    return 1
}
```

### 3. On-Demand Archive Access

```bash
# Quick search in archives (for Claude to use when needed)
search_session_history() {
    local SEARCH_TERM="$1"
    local DAYS_BACK="${2:-7}"  # Default to last 7 days
    
    echo "🔍 Searching session history for: $SEARCH_TERM"
    
    # Search current session first
    grep -n "$SEARCH_TERM" "$(find_project_root)/memory/SESSION_CONTINUITY.md" 2>/dev/null && \
        echo "Found in current session"
    
    # Then search archives if needed
    if [[ "$DAYS_BACK" -gt 0 ]]; then
        retrieve_archive "$SEARCH_TERM"
    fi
}
```

## Benefits

1. **Reduced Boot Time**: SESSION_CONTINUITY.md stays under 2KB
2. **Full History**: Complete archives available on-demand
3. **Automatic Management**: No manual cleanup needed
4. **Efficient Storage**: Compression reduces disk usage by ~80%
5. **Fast Searches**: Index enables quick archive lookups
6. **Graceful Degradation**: System works even if archives fail

## Implementation Timeline

1. **Phase 1**: Basic archival functions (immediate)
   - Add archive_session_data() to CLAUDE.md
   - Integrate with boot sequence
   - Test with current 700-line file

2. **Phase 2**: Retrieval and search (next session)
   - Add retrieve_archive() function
   - Implement search_session_history()
   - Create archive index

3. **Phase 3**: Automated maintenance (following session)
   - Weekly rollups
   - Monthly summaries  
   - Old archive cleanup

## Testing Strategy

1. Test archival with current large SESSION_CONTINUITY.md
2. Verify boot time improvement
3. Test archive retrieval
4. Validate compression ratios
5. Test edge cases (missing dirs, permissions)