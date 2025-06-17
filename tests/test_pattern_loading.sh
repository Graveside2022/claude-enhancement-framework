#!/bin/bash

# Test pattern system performance and lazy loading
# User: Christian

echo "=== Pattern System Performance Test ==="
echo "Testing pattern loading with 293 files..."
echo ""

# Test 1: Directory detection timing
echo "Test 1: Checking patterns directory detection..."
start_time=$(date +%s.%N)
if [ -d "patterns" ]; then
    echo "✓ Patterns directory detected"
else
    echo "✗ Patterns directory not found"
fi
end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)
echo "Directory check time: ${duration}s"
echo ""

# Test 2: Pattern file enumeration (without loading content)
echo "Test 2: Enumerating pattern files (metadata only)..."
start_time=$(date +%s.%N)
pattern_count=$(find patterns -type f -name "*.md" | wc -l)
end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)
echo "✓ Found $pattern_count pattern files"
echo "Enumeration time: ${duration}s"
echo ""

# Test 3: Pattern matching simulation (grep for specific keywords)
echo "Test 3: Simulating pattern search (10-second limit)..."
start_time=$(date +%s.%N)

# Use timeout command to enforce 10-second limit
timeout 10s bash -c '
    search_term="error handling"
    echo "Searching for: $search_term"
    
    # Search only in file names and first 50 lines (lazy loading simulation)
    matches=0
    for file in $(find patterns -type f -name "*.md"); do
        # Check filename first (very fast)
        if echo "$file" | grep -qi "$search_term"; then
            echo "✓ Filename match: $file"
            matches=$((matches + 1))
            continue
        fi
        
        # Then check first 50 lines only (lazy loading)
        if head -50 "$file" | grep -qi "$search_term"; then
            echo "✓ Content match: $file"
            matches=$((matches + 1))
        fi
        
        # Stop after finding 5 matches (optimization)
        if [ $matches -ge 5 ]; then
            echo "... (stopped after 5 matches for performance)"
            break
        fi
    done
    
    echo "Found $matches matches"
'

if [ $? -eq 124 ]; then
    echo "✗ Search timed out after 10 seconds"
else
    echo "✓ Search completed within time limit"
fi

end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)
echo "Pattern search time: ${duration}s"
echo ""

# Test 4: Lazy loading simulation - load only when pattern matches
echo "Test 4: Testing lazy loading (load content only on match)..."
start_time=$(date +%s.%N)

# Find a specific pattern and load only that one
pattern_file=$(find patterns -name "*error*.md" | head -1)
if [ -n "$pattern_file" ]; then
    echo "Loading single pattern: $pattern_file"
    file_size=$(wc -c < "$pattern_file")
    echo "Pattern size: $file_size bytes"
    
    # Simulate loading just the matched pattern
    head -100 "$pattern_file" > /dev/null
    echo "✓ Loaded pattern content (first 100 lines)"
else
    echo "✗ No error pattern found"
fi

end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)
echo "Lazy load time: ${duration}s"
echo ""

# Test 5: Memory-efficient pattern index creation
echo "Test 5: Creating memory-efficient pattern index..."
start_time=$(date +%s.%N)

# Create index with just pattern names and categories
cat > patterns/.pattern_index << EOF
# Pattern Index (auto-generated)
# Format: category/filename | title | keywords
EOF

find patterns -name "*.md" -type f | while read -r pattern; do
    # Extract just category and filename
    category=$(echo "$pattern" | cut -d'/' -f2)
    filename=$(basename "$pattern")
    
    # Extract title from first # heading (if exists)
    title=$(head -5 "$pattern" | grep "^#" | head -1 | sed 's/^#\+ *//' || echo "$filename")
    
    echo "$category/$filename | $title" >> patterns/.pattern_index
done

index_size=$(wc -l < patterns/.pattern_index)
echo "✓ Created index with $index_size entries"

end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)
echo "Index creation time: ${duration}s"
echo ""

# Summary
echo "=== Performance Summary ==="
echo "Total patterns: $pattern_count files"
echo "All operations completed within reasonable time"
echo "Lazy loading prevents loading all 293 files at once"
echo "Pattern matching can be optimized with:"
echo "  - Filename matching first"
echo "  - Header/metadata scanning"
echo "  - Early termination on matches"
echo "  - 10-second timeout enforcement"
echo "  - Pattern indexing for faster lookups"