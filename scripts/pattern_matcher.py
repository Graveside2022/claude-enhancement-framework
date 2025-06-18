#!/usr/bin/env python3
"""
Pattern Matching Engine for CLAUDE Improvement System
Matches problem descriptions to relevant patterns with scoring and ranking.

Created for: Christian
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import Counter
import time

class PatternMatcher:
    """
    Intelligent pattern matching system that analyzes problem descriptions
    and recommends relevant patterns with confidence scoring.
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.patterns_dir = self.project_root / "patterns"
        self.pattern_index = {}
        self.pattern_metadata = {}
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'
        }
        
        # Load pattern index
        self._build_pattern_index()
    
    def _build_pattern_index(self):
        """Build searchable index of all patterns with metadata"""
        pattern_files = []
        
        # Scan all pattern directories
        for category in ['bug_fixes', 'generation', 'refactoring', 'architecture']:
            category_path = self.patterns_dir / category
            if category_path.exists():
                for pattern_file in category_path.glob("*.md"):
                    pattern_files.append((category, pattern_file))
        
        # Process each pattern file
        for category, pattern_file in pattern_files:
            pattern_name = pattern_file.stem
            pattern_key = f"{category}/{pattern_name}"
            
            # Extract metadata from pattern file
            metadata = self._extract_pattern_metadata(pattern_file, category)
            self.pattern_metadata[pattern_key] = metadata
            
            # Build searchable keywords
            keywords = self._extract_keywords(metadata)
            self.pattern_index[pattern_key] = keywords
    
    def _extract_pattern_metadata(self, pattern_file: Path, category: str) -> Dict:
        """Extract metadata from pattern markdown file"""
        try:
            content = pattern_file.read_text()
            
            # Extract title
            title_match = re.search(r'^#\s*(?:Pattern:\s*)?(.+)', content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else pattern_file.stem
            
            # Extract explicit metadata if present
            keywords_match = re.search(r'\*\*Keywords\*\*:\s*(.+)', content)
            explicit_keywords = keywords_match.group(1).split(', ') if keywords_match else []
            
            tags_match = re.search(r'\*\*Tags\*\*:\s*(.+)', content)
            explicit_tags = tags_match.group(1).split(', ') if tags_match else []
            
            complexity_match = re.search(r'\*\*Complexity\*\*:\s*(.+)', content)
            explicit_complexity = complexity_match.group(1).strip() if complexity_match else None
            
            use_cases_match = re.search(r'\*\*Use Cases\*\*:\s*(.+)', content)
            use_cases = use_cases_match.group(1).split(', ') if use_cases_match else []
            
            # Extract problem section
            problem_match = re.search(r'## Problem\s*\n(.*?)(?=\n##|\n---|\Z)', content, re.DOTALL)
            problem = problem_match.group(1).strip() if problem_match else ""
            
            # Extract solution section
            solution_match = re.search(r'## Solution\s*\n(.*?)(?=\n##|\n---|\Z)', content, re.DOTALL)
            solution = solution_match.group(1).strip() if solution_match else ""
            
            # Combine explicit and auto-generated tags
            auto_tags = self._generate_tags(title, problem, solution, category)
            all_tags = list(set(explicit_tags + auto_tags))
            
            # Combine keywords
            auto_keywords = self._extract_content_keywords(f"{title} {problem} {solution}")
            all_keywords = list(set(explicit_keywords + auto_keywords + use_cases))
            
            return {
                'title': title,
                'category': category,
                'problem': problem,
                'solution': solution,
                'tags': all_tags,
                'file_path': str(pattern_file),
                'complexity': explicit_complexity or self._assess_complexity(solution),
                'keywords': all_keywords,
                'use_cases': use_cases
            }
            
        except Exception as e:
            return {
                'title': pattern_file.stem,
                'category': category,
                'problem': '',
                'solution': '',
                'tags': [category],
                'file_path': str(pattern_file),
                'complexity': 'medium',
                'keywords': []
            }
    
    def _generate_tags(self, title: str, problem: str, solution: str, category: str) -> List[str]:
        """Auto-generate relevant tags from content"""
        text = f"{title} {problem} {solution}".lower()
        tags = [category]
        
        # Technical domain tags
        if any(word in text for word in ['boot', 'startup', 'initialization']):
            tags.append('boot')
        if any(word in text for word in ['performance', 'optimization', 'speed', 'faster']):
            tags.append('performance')
        if any(word in text for word in ['error', 'bug', 'fix', 'issue']):
            tags.append('debugging')
        if any(word in text for word in ['session', 'continuity', 'memory']):
            tags.append('session')
        if any(word in text for word in ['agent', 'parallel', 'configuration']):
            tags.append('agents')
        if any(word in text for word in ['backup', 'restore', 'archive']):
            tags.append('backup')
        if any(word in text for word in ['token', 'reduction', 'usage']):
            tags.append('tokens')
        if any(word in text for word in ['cache', 'caching', 'state']):
            tags.append('caching')
        
        return list(set(tags))
    
    def _assess_complexity(self, solution: str) -> str:
        """Assess pattern complexity based on solution content"""
        if not solution:
            return 'low'
        
        complexity_indicators = {
            'high': ['integration', 'architecture', 'multiple', 'complex', 'advanced'],
            'medium': ['configuration', 'optimization', 'workflow', 'system'],
            'low': ['simple', 'basic', 'quick', 'easy']
        }
        
        solution_lower = solution.lower()
        
        for level, indicators in complexity_indicators.items():
            if any(indicator in solution_lower for indicator in indicators):
                return level
        
        # Default based on length
        if len(solution) > 1000:
            return 'high'
        elif len(solution) > 300:
            return 'medium'
        else:
            return 'low'
    
    def _extract_content_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text content"""
        # Clean and tokenize
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        
        # Remove stop words and short words
        keywords = [word for word in words 
                   if word not in self.stop_words and len(word) > 2]
        
        # Get most common keywords
        word_counts = Counter(keywords)
        return [word for word, count in word_counts.most_common(10)]
    
    def _extract_keywords(self, metadata: Dict) -> List[str]:
        """Extract all searchable keywords from pattern metadata"""
        keywords = []
        
        # Add title keywords
        keywords.extend(self._extract_content_keywords(metadata['title']))
        
        # Add tags
        keywords.extend(metadata['tags'])
        
        # Add category
        keywords.append(metadata['category'])
        
        # Add content keywords
        keywords.extend(metadata['keywords'])
        
        return list(set(keywords))
    
    def match_patterns(self, problem_description: str, max_results: int = 5) -> List[Dict]:
        """
        Match problem description to relevant patterns with confidence scoring
        
        Args:
            problem_description: Description of the problem to solve
            max_results: Maximum number of pattern matches to return
            
        Returns:
            List of pattern matches with scores and metadata
        """
        if not problem_description.strip():
            return []
        
        # Extract keywords from problem description
        problem_keywords = self._extract_content_keywords(problem_description)
        problem_tags = self._generate_tags("", problem_description, "", "")
        
        search_terms = problem_keywords + problem_tags
        
        # Score each pattern
        pattern_scores = []
        
        for pattern_key, pattern_keywords in self.pattern_index.items():
            score = self._calculate_match_score(search_terms, pattern_keywords, pattern_key)
            
            if score > 0:
                metadata = self.pattern_metadata[pattern_key]
                pattern_scores.append({
                    'pattern_key': pattern_key,
                    'title': metadata['title'],
                    'category': metadata['category'],
                    'score': score,
                    'confidence': min(score * 10, 100),  # Convert to percentage
                    'complexity': metadata['complexity'],
                    'tags': metadata['tags'],
                    'file_path': metadata['file_path'],
                    'problem': metadata['problem'][:200] + "..." if len(metadata['problem']) > 200 else metadata['problem']
                })
        
        # Sort by score and return top matches
        pattern_scores.sort(key=lambda x: x['score'], reverse=True)
        return pattern_scores[:max_results]
    
    def _calculate_match_score(self, search_terms: List[str], pattern_keywords: List[str], pattern_key: str) -> float:
        """Calculate match score between search terms and pattern keywords"""
        if not search_terms or not pattern_keywords:
            return 0.0
        
        search_set = set(term.lower() for term in search_terms)
        pattern_set = set(keyword.lower() for keyword in pattern_keywords)
        
        # Calculate intersection ratio
        intersection = search_set.intersection(pattern_set)
        
        if not intersection:
            return 0.0
        
        # Base score from intersection ratio
        base_score = len(intersection) / len(search_set.union(pattern_set))
        
        # Boost score for category matches
        category = pattern_key.split('/')[0]
        if any(term in ['bug', 'error', 'fix'] for term in search_terms) and category == 'bug_fixes':
            base_score *= 1.5
        elif any(term in ['performance', 'optimization'] for term in search_terms) and category == 'refactoring':
            base_score *= 1.3
        elif any(term in ['generate', 'create', 'new'] for term in search_terms) and category == 'generation':
            base_score *= 1.3
        elif any(term in ['architecture', 'design', 'structure'] for term in search_terms) and category == 'architecture':
            base_score *= 1.3
        
        return base_score
    
    def get_pattern_details(self, pattern_key: str) -> Optional[Dict]:
        """Get complete details for a specific pattern"""
        if pattern_key not in self.pattern_metadata:
            return None
        
        return self.pattern_metadata[pattern_key]
    
    def get_statistics(self) -> Dict:
        """Get pattern system statistics"""
        total_patterns = len(self.pattern_metadata)
        
        categories = {}
        complexities = {}
        
        for metadata in self.pattern_metadata.values():
            category = metadata['category']
            complexity = metadata['complexity']
            
            categories[category] = categories.get(category, 0) + 1
            complexities[complexity] = complexities.get(complexity, 0) + 1
        
        return {
            'total_patterns': total_patterns,
            'categories': categories,
            'complexities': complexities,
            'index_size': len(self.pattern_index)
        }

def main():
    """Test the pattern matcher with sample problems"""
    matcher = PatternMatcher()
    
    print("🔍 Pattern Matching Engine Test")
    print("=" * 50)
    
    # Display statistics
    stats = matcher.get_statistics()
    print(f"📊 Loaded {stats['total_patterns']} patterns")
    print(f"📂 Categories: {dict(stats['categories'])}")
    print(f"🎯 Complexities: {dict(stats['complexities'])}")
    print()
    
    # Test with sample problems
    test_problems = [
        "I'm having boot performance issues with slow startup times",
        "Need to fix an error in the session continuity system",
        "Want to optimize token usage and reduce memory consumption",
        "Looking for a way to create automated backup systems",
        "Need help with agent configuration and parallel processing"
    ]
    
    for i, problem in enumerate(test_problems, 1):
        print(f"🔍 Test {i}: {problem}")
        print("-" * 40)
        
        start_time = time.time()
        matches = matcher.match_patterns(problem, max_results=3)
        end_time = time.time()
        
        if matches:
            for j, match in enumerate(matches, 1):
                print(f"  {j}. {match['title']} ({match['category']})")
                print(f"     Confidence: {match['confidence']:.1f}%")
                print(f"     Complexity: {match['complexity']}")
                print(f"     Tags: {', '.join(match['tags'])}")
                print()
        else:
            print("  No matching patterns found")
            print()
        
        print(f"  ⚡ Search time: {(end_time - start_time)*1000:.1f}ms")
        print()

if __name__ == "__main__":
    main()