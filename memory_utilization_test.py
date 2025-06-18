#!/usr/bin/env python3
"""
Memory Directory Utilization Test
Test whether the memory/ directory files are actually being read/written by scripts
"""

import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Set

class MemoryUtilizationTester:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.memory_dir = self.project_root / "memory"
        self.memory_files = [
            "learning_archive.md",
            "error_patterns.md", 
            "side_effects_log.md"
        ]
        
        self.results = {
            "memory_files_exist": {},
            "files_with_content": {},
            "scripts_referencing_memory": {},
            "actual_readers": [],
            "actual_writers": [],
            "utilization_score": 0
        }
    
    def test_memory_files_existence(self):
        """Test if memory files exist and have content"""
        print("=== Testing Memory File Existence ===")
        
        for filename in self.memory_files:
            file_path = self.memory_dir / filename
            exists = file_path.exists()
            self.results["memory_files_exist"][filename] = exists
            
            if exists:
                try:
                    content = file_path.read_text()
                    has_content = len(content.strip()) > 100  # More than just template
                    self.results["files_with_content"][filename] = has_content
                    print(f"✓ {filename}: exists, {len(content)} chars, content: {'yes' if has_content else 'no'}")
                except Exception as e:
                    print(f"✗ {filename}: exists but unreadable - {e}")
                    self.results["files_with_content"][filename] = False
            else:
                print(f"✗ {filename}: does not exist")
                self.results["files_with_content"][filename] = False
    
    def test_script_references(self):
        """Test which scripts reference memory files"""
        print("\n=== Testing Script References ===")
        
        # Find all script files
        script_extensions = [".py", ".sh", ".bash"]
        script_files = []
        
        for ext in script_extensions:
            script_files.extend(self.project_root.rglob(f"*{ext}"))
        
        print(f"Found {len(script_files)} script files")
        
        for memory_file in self.memory_files:
            referencing_scripts = []
            
            for script_file in script_files:
                try:
                    content = script_file.read_text(errors='ignore')
                    if memory_file in content:
                        referencing_scripts.append(str(script_file))
                except:
                    continue
            
            self.results["scripts_referencing_memory"][memory_file] = referencing_scripts
            print(f"{memory_file}: referenced in {len(referencing_scripts)} scripts")
            for script in referencing_scripts[:3]:  # Show first 3
                print(f"  - {Path(script).name}")
    
    def test_actual_file_operations(self):
        """Test for scripts that actually read/write memory files"""
        print("\n=== Testing Actual File Operations ===")
        
        # Search for actual file operations
        read_patterns = [
            r'open\s*\(\s*["\'].*memory.*["\']',
            r'read_text\s*\(\s*["\'].*memory.*["\']',
            r'with\s+open\s*\(\s*["\'].*memory.*["\']',
            r'cat\s+.*memory/',
            r'<\s+.*memory/'
        ]
        
        write_patterns = [
            r'write\s*\(\s*["\'].*memory.*["\']',
            r'write_text\s*\(\s*["\'].*memory.*["\']', 
            r'>\s+.*memory/',
            r'>>\s+.*memory/',
            r'echo.*>\s*.*memory/'
        ]
        
        script_files = list(self.project_root.rglob("*.py")) + list(self.project_root.rglob("*.sh"))
        
        readers = set()
        writers = set()
        
        for script_file in script_files:
            try:
                content = script_file.read_text(errors='ignore')
                
                # Check for read operations
                for pattern in read_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        readers.add(str(script_file))
                        break
                
                # Check for write operations  
                for pattern in write_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        writers.add(str(script_file))
                        break
                        
            except:
                continue
        
        self.results["actual_readers"] = list(readers)
        self.results["actual_writers"] = list(writers)
        
        print(f"Scripts that READ memory files: {len(readers)}")
        for reader in list(readers)[:5]:
            print(f"  - {Path(reader).name}")
            
        print(f"Scripts that WRITE memory files: {len(writers)}")  
        for writer in list(writers)[:5]:
            print(f"  - {Path(writer).name}")
    
    def test_memory_file_modifications(self):
        """Test when memory files were last modified"""
        print("\n=== Testing File Modification Times ===")
        
        for filename in self.memory_files:
            file_path = self.memory_dir / filename
            if file_path.exists():
                stat = file_path.stat()
                import datetime
                mod_time = datetime.datetime.fromtimestamp(stat.st_mtime)
                print(f"{filename}: last modified {mod_time}")
            else:
                print(f"{filename}: does not exist")
    
    def calculate_utilization_score(self):
        """Calculate overall utilization score"""
        print("\n=== Calculating Utilization Score ===")
        
        score = 0
        max_score = 100
        
        # File existence (20 points)
        existing_files = sum(1 for exists in self.results["memory_files_exist"].values() if exists)
        score += (existing_files / len(self.memory_files)) * 20
        
        # File content (20 points)
        content_files = sum(1 for has_content in self.results["files_with_content"].values() if has_content)
        score += (content_files / len(self.memory_files)) * 20
        
        # Script references (30 points)  
        total_references = sum(len(refs) for refs in self.results["scripts_referencing_memory"].values())
        score += min(total_references / 10, 1.0) * 30  # Cap at 10 references for full points
        
        # Actual readers (15 points)
        score += min(len(self.results["actual_readers"]) / 3, 1.0) * 15
        
        # Actual writers (15 points)
        score += min(len(self.results["actual_writers"]) / 3, 1.0) * 15
        
        self.results["utilization_score"] = score
        print(f"Utilization Score: {score:.1f}/{max_score}")
        
        if score < 30:
            print("❌ LOW UTILIZATION - Memory files are barely used")
        elif score < 60:
            print("⚠️ MODERATE UTILIZATION - Some usage but could improve")  
        else:
            print("✅ HIGH UTILIZATION - Memory files are actively used")
    
    def generate_report(self):
        """Generate detailed utilization report"""
        print("\n" + "="*60)
        print("MEMORY DIRECTORY UTILIZATION REPORT")
        print("="*60)
        
        # Summary
        existing = sum(1 for exists in self.results["memory_files_exist"].values() if exists)
        with_content = sum(1 for has_content in self.results["files_with_content"].values() if has_content)
        total_refs = sum(len(refs) for refs in self.results["scripts_referencing_memory"].values())
        
        print(f"Files Exist: {existing}/{len(self.memory_files)}")
        print(f"Files with Content: {with_content}/{len(self.memory_files)}")
        print(f"Total Script References: {total_refs}")
        print(f"Actual Readers: {len(self.results['actual_readers'])}")
        print(f"Actual Writers: {len(self.results['actual_writers'])}")
        print(f"Utilization Score: {self.results['utilization_score']:.1f}/100")
        
        # Detailed breakdown
        print(f"\nDETAILED BREAKDOWN:")
        for filename in self.memory_files:
            exists = self.results["memory_files_exist"][filename]
            has_content = self.results["files_with_content"][filename]
            refs = len(self.results["scripts_referencing_memory"].get(filename, []))
            
            status = "✓" if exists and has_content else "⚠️" if exists else "✗"
            print(f"{status} {filename}: exists={exists}, content={has_content}, refs={refs}")
        
        # Recommendations
        print(f"\nRECOMMENDATIONS:")
        if self.results["utilization_score"] < 30:
            print("- Memory files appear to be mostly unused")
            print("- Consider removing unused files or implementing actual usage")
            print("- Review scripts to see if memory persistence is actually needed")
        elif self.results["utilization_score"] < 60:
            print("- Some memory file usage but inconsistent")
            print("- Ensure all memory files are being updated by scripts")
            print("- Add write operations to capture learning data")
        else:
            print("- Good utilization of memory files")
            print("- Continue monitoring for effective usage patterns")
    
    def run_all_tests(self):
        """Run all utilization tests"""
        print("MEMORY DIRECTORY UTILIZATION TEST")
        print(f"Project Root: {self.project_root}")
        print(f"User: Christian")
        print()
        
        self.test_memory_files_existence()
        self.test_script_references()
        self.test_actual_file_operations()
        self.test_memory_file_modifications()
        self.calculate_utilization_score()
        self.generate_report()
        
        return self.results

def main():
    """Run the memory utilization test"""
    tester = MemoryUtilizationTester()
    results = tester.run_all_tests()
    
    # Save results
    import json
    results_file = Path("memory_utilization_test_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {results_file}")

if __name__ == "__main__":
    main()