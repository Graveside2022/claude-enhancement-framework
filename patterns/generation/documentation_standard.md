# Pattern: Documentation Standard

## Problem

CLAUDE improvements need consistent, comprehensive documentation to ensure maintainability, knowledge transfer, and system understanding. Ad-hoc documentation leads to incomplete coverage, inconsistent formatting, and difficulty finding critical information when needed.

## Solution

**4-Layer Documentation Standard:**

1. **System Documentation** - High-level architecture and design decisions
2. **Feature Documentation** - Detailed component and function descriptions  
3. **Process Documentation** - Step-by-step procedures and workflows
4. **Reference Documentation** - Quick-access guides and troubleshooting

## Code Template

```bash
#!/bin/bash
# CLAUDE Documentation Standard Generator
# Generated: [TIMESTAMP]
# User: Christian
# Documentation Type: [DOC_TYPE]

generate_claude_documentation() {
    local doc_type="$1"        # system|feature|process|reference
    local component_name="$2"   # name of what's being documented
    local output_dir="$3"      # where to place documentation
    
    echo "📚 CLAUDE DOCUMENTATION GENERATOR - User: Christian"
    echo "Type: $doc_type | Component: $component_name"
    echo "Output: $output_dir"
    echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    
    # Create output directory if needed
    mkdir -p "$output_dir"
    
    case "$doc_type" in
        system)
            generate_system_documentation "$component_name" "$output_dir"
            ;;
        feature)
            generate_feature_documentation "$component_name" "$output_dir"
            ;;
        process)
            generate_process_documentation "$component_name" "$output_dir"
            ;;
        reference)
            generate_reference_documentation "$component_name" "$output_dir"
            ;;
        all)
            generate_complete_documentation_set "$component_name" "$output_dir"
            ;;
        *)
            echo "❌ Invalid documentation type: $doc_type"
            echo "Valid types: system|feature|process|reference|all"
            return 1
            ;;
    esac
    
    echo "✅ Documentation generation complete"
}

generate_system_documentation() {
    local component="$1"
    local output_dir="$2"
    
    echo "🏗️ Generating system documentation..."
    
    local doc_file="$output_dir/${component}_system_architecture.md"
    
    cat > "$doc_file" << EOF
# ${component} System Architecture
Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian
Type: System Documentation

## Overview

### Purpose
[Brief description of what this system/component accomplishes]

### Scope
[What is included and excluded from this system]

### Key Principles
- [Principle 1: e.g., Timing rule enforcement]
- [Principle 2: e.g., Pattern-first approach]
- [Principle 3: e.g., Memory persistence]
- [Principle 4: e.g., Error learning]

## Architecture

### High-Level Design
\`\`\`
[ASCII diagram or description of major components and their relationships]

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Component A   │───▶│   Component B   │───▶│   Component C   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
          │                       │                       │
          ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Store    │    │   Config Mgmt   │    │   Output Gen    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
\`\`\`

### Component Responsibilities
- **Component A**: [Primary responsibility and key functions]
- **Component B**: [Primary responsibility and key functions]  
- **Component C**: [Primary responsibility and key functions]

### Data Flow
1. [Step 1: Input processing]
2. [Step 2: Transformation]
3. [Step 3: Output generation]
4. [Step 4: State persistence]

### Integration Points
- **External Systems**: [List systems this integrates with]
- **Configuration Sources**: [Where configuration comes from]
- **Data Dependencies**: [What data sources are required]
- **Output Targets**: [Where results are delivered]

## Design Decisions

### Decision 1: [Architecture Choice]
- **Problem**: [What problem this decision solved]
- **Options Considered**: [Alternative approaches evaluated]
- **Decision**: [What was chosen and why]
- **Trade-offs**: [What was gained vs what was sacrificed]
- **Impact**: [How this affects the overall system]

### Decision 2: [Technology Choice]
- **Problem**: [What problem this decision solved]
- **Options Considered**: [Alternative technologies evaluated]
- **Decision**: [What was chosen and why]
- **Trade-offs**: [What was gained vs what was sacrificed]
- **Impact**: [How this affects the overall system]

### Decision 3: [Process Choice]
- **Problem**: [What problem this decision solved]
- **Options Considered**: [Alternative processes evaluated]
- **Decision**: [What was chosen and why]
- **Trade-offs**: [What was gained vs what was sacrificed]
- **Impact**: [How this affects the overall system]

## Quality Attributes

### Performance
- **Response Time**: [Target response times]
- **Throughput**: [Expected volume handling]
- **Resource Usage**: [Memory, CPU, storage requirements]

### Reliability
- **Availability**: [Uptime requirements and targets]
- **Error Handling**: [How errors are detected and managed]
- **Recovery**: [Recovery time objectives and procedures]

### Maintainability
- **Code Organization**: [How code is structured for maintenance]
- **Documentation**: [Documentation standards and coverage]
- **Testing**: [Testing approach and coverage requirements]

### Security
- **Authentication**: [How user identity is verified]
- **Authorization**: [How access is controlled]
- **Data Protection**: [How sensitive data is protected]

## Constraints and Assumptions

### Technical Constraints
- [Constraint 1: e.g., Must run on macOS]
- [Constraint 2: e.g., No external dependencies]
- [Constraint 3: e.g., File-based storage only]

### Business Constraints
- [Constraint 1: e.g., Single user system]
- [Constraint 2: e.g., Local operation only]
- [Constraint 3: e.g., No network connectivity required]

### Assumptions
- [Assumption 1: e.g., User has administrative privileges]
- [Assumption 2: e.g., Disk space is adequate]
- [Assumption 3: e.g., System clock is accurate]

## Evolution and Future Considerations

### Known Limitations
- [Limitation 1: Current system limitation]
- [Limitation 2: Scalability concern]
- [Limitation 3: Feature gap]

### Planned Improvements
- [Improvement 1: Near-term enhancement]
- [Improvement 2: Architecture evolution]
- [Improvement 3: Feature addition]

### Migration Considerations
- [Consideration 1: How to migrate from current state]
- [Consideration 2: Backward compatibility requirements]
- [Consideration 3: Data preservation needs]

## References

### Related Documentation
- [Link to feature documentation]
- [Link to process documentation]
- [Link to reference guides]

### External Resources
- [Link to relevant standards]
- [Link to best practices]
- [Link to tool documentation]

---
*Documentation maintained by: Christian*
*Last Updated: $(date -u +%Y-%m-%dT%H:%M:%SZ)*
EOF
    
    echo "✓ System documentation created: $doc_file"
}

generate_feature_documentation() {
    local component="$1"
    local output_dir="$2"
    
    echo "⚙️ Generating feature documentation..."
    
    local doc_file="$output_dir/${component}_feature_guide.md"
    
    cat > "$doc_file" << EOF
# ${component} Feature Guide
Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian
Type: Feature Documentation

## Feature Overview

### What It Does
[Clear description of the feature's primary function]

### Why It Exists
[Problem this feature solves]

### Who Uses It
[Primary users and use cases]

## Functional Specification

### Core Capabilities
1. **Capability 1**: [Description of what it can do]
2. **Capability 2**: [Description of what it can do]
3. **Capability 3**: [Description of what it can do]

### Input Requirements
- **Input Type 1**: [Format, constraints, validation rules]
- **Input Type 2**: [Format, constraints, validation rules]
- **Input Type 3**: [Format, constraints, validation rules]

### Output Specifications
- **Output Type 1**: [Format, content, location]
- **Output Type 2**: [Format, content, location]
- **Output Type 3**: [Format, content, location]

### Business Rules
1. **Rule 1**: [Business logic constraint]
2. **Rule 2**: [Business logic constraint]
3. **Rule 3**: [Business logic constraint]

## Technical Implementation

### Key Functions
\`\`\`bash
# Primary function
${component}_main_function() {
    # [Description of primary function implementation]
}

# Supporting function 1
${component}_helper_function_1() {
    # [Description of helper function]
}

# Supporting function 2  
${component}_helper_function_2() {
    # [Description of helper function]
}
\`\`\`

### Configuration Options
\`\`\`bash
# Configuration variables
${component^^}_CONFIG_OPTION_1="default_value"    # [Description]
${component^^}_CONFIG_OPTION_2="default_value"    # [Description]
${component^^}_CONFIG_OPTION_3="default_value"    # [Description]
\`\`\`

### File Dependencies
- **Input Files**: [List files this feature reads]
- **Output Files**: [List files this feature creates/modifies]
- **Configuration Files**: [List configuration files used]
- **Log Files**: [List log files generated]

### Integration Points
- **Upstream Systems**: [What provides input to this feature]
- **Downstream Systems**: [What consumes output from this feature]
- **Shared Resources**: [What resources are shared with other features]

## Usage Guide

### Basic Usage
\`\`\`bash
# Simple usage example
${component}_main_function "input_value" "configuration"

# Expected output:
# [Show what typical output looks like]
\`\`\`

### Advanced Usage
\`\`\`bash
# Complex usage example with multiple options
${component}_main_function \\
    --input "complex_input" \\
    --config "custom_config" \\
    --output-dir "custom_output" \\
    --verbose

# Expected output:
# [Show what advanced output looks like]
\`\`\`

### Configuration Examples
\`\`\`bash
# Development configuration
export ${component^^}_MODE="development"
export ${component^^}_LOG_LEVEL="debug"
export ${component^^}_OUTPUT_FORMAT="verbose"

# Production configuration
export ${component^^}_MODE="production"
export ${component^^}_LOG_LEVEL="info"
export ${component^^}_OUTPUT_FORMAT="compact"
\`\`\`

## Error Handling

### Common Errors
1. **Error Type 1**: [Error description]
   - **Cause**: [What causes this error]
   - **Solution**: [How to fix it]
   - **Prevention**: [How to avoid it]

2. **Error Type 2**: [Error description]
   - **Cause**: [What causes this error]
   - **Solution**: [How to fix it]
   - **Prevention**: [How to avoid it]

3. **Error Type 3**: [Error description]
   - **Cause**: [What causes this error]
   - **Solution**: [How to fix it]
   - **Prevention**: [How to avoid it]

### Error Recovery
\`\`\`bash
# Error recovery example
if ! ${component}_main_function "input"; then
    echo "Primary function failed, attempting recovery..."
    ${component}_recovery_procedure
    ${component}_main_function "input" --retry
fi
\`\`\`

## Testing and Validation

### Unit Tests
\`\`\`bash
# Test basic functionality
test_${component}_basic() {
    # [Test implementation]
}

# Test edge cases
test_${component}_edge_cases() {
    # [Test implementation]
}

# Test error conditions
test_${component}_error_handling() {
    # [Test implementation]
}
\`\`\`

### Integration Tests
\`\`\`bash
# Test with upstream systems
test_${component}_integration_upstream() {
    # [Test implementation]
}

# Test with downstream systems
test_${component}_integration_downstream() {
    # [Test implementation]
}
\`\`\`

### Performance Tests
\`\`\`bash
# Test performance characteristics
test_${component}_performance() {
    # [Test implementation]
}
\`\`\`

## Monitoring and Metrics

### Key Metrics
- **Performance Metrics**: [Response time, throughput, etc.]
- **Quality Metrics**: [Error rates, success rates, etc.]
- **Usage Metrics**: [Frequency, patterns, etc.]

### Monitoring Points
\`\`\`bash
# Add monitoring to feature
${component}_with_monitoring() {
    local start_time=\$(date +%s)
    
    # Execute feature
    ${component}_main_function "\$@"
    local result=\$?
    
    # Record metrics
    local end_time=\$(date +%s)
    local duration=\$((end_time - start_time))
    
    echo "Execution time: \${duration}s, Result: \$result" >> ${component}_metrics.log
    
    return \$result
}
\`\`\`

## Maintenance and Support

### Regular Maintenance Tasks
1. **Daily**: [Daily maintenance requirements]
2. **Weekly**: [Weekly maintenance requirements]
3. **Monthly**: [Monthly maintenance requirements]

### Troubleshooting Checklist
- [ ] Verify input file format and content
- [ ] Check configuration settings
- [ ] Validate file permissions
- [ ] Review recent log entries
- [ ] Test with minimal example
- [ ] Check system resources

### Known Issues and Workarounds
1. **Issue 1**: [Description]
   - **Workaround**: [Temporary solution]
   - **Status**: [Fix status]

2. **Issue 2**: [Description]
   - **Workaround**: [Temporary solution]
   - **Status**: [Fix status]

## Change History

### Version History
- **v1.0**: [Initial implementation - date]
- **v1.1**: [Feature enhancement - date]
- **v1.2**: [Bug fixes - date]

### Breaking Changes
- **Change 1**: [Description and migration path]
- **Change 2**: [Description and migration path]

---
*Feature maintained by: Christian*
*Last Updated: $(date -u +%Y-%m-%dT%H:%M:%SZ)*
EOF
    
    echo "✓ Feature documentation created: $doc_file"
}

generate_process_documentation() {
    local component="$1"
    local output_dir="$2"
    
    echo "📋 Generating process documentation..."
    
    local doc_file="$output_dir/${component}_process_guide.md"
    
    cat > "$doc_file" << EOF
# ${component} Process Guide
Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian
Type: Process Documentation

## Process Overview

### Process Purpose
[What this process accomplishes and why it's important]

### When to Execute
[Triggers and timing for process execution]

### Prerequisites
[What must be in place before starting this process]

### Expected Outcomes
[What should result from successful process completion]

## Step-by-Step Procedure

### Phase 1: Preparation
1. **Step 1.1**: [Detailed preparation step]
   - **Action**: [Specific action to take]
   - **Verification**: [How to verify step completion]
   - **Time Estimate**: [Expected duration]

2. **Step 1.2**: [Detailed preparation step]
   - **Action**: [Specific action to take]
   - **Verification**: [How to verify step completion]
   - **Time Estimate**: [Expected duration]

3. **Step 1.3**: [Detailed preparation step]
   - **Action**: [Specific action to take]
   - **Verification**: [How to verify step completion]
   - **Time Estimate**: [Expected duration]

### Phase 2: Execution
1. **Step 2.1**: [Detailed execution step]
   - **Command**: \`${component}_command_1\`
   - **Expected Output**: [What should appear]
   - **Success Criteria**: [How to know it worked]
   - **Time Estimate**: [Expected duration]

2. **Step 2.2**: [Detailed execution step]
   - **Command**: \`${component}_command_2\`
   - **Expected Output**: [What should appear]
   - **Success Criteria**: [How to know it worked]
   - **Time Estimate**: [Expected duration]

3. **Step 2.3**: [Detailed execution step]
   - **Command**: \`${component}_command_3\`
   - **Expected Output**: [What should appear]
   - **Success Criteria**: [How to know it worked]
   - **Time Estimate**: [Expected duration]

### Phase 3: Validation
1. **Step 3.1**: [Detailed validation step]
   - **Check**: [What to verify]
   - **Method**: [How to perform the check]
   - **Expected Result**: [What should be found]

2. **Step 3.2**: [Detailed validation step]
   - **Check**: [What to verify]
   - **Method**: [How to perform the check]
   - **Expected Result**: [What should be found]

3. **Step 3.3**: [Detailed validation step]
   - **Check**: [What to verify]
   - **Method**: [How to perform the check]
   - **Expected Result**: [What should be found]

### Phase 4: Completion
1. **Step 4.1**: [Detailed completion step]
   - **Action**: [Final action to take]
   - **Documentation**: [What to record]
   - **Notification**: [Who to notify]

2. **Step 4.2**: [Detailed completion step]
   - **Action**: [Final action to take]
   - **Documentation**: [What to record]
   - **Notification**: [Who to notify]

## Process Automation

### Automated Script
\`\`\`bash
#!/bin/bash
# ${component} Process Automation
# User: Christian

execute_${component}_process() {
    local process_id="\$1"
    local log_file="${component}_process_\$(date +%Y%m%d_%H%M%S).log"
    
    echo "🔄 Starting ${component} process: \$process_id" | tee "\$log_file"
    echo "Timestamp: \$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "\$log_file"
    
    # Phase 1: Preparation
    echo "📋 Phase 1: Preparation" | tee -a "\$log_file"
    ${component}_prepare || return 1
    
    # Phase 2: Execution  
    echo "⚙️ Phase 2: Execution" | tee -a "\$log_file"
    ${component}_execute || return 1
    
    # Phase 3: Validation
    echo "✅ Phase 3: Validation" | tee -a "\$log_file"
    ${component}_validate || return 1
    
    # Phase 4: Completion
    echo "🏁 Phase 4: Completion" | tee -a "\$log_file"
    ${component}_complete || return 1
    
    echo "✅ ${component} process completed successfully" | tee -a "\$log_file"
    return 0
}

${component}_prepare() {
    echo "  Preparing ${component} process..."
    # [Preparation commands]
    return 0
}

${component}_execute() {
    echo "  Executing ${component} process..."
    # [Execution commands]
    return 0
}

${component}_validate() {
    echo "  Validating ${component} process..."
    # [Validation commands]
    return 0
}

${component}_complete() {
    echo "  Completing ${component} process..."
    # [Completion commands]
    return 0
}
\`\`\`

### Manual Execution Checklist
- [ ] Prerequisites verified
- [ ] Phase 1: Preparation completed
- [ ] Phase 2: Execution completed
- [ ] Phase 3: Validation completed
- [ ] Phase 4: Completion completed
- [ ] Process documentation updated
- [ ] Stakeholders notified

## Error Handling and Recovery

### Common Process Failures
1. **Preparation Failure**
   - **Symptoms**: [How to recognize this failure]
   - **Causes**: [Common root causes]
   - **Recovery**: [Steps to recover]
   - **Prevention**: [How to avoid in future]

2. **Execution Failure**
   - **Symptoms**: [How to recognize this failure]
   - **Causes**: [Common root causes]
   - **Recovery**: [Steps to recover]
   - **Prevention**: [How to avoid in future]

3. **Validation Failure**
   - **Symptoms**: [How to recognize this failure]
   - **Causes**: [Common root causes]
   - **Recovery**: [Steps to recover]
   - **Prevention**: [How to avoid in future]

### Recovery Procedures
\`\`\`bash
# Process recovery automation
recover_${component}_process() {
    local failure_phase="\$1"
    
    case "\$failure_phase" in
        preparation)
            echo "Recovering from preparation failure..."
            # [Recovery commands]
            ;;
        execution)
            echo "Recovering from execution failure..."
            # [Recovery commands]
            ;;
        validation)
            echo "Recovering from validation failure..."
            # [Recovery commands]
            ;;
        *)
            echo "Unknown failure phase: \$failure_phase"
            return 1
            ;;
    esac
}
\`\`\`

## Quality Assurance

### Process Validation Checklist
- [ ] All steps documented clearly
- [ ] Commands tested and verified
- [ ] Error conditions identified
- [ ] Recovery procedures validated
- [ ] Automation tested
- [ ] Documentation reviewed

### Performance Metrics
- **Total Process Time**: [Expected duration]
- **Success Rate**: [Historical success percentage]
- **Error Rate**: [Historical error percentage]
- **Recovery Time**: [Average time to recover from failures]

### Continuous Improvement
- **Process Review Frequency**: [How often to review]
- **Feedback Collection**: [How to gather improvement suggestions]
- **Update Procedures**: [How to modify this process]

## References and Resources

### Related Processes
- [Link to upstream process]
- [Link to downstream process]
- [Link to parallel processes]

### Supporting Documentation
- [Link to system architecture]
- [Link to feature documentation]
- [Link to troubleshooting guides]

### External Resources
- [Relevant standards]
- [Best practices]
- [Tool documentation]

---
*Process maintained by: Christian*
*Last Updated: $(date -u +%Y-%m-%dT%H:%M:%SZ)*
EOF
    
    echo "✓ Process documentation created: $doc_file"
}

generate_reference_documentation() {
    local component="$1"
    local output_dir="$2"
    
    echo "📖 Generating reference documentation..."
    
    local doc_file="$output_dir/${component}_reference.md"
    
    cat > "$doc_file" << EOF
# ${component} Quick Reference
Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian
Type: Reference Documentation

## Quick Start

### Essential Commands
\`\`\`bash
# Most common operations
${component}_status                    # Check current status
${component}_start                     # Start the component
${component}_stop                      # Stop the component
${component}_restart                   # Restart the component
${component}_validate                  # Validate configuration
\`\`\`

### Common Use Cases
1. **Quick Status Check**: \`${component}_status\`
2. **Standard Operation**: \`${component}_start && ${component}_validate\`
3. **Troubleshooting**: \`${component}_stop && ${component}_diagnose && ${component}_start\`
4. **Configuration Update**: \`${component}_stop && ${component}_update_config && ${component}_start\`

## Command Reference

### Core Commands
| Command | Purpose | Example |
|---------|---------|---------|
| \`${component}_init\` | Initialize component | \`${component}_init --config default\` |
| \`${component}_start\` | Start component | \`${component}_start --verbose\` |
| \`${component}_stop\` | Stop component | \`${component}_stop --force\` |
| \`${component}_status\` | Check status | \`${component}_status --detailed\` |
| \`${component}_restart\` | Restart component | \`${component}_restart --quick\` |

### Configuration Commands
| Command | Purpose | Example |
|---------|---------|---------|
| \`${component}_config_get\` | Get configuration value | \`${component}_config_get timeout\` |
| \`${component}_config_set\` | Set configuration value | \`${component}_config_set timeout 30\` |
| \`${component}_config_list\` | List all configuration | \`${component}_config_list\` |
| \`${component}_config_validate\` | Validate configuration | \`${component}_config_validate\` |
| \`${component}_config_reset\` | Reset to defaults | \`${component}_config_reset\` |

### Diagnostic Commands
| Command | Purpose | Example |
|---------|---------|---------|
| \`${component}_diagnose\` | Run diagnostics | \`${component}_diagnose --full\` |
| \`${component}_test\` | Run tests | \`${component}_test --integration\` |
| \`${component}_logs\` | View logs | \`${component}_logs --tail 50\` |
| \`${component}_debug\` | Enable debug mode | \`${component}_debug --enable\` |
| \`${component}_health\` | Health check | \`${component}_health --detailed\` |

### Maintenance Commands
| Command | Purpose | Example |
|---------|---------|---------|
| \`${component}_backup\` | Create backup | \`${component}_backup --compress\` |
| \`${component}_restore\` | Restore from backup | \`${component}_restore backup_file\` |
| \`${component}_cleanup\` | Clean temporary files | \`${component}_cleanup --all\` |
| \`${component}_update\` | Update component | \`${component}_update --check\` |
| \`${component}_reset\` | Reset to clean state | \`${component}_reset --confirm\` |

## Configuration Reference

### Core Configuration Options
\`\`\`bash
# Basic settings
${component^^}_ENABLED=true                    # Enable/disable component
${component^^}_MODE=production                 # Operation mode
${component^^}_LOG_LEVEL=info                  # Logging level
${component^^}_TIMEOUT=30                      # Operation timeout
${component^^}_RETRY_COUNT=3                   # Retry attempts

# Advanced settings
${component^^}_MEMORY_LIMIT=512M               # Memory limit
${component^^}_CACHE_SIZE=100                  # Cache size
${component^^}_CONCURRENT_JOBS=4               # Parallel jobs
${component^^}_BACKUP_RETENTION=7              # Backup retention days
${component^^}_HEALTH_CHECK_INTERVAL=60        # Health check interval
\`\`\`

### Environment-Specific Configuration
\`\`\`bash
# Development environment
export ${component^^}_MODE=development
export ${component^^}_LOG_LEVEL=debug
export ${component^^}_CACHE_SIZE=10

# Staging environment  
export ${component^^}_MODE=staging
export ${component^^}_LOG_LEVEL=info
export ${component^^}_CACHE_SIZE=50

# Production environment
export ${component^^}_MODE=production
export ${component^^}_LOG_LEVEL=warn
export ${component^^}_CACHE_SIZE=100
\`\`\`

## File Locations

### Configuration Files
- **Main Config**: \`~/.${component}/config.conf\`
- **User Config**: \`~/.${component}/user.conf\`
- **Environment Config**: \`/etc/${component}/${component}.conf\`

### Data Files
- **Data Directory**: \`~/.${component}/data/\`
- **Cache Directory**: \`~/.${component}/cache/\`
- **Temp Directory**: \`/tmp/${component}/\`

### Log Files
- **Main Log**: \`~/.${component}/logs/${component}.log\`
- **Error Log**: \`~/.${component}/logs/error.log\`
- **Debug Log**: \`~/.${component}/logs/debug.log\`

### Backup Files
- **Backup Directory**: \`~/.${component}/backups/\`
- **Auto Backups**: \`~/.${component}/backups/auto/\`
- **Manual Backups**: \`~/.${component}/backups/manual/\`

## Exit Codes

### Standard Exit Codes
| Code | Meaning | Description |
|------|---------|-------------|
| 0 | Success | Operation completed successfully |
| 1 | General Error | Unspecified error occurred |
| 2 | Misuse | Invalid command line arguments |
| 3 | Configuration Error | Configuration file problem |
| 4 | Permission Error | Insufficient permissions |
| 5 | Resource Error | Resource unavailable (file, memory, etc.) |
| 6 | Timeout Error | Operation timed out |
| 7 | Validation Error | Input validation failed |
| 8 | Connection Error | Network or connection issue |
| 9 | Authentication Error | Authentication failed |
| 10 | Service Error | External service error |

## Troubleshooting Quick Reference

### Common Issues and Solutions
| Issue | Quick Fix | Detailed Solution |
|-------|-----------|-------------------|
| Component won't start | \`${component}_diagnose\` | Check logs and configuration |
| Configuration errors | \`${component}_config_validate\` | Review config file syntax |
| Permission problems | \`chmod +x ~/.${component}/bin/*\` | Fix file permissions |
| Log file full | \`${component}_cleanup --logs\` | Clean old log files |
| Performance slow | \`${component}_config_set cache_size 200\` | Increase cache size |

### Emergency Procedures
\`\`\`bash
# Complete reset (USE WITH CAUTION)
${component}_stop --force
${component}_backup --emergency
${component}_reset --full
${component}_init --defaults
${component}_start

# Quick recovery
${component}_stop
${component}_restore latest_backup
${component}_start --verify
\`\`\`

## Integration Examples

### Basic Integration
\`\`\`bash
#!/bin/bash
# Integrate ${component} into workflow

# Initialize
${component}_init --quiet

# Configure for current environment
${component}_config_set mode \$ENVIRONMENT
${component}_config_set log_level \$LOG_LEVEL

# Start and verify
${component}_start
${component}_health --wait

# Use in script
if ${component}_status --quiet; then
    # Component is running
    ${component}_process_data "\$input_file"
else
    echo "Component not available"
    exit 1
fi
\`\`\`

### Advanced Integration
\`\`\`bash
#!/bin/bash
# Advanced integration with error handling

${component}_safe_operation() {
    local operation="\$1"
    local max_retries=3
    local retry_count=0
    
    while [ \$retry_count -lt \$max_retries ]; do
        if ${component}_\$operation; then
            return 0
        else
            retry_count=\$((retry_count + 1))
            echo "Retry \$retry_count/\$max_retries for operation: \$operation"
            sleep 5
        fi
    done
    
    echo "Operation failed after \$max_retries attempts: \$operation"
    return 1
}
\`\`\`

## Performance Tips

### Optimization Checklist
- [ ] Set appropriate cache size for workload
- [ ] Configure memory limits based on available RAM
- [ ] Adjust concurrent job count for CPU cores
- [ ] Enable compression for large data sets
- [ ] Use appropriate log levels (avoid debug in production)
- [ ] Regular cleanup of temporary files
- [ ] Monitor and rotate log files

### Monitoring Commands
\`\`\`bash
# Monitor performance
watch -n 5 '${component}_status --performance'

# Check resource usage
${component}_stats --resources

# Monitor logs in real-time
tail -f ~/.${component}/logs/${component}.log | grep ERROR
\`\`\`

---
*Reference maintained by: Christian*
*Last Updated: $(date -u +%Y-%m-%dT%H:%M:%SZ)*
EOF
    
    echo "✓ Reference documentation created: $doc_file"
}

generate_complete_documentation_set() {
    local component="$1"
    local output_dir="$2"
    
    echo "📚 Generating complete documentation set..."
    
    # Generate all documentation types
    generate_system_documentation "$component" "$output_dir"
    generate_feature_documentation "$component" "$output_dir"
    generate_process_documentation "$component" "$output_dir"
    generate_reference_documentation "$component" "$output_dir"
    
    # Create documentation index
    local index_file="$output_dir/${component}_documentation_index.md"
    
    cat > "$index_file" << EOF
# ${component} Documentation Index
Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: Christian

## Complete Documentation Set

This directory contains comprehensive documentation for the ${component} component.

### 🏗️ System Documentation
**File**: [\`${component}_system_architecture.md\`](${component}_system_architecture.md)
**Purpose**: High-level architecture, design decisions, and system overview
**Audience**: Architects, senior developers, system administrators

### ⚙️ Feature Documentation  
**File**: [\`${component}_feature_guide.md\`](${component}_feature_guide.md)
**Purpose**: Detailed feature specifications, implementation details, and usage
**Audience**: Developers, testers, technical users

### 📋 Process Documentation
**File**: [\`${component}_process_guide.md\`](${component}_process_guide.md)
**Purpose**: Step-by-step procedures, workflows, and automation
**Audience**: Operators, administrators, process managers

### 📖 Reference Documentation
**File**: [\`${component}_reference.md\`](${component}_reference.md)
**Purpose**: Quick reference, commands, configuration, troubleshooting
**Audience**: All users, support staff, developers

## Documentation Standards Applied

### ✅ Completeness
- System architecture documented
- Feature specifications complete
- Process procedures detailed
- Reference information comprehensive

### ✅ Consistency
- Standard formatting throughout
- Consistent terminology and style
- Cross-references between documents
- Unified navigation structure

### ✅ Maintainability
- Clear ownership (Christian)
- Update timestamps on all documents
- Version control friendly format
- Automated generation capabilities

### ✅ Accessibility
- Clear table of contents
- Logical information hierarchy
- Quick start information
- Multiple entry points

## Usage Recommendations

### For New Users
1. Start with **Reference Documentation** for quick orientation
2. Review **Process Documentation** for step-by-step guidance
3. Consult **Feature Documentation** for detailed usage
4. Refer to **System Documentation** for architectural understanding

### For Developers
1. Begin with **System Documentation** for architectural context
2. Study **Feature Documentation** for implementation details
3. Use **Process Documentation** for development workflows
4. Keep **Reference Documentation** handy for quick lookups

### For Administrators
1. Focus on **Process Documentation** for operational procedures
2. Use **Reference Documentation** for troubleshooting
3. Review **System Documentation** for deployment considerations
4. Reference **Feature Documentation** for configuration details

## Maintenance Schedule

### Regular Updates
- **Weekly**: Update reference information for any changes
- **Monthly**: Review process documentation for accuracy
- **Quarterly**: Update feature documentation for new capabilities
- **Annually**: Comprehensive review of system documentation

### Change Management
- Document all changes in component history
- Update related documentation when features change
- Maintain backward compatibility in documentation
- Archive old versions for reference

---
*Complete documentation set maintained by: Christian*
*Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)*
EOF
    
    echo "✓ Documentation index created: $index_file"
    echo "✅ Complete documentation set generated"
}

# Usage examples
# generate_claude_documentation "system" "timing_rules" "docs/"
# generate_claude_documentation "feature" "pattern_recognition" "docs/"
# generate_claude_documentation "process" "backup_management" "docs/"
# generate_claude_documentation "reference" "error_handling" "docs/"
# generate_claude_documentation "all" "claude_core" "docs/"
```

## Testing Requirements

- **Complexity Score**: 18+ (High complexity - comprehensive documentation system)
- **TDD Used**: Yes - Test documentation generation and validation
- **Test Pattern**: Documentation testing - verify completeness and accuracy

### Test Categories:
1. **Content Tests**: Verify all required sections are generated
2. **Format Tests**: Ensure consistent markdown formatting
3. **Link Tests**: Validate cross-references and links
4. **Template Tests**: Test variable substitution accuracy
5. **Integration Tests**: Verify documentation matches actual implementation

### Validation Steps:
1. Template variable substitution accuracy
2. Section completeness and organization
3. Cross-reference link validity
4. Format consistency across document types
5. Content alignment with actual implementation

## When to Use

- **New Component Development**: Document as you build
- **System Architecture Changes**: Update system documentation
- **Process Improvements**: Document new procedures
- **Knowledge Transfer**: Create comprehensive guides
- **Compliance Requirements**: Ensure documentation standards
- **New Team Members**: Provide complete reference materials

## Time Saved

**Estimated**: 3-5 hours per component documentation set
**Prevents**: 10-15 hours of knowledge reconstruction and tribal knowledge loss

**Actual Uses**: Track documentation generation efficiency

## Usage Examples

### Example 1: New Feature Documentation
```bash
generate_claude_documentation "feature" "pattern_matching" "docs/"
```

### Example 2: Process Documentation
```bash
generate_claude_documentation "process" "backup_procedure" "docs/"
```

### Example 3: Complete System Documentation
```bash
generate_claude_documentation "all" "claude_core_system" "docs/"
```

### Example 4: Quick Reference Only
```bash
generate_claude_documentation "reference" "error_codes" "docs/"
```

### Example 5: Architecture Documentation
```bash
generate_claude_documentation "system" "timing_enforcement" "docs/"
```

## Success Indicators

- ✅ All four documentation types consistently generated
- ✅ Documentation matches actual implementation
- ✅ Cross-references and links work correctly
- ✅ Information is findable and accessible
- ✅ Documentation stays current with changes
- ✅ New team members can use documentation effectively
- ✅ Knowledge transfer no longer relies on tribal knowledge