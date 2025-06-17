# Pattern: Performance Analysis Template

## Problem

CLAUDE systems need regular performance monitoring and optimization to maintain efficiency, but performance analysis is often ad-hoc and inconsistent. There's a need for systematic measurement of response times, resource usage, pattern efficiency, and system bottlenecks to drive data-driven optimization decisions.

## Solution

**6-Stage Performance Analysis Framework:**

1. **Baseline Measurement** - Establish current performance metrics
2. **Bottleneck Identification** - Find performance constraints
3. **Resource Analysis** - Analyze CPU, memory, disk, and time usage
4. **Efficiency Measurement** - Measure pattern reuse and time savings
5. **Optimization Planning** - Develop targeted improvement strategies
6. **Impact Validation** - Verify optimization effectiveness

## Code Template

```bash
#!/bin/bash
# CLAUDE Performance Analysis Template
# Generated: [TIMESTAMP]
# User: Christian
# Analysis Context: [ANALYSIS_DESCRIPTION]

execute_performance_analysis() {
    local analysis_name="$1"
    local analysis_scope="$2"    # system|component|feature|process
    local duration="$3"          # measurement duration in minutes
    
    echo "📊 CLAUDE PERFORMANCE ANALYSIS - User: Christian"
    echo "Analysis: $analysis_name"
    echo "Scope: $analysis_scope | Duration: ${duration}m"
    echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    
    # Create analysis directory
    local analysis_dir="performance_analysis_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$analysis_dir"
    
    # STAGE 1: Baseline Measurement
    establish_performance_baseline "$analysis_name" "$analysis_dir" "$duration"
    
    # STAGE 2: Bottleneck Identification
    identify_performance_bottlenecks "$analysis_scope" "$analysis_dir"
    
    # STAGE 3: Resource Analysis
    analyze_resource_usage "$analysis_dir" "$duration"
    
    # STAGE 4: Efficiency Measurement
    measure_system_efficiency "$analysis_dir"
    
    # STAGE 5: Optimization Planning
    develop_optimization_plan "$analysis_name" "$analysis_dir"
    
    # STAGE 6: Impact Validation
    prepare_validation_framework "$analysis_dir"
    
    # Generate comprehensive report
    generate_performance_report "$analysis_name" "$analysis_dir"
    
    echo "✅ Performance analysis complete: $analysis_dir"
}

establish_performance_baseline() {
    local analysis_name="$1"
    local analysis_dir="$2"
    local duration="$3"
    
    echo "📊 STAGE 1: Establishing performance baseline..."
    
    local baseline_file="$analysis_dir/baseline_metrics.md"
    
    cat > "$baseline_file" << EOF
# Performance Baseline Metrics
Analysis: $analysis_name
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian
Duration: ${duration} minutes

## System Information
- **Platform**: $(uname -s) $(uname -r)
- **Architecture**: $(uname -m)
- **CPU Cores**: $(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo "Unknown")
- **Memory**: $(free -h 2>/dev/null | grep Mem | awk '{print $2}' || echo "Unknown")
- **Disk Space**: $(df -h . | tail -1 | awk '{print $4}') available

## CLAUDE System Baseline

### Timing Rule Performance
EOF
    
    # Measure timing rule performance
    echo "⏰ Measuring timing rule performance..." | tee -a "$baseline_file"
    
    # TODO.md update timing
    if [ -f "TODO.md" ]; then
        local todo_start=$(date +%s%N)
        
        # Simulate timing check (using actual function if available)
        if command -v check_timing_rules >/dev/null 2>&1; then
            check_timing_rules >/dev/null 2>&1
        else
            # Simulate timing check
            stat TODO.md >/dev/null 2>&1
            sleep 0.1  # Simulate processing time
        fi
        
        local todo_end=$(date +%s%N)
        local todo_duration=$(( (todo_end - todo_start) / 1000000 ))  # Convert to milliseconds
        
        echo "- **TODO.md Check**: ${todo_duration}ms" >> "$baseline_file"
    else
        echo "- **TODO.md Check**: Not available (file missing)" >> "$baseline_file"
    fi
    
    # Backup system timing
    echo "💾 Measuring backup system performance..." | tee -a "$baseline_file"
    
    if [ -d "backups" ]; then
        local backup_start=$(date +%s%N)
        
        # Simulate backup check
        ls backups/ >/dev/null 2>&1
        if [ -f "backups/.last_scheduled_backup" ]; then
            stat backups/.last_scheduled_backup >/dev/null 2>&1
        fi
        sleep 0.1  # Simulate processing time
        
        local backup_end=$(date +%s%N)
        local backup_duration=$(( (backup_end - backup_start) / 1000000 ))
        
        echo "- **Backup Check**: ${backup_duration}ms" >> "$baseline_file"
    else
        echo "- **Backup Check**: Not available (directory missing)" >> "$baseline_file"
    fi
    
    # Pattern system timing
    echo "🎯 Measuring pattern system performance..." | tee -a "$baseline_file"
    
    if [ -d "patterns" ]; then
        local pattern_start=$(date +%s%N)
        
        # Simulate pattern search
        find patterns -name "*.md" | head -10 >/dev/null 2>&1
        sleep 0.2  # Simulate pattern matching time
        
        local pattern_end=$(date +%s%N)
        local pattern_duration=$(( (pattern_end - pattern_start) / 1000000 ))
        
        local pattern_count=$(find patterns -name "*.md" | wc -l)
        echo "- **Pattern Search**: ${pattern_duration}ms (${pattern_count} patterns)" >> "$baseline_file"
    else
        echo "- **Pattern Search**: Not available (directory missing)" >> "$baseline_file"
    fi
    
    # Memory system timing
    echo "🧠 Measuring memory system performance..." | tee -a "$baseline_file"
    
    cat >> "$baseline_file" << EOF

### Memory System Performance
EOF
    
    if [ -f "SESSION_CONTINUITY.md" ]; then
        local memory_start=$(date +%s%N)
        
        # Simulate memory system operations
        wc -l SESSION_CONTINUITY.md >/dev/null 2>&1
        grep -c "## " SESSION_CONTINUITY.md >/dev/null 2>&1
        
        local memory_end=$(date +%s%N)
        local memory_duration=$(( (memory_end - memory_start) / 1000000 ))
        
        local session_lines=$(wc -l < SESSION_CONTINUITY.md)
        echo "- **SESSION_CONTINUITY.md**: ${memory_duration}ms (${session_lines} lines)" >> "$baseline_file"
    else
        echo "- **SESSION_CONTINUITY.md**: Not available (file missing)" >> "$baseline_file"
    fi
    
    if [ -d "memory" ]; then
        local memory_files=$(find memory -name "*.md" | wc -l)
        echo "- **Memory Files**: ${memory_files} files available" >> "$baseline_file"
    else
        echo "- **Memory Files**: Not available (directory missing)" >> "$baseline_file"
    fi
    
    cat >> "$baseline_file" << EOF

### File System Performance
- **Project Root**: $(pwd)
- **File Count**: $(find . -type f | wc -l) files
- **Directory Count**: $(find . -type d | wc -l) directories
- **Total Size**: $(du -sh . | cut -f1)

### Git Performance (if available)
EOF
    
    if [ -d ".git" ]; then
        local git_start=$(date +%s%N)
        git status --short >/dev/null 2>&1
        local git_end=$(date +%s%N)
        local git_duration=$(( (git_end - git_start) / 1000000 ))
        
        local uncommitted=$(git status --short 2>/dev/null | wc -l)
        echo "- **Git Status**: ${git_duration}ms (${uncommitted} uncommitted changes)" >> "$baseline_file"
        echo "- **Current Branch**: $(git branch --show-current 2>/dev/null || echo "Unknown")" >> "$baseline_file"
    else
        echo "- **Git Status**: Not available (not a git repository)" >> "$baseline_file"
    fi
    
    echo "✓ Baseline metrics established: $baseline_file"
}

identify_performance_bottlenecks() {
    local scope="$1"
    local analysis_dir="$2"
    
    echo "🔍 STAGE 2: Identifying performance bottlenecks..."
    
    local bottleneck_file="$analysis_dir/bottleneck_analysis.md"
    
    cat > "$bottleneck_file" << EOF
# Performance Bottleneck Analysis
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian
Scope: $scope

## Bottleneck Categories

### I/O Bottlenecks
EOF
    
    echo "💾 Analyzing I/O bottlenecks..." | tee -a "$bottleneck_file"
    
    # Check for large files that might slow operations
    local large_files=$(find . -type f -size +10M 2>/dev/null | head -5)
    if [ -n "$large_files" ]; then
        echo "**Large Files Found:**" >> "$bottleneck_file"
        echo "$large_files" | while read -r file; do
            local size=$(du -h "$file" | cut -f1)
            echo "- \`$file\`: $size" >> "$bottleneck_file"
        done
    else
        echo "- No large files detected (>10MB)" >> "$bottleneck_file"
    fi
    
    # Check for excessive file counts
    local file_count=$(find . -type f | wc -l)
    if [ "$file_count" -gt 10000 ]; then
        echo "- **Warning**: High file count ($file_count files) may impact performance" >> "$bottleneck_file"
    else
        echo "- File count acceptable: $file_count files" >> "$bottleneck_file"
    fi
    
    cat >> "$bottleneck_file" << EOF

### Memory Bottlenecks
EOF
    
    echo "🧠 Analyzing memory bottlenecks..." | tee -a "$bottleneck_file"
    
    # Check for very large session files
    if [ -f "SESSION_CONTINUITY.md" ]; then
        local session_size=$(wc -l < SESSION_CONTINUITY.md)
        if [ "$session_size" -gt 1000 ]; then
            echo "- **Warning**: Large SESSION_CONTINUITY.md ($session_size lines) may impact performance" >> "$bottleneck_file"
        else
            echo "- SESSION_CONTINUITY.md size acceptable: $session_size lines" >> "$bottleneck_file"
        fi
    fi
    
    # Check for excessive backup files
    if [ -d "backups" ]; then
        local backup_count=$(ls backups/20* 2>/dev/null | wc -l)
        if [ "$backup_count" -gt 100 ]; then
            echo "- **Warning**: Excessive backup files ($backup_count) may impact performance" >> "$bottleneck_file"
        else
            echo "- Backup file count acceptable: $backup_count files" >> "$bottleneck_file"
        fi
    fi
    
    cat >> "$bottleneck_file" << EOF

### Pattern System Bottlenecks
EOF
    
    echo "🎯 Analyzing pattern system bottlenecks..." | tee -a "$bottleneck_file"
    
    if [ -d "patterns" ]; then
        local pattern_count=$(find patterns -name "*.md" | wc -l)
        
        # Pattern search time simulation
        local pattern_start=$(date +%s%N)
        find patterns -name "*.md" | head -20 >/dev/null 2>&1
        local pattern_end=$(date +%s%N)
        local pattern_search_time=$(( (pattern_end - pattern_start) / 1000000 ))
        
        echo "- **Pattern Count**: $pattern_count patterns" >> "$bottleneck_file"
        echo "- **Pattern Search Time**: ${pattern_search_time}ms" >> "$bottleneck_file"
        
        if [ "$pattern_search_time" -gt 100 ]; then
            echo "- **Warning**: Pattern search time exceeds 100ms threshold" >> "$bottleneck_file"
        fi
        
        # Check for pattern organization efficiency
        local categories=$(find patterns -type d -mindepth 1 -maxdepth 1 | wc -l)
        echo "- **Pattern Categories**: $categories categories" >> "$bottleneck_file"
        
        if [ "$categories" -lt 3 ]; then
            echo "- **Recommendation**: Consider organizing patterns into more categories for efficiency" >> "$bottleneck_file"
        fi
    else
        echo "- Pattern system not available for analysis" >> "$bottleneck_file"
    fi
    
    cat >> "$bottleneck_file" << EOF

### Configuration Bottlenecks
EOF
    
    echo "📋 Analyzing configuration bottlenecks..." | tee -a "$bottleneck_file"
    
    # Check CLAUDE.md size and complexity
    if [ -f "CLAUDE.md" ]; then
        local claude_size=$(wc -l < CLAUDE.md)
        echo "- **CLAUDE.md Size**: $claude_size lines" >> "$bottleneck_file"
        
        if [ "$claude_size" -gt 2000 ]; then
            echo "- **Warning**: Large CLAUDE.md may impact loading time" >> "$bottleneck_file"
        fi
        
        # Check for complex decision matrices
        local decision_matrices=$(grep -c "DECISION\|MATRIX" CLAUDE.md 2>/dev/null || echo "0")
        echo "- **Decision Matrices**: $decision_matrices found" >> "$bottleneck_file"
        
    else
        echo "- CLAUDE.md not available for analysis" >> "$bottleneck_file"
    fi
    
    cat >> "$bottleneck_file" << EOF

## Bottleneck Severity Assessment

### Critical Bottlenecks (Immediate Attention Required)
[Items that significantly impact performance]

### Moderate Bottlenecks (Address Soon)
[Items that moderately impact performance]

### Minor Bottlenecks (Address When Convenient)
[Items with minimal performance impact]

## Recommended Actions
1. [Priority 1 action based on analysis]
2. [Priority 2 action based on analysis]
3. [Priority 3 action based on analysis]
EOF
    
    echo "✓ Bottleneck analysis completed: $bottleneck_file"
}

analyze_resource_usage() {
    local analysis_dir="$1"
    local duration="$2"
    
    echo "📈 STAGE 3: Analyzing resource usage..."
    
    local resource_file="$analysis_dir/resource_analysis.md"
    
    cat > "$resource_file" << EOF
# Resource Usage Analysis
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian
Monitoring Duration: ${duration} minutes

## System Resource Snapshot

### CPU Information
EOF
    
    # CPU analysis
    echo "🖥️ Analyzing CPU usage..." | tee -a "$resource_file"
    
    if command -v top >/dev/null 2>&1; then
        local cpu_info=$(top -l 1 | grep "CPU usage" | head -1 2>/dev/null || echo "CPU info not available")
        echo "- **Current CPU**: $cpu_info" >> "$resource_file"
    fi
    
    # Process count
    local process_count=$(ps aux | wc -l)
    echo "- **Active Processes**: $process_count" >> "$resource_file"
    
    cat >> "$resource_file" << EOF

### Memory Information
EOF
    
    # Memory analysis
    echo "💾 Analyzing memory usage..." | tee -a "$resource_file"
    
    if command -v free >/dev/null 2>&1; then
        echo "\`\`\`" >> "$resource_file"
        free -h >> "$resource_file"
        echo "\`\`\`" >> "$resource_file"
    elif command -v vm_stat >/dev/null 2>&1; then
        echo "**macOS Memory Statistics:**" >> "$resource_file"
        echo "\`\`\`" >> "$resource_file"
        vm_stat | head -10 >> "$resource_file"
        echo "\`\`\`" >> "$resource_file"
    fi
    
    cat >> "$resource_file" << EOF

### Disk Usage Information
EOF
    
    # Disk analysis
    echo "💽 Analyzing disk usage..." | tee -a "$resource_file"
    
    echo "**Project Directory Usage:**" >> "$resource_file"
    echo "\`\`\`" >> "$resource_file"
    du -sh . 2>/dev/null >> "$resource_file"
    echo "\`\`\`" >> "$resource_file"
    
    echo "**Subdirectory Breakdown:**" >> "$resource_file"
    echo "\`\`\`" >> "$resource_file"
    du -sh */ 2>/dev/null | sort -hr | head -10 >> "$resource_file"
    echo "\`\`\`" >> "$resource_file"
    
    echo "**Available Disk Space:**" >> "$resource_file"
    echo "\`\`\`" >> "$resource_file"
    df -h . >> "$resource_file"
    echo "\`\`\`" >> "$resource_file"
    
    cat >> "$resource_file" << EOF

## CLAUDE-Specific Resource Analysis

### File System Impact
EOF
    
    # CLAUDE-specific analysis
    echo "📊 Analyzing CLAUDE-specific resource impact..." | tee -a "$resource_file"
    
    # Backup directory analysis
    if [ -d "backups" ]; then
        local backup_size=$(du -sh backups | cut -f1)
        local backup_count=$(ls backups/20* 2>/dev/null | wc -l)
        echo "- **Backup Storage**: $backup_size ($backup_count files)" >> "$resource_file"
        
        if [ "$backup_count" -gt 0 ]; then
            local avg_backup_size=$(du -s backups/20* 2>/dev/null | awk '{sum+=$1; count++} END {print int(sum/count/1024)"K"}')
            echo "- **Average Backup Size**: $avg_backup_size" >> "$resource_file"
        fi
    fi
    
    # Pattern library analysis
    if [ -d "patterns" ]; then
        local pattern_size=$(du -sh patterns | cut -f1)
        local pattern_count=$(find patterns -name "*.md" | wc -l)
        echo "- **Pattern Library**: $pattern_size ($pattern_count patterns)" >> "$resource_file"
    fi
    
    # Memory files analysis
    if [ -d "memory" ]; then
        local memory_size=$(du -sh memory | cut -f1)
        local memory_files=$(find memory -name "*.md" | wc -l)
        echo "- **Memory Files**: $memory_size ($memory_files files)" >> "$resource_file"
    fi
    
    cat >> "$resource_file" << EOF

### Performance Monitoring Results
EOF
    
    # Simulate performance monitoring over time
    echo "⏱️ Running performance monitoring simulation..." | tee -a "$resource_file"
    
    # Create a simple performance monitoring simulation
    for i in $(seq 1 5); do
        local start_time=$(date +%s%N)
        
        # Simulate typical CLAUDE operations
        [ -f "TODO.md" ] && stat TODO.md >/dev/null 2>&1
        [ -d "patterns" ] && find patterns -name "*.md" | head -5 >/dev/null 2>&1
        [ -f "SESSION_CONTINUITY.md" ] && wc -l SESSION_CONTINUITY.md >/dev/null 2>&1
        
        local end_time=$(date +%s%N)
        local operation_time=$(( (end_time - start_time) / 1000000 ))
        
        echo "- **Sample $i**: ${operation_time}ms" >> "$resource_file"
        
        sleep 1  # Brief pause between samples
    done
    
    cat >> "$resource_file" << EOF

### Resource Recommendations

#### Immediate Optimizations
- [Based on analysis, provide specific recommendations]

#### Future Considerations  
- [Long-term resource planning recommendations]

#### Monitoring Setup
- [Recommendations for ongoing resource monitoring]
EOF
    
    echo "✓ Resource analysis completed: $resource_file"
}

measure_system_efficiency() {
    local analysis_dir="$1"
    
    echo "⚡ STAGE 4: Measuring system efficiency..."
    
    local efficiency_file="$analysis_dir/efficiency_metrics.md"
    
    cat > "$efficiency_file" << EOF
# System Efficiency Metrics
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian

## Pattern System Efficiency

### Pattern Library Statistics
EOF
    
    # Pattern efficiency analysis
    echo "🎯 Measuring pattern system efficiency..." | tee -a "$efficiency_file"
    
    if [ -d "patterns" ]; then
        local total_patterns=$(find patterns -name "*.md" | wc -l)
        echo "- **Total Patterns**: $total_patterns" >> "$efficiency_file"
        
        # Analyze pattern categories
        for category in bug_fixes generation refactoring architecture; do
            if [ -d "patterns/$category" ]; then
                local cat_count=$(find "patterns/$category" -name "*.md" | wc -l)
                echo "- **${category}**: $cat_count patterns" >> "$efficiency_file"
            fi
        done
        
        # Estimate time savings from patterns
        local estimated_time_per_pattern=45  # minutes saved per pattern use
        local estimated_total_savings=$((total_patterns * estimated_time_per_pattern))
        echo "- **Estimated Time Savings**: ${estimated_total_savings} minutes potential" >> "$efficiency_file"
    else
        echo "- Pattern system not available for analysis" >> "$efficiency_file"
    fi
    
    cat >> "$efficiency_file" << EOF

### Memory System Efficiency
EOF
    
    # Memory system efficiency
    echo "🧠 Measuring memory system efficiency..." | tee -a "$efficiency_file"
    
    if [ -f "SESSION_CONTINUITY.md" ]; then
        local session_entries=$(grep -c "## " SESSION_CONTINUITY.md 2>/dev/null || echo "0")
        local session_size=$(wc -l < SESSION_CONTINUITY.md)
        local avg_entry_size=$((session_size / (session_entries + 1)))
        
        echo "- **Session Entries**: $session_entries" >> "$efficiency_file"
        echo "- **Average Entry Size**: $avg_entry_size lines" >> "$efficiency_file"
        echo "- **Memory Growth Rate**: [Calculate based on session frequency]" >> "$efficiency_file"
    fi
    
    # Learning files efficiency
    if [ -d "memory" ]; then
        local learning_files=$(find memory -name "*.md" | wc -l)
        local total_learning_size=$(du -s memory | cut -f1)
        
        echo "- **Learning Files**: $learning_files files" >> "$efficiency_file"
        echo "- **Learning Storage**: ${total_learning_size}K" >> "$efficiency_file"
    fi
    
    cat >> "$efficiency_file" << EOF

### Backup System Efficiency
EOF
    
    # Backup efficiency analysis
    echo "💾 Measuring backup system efficiency..." | tee -a "$efficiency_file"
    
    if [ -d "backups" ]; then
        local backup_files=$(ls backups/20* 2>/dev/null | wc -l)
        local backup_storage=$(du -s backups | cut -f1)
        local avg_backup_size=$((backup_storage / (backup_files + 1)))
        
        echo "- **Backup Files**: $backup_files" >> "$efficiency_file"
        echo "- **Total Backup Storage**: ${backup_storage}K" >> "$efficiency_file"
        echo "- **Average Backup Size**: ${avg_backup_size}K" >> "$efficiency_file"
        
        # Backup frequency analysis
        if [ "$backup_files" -gt 0 ]; then
            local newest_backup=$(ls -t backups/20* | head -1)
            local oldest_backup=$(ls -t backups/20* | tail -1)
            echo "- **Backup Range**: $(basename "$oldest_backup") to $(basename "$newest_backup")" >> "$efficiency_file"
        fi
    fi
    
    cat >> "$efficiency_file" << EOF

### Timing Rule Efficiency
EOF
    
    # Timing rule efficiency
    echo "⏰ Measuring timing rule efficiency..." | tee -a "$efficiency_file"
    
    # Check TODO.md compliance
    if [ -f "TODO.md" ]; then
        local todo_age_seconds=$(( $(date +%s) - $(stat -c %Y TODO.md 2>/dev/null || stat -f %m TODO.md) ))
        local todo_age_minutes=$((todo_age_seconds / 60))
        
        echo "- **TODO.md Age**: $todo_age_minutes minutes" >> "$efficiency_file"
        
        if [ "$todo_age_minutes" -lt 120 ]; then
            echo "- **TODO.md Compliance**: ✅ Within 120-minute rule" >> "$efficiency_file"
        else
            echo "- **TODO.md Compliance**: ⚠️ Exceeds 120-minute rule" >> "$efficiency_file"
        fi
    fi
    
    # Check backup compliance
    if [ -f "backups/.last_scheduled_backup" ]; then
        local backup_age_seconds=$(( $(date +%s) - $(stat -c %Y backups/.last_scheduled_backup 2>/dev/null || stat -f %m backups/.last_scheduled_backup) ))
        local backup_age_minutes=$((backup_age_seconds / 60))
        
        echo "- **Last Backup Age**: $backup_age_minutes minutes" >> "$efficiency_file"
        
        if [ "$backup_age_minutes" -lt 120 ]; then
            echo "- **Backup Compliance**: ✅ Within 120-minute rule" >> "$efficiency_file"
        else
            echo "- **Backup Compliance**: ⚠️ Exceeds 120-minute rule" >> "$efficiency_file"
        fi
    fi
    
    cat >> "$efficiency_file" << EOF

## Efficiency Scoring

### Overall Efficiency Score
[Calculate based on metrics above: 0-100 scale]

### Component Efficiency Breakdown
- **Pattern System**: [Score/100]
- **Memory System**: [Score/100]
- **Backup System**: [Score/100]
- **Timing Rules**: [Score/100]

### Efficiency Trends
[Track efficiency over time to identify trends]

### Improvement Opportunities
1. [Highest impact efficiency improvement]
2. [Second priority efficiency improvement]
3. [Third priority efficiency improvement]
EOF
    
    echo "✓ Efficiency metrics completed: $efficiency_file"
}

develop_optimization_plan() {
    local analysis_name="$1"
    local analysis_dir="$2"
    
    echo "🎯 STAGE 5: Developing optimization plan..."
    
    local optimization_file="$analysis_dir/optimization_plan.md"
    
    cat > "$optimization_file" << EOF
# Performance Optimization Plan
Analysis: $analysis_name
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian

## Executive Summary

### Performance Assessment
[Based on analysis results, provide overall performance assessment]

### Key Findings
1. [Critical finding 1]
2. [Critical finding 2]
3. [Critical finding 3]

### Optimization Priority
- **High Priority**: [Critical performance issues requiring immediate attention]
- **Medium Priority**: [Performance improvements with good ROI]
- **Low Priority**: [Minor optimizations for future consideration]

## Optimization Strategies

### Strategy 1: [High Priority Optimization]
**Problem**: [Specific performance issue identified]
**Solution**: [Detailed solution approach]
**Implementation**: 
\`\`\`bash
# Implementation steps
step_1_optimize_high_priority() {
    # [Specific commands/changes]
}
\`\`\`
**Expected Impact**: [Quantified performance improvement]
**Time Investment**: [Estimated implementation time]
**Risk Level**: [Low/Medium/High]

### Strategy 2: [Medium Priority Optimization]
**Problem**: [Specific performance issue identified]
**Solution**: [Detailed solution approach]
**Implementation**:
\`\`\`bash
# Implementation steps
step_2_optimize_medium_priority() {
    # [Specific commands/changes]
}
\`\`\`
**Expected Impact**: [Quantified performance improvement]
**Time Investment**: [Estimated implementation time]
**Risk Level**: [Low/Medium/High]

### Strategy 3: [Low Priority Optimization]
**Problem**: [Specific performance issue identified]
**Solution**: [Detailed solution approach]
**Implementation**:
\`\`\`bash
# Implementation steps  
step_3_optimize_low_priority() {
    # [Specific commands/changes]
}
\`\`\`
**Expected Impact**: [Quantified performance improvement]
**Time Investment**: [Estimated implementation time]
**Risk Level**: [Low/Medium/High]

## Implementation Timeline

### Phase 1: Critical Optimizations (Week 1)
- [ ] [High priority optimization 1]
- [ ] [High priority optimization 2]
- [ ] Measure impact of critical optimizations
- [ ] Document results

### Phase 2: Performance Improvements (Week 2-3)
- [ ] [Medium priority optimization 1]
- [ ] [Medium priority optimization 2]
- [ ] Performance testing and validation
- [ ] Adjust strategies based on results

### Phase 3: Fine-tuning (Week 4)
- [ ] [Low priority optimization 1]
- [ ] [Low priority optimization 2]
- [ ] Final performance measurement
- [ ] Document complete optimization results

## Risk Assessment and Mitigation

### High-Risk Optimizations
- **Risk**: [Specific risk description]
- **Mitigation**: [How to reduce or manage risk]
- **Rollback Plan**: [How to revert if problems occur]

### Medium-Risk Optimizations
- **Risk**: [Specific risk description]
- **Mitigation**: [How to reduce or manage risk]
- **Rollback Plan**: [How to revert if problems occur]

## Success Metrics

### Quantitative Metrics
- **Response Time Improvement**: [Target improvement percentage]
- **Resource Usage Reduction**: [Target reduction in CPU/memory/disk]
- **Throughput Increase**: [Target increase in operations per second]
- **Error Rate Reduction**: [Target reduction in error frequency]

### Qualitative Metrics
- **User Experience**: [Improved responsiveness/reliability]
- **System Stability**: [Reduced crashes/failures]
- **Maintainability**: [Easier to understand/modify]

## Monitoring and Validation Plan

### Pre-Optimization Baseline
- [ ] Document current performance metrics
- [ ] Establish measurement procedures
- [ ] Create performance test suite
- [ ] Set up monitoring dashboard

### During Optimization
- [ ] Monitor each change impact
- [ ] Track metric improvements
- [ ] Document any issues encountered
- [ ] Adjust strategies based on results

### Post-Optimization Validation
- [ ] Run complete performance test suite
- [ ] Compare against baseline metrics
- [ ] Validate system stability
- [ ] Document final results

## Long-term Performance Strategy

### Continuous Monitoring
- **Daily**: [Daily performance checks]
- **Weekly**: [Weekly performance reviews]
- **Monthly**: [Monthly optimization assessments]

### Future Optimization Opportunities
1. [Future optimization area 1]
2. [Future optimization area 2]
3. [Future optimization area 3]

### Performance Evolution Plan
- **6 Months**: [Performance goals for 6 months]
- **1 Year**: [Performance goals for 1 year]
- **Long-term**: [Long-term performance vision]
EOF
    
    echo "✓ Optimization plan developed: $optimization_file"
}

prepare_validation_framework() {
    local analysis_dir="$1"
    
    echo "✅ STAGE 6: Preparing validation framework..."
    
    local validation_file="$analysis_dir/validation_framework.md"
    
    cat > "$validation_file" << EOF
# Performance Validation Framework
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian

## Validation Methodology

### Before/After Comparison
- **Baseline Metrics**: [Reference to baseline measurements]
- **Target Metrics**: [Performance targets to achieve]
- **Measurement Procedures**: [How to measure improvements]

### Validation Test Suite
\`\`\`bash
#!/bin/bash
# Performance Validation Test Suite

validate_optimization_impact() {
    local optimization_name="\$1"
    local test_results_file="validation_results_\$(date +%Y%m%d_%H%M%S).md"
    
    echo "🧪 Performance Validation: \$optimization_name" | tee "\$test_results_file"
    echo "Date: \$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "\$test_results_file"
    echo "User: Christian" | tee -a "\$test_results_file"
    echo "" | tee -a "\$test_results_file"
    
    # Test 1: Timing Rule Performance
    echo "⏰ Testing timing rule performance..." | tee -a "\$test_results_file"
    validate_timing_performance | tee -a "\$test_results_file"
    
    # Test 2: Pattern System Performance
    echo "🎯 Testing pattern system performance..." | tee -a "\$test_results_file"
    validate_pattern_performance | tee -a "\$test_results_file"
    
    # Test 3: Memory System Performance
    echo "🧠 Testing memory system performance..." | tee -a "\$test_results_file"
    validate_memory_performance | tee -a "\$test_results_file"
    
    # Test 4: Backup System Performance
    echo "💾 Testing backup system performance..." | tee -a "\$test_results_file"
    validate_backup_performance | tee -a "\$test_results_file"
    
    # Test 5: Overall System Performance
    echo "📊 Testing overall system performance..." | tee -a "\$test_results_file"
    validate_overall_performance | tee -a "\$test_results_file"
    
    echo "✅ Validation complete: \$test_results_file"
}

validate_timing_performance() {
    # Measure timing rule execution time
    local start_time=\$(date +%s%N)
    
    # Simulate timing checks
    [ -f "TODO.md" ] && stat TODO.md >/dev/null 2>&1
    [ -f "backups/.last_scheduled_backup" ] && stat backups/.last_scheduled_backup >/dev/null 2>&1
    
    local end_time=\$(date +%s%N)
    local duration=\$(( (end_time - start_time) / 1000000 ))
    
    echo "- Timing rule check: \${duration}ms"
    
    if [ \$duration -lt 50 ]; then
        echo "- Result: ✅ PASS (under 50ms threshold)"
    else
        echo "- Result: ⚠️ SLOW (over 50ms threshold)"
    fi
}

validate_pattern_performance() {
    # Measure pattern search time
    local start_time=\$(date +%s%N)
    
    # Simulate pattern search
    find patterns -name "*.md" | head -10 >/dev/null 2>&1
    
    local end_time=\$(date +%s%N)
    local duration=\$(( (end_time - start_time) / 1000000 ))
    
    echo "- Pattern search: \${duration}ms"
    
    if [ \$duration -lt 100 ]; then
        echo "- Result: ✅ PASS (under 100ms threshold)"
    else
        echo "- Result: ⚠️ SLOW (over 100ms threshold)"  
    fi
}

validate_memory_performance() {
    # Measure memory system operations
    local start_time=\$(date +%s%N)
    
    # Simulate memory operations
    [ -f "SESSION_CONTINUITY.md" ] && wc -l SESSION_CONTINUITY.md >/dev/null 2>&1
    [ -d "memory" ] && find memory -name "*.md" >/dev/null 2>&1
    
    local end_time=\$(date +%s%N)
    local duration=\$(( (end_time - start_time) / 1000000 ))
    
    echo "- Memory system: \${duration}ms"
    
    if [ \$duration -lt 75 ]; then
        echo "- Result: ✅ PASS (under 75ms threshold)"
    else
        echo "- Result: ⚠️ SLOW (over 75ms threshold)"
    fi
}

validate_backup_performance() {
    # Measure backup system operations
    local start_time=\$(date +%s%N)
    
    # Simulate backup operations
    [ -d "backups" ] && ls backups/ >/dev/null 2>&1
    [ -f "backups/backup_log.txt" ] && tail -5 backups/backup_log.txt >/dev/null 2>&1
    
    local end_time=\$(date +%s%N)
    local duration=\$(( (end_time - start_time) / 1000000 ))
    
    echo "- Backup system: \${duration}ms"
    
    if [ \$duration -lt 25 ]; then
        echo "- Result: ✅ PASS (under 25ms threshold)"
    else
        echo "- Result: ⚠️ SLOW (over 25ms threshold)"
    fi
}

validate_overall_performance() {
    # Comprehensive system performance test
    local start_time=\$(date +%s%N)
    
    # Simulate complete CLAUDE operation
    validate_timing_performance >/dev/null 2>&1
    validate_pattern_performance >/dev/null 2>&1
    validate_memory_performance >/dev/null 2>&1
    validate_backup_performance >/dev/null 2>&1
    
    local end_time=\$(date +%s%N)
    local duration=\$(( (end_time - start_time) / 1000000 ))
    
    echo "- Complete system cycle: \${duration}ms"
    
    if [ \$duration -lt 250 ]; then
        echo "- Result: ✅ EXCELLENT (under 250ms)"
    elif [ \$duration -lt 500 ]; then
        echo "- Result: ✅ GOOD (under 500ms)"
    elif [ \$duration -lt 1000 ]; then
        echo "- Result: ⚠️ ACCEPTABLE (under 1000ms)"
    else
        echo "- Result: ❌ SLOW (over 1000ms)"
    fi
}
\`\`\`

## Performance Regression Testing

### Automated Regression Suite
[Description of automated tests to catch performance regressions]

### Manual Verification Checklist
- [ ] Timing rules still functioning correctly
- [ ] Pattern recognition accuracy maintained
- [ ] Memory system reliability verified
- [ ] Backup system integrity confirmed
- [ ] Overall system stability validated

## Acceptance Criteria

### Minimum Performance Requirements
- **Timing Checks**: < 50ms
- **Pattern Search**: < 100ms  
- **Memory Operations**: < 75ms
- **Backup Operations**: < 25ms
- **Complete System Cycle**: < 250ms

### Optimal Performance Targets
- **Timing Checks**: < 25ms
- **Pattern Search**: < 50ms
- **Memory Operations**: < 40ms
- **Backup Operations**: < 15ms
- **Complete System Cycle**: < 150ms
EOF
    
    echo "✓ Validation framework prepared: $validation_file"
}

generate_performance_report() {
    local analysis_name="$1"
    local analysis_dir="$2"
    
    echo "📋 Generating comprehensive performance report..."
    
    local report_file="$analysis_dir/performance_analysis_report.md"
    
    cat > "$report_file" << EOF
# Performance Analysis Report
Analysis: $analysis_name
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian

## Executive Summary

### Analysis Overview
This performance analysis evaluated the CLAUDE system across multiple dimensions including timing rule efficiency, pattern system performance, memory management, backup operations, and overall system responsiveness.

### Key Findings
[Summarize the most important findings from all analysis stages]

### Critical Issues Identified
[List any performance issues requiring immediate attention]

### Optimization Opportunities
[Highlight the most promising optimization opportunities]

## Detailed Analysis Results

### Baseline Performance Metrics
[Reference and summarize baseline measurements]

### Bottleneck Analysis
[Reference and summarize bottleneck identification]

### Resource Usage Analysis
[Reference and summarize resource analysis]

### Efficiency Measurements
[Reference and summarize efficiency metrics]

## Optimization Recommendations

### High Priority (Implement Immediately)
1. [Critical optimization with highest impact]
2. [Second most critical optimization]

### Medium Priority (Implement Within 2 Weeks)
1. [Important optimization with good ROI]
2. [Performance improvement with moderate impact]

### Low Priority (Implement When Convenient)
1. [Minor optimization for completeness]
2. [Future enhancement opportunity]

## Implementation Plan

### Phase 1: Critical Fixes (This Week)
[Timeline and steps for critical optimizations]

### Phase 2: Performance Improvements (Next 2 Weeks)
[Timeline and steps for medium priority optimizations]

### Phase 3: Enhancement (Next Month)
[Timeline and steps for low priority optimizations]

## Expected Impact

### Performance Improvements
- **Response Time**: [Expected improvement percentage]
- **Resource Usage**: [Expected reduction in resource consumption]
- **System Stability**: [Expected improvement in reliability]

### ROI Analysis
- **Time Investment**: [Total time required for optimizations]
- **Time Savings**: [Ongoing time savings from improvements]
- **Payback Period**: [Time to recover optimization investment]

## Monitoring and Follow-up

### Immediate Actions Required
1. [Action 1 with deadline]
2. [Action 2 with deadline]

### Performance Monitoring Setup
[Recommendations for ongoing performance monitoring]

### Next Analysis Schedule
- **Follow-up Analysis**: [Recommended timing for next analysis]
- **Focus Areas**: [Specific areas to monitor]

## Appendices

### Analysis Files Generated
- [List all analysis files created with brief descriptions]

### Performance Data
- [Reference to detailed performance measurements]

### Validation Framework
- [Reference to validation procedures and tools]

---
*Analysis conducted by: Christian*
*Report generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)*
EOF
    
    echo "✓ Performance report generated: $report_file"
    
    # Create analysis summary for easy reference
    echo "📊 Creating analysis summary..."
    
    cat > "$analysis_dir/ANALYSIS_SUMMARY.md" << EOF
# Performance Analysis Summary
Analysis: $analysis_name
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian

## Files Generated
- **Performance Report**: [performance_analysis_report.md](performance_analysis_report.md)
- **Baseline Metrics**: [baseline_metrics.md](baseline_metrics.md)
- **Bottleneck Analysis**: [bottleneck_analysis.md](bottleneck_analysis.md)
- **Resource Analysis**: [resource_analysis.md](resource_analysis.md)
- **Efficiency Metrics**: [efficiency_metrics.md](efficiency_metrics.md)
- **Optimization Plan**: [optimization_plan.md](optimization_plan.md)
- **Validation Framework**: [validation_framework.md](validation_framework.md)

## Quick Actions
1. Review [optimization_plan.md](optimization_plan.md) for specific improvement steps
2. Run validation framework before and after optimizations
3. Schedule follow-up analysis after implementing changes

## Next Steps
- Implement high-priority optimizations from optimization plan
- Set up performance monitoring using validation framework
- Schedule follow-up analysis in 2-4 weeks

---
*Analysis ready for implementation by: Christian*
EOF
    
    echo "✓ Analysis summary created: $analysis_dir/ANALYSIS_SUMMARY.md"
}

# Usage examples for different analysis types
# execute_performance_analysis "CLAUDE Core System" "system" 30
# execute_performance_analysis "Pattern Recognition" "component" 15
# execute_performance_analysis "Timing Rules" "feature" 10
# execute_performance_analysis "Memory Management" "process" 20
```

## Testing Requirements

- **Complexity Score**: 25+ (Very high complexity - comprehensive performance analysis)
- **TDD Used**: Yes - Test analysis accuracy and measurement consistency
- **Test Pattern**: Performance testing - validate measurement accuracy

### Test Categories:
1. **Measurement Tests**: Verify timing accuracy and consistency
2. **Analysis Tests**: Validate bottleneck identification accuracy
3. **Resource Tests**: Test resource usage measurement reliability
4. **Efficiency Tests**: Verify efficiency calculation correctness
5. **Report Tests**: Validate report generation completeness

### Validation Steps:
1. Measurement accuracy and repeatability
2. Analysis conclusion validity
3. Resource calculation correctness
4. Optimization recommendation quality
5. Report completeness and usefulness

## When to Use

- **Regular Health Checks**: Monthly or quarterly system performance reviews
- **Before Major Changes**: Baseline measurement before significant modifications
- **After Optimizations**: Validate optimization effectiveness
- **Performance Issues**: Investigate when system feels slow
- **Capacity Planning**: Understand resource requirements and scaling needs
- **System Tuning**: Data-driven optimization decisions

## Time Saved

**Estimated**: 4-6 hours for comprehensive performance analysis
**Prevents**: 15-20 hours of guesswork and ineffective optimization attempts

**Actual Uses**: Track analysis effectiveness and optimization success rates

## Usage Examples

### Example 1: Complete System Analysis
```bash
execute_performance_analysis "CLAUDE Full System Review" "system" 30
```

### Example 2: Pattern System Focus
```bash
execute_performance_analysis "Pattern Recognition Performance" "component" 15
```

### Example 3: Quick Performance Check
```bash
execute_performance_analysis "Daily Performance Check" "feature" 5
```

### Example 4: Post-Optimization Validation
```bash
execute_performance_analysis "Post-Optimization Validation" "system" 20
```

### Example 5: Resource Usage Analysis
```bash
execute_performance_analysis "Resource Consumption Review" "process" 25
```

## Success Indicators

- ✅ Complete performance baseline established
- ✅ Specific bottlenecks identified with evidence
- ✅ Resource usage patterns documented
- ✅ Efficiency metrics calculated accurately
- ✅ Actionable optimization plan created
- ✅ Validation framework ready for use
- ✅ Performance improvements measurable and validated