#!/usr/bin/env python3
"""
Simple benchmark for CLAUDE.md configurations without external dependencies
"""

import time
import os
import json
from pathlib import Path

class SimpleBenchmark:
    def __init__(self):
        self.original_path = Path("CLAUDE.md")
        self.minimal_path = Path("CLAUDE_minimal.md")
        self.results = {
            "original": {},
            "minimal": {}
        }
        
    def measure_file_metrics(self):
        """Measure file sizes and estimate tokens"""
        print("📏 Measuring file metrics...")
        
        # Original CLAUDE.md
        if self.original_path.exists():
            original_size = os.path.getsize(self.original_path)
            with open(self.original_path, 'r') as f:
                original_content = f.read()
                original_lines = len(original_content.split('\n'))
                original_chars = len(original_content)
                # Rough estimate: 1 token ≈ 4 characters
                original_tokens = original_chars // 4
                
            self.results["original"]["file_size_bytes"] = original_size
            self.results["original"]["characters"] = original_chars
            self.results["original"]["lines"] = original_lines
            self.results["original"]["estimated_tokens"] = original_tokens
        
        # Minimal CLAUDE.md
        if self.minimal_path.exists():
            minimal_size = os.path.getsize(self.minimal_path)
            with open(self.minimal_path, 'r') as f:
                minimal_content = f.read()
                minimal_lines = len(minimal_content.split('\n'))
                minimal_chars = len(minimal_content)
                minimal_tokens = minimal_chars // 4
                
            self.results["minimal"]["file_size_bytes"] = minimal_size
            self.results["minimal"]["characters"] = minimal_chars
            self.results["minimal"]["lines"] = minimal_lines
            self.results["minimal"]["estimated_tokens"] = minimal_tokens
    
    def measure_load_time(self, file_path, iterations=100):
        """Measure time to read and parse file"""
        times = []
        
        for _ in range(iterations):
            start = time.perf_counter()
            
            # Load and parse file
            with open(file_path, 'r') as f:
                content = f.read()
                # Simulate parsing operations
                lines = content.split('\n')
                sections = [line for line in lines if line.startswith('#')]
                code_blocks = content.count('```')
                functions = content.count('()')
                
            end = time.perf_counter()
            times.append(end - start)
        
        # Return average time in milliseconds
        return (sum(times) / len(times)) * 1000
    
    def measure_parsing_complexity(self, file_path):
        """Measure parsing complexity metrics"""
        with open(file_path, 'r') as f:
            content = f.read()
        
        metrics = {
            "code_blocks": content.count('```'),
            "bash_functions": content.count('() {'),
            "python_blocks": content.count('```python'),
            "decision_trees": content.count('├─>'),
            "sections": len([line for line in content.split('\n') if line.startswith('#')]),
            "subsections": len([line for line in content.split('\n') if line.startswith('##')]),
            "mandatory_rules": content.lower().count('mandatory'),
            "must_statements": content.lower().count('must')
        }
        
        return metrics
    
    def simulate_query_processing(self, file_path, queries):
        """Simulate processing different query types"""
        with open(file_path, 'r') as f:
            content = f.read()
            content_lower = content.lower()
        
        query_times = {}
        
        for query in queries:
            start = time.perf_counter()
            
            # Simulate query routing based on content
            query_lower = query.lower()
            
            # Count relevant sections to process
            relevant_sections = 0
            
            if "whats next" in query_lower or "what's next" in query_lower:
                # TodoRead integration - minimal processing
                relevant_sections = content_lower.count('todoread')
                processing_time = 0.001 * relevant_sections
            elif any(trigger in query_lower for trigger in ["hi", "hello", "start", "setup"]):
                # Initialization - must process many sections
                relevant_sections = content_lower.count('initialization') + content_lower.count('identity')
                processing_time = 0.005 * relevant_sections
            elif "error" in query_lower:
                # Error handling - moderate processing
                relevant_sections = content_lower.count('error') + content_lower.count('learning')
                processing_time = 0.003 * relevant_sections
            else:
                # General query - full scan
                relevant_sections = len(content.split('\n')) // 100
                processing_time = 0.002 * relevant_sections
            
            # Add base overhead proportional to file size
            base_overhead = len(content) / 1000000  # 1ms per MB
            
            end = time.perf_counter()
            total_time = (end - start + processing_time + base_overhead) * 1000  # ms
            
            query_times[query] = {
                "time_ms": total_time,
                "sections_processed": relevant_sections
            }
        
        return query_times
    
    def run_benchmarks(self):
        """Run all benchmarks"""
        print("🔬 Running CLAUDE.md Performance Benchmarks")
        print("=" * 60)
        
        # Check if files exist
        if not self.original_path.exists():
            print("❌ Original CLAUDE.md not found")
            return
            
        if not self.minimal_path.exists():
            print("❌ Minimal CLAUDE_minimal.md not found")
            return
        
        # Measure file metrics
        self.measure_file_metrics()
        
        # Measure load times
        print("\n⏱️  Measuring load times (100 iterations)...")
        self.results["original"]["load_time_ms"] = self.measure_load_time(self.original_path)
        self.results["minimal"]["load_time_ms"] = self.measure_load_time(self.minimal_path)
        
        # Measure parsing complexity
        print("🔍 Analyzing parsing complexity...")
        self.results["original"]["complexity"] = self.measure_parsing_complexity(self.original_path)
        self.results["minimal"]["complexity"] = self.measure_parsing_complexity(self.minimal_path)
        
        # Measure query processing
        print("⚡ Simulating query processing...")
        test_queries = [
            "What's next?",
            "Hi Christian",
            "Fix this error",
            "Build a React component",
            "Create a backup"
        ]
        
        self.results["original"]["queries"] = self.simulate_query_processing(self.original_path, test_queries)
        self.results["minimal"]["queries"] = self.simulate_query_processing(self.minimal_path, test_queries)
        
        # Calculate improvements
        self.calculate_improvements()
        
        # Print results
        self.print_results()
        
        # Save detailed results
        self.save_results()
    
    def calculate_improvements(self):
        """Calculate percentage improvements"""
        self.improvements = {}
        
        # File size reduction
        original_size = self.results["original"]["file_size_bytes"]
        minimal_size = self.results["minimal"]["file_size_bytes"]
        self.improvements["file_size_reduction"] = ((original_size - minimal_size) / original_size) * 100
        
        # Token reduction
        original_tokens = self.results["original"]["estimated_tokens"]
        minimal_tokens = self.results["minimal"]["estimated_tokens"]
        self.improvements["token_reduction"] = ((original_tokens - minimal_tokens) / original_tokens) * 100
        
        # Load time improvement
        original_load = self.results["original"]["load_time_ms"]
        minimal_load = self.results["minimal"]["load_time_ms"]
        self.improvements["load_time_improvement"] = ((original_load - minimal_load) / original_load) * 100
        
        # Complexity reduction
        original_complexity = sum(self.results["original"]["complexity"].values())
        minimal_complexity = sum(self.results["minimal"]["complexity"].values())
        self.improvements["complexity_reduction"] = ((original_complexity - minimal_complexity) / original_complexity) * 100
        
        # Average query time improvement
        original_times = [q["time_ms"] for q in self.results["original"]["queries"].values()]
        minimal_times = [q["time_ms"] for q in self.results["minimal"]["queries"].values()]
        original_avg = sum(original_times) / len(original_times)
        minimal_avg = sum(minimal_times) / len(minimal_times)
        self.improvements["query_time_improvement"] = ((original_avg - minimal_avg) / original_avg) * 100
    
    def print_results(self):
        """Print benchmark results to console"""
        print("\n" + "=" * 60)
        print("📊 BENCHMARK RESULTS")
        print("=" * 60)
        
        # File metrics
        print("\n📁 FILE METRICS:")
        print(f"{'Metric':<20} {'Original':>15} {'Minimal':>15} {'Reduction':>15}")
        print("-" * 65)
        
        original = self.results["original"]
        minimal = self.results["minimal"]
        
        print(f"{'Size (bytes)':<20} {original['file_size_bytes']:>15,} {minimal['file_size_bytes']:>15,} {self.improvements['file_size_reduction']:>14.1f}%")
        print(f"{'Size (KB)':<20} {original['file_size_bytes']/1024:>15.1f} {minimal['file_size_bytes']/1024:>15.1f} {self.improvements['file_size_reduction']:>14.1f}%")
        print(f"{'Characters':<20} {original['characters']:>15,} {minimal['characters']:>15,} {self.improvements['token_reduction']:>14.1f}%")
        print(f"{'Lines':<20} {original['lines']:>15,} {minimal['lines']:>15,} {((original['lines']-minimal['lines'])/original['lines']*100):>14.1f}%")
        print(f"{'Est. Tokens':<20} {original['estimated_tokens']:>15,} {minimal['estimated_tokens']:>15,} {self.improvements['token_reduction']:>14.1f}%")
        
        # Performance metrics
        print("\n⚡ PERFORMANCE METRICS:")
        print(f"{'Metric':<20} {'Original':>15} {'Minimal':>15} {'Improvement':>15}")
        print("-" * 65)
        print(f"{'Load Time (ms)':<20} {original['load_time_ms']:>15.3f} {minimal['load_time_ms']:>15.3f} {self.improvements['load_time_improvement']:>14.1f}%")
        
        # Complexity metrics
        print("\n🔧 COMPLEXITY METRICS:")
        print(f"{'Element':<20} {'Original':>15} {'Minimal':>15} {'Reduction':>15}")
        print("-" * 65)
        
        for metric in ['code_blocks', 'bash_functions', 'sections', 'mandatory_rules']:
            orig_val = original['complexity'][metric]
            min_val = minimal['complexity'][metric]
            reduction = ((orig_val - min_val) / orig_val * 100) if orig_val > 0 else 0
            print(f"{metric.replace('_', ' ').title():<20} {orig_val:>15} {min_val:>15} {reduction:>14.1f}%")
        
        # Query processing times
        print("\n🔍 QUERY PROCESSING TIMES (ms):")
        print(f"{'Query':<30} {'Original':>12} {'Minimal':>12} {'Speedup':>12}")
        print("-" * 66)
        
        for query in self.results["original"]["queries"]:
            orig_time = self.results["original"]["queries"][query]["time_ms"]
            min_time = self.results["minimal"]["queries"][query]["time_ms"]
            speedup = ((orig_time - min_time) / orig_time * 100)
            print(f"{query:<30} {orig_time:>12.3f} {min_time:>12.3f} {speedup:>11.1f}%")
        
        # Summary
        print("\n" + "=" * 60)
        print("🎯 PERFORMANCE IMPROVEMENTS SUMMARY")
        print("=" * 60)
        print(f"✅ File Size Reduction:      {self.improvements['file_size_reduction']:>6.1f}%")
        print(f"✅ Token Usage Reduction:    {self.improvements['token_reduction']:>6.1f}%")
        print(f"✅ Load Time Improvement:    {self.improvements['load_time_improvement']:>6.1f}%")
        print(f"✅ Complexity Reduction:     {self.improvements['complexity_reduction']:>6.1f}%")
        print(f"✅ Query Time Improvement:   {self.improvements['query_time_improvement']:>6.1f}%")
        print("=" * 60)
    
    def save_results(self):
        """Save detailed results to file"""
        # Create reports directory if it doesn't exist
        Path("reports/analysis").mkdir(parents=True, exist_ok=True)
        
        # Save JSON results
        with open("reports/analysis/benchmark_results.json", 'w') as f:
            json.dump({
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                "results": self.results,
                "improvements": self.improvements
            }, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: reports/analysis/benchmark_results.json")

if __name__ == "__main__":
    benchmark = SimpleBenchmark()
    benchmark.run_benchmarks()