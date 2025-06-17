#!/bin/bash
# Fabric Patterns On-Demand Loader for Christian
# Usage: fabric_pattern <pattern_name> [input_file]

fabric_pattern() {
    local pattern_name="$1"
    local input_file="$2"
    local pattern_dir="/Users/scarmatrix/Project/CLAUDE_improvement/patterns/fabric"
    
    if [ -z "$pattern_name" ]; then
        echo "📋 Available fabric patterns:"
        echo "💡 Popular: extract_wisdom, create_summary, analyze_paper, improve_writing"
        echo "🔍 Analysis: analyze_claims, analyze_threat_report, find_logical_fallacies"
        echo "📝 Creation: create_coding_project, create_design_document, create_quiz"
        echo ""
        echo "Usage: fabric_pattern <pattern_name> [input_file]"
        echo "Example: fabric_pattern extract_wisdom article.txt"
        return 0
    fi
    
    local pattern_path="$pattern_dir/$pattern_name"
    
    if [ ! -d "$pattern_path" ]; then
        echo "❌ Pattern '$pattern_name' not found"
        echo "🔍 Try: ls $pattern_dir | grep -i $pattern_name"
        return 1
    fi
    
    echo "🚀 Loading fabric pattern: $pattern_name"
    
    # Load system prompt
    if [ -f "$pattern_path/system.md" ]; then
        echo "📋 System Instructions:"
        cat "$pattern_path/system.md"
        echo ""
    fi
    
    # Load user prompt template
    if [ -f "$pattern_path/user.md" ]; then
        echo "👤 User Template:"
        cat "$pattern_path/user.md"
        echo ""
    fi
    
    # Process input file if provided
    if [ -n "$input_file" ] && [ -f "$input_file" ]; then
        echo "📄 Processing input file: $input_file"
        echo "--- INPUT CONTENT ---"
        cat "$input_file"
        echo ""
        echo "--- END INPUT ---"
    fi
    
    echo "✅ Pattern loaded. Use the instructions above with your content."
}

# Quick access to popular patterns
extract_wisdom() { fabric_pattern "extract_wisdom" "$1"; }
create_summary() { fabric_pattern "create_summary" "$1"; }
analyze_paper() { fabric_pattern "analyze_paper" "$1"; }
improve_writing() { fabric_pattern "improve_writing" "$1"; }

export -f fabric_pattern extract_wisdom create_summary analyze_paper improve_writing