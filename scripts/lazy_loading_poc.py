#!/usr/bin/env python3
"""
Lazy Loading Proof of Concept for CLAUDE Startup Optimization
This demonstrates how to reduce startup overhead from ~1.5s to ~200ms
"""

import os
import time
import json
import hashlib
from pathlib import Path
from functools import lru_cache
from typing import Dict, List, Optional, Tuple

class LazyClaudeLoader:
    """Optimized loader that defers heavy operations until needed"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.start_time = time.time()
        
        # Minimal initialization
        self._core_loaded = False
        self._patterns_indexed = False
        self._learning_loaded = False
        self._discovery_cached = False
        
        # Caches
        self.pattern_index: Optional[Dict] = None
        self.loaded_patterns: Dict[str, str] = {}
        self.learning_metadata: Dict[str, Dict] = {}
        self.discovery_cache: Optional[Dict] = None
        
        # Only load critical identity rules on startup
        self._load_critical_only()
        
        self.startup_time = time.time() - self.start_time
        print(f"✅ Minimal startup completed in {self.startup_time*1000:.0f}ms")
    
    def _load_critical_only(self):
        """Load only user identity and safety rules - <50ms"""
        # Simulate loading just first 200 lines of CLAUDE.md
        claude_md = self.project_root / "CLAUDE.md"
        if claude_md.exists():
            with open(claude_md, 'r') as f:
                # Read only critical sections
                lines = []
                for i, line in enumerate(f):
                    if i < 200:  # First 200 lines contain identity & critical rules
                        lines.append(line)
                    else:
                        break
            print(f"📋 Loaded critical rules only (200 lines)")
        
        # Check for initialization triggers
        self.init_triggers = {
            "hi", "hello", "ready", "start", "setup", "boot", 
            "startup", "i'm christian", "this is christian"
        }
    
    def needs_full_init(self, user_input: str) -> bool:
        """Check if user input requires full initialization"""
        input_lower = user_input.lower()
        return any(trigger in input_lower for trigger in self.init_triggers)
    
    @lru_cache(maxsize=1)
    def load_full_claude_md(self):
        """Load complete CLAUDE.md when needed - cached after first load"""
        if self._core_loaded:
            return
        
        start = time.time()
        claude_md = self.project_root / "CLAUDE.md"
        if claude_md.exists():
            with open(claude_md, 'r') as f:
                self.full_content = f.read()
        self._core_loaded = True
        print(f"📄 Full CLAUDE.md loaded in {(time.time()-start)*1000:.0f}ms")
    
    def get_pattern_index(self) -> Dict:
        """Build lightweight pattern index without reading content"""
        if self._patterns_indexed:
            return self.pattern_index
        
        start = time.time()
        self.pattern_index = {}
        patterns_dir = self.project_root / "patterns"
        
        if patterns_dir.exists():
            for category in patterns_dir.iterdir():
                if category.is_dir() and not category.name.startswith('.'):
                    self.pattern_index[category.name] = []
                    for pattern_file in category.glob("*.md"):
                        # Just store metadata, not content
                        self.pattern_index[category.name].append({
                            'name': pattern_file.stem,
                            'path': str(pattern_file),
                            'size': pattern_file.stat().st_size
                        })
        
        self._patterns_indexed = True
        elapsed = (time.time() - start) * 1000
        print(f"🗂️  Pattern index built in {elapsed:.0f}ms ({sum(len(v) for v in self.pattern_index.values())} patterns)")
        return self.pattern_index
    
    def load_pattern(self, pattern_path: str) -> str:
        """Load individual pattern on demand with caching"""
        if pattern_path in self.loaded_patterns:
            return self.loaded_patterns[pattern_path]
        
        start = time.time()
        with open(pattern_path, 'r') as f:
            content = f.read()
        self.loaded_patterns[pattern_path] = content
        
        # Keep cache size limited (LRU behavior)
        if len(self.loaded_patterns) > 20:
            # Remove oldest entries
            oldest = list(self.loaded_patterns.keys())[:-20]
            for key in oldest:
                del self.loaded_patterns[key]
        
        print(f"📄 Pattern loaded in {(time.time()-start)*1000:.0f}ms: {Path(pattern_path).name}")
        return content
    
    def get_learning_metadata(self) -> Dict:
        """Load only metadata about learning files, not content"""
        if self._learning_loaded:
            return self.learning_metadata
        
        start = time.time()
        learning_files = [
            self.project_root / "memory" / "learning_archive.md",
            self.project_root / "memory" / "error_patterns.md",
            self.project_root / "memory" / "side_effects_log.md",
            Path.home() / ".claude" / "LEARNED_CORRECTIONS.md",
            Path.home() / ".claude" / "PYTHON_LEARNINGS.md",
        ]
        
        for file_path in learning_files:
            if file_path.exists():
                stat = file_path.stat()
                # Quick line count without loading full content
                with open(file_path, 'r') as f:
                    line_count = sum(1 for _ in f)
                
                self.learning_metadata[str(file_path)] = {
                    'exists': True,
                    'size': stat.st_size,
                    'lines': line_count,
                    'modified': stat.st_mtime
                }
            else:
                self.learning_metadata[str(file_path)] = {'exists': False}
        
        self._learning_loaded = True
        elapsed = (time.time() - start) * 1000
        print(f"📊 Learning metadata loaded in {elapsed:.0f}ms")
        return self.learning_metadata
    
    def get_cached_discovery(self) -> Optional[Dict]:
        """Use cached project discovery if available and fresh"""
        cache_file = self.project_root / ".claude_discovery_cache"
        cache_max_age = 3600  # 1 hour
        
        if cache_file.exists():
            stat = cache_file.stat()
            age = time.time() - stat.st_mtime
            
            if age < cache_max_age:
                with open(cache_file, 'r') as f:
                    self.discovery_cache = json.load(f)
                print(f"📦 Using cached discovery (age: {age/60:.0f} minutes)")
                return self.discovery_cache
        
        return None
    
    def run_minimal_discovery(self) -> Dict:
        """Run only essential discovery checks"""
        start = time.time()
        discovery = {
            'has_claude_md': (self.project_root / "CLAUDE.md").exists(),
            'project_type': self._detect_project_type(),
            'timestamp': time.time()
        }
        
        # Cache the results
        cache_file = self.project_root / ".claude_discovery_cache"
        with open(cache_file, 'w') as f:
            json.dump(discovery, f, indent=2)
        
        elapsed = (time.time() - start) * 1000
        print(f"🔍 Minimal discovery in {elapsed:.0f}ms")
        return discovery
    
    def _detect_project_type(self) -> str:
        """Quick project type detection"""
        if (self.project_root / "package.json").exists():
            return "nodejs"
        elif (self.project_root / "requirements.txt").exists():
            return "python"
        elif (self.project_root / "go.mod").exists():
            return "go"
        else:
            return "unknown"
    
    def should_load_patterns(self, query: str) -> bool:
        """Determine if patterns need to be loaded for this query"""
        pattern_keywords = ['pattern', 'similar', 'before', 'existing', 'reuse']
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in pattern_keywords)
    
    def should_load_learning(self, query: str) -> bool:
        """Determine if learning files need to be loaded"""
        learning_keywords = ['error', 'mistake', 'wrong', 'failed', 'learned']
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in learning_keywords)
    
    def process_query(self, query: str) -> Dict:
        """Main entry point - loads only what's needed for the query"""
        query_start = time.time()
        loaded_components = []
        
        # Check if full initialization needed
        if self.needs_full_init(query):
            self.load_full_claude_md()
            loaded_components.append("full_claude_md")
        
        # Check if patterns needed
        if self.should_load_patterns(query):
            self.get_pattern_index()
            loaded_components.append("pattern_index")
        
        # Check if learning needed
        if self.should_load_learning(query):
            self.get_learning_metadata()
            loaded_components.append("learning_metadata")
        
        # Use cached discovery or run minimal
        discovery = self.get_cached_discovery()
        if not discovery:
            discovery = self.run_minimal_discovery()
            loaded_components.append("discovery")
        
        query_time = (time.time() - query_start) * 1000
        
        return {
            'query_time_ms': query_time,
            'loaded_components': loaded_components,
            'total_time_ms': (time.time() - self.start_time) * 1000
        }


# Demonstration
if __name__ == "__main__":
    print("🚀 CLAUDE Lazy Loading Proof of Concept\n")
    
    # Test different query types
    test_queries = [
        "What's next?",  # Simple query - should be fast
        "Hi, I'm Christian",  # Init trigger - loads more
        "Find existing patterns for error handling",  # Pattern query
        "What went wrong with my last attempt?",  # Learning query
        "Build a new React component",  # Complex task
    ]
    
    for query in test_queries:
        print(f"\n--- Query: '{query}' ---")
        loader = LazyClaudeLoader()
        result = loader.process_query(query)
        print(f"⏱️  Query processed in {result['query_time_ms']:.0f}ms")
        print(f"📦 Loaded: {', '.join(result['loaded_components']) or 'minimal only'}")
        print(f"⏱️  Total time: {result['total_time_ms']:.0f}ms")
        
    print("\n✅ Lazy loading demonstration complete!")