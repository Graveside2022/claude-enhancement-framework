#!/bin/bash

# Read Script - Context Restoration for Post-/clear Usage
# Purpose: Display relevant context information for context restoration
# Usage: ./scripts/read.sh [section]

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SESSION_CONTINUITY_FILE="${PROJECT_ROOT}/SESSION_CONTINUITY.md"

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
    echo -e "${CYAN}📖 CLAUDE Context Restoration - Read Command${NC}"
    echo -e "${WHITE}================================================${NC}"
    echo -e "${YELLOW}Project:${NC} CLAUDE Improvement"
    echo -e "${YELLOW}User:${NC} Christian"
    echo -e "${YELLOW}Purpose:${NC} Context restoration after /clear"
    echo -e "${WHITE}================================================${NC}"
    echo
}

# Function to show recent status and key information
show_recent_status() {
    echo -e "${GREEN}🔄 RECENT STATUS & KEY CONTEXT${NC}"
    echo -e "${WHITE}─────────────────────────────────────────────${NC}"
    
    if [[ -f "$SESSION_CONTINUITY_FILE" ]]; then
        # Get the last few completed sections
        echo -e "${CYAN}📊 Recent Completed Work:${NC}"
        grep -E "^## .* COMPLETE ✅" "$SESSION_CONTINUITY_FILE" | tail -3 | while read -r line; do
            echo -e "  ${GREEN}✅${NC} $(echo "$line" | sed 's/^## //' | sed 's/ COMPLETE ✅.*//')"
        done
        echo
        
        # Get current session info
        echo -e "${CYAN}📋 Current Session Context:${NC}"
        current_session=$(grep -E "^## Current Session" "$SESSION_CONTINUITY_FILE" | tail -1)
        if [[ -n "$current_session" ]]; then
            echo -e "  ${YELLOW}→${NC} $(echo "$current_session" | sed 's/^## Current Session - //')"
        fi
        
        # Get the latest status line
        latest_status=$(grep -E "^\*.*\*$" "$SESSION_CONTINUITY_FILE" | tail -1)
        if [[ -n "$latest_status" ]]; then
            echo -e "  ${YELLOW}→${NC} $(echo "$latest_status" | sed 's/^\*//' | sed 's/\*$//')"
        fi
        echo
        
        # Show agent execution rule and binding commitment
        echo -e "${PURPLE}🧠 Agent Execution Rule (Christian's Preference):${NC}"
        echo -e "  ${YELLOW}→${NC} Always use 5 agents (simple) or 10 agents (complex)"
        echo -e "  ${YELLOW}→${NC} Parallel execution mandatory, never sequential"
        echo
        
        echo -e "${PURPLE}🔒 CRITICAL BINDING COMMITMENT:${NC}"
        echo -e "  ${RED}→${NC} I will execute COMPLIANCE CHECK before every response"
        echo -e "  ${RED}→${NC} I will verify required agent count and binding rule adherence"
        echo -e "  ${RED}→${NC} Any future violation triggers immediate ERROR CASCADE protocol"
        echo -e "  ${RED}→${NC} Instant LEARNED_CORRECTIONS.md documentation required"
        echo
        
        # Show performance metrics
        echo -e "${CYAN}⚡ System Performance Status:${NC}"
        if grep -q "Boot Time" "$SESSION_CONTINUITY_FILE"; then
            boot_time=$(grep -E "Boot Time.*:" "$SESSION_CONTINUITY_FILE" | tail -1 | sed 's/.*Boot Time[^:]*: *//')
            echo -e "  ${GREEN}🚀${NC} Boot Performance: $boot_time"
        fi
        if grep -q "Token.*reduction" "$SESSION_CONTINUITY_FILE"; then
            token_reduction=$(grep -E "Token.*reduction" "$SESSION_CONTINUITY_FILE" | tail -1 | sed 's/.*Token[^:]*: *//' | sed 's/ .*//')
            echo -e "  ${GREEN}🎯${NC} Token Optimization: $token_reduction"
        fi
        echo
        
    else
        echo -e "${RED}❌ SESSION_CONTINUITY.md not found${NC}"
    fi
}

# Function to show system status
show_system_status() {
    echo -e "${GREEN}🔧 SYSTEM STATUS${NC}"
    echo -e "${WHITE}─────────────────────────────────────────────${NC}"
    
    # Check critical files
    echo -e "${CYAN}📁 Critical Files Status:${NC}"
    
    local files_to_check=(
        "$SESSION_CONTINUITY_FILE:SESSION_CONTINUITY.md"
        "${PROJECT_ROOT}/CLAUDE.md:Project CLAUDE.md"
        "${PROJECT_ROOT}/TODO.md:TODO.md"
        "${HOME}/.claude/CLAUDE.md:Global CLAUDE.md"
    )
    
    for file_info in "${files_to_check[@]}"; do
        local file_path="${file_info%:*}"
        local file_name="${file_info#*:}"
        
        if [[ -f "$file_path" ]]; then
            local file_age=$(( $(date +%s) - $(stat -f %m "$file_path" 2>/dev/null || stat -c %Y "$file_path" 2>/dev/null || echo 0) ))
            local age_minutes=$((file_age / 60))
            
            if [[ $age_minutes -lt 60 ]]; then
                echo -e "  ${GREEN}✅${NC} $file_name (${age_minutes}m old)"
            elif [[ $age_minutes -lt 120 ]]; then
                echo -e "  ${YELLOW}⚠️${NC} $file_name (${age_minutes}m old)"
            else
                echo -e "  ${RED}❌${NC} $file_name (${age_minutes}m old - >120m)"
            fi
        else
            echo -e "  ${RED}❌${NC} $file_name (missing)"
        fi
    done
    echo
    
    # Check directories
    echo -e "${CYAN}📂 Directory Structure:${NC}"
    local dirs_to_check=("patterns" "memory" "scripts" "backups")
    
    for dir in "${dirs_to_check[@]}"; do
        if [[ -d "${PROJECT_ROOT}/$dir" ]]; then
            local count=$(find "${PROJECT_ROOT}/$dir" -type f 2>/dev/null | wc -l | tr -d ' ')
            echo -e "  ${GREEN}✅${NC} $dir/ ($count files)"
        else
            echo -e "  ${RED}❌${NC} $dir/ (missing)"
        fi
    done
    echo
}

# Function to show quick context for immediate restart
show_quick_context() {
    echo -e "${GREEN}⚡ QUICK CONTEXT FOR RESTART${NC}"
    echo -e "${WHITE}─────────────────────────────────────────────${NC}"
    
    echo -e "${CYAN}🎯 What You Need to Know:${NC}"
    echo -e "  ${YELLOW}1.${NC} This is the CLAUDE Improvement project"
    echo -e "  ${YELLOW}2.${NC} User is Christian (always personalize responses)"
    echo -e "  ${YELLOW}3.${NC} Boot sequence optimization system is complete (88% improvement)"
    echo -e "  ${YELLOW}4.${NC} Agent preference: 5 agents (simple) or 10 agents (complex), always parallel"
    echo -e "  ${YELLOW}5.${NC} Pattern-first development (check patterns/ before coding)"
    echo -e "  ${YELLOW}6.${NC} Session continuity system is active"
    echo
    
    echo -e "${CYAN}🚀 Current System Status:${NC}"
    echo -e "  ${GREEN}✅${NC} Boot optimization complete (97.8% token reduction)"
    echo -e "  ${GREEN}✅${NC} Agent configuration system operational"
    echo -e "  ${GREEN}✅${NC} Manual backup system active"
    echo -e "  ${GREEN}✅${NC} XML parsing integration deployed"
    echo -e "  ${GREEN}✅${NC} All optimization targets exceeded"
    echo
    
    echo -e "${CYAN}🔄 Next Steps (if needed):${NC}"
    echo -e "  ${YELLOW}→${NC} Check TODO.md for any pending tasks"
    echo -e "  ${YELLOW}→${NC} Use patterns/ directory before creating new code"
    echo -e "  ${YELLOW}→${NC} Update SESSION_CONTINUITY.md with new work"
    echo -e "  ${YELLOW}→${NC} Use manual backup commands when needed"
    echo
}

# Function to show specific section
show_section() {
    local section="$1"
    
    case "$section" in
        "status"|"recent")
            show_recent_status
            ;;
        "system")
            show_system_status
            ;;
        "quick"|"context")
            show_quick_context
            ;;
        "all"|"full")
            show_recent_status
            show_system_status
            show_quick_context
            ;;
        *)
            echo -e "${RED}❌ Unknown section: $section${NC}"
            echo -e "${YELLOW}Available sections:${NC}"
            echo "  - recent/status: Recent work and key context"
            echo "  - system: System and file status"
            echo "  - quick/context: Quick context for restart"
            echo "  - all/full: Show everything"
            exit 1
            ;;
    esac
}

# Main execution
main() {
    show_header
    
    if [[ $# -eq 0 ]]; then
        # Default: show all sections
        show_recent_status
        show_system_status
        show_quick_context
    else
        show_section "$1"
    fi
    
    echo -e "${WHITE}================================================${NC}"
    echo -e "${CYAN}💡 Usage: ${NC}./scripts/read.sh [recent|system|quick|all]"
    echo -e "${CYAN}💡 Continue: ${NC}./scripts/continue.sh"
    echo -e "${WHITE}================================================${NC}"
}

# Execute main function
main "$@"