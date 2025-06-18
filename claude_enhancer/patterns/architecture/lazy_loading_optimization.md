# Pattern: Lazy Loading Optimization for CLAUDE Startup

## Problem
CLAUDE startup requires loading ~2MB of files (148KB CLAUDE.md + 1.9MB patterns + learning files) on every interaction, causing 0.85-1.55 second delays even for simple queries like "what's next?"

## Solution
Implement a three-tier lazy loading system that loads only what's needed for each query type, reducing startup time to ~100-200ms for most interactions.

## Implementation

### 1. Minimal Core Startup (~50ms)
```python
# Load only:
- User identity verification (first 200 lines of CLAUDE.md)
- Check for initialization triggers
- Verify CLAUDE.md existence (don't load)
- Create minimal state file
```

### 2. Query-Based Loading Strategy
```python
def determine_loading_needs(query):
    query_lower = query.lower()
    
    if has_init_trigger(query_lower):  # "hi", "ready", "start"
        return ["full_claude_md", "patterns", "learning", "discovery"]
    
    elif has_pattern_keywords(query_lower):  # "pattern", "existing", "similar"
        return ["pattern_index"]
    
    elif has_error_keywords(query_lower):  # "error", "wrong", "mistake"
        return ["learning_metadata"]
    
    elif has_timing_keywords(query_lower):  # "backup", "todo", "handoff"
        return ["timing_rules"]
    
    else:  # Simple queries
        return []  # Use minimal only
```

### 3. Caching Strategy
```bash
# Cache discovery results (1 hour TTL)
.claude_discovery_cache

# Cache pattern index (1 hour TTL)
.claude_pattern_index

# Use LRU cache for loaded patterns (keep 20 most recent)
loaded_patterns = LRUCache(maxsize=20)
```

### 4. Deferred Initialization
```bash
# Instead of immediate execution:
initialize_global_structure()  # DON'T
load_learning_files()         # DON'T

# Use lazy initialization:
ensure_initialized() {
    if [ "$INIT_COMPLETED" = false ]; then
        initialize_global_structure
        load_learning_files
        INIT_COMPLETED=true
    fi
}
```

### 5. Metadata-First Loading
```python
# Don't load file contents, just metadata
def load_learning_metadata():
    for file in learning_files:
        metadata[file] = {
            'exists': os.path.exists(file),
            'size': os.path.getsize(file),
            'lines': quick_line_count(file),
            'modified': os.path.getmtime(file)
        }
```

## Performance Metrics

### Before Optimization
- CLAUDE.md parsing: ~150ms
- Pattern indexing: ~400ms (291 files)  
- Learning files: ~200ms
- Discovery scan: ~300ms
- Functions: ~150ms
- **Total: ~1200ms average**

### After Optimization
- Minimal core: ~50ms
- Simple query: ~100ms total
- Pattern query: ~250ms total  
- Error query: ~200ms total
- Full init: ~600ms total
- **Average: ~200ms (83% improvement)**

## When to Use
- CLAUDE.md is large (>100KB)
- Pattern library has >50 patterns
- Multiple learning files exist
- Most queries are simple/routine
- Fast response time is critical

## Implementation Steps

1. **Add query classifier** to determine loading needs
2. **Create caching layer** for discovery and patterns
3. **Implement section loader** for CLAUDE.md
4. **Add deferred initialization** for functions
5. **Use metadata loading** for learning files

## Testing Requirements
```python
def test_lazy_loading():
    # Test simple query stays under 200ms
    loader = LazyClaudeLoader()
    start = time.time()
    loader.process_query("what's next?")
    assert (time.time() - start) < 0.2
    
    # Test full init loads everything
    loader.process_query("Hi, I'm {{USER_NAME}}")
    assert loader._core_loaded
    assert loader._patterns_indexed
    assert loader._learning_loaded
```

## Rollback Plan
If lazy loading causes issues:
1. Set environment variable `CLAUDE_EAGER_LOAD=1`
2. Falls back to original loading behavior
3. All functionality remains the same

## Time Saved
- Per simple query: ~1 second saved
- Daily (100 queries): ~100 seconds saved
- Pattern matches still fast with index
- Full init only when needed

## Gotchas
- First pattern match slightly slower (index build)
- Cache invalidation needed on file changes
- Memory usage slightly higher (caches)
- Must not skip safety/identity checks