#!/bin/bash
# Large Prompt Handler for Christian
# Manages prompts that exceed MCP token limits

handle_large_prompt() {
    local prompt_text="$1"
    local continuation_id="$2"
    local temp_dir="/tmp/claude_prompts"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    
    mkdir -p "$temp_dir"
    
    if [ -z "$prompt_text" ]; then
        echo "📝 Usage: handle_large_prompt \"your prompt text\" [continuation_id]"
        echo "💡 This saves large prompts to files for MCP tools"
        return 1
    fi
    
    # Save prompt to temporary file
    local prompt_file="$temp_dir/prompt_${timestamp}.txt"
    echo "$prompt_text" > "$prompt_file"
    
    echo "💾 Prompt saved to: $prompt_file"
    echo "📊 Prompt length: $(echo "$prompt_text" | wc -c) characters"
    
    # Show how to use with MCP tools
    echo ""
    echo "🔧 To use with MCP tools:"
    echo "Files parameter: [\"$prompt_file\"]"
    echo "Prompt parameter: \"\" (empty)"
    
    if [ -n "$continuation_id" ]; then
        echo "Continuation ID: $continuation_id"
    fi
    
    # Create quick access command
    echo ""
    echo "📋 Quick commands created:"
    echo "💡 view_saved_prompt - View the saved prompt"
    echo "🔄 continue_with_file - Continue conversation with file"
    
    # Export functions for this session
    export LAST_PROMPT_FILE="$prompt_file"
    export LAST_CONTINUATION_ID="$continuation_id"
}

view_saved_prompt() {
    if [ -n "$LAST_PROMPT_FILE" ] && [ -f "$LAST_PROMPT_FILE" ]; then
        echo "📄 Viewing saved prompt:"
        echo "File: $LAST_PROMPT_FILE"
        echo "--- CONTENT ---"
        cat "$LAST_PROMPT_FILE"
        echo "--- END ---"
    else
        echo "❌ No saved prompt found"
    fi
}

continue_with_file() {
    if [ -n "$LAST_PROMPT_FILE" ] && [ -f "$LAST_PROMPT_FILE" ]; then
        echo "🔄 To continue conversation:"
        echo "Tool: mcp__zen__thinkdeep"
        echo "Files: [\"$LAST_PROMPT_FILE\"]"
        echo "Prompt: \"\" (leave empty)"
        
        if [ -n "$LAST_CONTINUATION_ID" ]; then
            echo "Continuation ID: $LAST_CONTINUATION_ID"
        fi
    else
        echo "❌ No saved prompt to continue with"
    fi
}

# Function to extract context from current conversation
extract_conversation_context() {
    local context_file="/tmp/claude_prompts/conversation_context_$(date +%Y%m%d_%H%M%S).txt"
    
    echo "🔍 Extracting conversation context..."
    
    # Build context from available files
    {
        echo "# CONVERSATION CONTEXT FOR CHRISTIAN"
        echo "Generated: $(date)"
        echo ""
        
        if [ -f "SESSION_CONTINUITY.md" ]; then
            echo "## SESSION CONTINUITY"
            tail -50 SESSION_CONTINUITY.md
            echo ""
        fi
        
        if [ -f "TODO.md" ]; then
            echo "## CURRENT TODO"
            tail -20 TODO.md
            echo ""
        fi
        
        if [ -f "CLAUDE.md" ]; then
            echo "## PROJECT CONFIGURATION"
            echo "CLAUDE.md exists with $(wc -l < CLAUDE.md) lines"
            echo ""
        fi
        
        echo "## REQUEST"
        echo "Christian wants surgical optimizations for CLAUDE.md files"
        echo "Focus: fabric patterns utilization, practical improvements"
        echo "Evidence: 208 fabric patterns loaded but not used"
        
    } > "$context_file"
    
    echo "💾 Context saved to: $context_file"
    export LAST_CONTEXT_FILE="$context_file"
    
    return 0
}

export -f handle_large_prompt view_saved_prompt continue_with_file extract_conversation_context