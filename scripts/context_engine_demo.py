#!/usr/bin/env python3
"""
Context Engine Demo - Shows how to use the context engine for project-aware suggestions
"""

from context_engine import ContextEngine
import json

def demo_context_engine():
    """Demonstrate context engine capabilities."""
    print("=== Context Engine Demo ===\n")
    
    # Initialize the context engine
    engine = ContextEngine()
    
    # Demo 1: Startup context
    print("1. STARTUP CONTEXT")
    print("-" * 50)
    startup_suggestions = engine.get_suggestions("project startup and initialization")
    for i, suggestion in enumerate(startup_suggestions[:3], 1):
        print(f"{i}. {suggestion['title']}")
        print(f"   Confidence: {suggestion['confidence']:.2f}")
        print(f"   Description: {suggestion['description']}")
        print(f"   Action: {suggestion['action']}")
        print(f"   Estimated Time: {suggestion['estimated_time']}")
        print()
    
    # Demo 2: Development context
    print("2. DEVELOPMENT CONTEXT")
    print("-" * 50)
    dev_suggestions = engine.get_suggestions("implementing new features and code development")
    for i, suggestion in enumerate(dev_suggestions[:3], 1):
        print(f"{i}. {suggestion['title']}")
        print(f"   Confidence: {suggestion['confidence']:.2f}")
        print(f"   Description: {suggestion['description']}")
        print(f"   Action: {suggestion['action']}")
        print(f"   Estimated Time: {suggestion['estimated_time']}")
        print()
    
    # Demo 3: Project analysis
    print("3. PROJECT ANALYSIS")
    print("-" * 50)
    context = engine.analyze_current_context()
    project_state = context['project_state']
    
    print(f"Session Continuity: {'✓' if project_state['session_continuity_exists'] else '✗'}")
    print(f"Patterns Available: {project_state['patterns_count']}")
    print(f"Memory Files: {project_state['memory_files_count']}")
    print(f"Scripts Available: {project_state['scripts_count']}")
    print(f"Last Activity: {project_state['last_activity']}")
    print()
    
    # Demo 4: Historical insights
    print("4. HISTORICAL INSIGHTS")
    print("-" * 50)
    history = context['history_analysis']
    print(f"Total Sessions: {history['total_sessions']}")
    print(f"Cleanup Operations: {history['cleanup_operations']}")
    print(f"Performance Improvements: {len(history['performance_improvements'])}")
    print(f"Common Tasks: {dict(history['common_tasks'])}")
    print()
    
    # Demo 5: Pattern insights
    print("5. PATTERN INSIGHTS")
    print("-" * 50)
    patterns = context['pattern_analysis']
    print(f"Total Patterns: {patterns['total_patterns']}")
    print(f"Pattern Categories: {dict(patterns['pattern_categories'])}")
    print(f"Recent Patterns: {patterns['recent_patterns'][:3]}")
    print()
    
    # Demo 6: Context-aware suggestions for specific scenarios
    scenarios = [
        ("cleanup and optimization", "maintenance"),
        ("performance improvements", "optimization"),
        ("pattern creation", "development")
    ]
    
    print("6. SCENARIO-BASED SUGGESTIONS")
    print("-" * 50)
    for scenario, context_type in scenarios:
        print(f"\nScenario: {scenario}")
        suggestions = engine.get_suggestions(scenario)
        if suggestions:
            top_suggestion = suggestions[0]
            print(f"  → {top_suggestion['title']} (confidence: {top_suggestion['confidence']:.2f})")
            print(f"    {top_suggestion['description']}")
        else:
            print("  → No specific suggestions available")
    
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo_context_engine()