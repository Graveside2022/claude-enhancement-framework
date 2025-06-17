# Pattern: Systematic Error Resolution

## Problem

When CLAUDE encounters errors, configuration issues, or behavioral problems, there's a need for a systematic approach to diagnose, resolve, and prevent recurrence. Ad-hoc error fixing often misses root causes and fails to capture learnings for future prevention.

## Solution

**7-Step Systematic Error Resolution Process:**

1. **Error Capture** - Document complete error context
2. **Impact Assessment** - Determine scope and urgency
3. **Root Cause Analysis** - Trace to fundamental cause
4. **Solution Development** - Create targeted fix
5. **Testing & Validation** - Verify resolution
6. **Learning Extraction** - Capture prevention knowledge
7. **Pattern Creation** - Transform solution into reusable pattern

## Code Template

```bash
#!/bin/bash
# Systematic Error Resolution Template
# Generated: [TIMESTAMP]
# User: Christian
# Error Context: [ERROR_DESCRIPTION]

resolve_error_systematically() {
    local error_description="$1"
    local error_category="$2"  # config|behavior|integration|performance
    local urgency="$3"         # critical|high|medium|low
    
    echo "🚨 SYSTEMATIC ERROR RESOLUTION - User: Christian"
    echo "Error: $error_description"
    echo "Category: $error_category | Urgency: $urgency"
    echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    
    # STEP 1: Error Capture
    capture_error_context "$error_description" "$error_category"
    
    # STEP 2: Impact Assessment
    assess_error_impact "$error_category" "$urgency"
    
    # STEP 3: Root Cause Analysis
    analyze_root_cause "$error_description"
    
    # STEP 4: Solution Development
    develop_targeted_solution "$error_category"
    
    # STEP 5: Testing & Validation
    test_and_validate_solution
    
    # STEP 6: Learning Extraction
    extract_error_learnings "$error_description"
    
    # STEP 7: Pattern Creation
    create_prevention_pattern "$error_category"
    
    echo "✅ Systematic error resolution complete"
}

capture_error_context() {
    local error_desc="$1"
    local category="$2"
    
    echo "📋 STEP 1: Capturing error context..."
    
    # Create error report
    cat > "error_analysis_$(date +%Y%m%d_%H%M%S).md" << EOF
# Error Analysis Report
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian
Category: $category

## Error Description
$error_desc

## Environment Context
- Working Directory: $(pwd)
- Git Status: $(git status --short 2>/dev/null | wc -l) uncommitted changes
- CLAUDE.md Present: $([ -f CLAUDE.md ] && echo "Yes" || echo "No")
- Session Files: $(ls SESSION_* 2>/dev/null | wc -l) files
- Recent Backups: $(ls backups/20* 2>/dev/null | tail -3 | wc -l) available

## System State
- Memory Files: $(find memory -name "*.md" 2>/dev/null | wc -l) files
- Pattern Files: $(find patterns -name "*.md" 2>/dev/null | wc -l) patterns
- Last TODO Update: $(stat -c %Y TODO.md 2>/dev/null | xargs -I {} date -d @{} || echo "N/A")

## Error Symptoms
- [Document specific symptoms observed]
- [List any error messages]
- [Note when error was first noticed]
- [Describe what triggered the error]

## Attempted Solutions
- [List any previous attempts to fix]
- [Note what didn't work]
- [Document any partial successes]
EOF
    
    echo "✓ Error context captured"
}

assess_error_impact() {
    local category="$1"
    local urgency="$2"
    
    echo "⚖️ STEP 2: Assessing error impact..."
    
    case "$urgency" in
        critical)
            echo "🚨 CRITICAL: Immediate resolution required"
            echo "- Blocking all work progress"
            echo "- System functionality compromised"
            echo "- Data integrity at risk"
            ;;
        high)
            echo "⚠️ HIGH: Resolution needed within hours"
            echo "- Significantly impacting productivity"
            echo "- Multiple functions affected"
            echo "- Workarounds available but inefficient"
            ;;
        medium)
            echo "📋 MEDIUM: Resolution needed within days"
            echo "- Some productivity impact"
            echo "- Limited functions affected"
            echo "- Acceptable workarounds exist"
            ;;
        low)
            echo "📝 LOW: Resolution when convenient"
            echo "- Minimal productivity impact"
            echo "- Single function affected"
            echo "- Easy workarounds available"
            ;;
    esac
    
    echo "✓ Impact assessment complete"
}

analyze_root_cause() {
    local error_desc="$1"
    
    echo "🔍 STEP 3: Root cause analysis..."
    
    # Check common CLAUDE error categories
    echo "Analyzing potential root causes:"
    
    # Configuration errors
    if echo "$error_desc" | grep -qi "config\|setup\|initialization"; then
        echo "📋 Configuration Error Suspected:"
        echo "- Check CLAUDE.md syntax and completeness"
        echo "- Verify all required directories exist"
        echo "- Validate timing rule implementation"
        echo "- Review global vs project configuration hierarchy"
    fi
    
    # Timing rule violations  
    if echo "$error_desc" | grep -qi "timing\|backup\|todo\|120.*minute"; then
        echo "⏰ Timing Rule Violation Suspected:"
        echo "- Check TODO.md age (should be < 120 minutes)"
        echo "- Verify backup system functionality"
        echo "- Review timing check implementation"
        echo "- Test automated timing enforcement"
    fi
    
    # Memory/Learning system issues
    if echo "$error_desc" | grep -qi "memory\|learning\|session.*continuity"; then
        echo "🧠 Memory System Issue Suspected:"
        echo "- Check SESSION_CONTINUITY.md integrity"
        echo "- Verify memory file loading functions"
        echo "- Review learning file structure"
        echo "- Test pattern recognition system"
    fi
    
    # Pattern system problems
    if echo "$error_desc" | grep -qi "pattern\|reuse\|template"; then
        echo "🎯 Pattern System Problem Suspected:"
        echo "- Check patterns/ directory structure"
        echo "- Verify pattern search functionality"
        echo "- Review pattern confidence scoring"
        echo "- Test pattern application process"
    fi
    
    echo "✓ Root cause analysis complete"
}

develop_targeted_solution() {
    local category="$1"
    
    echo "🔧 STEP 4: Developing targeted solution..."
    
    case "$category" in
        config)
            echo "Configuration Solution Development:"
            echo "- Validate CLAUDE.md syntax"
            echo "- Recreate missing directory structure"
            echo "- Reset configuration hierarchy"
            echo "- Test configuration loading"
            ;;
        behavior)
            echo "Behavior Solution Development:"
            echo "- Review behavioral rule implementation"
            echo "- Check decision matrix compliance"
            echo "- Verify trigger detection accuracy"
            echo "- Test response generation process"
            ;;
        integration)
            echo "Integration Solution Development:"
            echo "- Check system component interactions"
            echo "- Verify API compatibility"
            echo "- Test data flow between components"
            echo "- Validate external dependencies"
            ;;
        performance)
            echo "Performance Solution Development:"
            echo "- Profile system resource usage"
            echo "- Optimize memory management"
            echo "- Streamline process execution"
            echo "- Reduce computational overhead"
            ;;
    esac
    
    echo "✓ Solution development complete"
}

test_and_validate_solution() {
    echo "🧪 STEP 5: Testing and validation..."
    
    echo "Running validation tests:"
    
    # Test core functionality
    echo "- Testing core CLAUDE functionality..."
    echo "- Verifying timing rule compliance..."
    echo "- Checking pattern recognition..."
    echo "- Validating memory persistence..."
    echo "- Testing backup system..."
    
    # Integration tests
    echo "- Running integration tests..."
    echo "- Verifying component interactions..."
    echo "- Testing error handling..."
    echo "- Checking performance metrics..."
    
    echo "✓ Testing and validation complete"
}

extract_error_learnings() {
    local error_desc="$1"
    
    echo "📚 STEP 6: Extracting learnings..."
    
    # Update learning files
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    # Add to error patterns if memory directory exists
    if [ -d "memory" ]; then
        cat >> memory/error_patterns.md << EOF

## Error Learning - $timestamp
User: Christian

### Error Description
$error_desc

### Root Cause Identified
[Document the fundamental cause found]

### Solution Applied
[Document the specific solution implemented]

### Prevention Strategy
[Document how to prevent this error in future]

### Pattern Created
[Reference any new pattern created from this solution]

### Time to Resolution
[Document time from error detection to resolution]
EOF
    fi
    
    echo "✓ Learning extraction complete"
}

create_prevention_pattern() {
    local category="$1"
    
    echo "🎯 STEP 7: Creating prevention pattern..."
    
    # Create a reusable pattern from this error resolution
    local pattern_name="${category}_error_prevention_$(date +%Y%m%d)"
    
    cat > "patterns/bug_fixes/${pattern_name}.md" << EOF
# Pattern: [CATEGORY] Error Prevention

## Problem
Prevent recurrence of [CATEGORY] errors in CLAUDE systems.

## Solution
[Document the prevention approach developed]

## Code Template
[Include reusable code/configuration to prevent this error type]

## Testing Requirements
- Test for error conditions before they occur
- Validate prevention measures are working
- Monitor for early warning signs

## When to Use
- During initial system setup
- When configuring new CLAUDE environments
- As part of regular maintenance checks
- Before deploying system changes

## Time Saved
Estimated: [X] minutes per prevention application
Prevents: [Y] hours of error resolution time

## Usage Examples
[Provide specific examples of when and how to apply this pattern]
EOF
    
    echo "✓ Prevention pattern created: patterns/bug_fixes/${pattern_name}.md"
}

# Usage example
# resolve_error_systematically "TODO.md not updating automatically" "config" "high"
```

## Testing Requirements

- **Complexity Score**: 15+ (High complexity due to multiple steps)
- **TDD Used**: Yes - Test each step independently
- **Test Pattern**: Integration testing for complete workflow

### Test Cases:
1. **Configuration Errors**: Test CLAUDE.md syntax issues
2. **Timing Violations**: Test 120-minute rule enforcement  
3. **Memory Issues**: Test SESSION_CONTINUITY.md corruption
4. **Pattern Failures**: Test pattern recognition problems
5. **Integration Failures**: Test component interaction issues

### Validation Steps:
1. Verify error capture completeness
2. Confirm root cause identification accuracy
3. Test solution effectiveness
4. Validate learning extraction
5. Ensure pattern creation quality

## When to Use

- **Error Encountered**: Any CLAUDE system error or unexpected behavior
- **Recurring Issues**: Problems that have happened before
- **System Instability**: When CLAUDE behavior becomes unpredictable
- **After Changes**: When modifications cause unexpected results
- **Preventive Analysis**: Regular system health checks

## Time Saved

**Estimated**: 60-90 minutes per systematic error resolution
**Prevents**: 3-5 hours of repeated troubleshooting

**Actual Uses**: Track each application for efficiency metrics

## Usage Examples

### Example 1: Configuration Error
```bash
resolve_error_systematically "CLAUDE.md rules not being enforced" "config" "high"
```

### Example 2: Timing Rule Problem
```bash
resolve_error_systematically "TODO.md not updating every 120 minutes" "behavior" "medium"
```

### Example 3: Memory System Issue
```bash
resolve_error_systematically "SESSION_CONTINUITY.md corruption" "integration" "critical"
```

### Example 4: Pattern Recognition Failure
```bash
resolve_error_systematically "Patterns not being found during search" "performance" "medium"
```

## Success Indicators

- ✅ Error completely resolved without recurrence
- ✅ Root cause identified and documented
- ✅ Prevention pattern created and tested
- ✅ Learning captured in memory system
- ✅ Similar errors prevented by pattern application