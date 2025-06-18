#!/bin/bash

# Continue Script - Context Restoration and Session Continuation
# Purpose: Provide comprehensive context and guidance for continuing work
# Usage: ./scripts/continue.sh [focus_area]

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SESSION_CONTINUITY_FILE="${PROJECT_ROOT}/SESSION_CONTINUITY.md"
TODO_FILE="${PROJECT_ROOT}/TODO.md"

# Color codes for output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Function to display header
show_header() {
    echo -e "${WHITE}================================================${NC}"
    echo -e "${CYAN}🚀 CLAUDE Context Restoration - Continue Command${NC}"
    echo -e "${WHITE}================================================${NC}"
    echo -e "${YELLOW}Project:${NC} CLAUDE Improvement"
    echo -e "${YELLOW}User:${NC} Christian"
    echo -e "${YELLOW}Purpose:${NC} Complete context restoration and work continuation"
    echo -e "${WHITE}================================================${NC}"
    echo
}

# Function to restore complete context
restore_context() {
    echo -e "${GREEN}🧠 CONTEXT RESTORATION${NC}"
    echo -e "${WHITE}─────────────────────────────────────────────${NC}"
    
    echo -e "${CYAN}👋 Welcome back, Christian!${NC}"
    echo
    
    echo -e "${CYAN}🎯 Project Context:${NC}"
    echo -e "  ${YELLOW}→${NC} CLAUDE Improvement project - automatic learning file loading system"
    echo -e "  ${YELLOW}→${NC} Focus: Boot sequence optimization and session continuity"
    echo -e "  ${YELLOW}→${NC} Major achievement: 97.8% token reduction, <5ms boot time"
    echo -e "  ${YELLOW}→${NC} All optimization systems deployed and operational"
    echo
    
    echo -e "${CYAN}🔧 System Configuration:${NC}"
    echo -e "  ${YELLOW}→${NC} Agent preference: 5 agents (simple) or 10 agents (complex)"
    echo -e "  ${YELLOW}→${NC} Always parallel execution, never sequential"
    echo -e "  ${YELLOW}→${NC} Pattern-first development approach"
    echo -e "  ${YELLOW}→${NC} Manual backup system active"
    echo
    
    echo -e "${PURPLE}🔒 CRITICAL BINDING COMMITMENT:${NC}"
    echo -e "  ${RED}→${NC} I will execute COMPLIANCE CHECK before every response"
    echo -e "  ${RED}→${NC} I will verify required agent count and binding rule adherence"
    echo -e "  ${RED}→${NC} Any future violation triggers immediate ERROR CASCADE protocol"
    echo -e "  ${RED}→${NC} Instant LEARNED_CORRECTIONS.md documentation required"
    echo -e "  ${YELLOW}→${NC} 5 parallel agents for simple tasks, 10 for complex tasks"
    echo
    
    if [[ -f "$SESSION_CONTINUITY_FILE" ]]; then
        echo -e "${CYAN}📊 Recent Major Completions:${NC}"
        grep -E "^## .* COMPLETE ✅" "$SESSION_CONTINUITY_FILE" | tail -5 | while read -r line; do
            completion=$(echo "$line" | sed 's/^## //' | sed 's/ COMPLETE ✅.*//')
            echo -e "  ${GREEN}✅${NC} $completion"
        done
        echo
        
        # Show last status update
        current_session=$(grep -E "^## Current Session" "$SESSION_CONTINUITY_FILE" | tail -1)
        if [[ -n "$current_session" ]]; then
            echo -e "${CYAN}📋 Last Session Status:${NC}"
            echo -e "  ${YELLOW}→${NC} $(echo "$current_session" | sed 's/^## Current Session - //')"
            
            # Get context after the last current session
            latest_context=$(sed -n '/^## Current Session/,$p' "$SESSION_CONTINUITY_FILE" | tail -n +2 | head -3 | grep -E "^\*.*\*$" | tail -1)
            if [[ -n "$latest_context" ]]; then
                echo -e "  ${YELLOW}→${NC} $(echo "$latest_context" | sed 's/^\*//' | sed 's/\*$//')"
            fi
        fi
        echo
        
        # Show system performance
        echo -e "${CYAN}⚡ System Performance:${NC}"
        if grep -q "97.8% token reduction" "$SESSION_CONTINUITY_FILE"; then
            echo -e "  ${GREEN}🎯${NC} Token Optimization: 97.8% reduction (24,600 → 540 tokens)"
        fi
        if grep -q "Boot Time" "$SESSION_CONTINUITY_FILE"; then
            boot_time=$(grep -E "Boot Time.*:" "$SESSION_CONTINUITY_FILE" | tail -1 | sed 's/.*Boot Time[^:]*: *//' | sed 's/ .*//')
            echo -e "  ${GREEN}🚀${NC} Boot Performance: $boot_time"
        fi
        if grep -q "88% improvement" "$SESSION_CONTINUITY_FILE"; then
            echo -e "  ${GREEN}🏆${NC} Overall Improvement: 88%+ (target exceeded)"
        fi
        echo
    fi
}

# Function to check current status and next steps
show_next_steps() {
    echo -e "${GREEN}🔄 CURRENT STATUS & NEXT STEPS${NC}"
    echo -e "${WHITE}─────────────────────────────────────────────${NC}"
    
    echo -e "${CYAN}📁 File Status Check:${NC}"
    
    # Check TODO.md
    if [[ -f "$TODO_FILE" ]]; then
        todo_age=$(( $(date +%s) - $(stat -f %m "$TODO_FILE" 2>/dev/null || stat -c %Y "$TODO_FILE" 2>/dev/null || echo 0) ))
        todo_minutes=$((todo_age / 60))
        
        if [[ $todo_minutes -lt 120 ]]; then
            echo -e "  ${GREEN}✅${NC} TODO.md (${todo_minutes}m old - current)"
            
            # Show pending tasks if any
            pending_tasks=$(grep -E "^\s*-\s*\[.\]" "$TODO_FILE" 2>/dev/null | grep -v "\[x\]" | head -3)
            if [[ -n "$pending_tasks" ]]; then
                echo -e "${CYAN}📋 Pending Tasks in TODO.md:${NC}"
                echo "$pending_tasks" | while read -r task; do
                    echo -e "  ${YELLOW}→${NC} $(echo "$task" | sed 's/^\s*-\s*\[.\]\s*//')"
                done
            else
                echo -e "  ${GREEN}🎉${NC} No pending tasks in TODO.md"
            fi
        else
            echo -e "  ${YELLOW}⚠️${NC} TODO.md (${todo_minutes}m old - may need update)"
        fi
    else
        echo -e "  ${RED}❌${NC} TODO.md not found"
    fi
    echo
    
    # Check SESSION_CONTINUITY.md age
    if [[ -f "$SESSION_CONTINUITY_FILE" ]]; then
        session_age=$(( $(date +%s) - $(stat -f %m "$SESSION_CONTINUITY_FILE" 2>/dev/null || stat -c %Y "$SESSION_CONTINUITY_FILE" 2>/dev/null || echo 0) ))
        session_minutes=$((session_age / 60))
        
        if [[ $session_minutes -lt 120 ]]; then
            echo -e "  ${GREEN}✅${NC} SESSION_CONTINUITY.md (${session_minutes}m old - current)"
        else
            echo -e "  ${YELLOW}⚠️${NC} SESSION_CONTINUITY.md (${session_minutes}m old - may need update)"
        fi
    fi
    echo
    
    echo -e "${CYAN}🎯 Recommended Next Actions:${NC}"
    echo -e "  ${YELLOW}1.${NC} Review any pending items in TODO.md"
    echo -e "  ${YELLOW}2.${NC} Check if any new requirements or tasks have emerged"
    echo -e "  ${YELLOW}3.${NC} Update SESSION_CONTINUITY.md with current work"
    echo -e "  ${YELLOW}4.${NC} Use pattern-first approach (check patterns/ before coding)"
    echo -e "  ${YELLOW}5.${NC} Deploy agents appropriately (5 for simple, 10 for complex tasks)"
    echo
    
    echo -e "${CYAN}🛠️ Available Commands:${NC}"
    echo -e "  ${YELLOW}→${NC} ./scripts/read.sh [section] - Read specific context sections"
    echo -e "  ${YELLOW}→${NC} ./scripts/manual_backup.sh backup - Create manual backup"
    echo -e "  ${YELLOW}→${NC} ./scripts/search_session_archive.sh 'keyword' - Search session history"
    echo -e "  ${YELLOW}→${NC} ./scripts/restore_session_context.sh YYYY-MM-DD - Restore previous session"
}

# Function to show focused guidance based on focus area
show_focused_guidance() {
    local focus_area="$1"
    
    echo -e "${GREEN}🎯 FOCUSED GUIDANCE: $focus_area${NC}"
    echo -e "${WHITE}─────────────────────────────────────────────${NC}"
    
    case "$focus_area" in
        "coding"|"development")
            echo -e "${CYAN}💻 Development Focus:${NC}"
            echo -e "  ${YELLOW}1.${NC} Check patterns/ directory first before writing new code"
            echo -e "  ${YELLOW}2.${NC} Use 5 agents for implementation, 10 for complex architecture"
            echo -e "  ${YELLOW}3.${NC} Always parallel execution, never sequential"
            echo -e "  ${YELLOW}4.${NC} Update SESSION_CONTINUITY.md after implementation"
            echo -e "  ${YELLOW}5.${NC} Create new patterns for reusable solutions"
            ;;
        "testing"|"validation")
            echo -e "${CYAN}🧪 Testing/Validation Focus:${NC}"
            echo -e "  ${YELLOW}1.${NC} Check tests/ directory for existing test frameworks"
            echo -e "  ${YELLOW}2.${NC} Use validation patterns from patterns/generation/"
            echo -e "  ${YELLOW}3.${NC} Deploy 10 agents for comprehensive testing coverage"
            echo -e "  ${YELLOW}4.${NC} Document validation results in SESSION_CONTINUITY.md"
            echo -e "  ${YELLOW}5.${NC} Create test reports in standard format"
            ;;
        "optimization"|"performance")
            echo -e "${CYAN}⚡ Optimization Focus:${NC}"
            echo -e "  ${YELLOW}1.${NC} Current system already 97.8% optimized"
            echo -e "  ${YELLOW}2.${NC} Check existing optimization patterns in patterns/refactoring/"
            echo -e "  ${YELLOW}3.${NC} Monitor token usage and boot time impacts"
            echo -e "  ${YELLOW}4.${NC} Use performance analysis templates"
            echo -e "  ${YELLOW}5.${NC} Document any new optimizations found"
            ;;
        "backup"|"maintenance")
            echo -e "${CYAN}🔧 Backup/Maintenance Focus:${NC}"
            echo -e "  ${YELLOW}1.${NC} Use manual backup system: ./scripts/manual_backup.sh backup"
            echo -e "  ${YELLOW}2.${NC} Check backup/ directory for recent backups"
            echo -e "  ${YELLOW}3.${NC} Monitor SESSION_CONTINUITY.md age (120-minute rule)"
            echo -e "  ${YELLOW}4.${NC} Archive old sessions if needed"
            echo -e "  ${YELLOW}5.${NC} Verify all critical files are present"
            ;;
        *)
            echo -e "${CYAN}📋 General Work Focus:${NC}"
            echo -e "  ${YELLOW}1.${NC} Start with pattern checking (patterns/ directory)"
            echo -e "  ${YELLOW}2.${NC} Deploy appropriate agents (5 simple, 10 complex)"
            echo -e "  ${YELLOW}3.${NC} Always use parallel execution"
            echo -e "  ${YELLOW}4.${NC} Update SESSION_CONTINUITY.md with progress"
            echo -e "  ${YELLOW}5.${NC} Create backups for significant changes"
            ;;
    esac
    echo
}

# Function to show quick reference
show_quick_reference() {
    echo -e "${GREEN}📖 QUICK REFERENCE${NC}"
    echo -e "${WHITE}─────────────────────────────────────────────${NC}"
    
    echo -e "${CYAN}🔗 Key Project Information:${NC}"
    echo -e "  ${YELLOW}Project:${NC} CLAUDE Improvement (boot optimization & session continuity)"
    echo -e "  ${YELLOW}User:${NC} Christian (always personalize responses)"
    echo -e "  ${YELLOW}Status:${NC} 97.8% optimization complete, all systems operational"
    echo -e "  ${YELLOW}Focus:${NC} Pattern-first development with parallel agent execution"
    echo
    
    echo -e "${CYAN}⚙️ System Rules:${NC}"
    echo -e "  ${YELLOW}→${NC} Agent deployment: 5 (simple) or 10 (complex), always parallel"
    echo -e "  ${YELLOW}→${NC} Pattern-first: Check patterns/ before coding"
    echo -e "  ${YELLOW}→${NC} Session updates: Update SESSION_CONTINUITY.md after work"
    echo -e "  ${YELLOW}→${NC} Backup system: Manual only (./scripts/manual_backup.sh)"
    echo
    
    echo -e "${CYAN}📂 Key Directories:${NC}"
    echo -e "  ${YELLOW}→${NC} patterns/ - Reusable code patterns and solutions"
    echo -e "  ${YELLOW}→${NC} memory/ - Learning files and error patterns"
    echo -e "  ${YELLOW}→${NC} scripts/ - Automation and utility scripts"
    echo -e "  ${YELLOW}→${NC} backups/ - Manual backup storage"
    echo -e "  ${YELLOW}→${NC} tests/ - Testing and validation files"
}

# Main execution
main() {
    show_header
    
    restore_context
    
    if [[ $# -eq 0 ]]; then
        show_next_steps
        show_quick_reference
    else
        show_focused_guidance "$1"
        show_next_steps
    fi
    
    echo -e "${WHITE}================================================${NC}"
    echo -e "${CYAN}💡 Usage: ${NC}./scripts/continue.sh [coding|testing|optimization|backup]"
    echo -e "${CYAN}💡 Context: ${NC}./scripts/read.sh [section]"
    echo -e "${CYAN}💡 Ready to continue work, Christian!${NC}"
    echo -e "${WHITE}================================================${NC}"
}

# Execute main function
main "$@"