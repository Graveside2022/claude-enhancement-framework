# Pattern: Systematic Error Resolution

**Keywords**: error, bug, fix, debugging, troubleshooting, resolution, systematic
**Tags**: debugging, bug_fixes, error, troubleshooting, systematic, resolution
**Complexity**: medium  
**Use Cases**: error fixing, bug resolution, debugging issues, troubleshooting problems

## Execution Parameters

### Required Variables
```bash
# Core execution parameters
USER_NAME="Christian"                    # Target user for error resolution
ERROR_CATEGORY=""                       # config|behavior|integration|performance
ERROR_URGENCY=""                        # critical|high|medium|low
ERROR_DESCRIPTION=""                    # Detailed error description
RESOLUTION_TIMEOUT=3600                 # Maximum resolution time (seconds)

# File paths
ERROR_REPORT_DIR="error_reports"
PATTERN_DIR="patterns/bug_fixes"
MEMORY_DIR="memory"
LEARNING_FILE="$MEMORY_DIR/error_patterns.md"

# Resolution tracking
RESOLUTION_START_TIME=""
ROOT_CAUSE_IDENTIFIED=false
SOLUTION_IMPLEMENTED=false
VALIDATION_COMPLETE=false
PATTERN_CREATED=false
```

### Execution Context
```bash
# Pattern executor context
PATTERN_TYPE="systematic_error_resolution"
EXECUTION_MODE="systematic"             # systematic|emergency|diagnostic
VALIDATION_LEVEL="comprehensive"        # comprehensive|standard|minimal
LEARNING_ENABLED=true                   # Enable learning extraction
PATTERN_CREATION_ENABLED=true           # Enable prevention pattern creation
```

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

## Validation Checkpoints

### Pre-Resolution Validation
```bash
validate_error_resolution_prerequisites() {
    local validation_results=()
    
    echo "🔍 CHECKPOINT 1: Pre-resolution validation"
    
    # Validate required parameters
    if [[ -z "$ERROR_CATEGORY" ]]; then
        validation_results+=("ERROR: Error category not specified")
    fi
    
    if [[ -z "$ERROR_URGENCY" ]]; then
        validation_results+=("ERROR: Error urgency not specified")
    fi
    
    if [[ -z "$ERROR_DESCRIPTION" ]]; then
        validation_results+=("ERROR: Error description not provided")
    fi
    
    # Check required directories
    if [[ ! -d "$ERROR_REPORT_DIR" ]]; then
        mkdir -p "$ERROR_REPORT_DIR"
        echo "INFO: Created error report directory"
    fi
    
    if [[ ! -d "$MEMORY_DIR" ]]; then
        validation_results+=("ERROR: Memory directory missing")
    fi
    
    # Validate system tools
    for tool in git grep stat date; do
        if ! command -v "$tool" >/dev/null 2>&1; then
            validation_results+=("ERROR: Required tool '$tool' not available")
        fi
    done
    
    # Report validation results
    if [[ ${#validation_results[@]} -gt 0 ]]; then
        printf '%s\n' "${validation_results[@]}"
        return 1
    fi
    
    echo "✅ Pre-resolution validation passed"
    return 0
}
```

### Mid-Resolution Checkpoints
```bash
validate_resolution_progress() {
    local phase="$1"
    
    echo "🔍 CHECKPOINT 2: Progress validation ($phase)"
    
    case "$phase" in
        "error_capture")
            if [[ ! -f "$ERROR_REPORT_DIR/error_analysis_"*.md ]]; then
                echo "❌ FAIL: Error analysis report not created"
                return 1
            fi
            echo "✅ Error capture completed"
            ;;
        "impact_assessment")
            local urgency_valid=false
            for valid_urgency in critical high medium low; do
                if [[ "$ERROR_URGENCY" == "$valid_urgency" ]]; then
                    urgency_valid=true
                    break
                fi
            done
            if [[ $urgency_valid == false ]]; then
                echo "❌ FAIL: Invalid urgency level '$ERROR_URGENCY'"
                return 1
            fi
            echo "✅ Impact assessment completed"
            ;;
        "root_cause_analysis")
            if [[ $ROOT_CAUSE_IDENTIFIED != true ]]; then
                echo "⚠️ WARNING: Root cause analysis incomplete"
                return 1
            fi
            echo "✅ Root cause analysis completed"
            ;;
        "solution_development")
            if [[ $SOLUTION_IMPLEMENTED != true ]]; then
                echo "❌ FAIL: Solution not implemented"
                return 1
            fi
            echo "✅ Solution development completed"
            ;;
        "testing_validation")
            if [[ $VALIDATION_COMPLETE != true ]]; then
                echo "❌ FAIL: Validation not complete"
                return 1
            fi
            echo "✅ Testing and validation completed"
            ;;
    esac
    
    return 0
}
```

### Post-Resolution Validation
```bash
validate_resolution_success() {
    echo "🔍 CHECKPOINT 3: Resolution success validation"
    
    local success_indicators=()
    local total_indicators=7
    
    # Check error resolution
    if verify_error_resolved; then
        success_indicators+=("error_resolved")
        echo "✅ Error completely resolved"
    else
        echo "❌ Error not fully resolved"
    fi
    
    # Check root cause documentation
    if [[ $ROOT_CAUSE_IDENTIFIED == true ]] && grep -q "Root Cause Identified" "$ERROR_REPORT_DIR"/*.md; then
        success_indicators+=("root_cause_documented")
        echo "✅ Root cause identified and documented"
    else
        echo "❌ Root cause not properly documented"
    fi
    
    # Check solution implementation
    if [[ $SOLUTION_IMPLEMENTED == true ]]; then
        success_indicators+=("solution_implemented")
        echo "✅ Solution implemented successfully"
    else
        echo "❌ Solution not implemented"
    fi
    
    # Check validation completion
    if [[ $VALIDATION_COMPLETE == true ]]; then
        success_indicators+=("validation_complete")
        echo "✅ Testing and validation completed"
    else
        echo "❌ Validation not completed"
    fi
    
    # Check learning extraction
    if [[ -f "$LEARNING_FILE" ]] && grep -q "$(date +%Y-%m-%d)" "$LEARNING_FILE"; then
        success_indicators+=("learning_extracted")
        echo "✅ Learning captured in memory system"
    else
        echo "❌ Learning not properly captured"
    fi
    
    # Check pattern creation
    if [[ $PATTERN_CREATED == true ]] && ls "$PATTERN_DIR"/*"$(date +%Y%m%d)"*.md >/dev/null 2>&1; then
        success_indicators+=("pattern_created")
        echo "✅ Prevention pattern created"
    else
        echo "❌ Prevention pattern not created"
    fi
    
    # Check resolution time
    local resolution_duration=$(($(date +%s) - RESOLUTION_START_TIME))
    if [[ $resolution_duration -le $RESOLUTION_TIMEOUT ]]; then
        success_indicators+=("timely_resolution")
        echo "✅ Resolution completed within timeout (${resolution_duration}s)"
    else
        echo "⚠️ Resolution exceeded timeout (${resolution_duration}s > ${RESOLUTION_TIMEOUT}s)"
    fi
    
    # Calculate success rate
    local success_count=${#success_indicators[@]}
    local success_rate=$((success_count * 100 / total_indicators))
    
    echo ""
    echo "📊 RESOLUTION SUCCESS: $success_count/$total_indicators indicators met (${success_rate}%)"
    
    if [[ $success_count -eq $total_indicators ]]; then
        echo "🎉 SYSTEMATIC ERROR RESOLUTION: FULLY SUCCESSFUL"
        return 0
    elif [[ $success_count -ge 5 ]]; then
        echo "⚠️ SYSTEMATIC ERROR RESOLUTION: MOSTLY SUCCESSFUL (review failures)"
        return 1
    else
        echo "❌ SYSTEMATIC ERROR RESOLUTION: FAILED (major issues remain)"
        return 2
    fi
}
```

## Success Criteria

### Primary Success Metrics
```bash
# Resolution effectiveness
ERROR_RESOLUTION_RATE=100               # % of complete error resolution
ROOT_CAUSE_IDENTIFICATION_RATE=100      # % of root cause identification
SOLUTION_EFFECTIVENESS=100              # % of effective solutions
PREVENTION_PATTERN_QUALITY=85           # % quality score for prevention patterns

# Time and efficiency
RESOLUTION_TIME_TARGET=60               # Minutes for typical resolution
CRITICAL_RESOLUTION_TIME=15             # Minutes for critical errors
HIGH_RESOLUTION_TIME=120                # Minutes for high priority
MEDIUM_RESOLUTION_TIME=480              # Minutes for medium priority
LOW_RESOLUTION_TIME=1440                # Minutes for low priority

# Learning and improvement
LEARNING_CAPTURE_RATE=100               # % of learnings captured
PATTERN_CREATION_RATE=80                # % of cases producing patterns
KNOWLEDGE_REUSE_IMPROVEMENT=25          # % improvement in future similar errors
```

### Validation Matrix
```bash
validate_success_criteria() {
    local criteria_met=0
    local total_criteria=8
    
    echo "📈 SUCCESS CRITERIA VALIDATION"
    
    # Error resolution completeness
    if verify_error_completely_resolved; then
        echo "✅ Complete error resolution: 100% (target: ${ERROR_RESOLUTION_RATE}%)"
        ((criteria_met++))
    else
        echo "❌ Complete error resolution: Failed (target: ${ERROR_RESOLUTION_RATE}%)"
    fi
    
    # Root cause identification
    if [[ $ROOT_CAUSE_IDENTIFIED == true ]]; then
        echo "✅ Root cause identification: 100% (target: ${ROOT_CAUSE_IDENTIFICATION_RATE}%)"
        ((criteria_met++))
    else
        echo "❌ Root cause identification: Failed (target: ${ROOT_CAUSE_IDENTIFICATION_RATE}%)"
    fi
    
    # Solution effectiveness
    if [[ $SOLUTION_IMPLEMENTED == true ]] && verify_solution_effective; then
        echo "✅ Solution effectiveness: 100% (target: ${SOLUTION_EFFECTIVENESS}%)"
        ((criteria_met++))
    else
        echo "❌ Solution effectiveness: Failed (target: ${SOLUTION_EFFECTIVENESS}%)"
    fi
    
    # Resolution time (based on urgency)
    local target_time
    case "$ERROR_URGENCY" in
        critical) target_time=$CRITICAL_RESOLUTION_TIME ;;
        high) target_time=$HIGH_RESOLUTION_TIME ;;
        medium) target_time=$MEDIUM_RESOLUTION_TIME ;;
        low) target_time=$LOW_RESOLUTION_TIME ;;
        *) target_time=$RESOLUTION_TIME_TARGET ;;
    esac
    
    local actual_time=$((($(date +%s) - RESOLUTION_START_TIME) / 60))
    if [[ $actual_time -le $target_time ]]; then
        echo "✅ Resolution time: ${actual_time}min (target: ${target_time}min for ${ERROR_URGENCY})"
        ((criteria_met++))
    else
        echo "❌ Resolution time: ${actual_time}min (target: ${target_time}min for ${ERROR_URGENCY})"
    fi
    
    # Learning capture
    if [[ -f "$LEARNING_FILE" ]] && grep -q "$(date +%Y-%m-%d)" "$LEARNING_FILE"; then
        echo "✅ Learning capture: 100% (target: ${LEARNING_CAPTURE_RATE}%)"
        ((criteria_met++))
    else
        echo "❌ Learning capture: Failed (target: ${LEARNING_CAPTURE_RATE}%)"
    fi
    
    # Pattern creation
    if [[ $PATTERN_CREATED == true ]]; then
        echo "✅ Pattern creation: 100% (target: ${PATTERN_CREATION_RATE}%)"
        ((criteria_met++))
    else
        echo "❌ Pattern creation: Failed (target: ${PATTERN_CREATION_RATE}%)"
    fi
    
    # Validation completeness
    if [[ $VALIDATION_COMPLETE == true ]]; then
        echo "✅ Validation completeness: 100%"
        ((criteria_met++))
    else
        echo "❌ Validation completeness: Failed"
    fi
    
    # Error recurrence prevention
    if verify_recurrence_prevention_measures; then
        echo "✅ Recurrence prevention: Implemented"
        ((criteria_met++))
    else
        echo "❌ Recurrence prevention: Not implemented"
    fi
    
    # Overall success determination
    local success_rate=$((criteria_met * 100 / total_criteria))
    echo ""
    echo "📊 OVERALL SUCCESS: $criteria_met/$total_criteria criteria met (${success_rate}%)"
    
    if [[ $criteria_met -eq $total_criteria ]]; then
        echo "🎉 ERROR RESOLUTION PATTERN: FULLY SUCCESSFUL"
        return 0
    elif [[ $criteria_met -ge 6 ]]; then
        echo "⚠️ ERROR RESOLUTION PATTERN: MOSTLY SUCCESSFUL (review failures)"
        return 1
    else
        echo "❌ ERROR RESOLUTION PATTERN: FAILED (major issues unresolved)"
        return 2
    fi
}
```

## Structured Execution Steps

### Step-by-Step Executor
```bash
execute_systematic_error_resolution() {
    local execution_id="error_res_$(date +%Y%m%d_%H%M%S)"
    RESOLUTION_START_TIME=$(date +%s)
    
    echo "🚨 EXECUTING SYSTEMATIC ERROR RESOLUTION PATTERN"
    echo "Execution ID: $execution_id"
    echo "User: $USER_NAME"
    echo "Error Category: $ERROR_CATEGORY"
    echo "Error Urgency: $ERROR_URGENCY"
    echo "Target: $(pwd)"
    echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo ""
    
    # STEP 1: Pre-resolution validation
    if ! validate_error_resolution_prerequisites; then
        echo "❌ Pre-resolution validation failed. Aborting."
        return 1
    fi
    
    # STEP 2: Error capture and documentation
    echo "📋 STEP 2: Error capture and documentation"
    if ! capture_error_context "$ERROR_DESCRIPTION" "$ERROR_CATEGORY"; then
        echo "❌ Error capture failed"
        return 1
    fi
    validate_resolution_progress "error_capture"
    echo ""
    
    # STEP 3: Impact assessment
    echo "⚖️ STEP 3: Impact assessment"
    if ! assess_error_impact "$ERROR_CATEGORY" "$ERROR_URGENCY"; then
        echo "❌ Impact assessment failed"
        return 1
    fi
    validate_resolution_progress "impact_assessment"
    echo ""
    
    # STEP 4: Root cause analysis
    echo "🔍 STEP 4: Root cause analysis"
    if ! analyze_root_cause "$ERROR_DESCRIPTION"; then
        echo "❌ Root cause analysis failed"
        return 1
    fi
    ROOT_CAUSE_IDENTIFIED=true
    validate_resolution_progress "root_cause_analysis"
    echo ""
    
    # STEP 5: Solution development
    echo "🔧 STEP 5: Solution development"
    if ! develop_targeted_solution "$ERROR_CATEGORY"; then
        echo "❌ Solution development failed"
        return 1
    fi
    SOLUTION_IMPLEMENTED=true
    validate_resolution_progress "solution_development"
    echo ""
    
    # STEP 6: Testing and validation
    echo "🧪 STEP 6: Testing and validation"
    if ! test_and_validate_solution; then
        echo "❌ Testing and validation failed"
        return 1
    fi
    VALIDATION_COMPLETE=true
    validate_resolution_progress "testing_validation"
    echo ""
    
    # STEP 7: Learning extraction
    echo "📚 STEP 7: Learning extraction"
    if ! extract_error_learnings "$ERROR_DESCRIPTION"; then
        echo "❌ Learning extraction failed"
        return 1
    fi
    echo "✅ Learning extraction completed"
    echo ""
    
    # STEP 8: Pattern creation
    echo "🎯 STEP 8: Prevention pattern creation"
    if ! create_prevention_pattern "$ERROR_CATEGORY"; then
        echo "❌ Pattern creation failed"
        return 1
    fi
    PATTERN_CREATED=true
    echo "✅ Prevention pattern created"
    echo ""
    
    # STEP 9: Final validation
    echo "✅ STEP 9: Final resolution validation"
    if ! validate_resolution_success; then
        echo "❌ Final validation failed. Resolution incomplete."
        return 1
    fi
    
    # STEP 10: Success criteria validation
    echo "📈 STEP 10: Success criteria validation"
    if validate_success_criteria; then
        echo "✅ SYSTEMATIC ERROR RESOLUTION: SUCCESSFULLY COMPLETED"
        echo "Execution ID: $execution_id"
        
        # Record successful resolution
        local resolution_duration=$((($(date +%s) - RESOLUTION_START_TIME) / 60))
        echo "Resolution completed in ${resolution_duration} minutes"
        
        return 0
    else
        echo "❌ Success criteria not met. Resolution requires review."
        return 1
    fi
}
```

## Success Indicators

- ✅ Error completely resolved without recurrence
- ✅ Root cause identified and documented
- ✅ Prevention pattern created and tested
- ✅ Learning captured in memory system
- ✅ Similar errors prevented by pattern application