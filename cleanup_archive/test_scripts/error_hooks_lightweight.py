#!/usr/bin/env python3
"""
Lightweight Error Detection Hooks for CLAUDE.md Optimization
Loads only essential triggers, defers detailed procedures
"""

import os
import re
from pathlib import Path

class ErrorDetectionHooks:
    """Minimal error detection system - loads instantly"""
    
    def __init__(self):
        # Primary triggers - MUST load
        self.primary_triggers = [
            "that's wrong",
            "you made an error", 
            "that's incorrect",
            "think about what went wrong"
        ]
        
        # Secondary triggers - lightweight patterns
        self.secondary_triggers = [
            r"actually,?\s*(it\s*)?should",
            r"no,?\s*that's",
            r"correction:",
            r"fixed?\s*version:",
            r"the\s*correct\s*(way|approach)",
        ]
        
        # Memory files to check (existence only)
        self.memory_files = {
            "global": [
                "$HOME/.claude/LEARNED_CORRECTIONS.md",
                "$HOME/.claude/PYTHON_LEARNINGS.md",
                "$HOME/.claude/INFRASTRUCTURE_LEARNINGS.md"
            ],
            "project": [
                "memory/error_patterns.md",
                "memory/learning_archive.md",
                "memory/side_effects_log.md"
            ]
        }
        
        # Deferred content marker
        self.detailed_procedures_loaded = False
        
    def check_error_triggers(self, user_input):
        """Quick error detection - no heavy processing"""
        input_lower = user_input.lower()
        
        # Check primary triggers (exact phrases)
        for trigger in self.primary_triggers:
            if trigger in input_lower:
                return {
                    "error_detected": True,
                    "trigger_type": "primary",
                    "trigger": trigger,
                    "action": "load_full_error_analysis"
                }
        
        # Check secondary triggers (regex patterns)
        for pattern in self.secondary_triggers:
            if re.search(pattern, input_lower):
                return {
                    "error_detected": True,
                    "trigger_type": "secondary",
                    "pattern": pattern,
                    "action": "assess_error_learning_needed"
                }
                
        return {"error_detected": False}
    
    def check_memory_files_exist(self):
        """Quick file existence check only - no content loading"""
        status = {
            "global_files": {},
            "project_files": {},
            "any_missing": False
        }
        
        # Expand paths and check existence
        home = os.path.expanduser("~")
        
        for file in self.memory_files["global"]:
            path = file.replace("$HOME", home)
            exists = os.path.exists(path)
            status["global_files"][file] = exists
            if not exists:
                status["any_missing"] = True
                
        for file in self.memory_files["project"]:
            exists = os.path.exists(file)
            status["project_files"][file] = exists
            if not exists:
                status["any_missing"] = True
                
        return status
    
    def load_detailed_procedures(self):
        """Load full error analysis procedures on-demand"""
        if self.detailed_procedures_loaded:
            return {"status": "already_loaded"}
            
        # This would load the 2,200+ lines of detailed procedures
        # For now, just mark as loaded
        self.detailed_procedures_loaded = True
        
        return {
            "status": "loaded",
            "procedures": [
                "ERROR_ANALYSIS_RECORD creation",
                "Deep analysis methodology", 
                "Error categorization",
                "Prevention procedures",
                "Meta-learning capabilities"
            ]
        }
    
    def get_quick_decision_tree(self):
        """Return lightweight decision tree for immediate use"""
        return """
ERROR DETECTION
    |
    ├─> Explicit error statement from Christian?
    │   ├─> "That's wrong" / "You made an error" → ACTIVATE IMMEDIATELY
    │   └─> Other correction → Assess if error learning needed
    │
    ├─> Correction provided by Christian?
    │   ├─> YES: Activate error analysis mode
    │   └─> NO: Continue monitoring
    │
    └─> Self-detected inconsistency?
        ├─> YES: Treat as user-identified error
        └─> NO: Continue normal operation
"""

# Lightweight hook functions for bash integration
def create_error_detection_stub():
    """Create minimal bash stub for error detection"""
    return """
# Lightweight error detection hook
detect_error_trigger() {
    local user_input="$1"
    local input_lower=$(echo "$user_input" | tr '[:upper:]' '[:lower:]')
    
    # Primary triggers only - fast detection
    if echo "$input_lower" | grep -E "that's wrong|you made an error|that's incorrect|think about what went wrong" >/dev/null 2>&1; then
        echo "ERROR_DETECTED: Primary trigger found"
        # Load full procedures only now
        load_error_analysis_procedures
        return 0
    fi
    
    return 1
}

# Stub function - loads full procedures on demand
load_error_analysis_procedures() {
    echo "📚 Loading detailed error analysis procedures..."
    # This would source the full 2,200+ lines
    # Currently deferred to save memory
    export ERROR_PROCEDURES_LOADED=true
}

# Quick memory file check
check_error_memory_files() {
    local missing=0
    
    # Just check existence, don't load contents
    [ -f "$HOME/.claude/LEARNED_CORRECTIONS.md" ] || missing=$((missing+1))
    [ -f "memory/error_patterns.md" ] || missing=$((missing+1))
    
    if [ $missing -gt 0 ]; then
        echo "⚠️ $missing error memory files missing"
    else
        echo "✓ Error memory files present"
    fi
}
"""

if __name__ == "__main__":
    # Test the lightweight hooks
    detector = ErrorDetectionHooks()
    
    print("Error Detection Hooks - Lightweight Version")
    print("==========================================")
    
    # Test trigger detection
    test_inputs = [
        "that's wrong, it should be different",
        "everything looks good",
        "you made an error in the calculation",
        "please fix this issue"
    ]
    
    for test in test_inputs:
        result = detector.check_error_triggers(test)
        print(f"\nInput: '{test}'")
        print(f"Result: {result}")
    
    # Check memory files
    print("\nMemory File Status:")
    print(detector.check_memory_files_exist())
    
    # Show decision tree
    print("\nQuick Decision Tree:")
    print(detector.get_quick_decision_tree())
    
    # Generate bash stub
    print("\nBash Integration Stub:")
    print(create_error_detection_stub())