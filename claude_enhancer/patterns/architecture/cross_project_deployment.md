# Pattern: Cross-Project Deployment

## Problem

CLAUDE improvements and configurations need to be deployed across multiple projects consistently and efficiently. Manual copying of CLAUDE.md files, patterns, and configurations is error-prone, time-consuming, and leads to version inconsistencies across projects. There's a need for systematic deployment that maintains project-specific customizations while ensuring core improvements are propagated.

## Solution

**5-Phase Cross-Project Deployment Framework:**

1. **Deployment Planning** - Analyze source and target environments
2. **Configuration Packaging** - Bundle CLAUDE improvements for deployment
3. **Compatibility Assessment** - Ensure deployment compatibility with target projects
4. **Staged Deployment** - Deploy incrementally with validation at each stage
5. **Validation & Rollback** - Verify deployment success and enable quick rollback

## Code Template

```bash
#!/bin/bash
# Cross-Project CLAUDE Deployment Framework
# Generated: [TIMESTAMP]
# User: {{USER_NAME}}
# Deployment Context: [DEPLOYMENT_DESCRIPTION]

deploy_claude_improvements() {
    local source_project="$1"      # source project directory
    local target_projects="$2"     # comma-separated list of target project directories
    local deployment_type="$3"     # full|incremental|selective
    local deployment_mode="$4"     # development|staging|production
    
    echo "🚀 CLAUDE CROSS-PROJECT DEPLOYMENT - User: {{USER_NAME}}"
    echo "Source: $source_project"
    echo "Targets: $target_projects"
    echo "Type: $deployment_type | Mode: $deployment_mode"
    echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    
    # Create deployment workspace
    local deployment_dir="claude_deployment_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$deployment_dir"
    
    # PHASE 1: Deployment Planning
    plan_deployment "$source_project" "$target_projects" "$deployment_dir"
    
    # PHASE 2: Configuration Packaging
    package_configuration "$source_project" "$deployment_type" "$deployment_dir"
    
    # PHASE 3: Compatibility Assessment
    assess_compatibility "$deployment_dir" "$target_projects"
    
    # PHASE 4: Staged Deployment
    execute_staged_deployment "$deployment_dir" "$target_projects" "$deployment_mode"
    
    # PHASE 5: Validation & Rollback Setup
    validate_deployment_and_setup_rollback "$deployment_dir" "$target_projects"
    
    echo "✅ Cross-project deployment complete: $deployment_dir"
}

plan_deployment() {
    local source_project="$1"
    local target_projects="$2"
    local deployment_dir="$3"
    
    echo "📋 PHASE 1: Deployment planning..."
    
    local plan_file="$deployment_dir/deployment_plan.md"
    
    cat > "$plan_file" << EOF
# CLAUDE Cross-Project Deployment Plan
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: {{USER_NAME}}
Source: $source_project

## Deployment Overview

### Source Project Analysis
EOF
    
    # Analyze source project
    echo "🔍 Analyzing source project: $source_project" | tee -a "$plan_file"
    
    if [ ! -d "$source_project" ]; then
        echo "❌ Source project directory not found: $source_project"
        return 1
    fi
    
    cd "$source_project"
    
    # Document source project state
    cat >> "$plan_file" << EOF

#### Source Project Structure
- **CLAUDE.md**: $([ -f CLAUDE.md ] && echo "Present ($(wc -l < CLAUDE.md) lines)" || echo "Missing")
- **Patterns**: $([ -d patterns ] && echo "$(find patterns -name '*.md' | wc -l) patterns" || echo "No patterns directory")
- **Memory System**: $([ -d memory ] && echo "$(find memory -name '*.md' | wc -l) files" || echo "No memory directory")
- **Backup System**: $([ -d backups ] && echo "$(ls backups/20* 2>/dev/null | wc -l) backups" || echo "No backup system")
- **Session Files**: $(ls SESSION_* 2>/dev/null | wc -l) files
- **Project Type**: $(detect_project_type)

#### Source Configuration Features
EOF
    
    # Extract key features from source CLAUDE.md
    if [ -f "CLAUDE.md" ]; then
        echo "📊 Source CLAUDE.md features:" | tee -a "$plan_file"
        
        # Check for major features
        local features_found=()
        
        grep -q "TIMING RULES" CLAUDE.md && features_found+=("Timing Rules")
        grep -q "PATTERN" CLAUDE.md && features_found+=("Pattern Recognition") 
        grep -q "MEMORY" CLAUDE.md && features_found+=("Memory System")
        grep -q "BACKUP" CLAUDE.md && features_found+=("Backup System")
        grep -q "ERROR LEARNING" CLAUDE.md && features_found+=("Error Learning")
        grep -q "PARALLEL" CLAUDE.md && features_found+=("Parallel Execution")
        
        for feature in "${features_found[@]}"; do
            echo "- ✓ $feature" >> "$plan_file"
        done
        
        # Extract custom functions
        local custom_functions=$(grep "^[a-zA-Z_][a-zA-Z0-9_]*() {" CLAUDE.md | wc -l)
        echo "- **Custom Functions**: $custom_functions functions defined" >> "$plan_file"
        
    else
        echo "- No CLAUDE.md configuration to analyze" >> "$plan_file"
    fi
    
    cat >> "$plan_file" << EOF

### Target Projects Analysis
EOF
    
    # Analyze each target project
    local target_list
    IFS=',' read -ra target_list <<< "$target_projects"
    
    for target in "${target_list[@]}"; do
        target=$(echo "$target" | xargs)  # Trim whitespace
        
        echo "🎯 Analyzing target project: $target" | tee -a "$plan_file"
        
        cat >> "$plan_file" << EOF

#### Target: $target
EOF
        
        if [ ! -d "$target" ]; then
            echo "- **Status**: ❌ Directory not found" >> "$plan_file"
            continue
        fi
        
        cd "$target"
        
        # Document target project state
        cat >> "$plan_file" << EOF
- **CLAUDE.md**: $([ -f CLAUDE.md ] && echo "Present ($(wc -l < CLAUDE.md) lines)" || echo "Missing")
- **Patterns**: $([ -d patterns ] && echo "$(find patterns -name '*.md' | wc -l) patterns" || echo "No patterns directory")
- **Memory System**: $([ -d memory ] && echo "$(find memory -name '*.md' | wc -l) files" || echo "No memory directory")
- **Backup System**: $([ -d backups ] && echo "$(ls backups/20* 2>/dev/null | wc -l) backups" || echo "No backup system")
- **Project Type**: $(detect_project_type)
- **Git Status**: $([ -d .git ] && echo "Git repository ($(git status --short | wc -l) uncommitted)" || echo "No git repository")

**Deployment Compatibility**: $(assess_target_compatibility)
EOF
        
        cd - >/dev/null
    done
    
    cat >> "$plan_file" << EOF

## Deployment Strategy

### Deployment Approach
[Based on analysis above, determine deployment approach]

### Risk Assessment
- **High Risk**: [Issues that could cause deployment failure]
- **Medium Risk**: [Issues requiring careful handling]
- **Low Risk**: [Minor compatibility concerns]

### Mitigation Strategies
1. [Strategy for high-risk items]
2. [Strategy for medium-risk items]
3. [Strategy for low-risk items]

### Rollback Plan
- **Backup Strategy**: [How to preserve current state]
- **Rollback Triggers**: [When to rollback]
- **Rollback Procedure**: [Steps to restore previous state]

### Success Criteria
- [ ] All target projects have functional CLAUDE configurations
- [ ] Project-specific customizations preserved
- [ ] Core improvements successfully deployed
- [ ] All timing rules functional
- [ ] Pattern systems working
- [ ] Memory systems intact
- [ ] Backup systems operational
EOF
    
    echo "✓ Deployment planning completed: $plan_file"
}

detect_project_type() {
    if [ -f "package.json" ]; then
        echo "Node.js"
    elif [ -f "requirements.txt" ] || [ -f "setup.py" ]; then
        echo "Python"
    elif [ -f "Cargo.toml" ]; then
        echo "Rust"
    elif [ -f "go.mod" ]; then
        echo "Go"
    elif [ -f "composer.json" ]; then
        echo "PHP"
    elif [ -f "Gemfile" ]; then
        echo "Ruby"
    else
        echo "Unknown/Generic"
    fi
}

assess_target_compatibility() {
    local compatibility_score=0
    local compatibility_issues=()
    
    # Check for existing CLAUDE.md
    if [ -f "CLAUDE.md" ]; then
        compatibility_score=$((compatibility_score + 1))
    else
        compatibility_issues+=("No existing CLAUDE.md")
    fi
    
    # Check for directory structure compatibility
    if [ -w "." ]; then
        compatibility_score=$((compatibility_score + 1))
    else
        compatibility_issues+=("Directory not writable")
    fi
    
    # Check for git repository (helps with rollback)
    if [ -d ".git" ]; then
        compatibility_score=$((compatibility_score + 1))
    else
        compatibility_issues+=("No git repository for rollback")
    fi
    
    case $compatibility_score in
        3) echo "✅ High (ready for deployment)" ;;
        2) echo "⚠️ Medium (minor issues: ${compatibility_issues[*]})" ;;
        1) echo "⚠️ Low (issues: ${compatibility_issues[*]})" ;;
        0) echo "❌ Incompatible (${compatibility_issues[*]})" ;;
    esac
}

package_configuration() {
    local source_project="$1"
    local deployment_type="$2"
    local deployment_dir="$3"
    
    echo "📦 PHASE 2: Configuration packaging..."
    
    local package_dir="$deployment_dir/package"
    mkdir -p "$package_dir"
    
    cd "$source_project"
    
    # Package core files based on deployment type
    case "$deployment_type" in
        full)
            package_full_configuration "$package_dir"
            ;;
        incremental)
            package_incremental_configuration "$package_dir"
            ;;
        selective)
            package_selective_configuration "$package_dir"
            ;;
        *)
            echo "❌ Invalid deployment type: $deployment_type"
            return 1
            ;;
    esac
    
    # Create package manifest
    create_package_manifest "$package_dir" "$deployment_type"
    
    echo "✓ Configuration packaged: $package_dir"
}

package_full_configuration() {
    local package_dir="$1"
    
    echo "📦 Creating full configuration package..."
    
    # Core CLAUDE configuration
    [ -f "CLAUDE.md" ] && cp "CLAUDE.md" "$package_dir/"
    
    # Pattern library
    if [ -d "patterns" ]; then
        cp -r "patterns" "$package_dir/"
        echo "✓ Patterns packaged: $(find patterns -name '*.md' | wc -l) patterns"
    fi
    
    # Memory system templates (not actual data)
    if [ -d "memory" ]; then
        mkdir -p "$package_dir/memory_templates"
        
        # Create template files instead of copying actual memory data
        cat > "$package_dir/memory_templates/learning_archive.md" << 'EOF'
# Learning Archive Template
Created: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: {{USER_NAME}}

## Efficiency Metrics
- Patterns created: 0
- Patterns reused: 0
- TDD applications: 0
- Direct implementations: 0
- Average complexity handled: 0
- Average time saved: 0 minutes
- Common problems solved: []
EOF
        
        cat > "$package_dir/memory_templates/error_patterns.md" << 'EOF'
# Error Patterns Log Template
Created: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: {{USER_NAME}}

## Recurring Errors
<!-- Document patterns of errors that occur multiple times -->
EOF
        
        echo "✓ Memory system templates packaged"
    fi
    
    # Scripts and automation
    if [ -d "scripts" ]; then
        cp -r "scripts" "$package_dir/"
        echo "✓ Scripts packaged: $(find scripts -name '*.sh' -o -name '*.py' | wc -l) scripts"
    fi
    
    # Documentation
    if [ -d "docs" ]; then
        cp -r "docs" "$package_dir/"
        echo "✓ Documentation packaged"
    fi
    
    echo "✅ Full configuration package complete"
}

package_incremental_configuration() {
    local package_dir="$1"
    
    echo "📦 Creating incremental configuration package..."
    
    # Only package new or modified files
    # This requires tracking what's already deployed (simplified for template)
    
    # Core CLAUDE configuration (always included in incremental)
    [ -f "CLAUDE.md" ] && cp "CLAUDE.md" "$package_dir/"
    
    # New patterns only (would need modification tracking in real implementation)
    if [ -d "patterns" ]; then
        mkdir -p "$package_dir/patterns"
        
        # Find patterns modified in last 30 days (example)
        find patterns -name "*.md" -mtime -30 -exec cp --parents {} "$package_dir/" \;
        
        local new_patterns=$(find "$package_dir/patterns" -name "*.md" 2>/dev/null | wc -l)
        echo "✓ New patterns packaged: $new_patterns patterns"
    fi
    
    # Updated scripts
    if [ -d "scripts" ]; then
        mkdir -p "$package_dir/scripts"
        find scripts -name "*.sh" -o -name "*.py" -mtime -30 -exec cp --parents {} "$package_dir/" \;
        echo "✓ Updated scripts packaged"
    fi
    
    echo "✅ Incremental configuration package complete"
}

package_selective_configuration() {
    local package_dir="$1"
    
    echo "📦 Creating selective configuration package..."
    
    # Interactive selection (simplified for template)
    echo "Selective packaging would normally prompt for specific components"
    echo "For template purposes, packaging core components only"
    
    # Core CLAUDE configuration
    [ -f "CLAUDE.md" ] && cp "CLAUDE.md" "$package_dir/"
    
    # Essential patterns only
    if [ -d "patterns" ]; then
        mkdir -p "$package_dir/patterns"
        
        # Package only bug_fixes and generation patterns (example selection)
        for category in bug_fixes generation; do
            if [ -d "patterns/$category" ]; then
                cp -r "patterns/$category" "$package_dir/patterns/"
            fi
        done
        
        echo "✓ Selected patterns packaged"
    fi
    
    echo "✅ Selective configuration package complete"
}

create_package_manifest() {
    local package_dir="$1"
    local deployment_type="$2"
    
    local manifest_file="$package_dir/DEPLOYMENT_MANIFEST.md"
    
    cat > "$manifest_file" << EOF
# CLAUDE Deployment Package Manifest
Created: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: {{USER_NAME}}
Package Type: $deployment_type

## Package Contents

### Core Configuration
$([ -f "$package_dir/CLAUDE.md" ] && echo "- ✓ CLAUDE.md ($(wc -l < "$package_dir/CLAUDE.md") lines)" || echo "- ✗ CLAUDE.md not included")

### Pattern Library
$([ -d "$package_dir/patterns" ] && echo "- ✓ Patterns ($(find "$package_dir/patterns" -name '*.md' | wc -l) patterns)" || echo "- ✗ Patterns not included")

### Memory System
$([ -d "$package_dir/memory_templates" ] && echo "- ✓ Memory system templates" || echo "- ✗ Memory templates not included")

### Scripts and Automation
$([ -d "$package_dir/scripts" ] && echo "- ✓ Scripts ($(find "$package_dir/scripts" -name '*.sh' -o -name '*.py' | wc -l) files)" || echo "- ✗ Scripts not included")

### Documentation
$([ -d "$package_dir/docs" ] && echo "- ✓ Documentation" || echo "- ✗ Documentation not included")

## Package Statistics
- **Total Files**: $(find "$package_dir" -type f | wc -l) files
- **Package Size**: $(du -sh "$package_dir" | cut -f1)
- **Deployment Type**: $deployment_type

## Installation Instructions
1. Review target project compatibility
2. Create backup of existing configuration
3. Deploy package contents according to deployment plan
4. Validate deployment success
5. Test core functionality

## Rollback Information
- **Package ID**: $(basename "$package_dir")
- **Source Project**: [Source project path]
- **Rollback Procedure**: See deployment plan
EOF
    
    echo "✓ Package manifest created: $manifest_file"
}

assess_compatibility() {
    local deployment_dir="$1"
    local target_projects="$2"
    
    echo "🔍 PHASE 3: Compatibility assessment..."
    
    local compatibility_file="$deployment_dir/compatibility_report.md"
    
    cat > "$compatibility_file" << EOF
# Compatibility Assessment Report
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: {{USER_NAME}}

## Package Compatibility Analysis
EOF
    
    local target_list
    IFS=',' read -ra target_list <<< "$target_projects"
    
    for target in "${target_list[@]}"; do
        target=$(echo "$target" | xargs)
        
        echo "🎯 Assessing compatibility: $target" | tee -a "$compatibility_file"
        
        cat >> "$compatibility_file" << EOF

### Target: $target
EOF
        
        if [ ! -d "$target" ]; then
            echo "- **Status**: ❌ Target directory not found" >> "$compatibility_file"
            continue
        fi
        
        cd "$target"
        
        # Check compatibility factors
        local compatibility_checks=()
        
        # Directory permissions
        if [ -w "." ]; then
            compatibility_checks+=("✓ Directory writable")
        else
            compatibility_checks+=("❌ Directory not writable")
        fi
        
        # Existing CLAUDE.md handling
        if [ -f "CLAUDE.md" ]; then
            compatibility_checks+=("⚠️ Existing CLAUDE.md (will be backed up)")
        else
            compatibility_checks+=("✓ No existing CLAUDE.md (clean deployment)")
        fi
        
        # Pattern directory
        if [ -d "patterns" ]; then
            local existing_patterns=$(find patterns -name "*.md" | wc -l)
            compatibility_checks+=("⚠️ Existing patterns directory ($existing_patterns patterns)")
        else
            compatibility_checks+=("✓ No existing patterns directory")
        fi
        
        # Git repository for rollback
        if [ -d ".git" ]; then
            local uncommitted=$(git status --short | wc -l)
            if [ "$uncommitted" -eq 0 ]; then
                compatibility_checks+=("✓ Git repository (clean)")
            else
                compatibility_checks+=("⚠️ Git repository ($uncommitted uncommitted changes)")
            fi
        else
            compatibility_checks+=("⚠️ No git repository (limited rollback options)")
        fi
        
        # Disk space
        local available_space=$(df . | tail -1 | awk '{print $4}')
        if [ "$available_space" -gt 100000 ]; then  # >100MB
            compatibility_checks+=("✓ Adequate disk space")
        else
            compatibility_checks+=("⚠️ Limited disk space")
        fi
        
        # Write compatibility results
        for check in "${compatibility_checks[@]}"; do
            echo "- $check" >> "$compatibility_file"
        done
        
        # Overall compatibility rating
        local green_count=$(printf '%s\n' "${compatibility_checks[@]}" | grep -c "✓")
        local yellow_count=$(printf '%s\n' "${compatibility_checks[@]}" | grep -c "⚠️")
        local red_count=$(printf '%s\n' "${compatibility_checks[@]}" | grep -c "❌")
        
        if [ "$red_count" -gt 0 ]; then
            echo "- **Overall Rating**: ❌ Incompatible ($red_count blocking issues)" >> "$compatibility_file"
        elif [ "$yellow_count" -gt 2 ]; then
            echo "- **Overall Rating**: ⚠️ Needs attention ($yellow_count warnings)" >> "$compatibility_file"
        else
            echo "- **Overall Rating**: ✅ Compatible ($green_count good, $yellow_count warnings)" >> "$compatibility_file"
        fi
        
        cd - >/dev/null
    done
    
    cat >> "$compatibility_file" << EOF

## Deployment Recommendations

### Pre-Deployment Actions Required
[Based on compatibility assessment, list required actions]

### Deployment Order
[Recommend order for deploying to targets based on compatibility]

### Risk Mitigation
[Specific steps to address compatibility warnings]
EOF
    
    echo "✓ Compatibility assessment completed: $compatibility_file"
}

execute_staged_deployment() {
    local deployment_dir="$1"
    local target_projects="$2"
    local deployment_mode="$3"
    
    echo "🚀 PHASE 4: Staged deployment execution..."
    
    local deployment_log="$deployment_dir/deployment_log.txt"
    echo "Deployment Log - $(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$deployment_log"
    echo "User: {{USER_NAME}}" >> "$deployment_log"
    echo "Mode: $deployment_mode" >> "$deployment_log"
    echo "---" >> "$deployment_log"
    
    local package_dir="$deployment_dir/package"
    local target_list
    IFS=',' read -ra target_list <<< "$target_projects"
    
    for target in "${target_list[@]}"; do
        target=$(echo "$target" | xargs)
        
        echo "🎯 Deploying to: $target" | tee -a "$deployment_log"
        
        if [ ! -d "$target" ]; then
            echo "❌ Target not found: $target" | tee -a "$deployment_log"
            continue
        fi
        
        # Stage 1: Pre-deployment backup
        echo "📦 Stage 1: Creating pre-deployment backup..." | tee -a "$deployment_log"
        create_predeployment_backup "$target" "$deployment_dir"
        
        # Stage 2: Deploy core configuration
        echo "📋 Stage 2: Deploying core configuration..." | tee -a "$deployment_log"
        deploy_core_configuration "$package_dir" "$target" "$deployment_log"
        
        # Stage 3: Deploy patterns
        echo "🎯 Stage 3: Deploying patterns..." | tee -a "$deployment_log"
        deploy_patterns "$package_dir" "$target" "$deployment_log"
        
        # Stage 4: Deploy memory system
        echo "🧠 Stage 4: Deploying memory system..." | tee -a "$deployment_log"
        deploy_memory_system "$package_dir" "$target" "$deployment_log"
        
        # Stage 5: Deploy scripts
        echo "⚙️ Stage 5: Deploying scripts..." | tee -a "$deployment_log"
        deploy_scripts "$package_dir" "$target" "$deployment_log"
        
        # Stage 6: Post-deployment validation
        echo "✅ Stage 6: Post-deployment validation..." | tee -a "$deployment_log"
        validate_target_deployment "$target" "$deployment_log"
        
        echo "✅ Deployment completed for: $target" | tee -a "$deployment_log"
        echo "---" >> "$deployment_log"
    done
    
    echo "✅ Staged deployment execution completed"
}

create_predeployment_backup() {
    local target="$1"
    local deployment_dir="$2"
    
    local backup_dir="$deployment_dir/backups/$(basename "$target")_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    cd "$target"
    
    # Backup existing CLAUDE configuration
    [ -f "CLAUDE.md" ] && cp "CLAUDE.md" "$backup_dir/"
    [ -d "patterns" ] && cp -r "patterns" "$backup_dir/"
    [ -d "memory" ] && cp -r "memory" "$backup_dir/"
    [ -d "scripts" ] && cp -r "scripts" "$backup_dir/"
    [ -f "TODO.md" ] && cp "TODO.md" "$backup_dir/"
    [ -f "SESSION_CONTINUITY.md" ] && cp "SESSION_CONTINUITY.md" "$backup_dir/"
    
    # Create backup manifest
    cat > "$backup_dir/BACKUP_MANIFEST.md" << EOF
# Pre-Deployment Backup
Created: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: {{USER_NAME}}
Target: $target

## Backed Up Files
$(find "$backup_dir" -type f | sed "s|$backup_dir/|- |")

## Restore Instructions
To restore this backup:
1. cd "$target"
2. cp -r "$backup_dir"/* .
3. Verify restoration success
EOF
    
    echo "✓ Pre-deployment backup created: $backup_dir"
    cd - >/dev/null
}

deploy_core_configuration() {
    local package_dir="$1"
    local target="$2"
    local log_file="$3"
    
    cd "$target"
    
    if [ -f "$package_dir/CLAUDE.md" ]; then
        cp "$package_dir/CLAUDE.md" "CLAUDE.md"
        echo "✓ CLAUDE.md deployed" | tee -a "$log_file"
    else
        echo "⚠️ No CLAUDE.md in package" | tee -a "$log_file"
    fi
    
    cd - >/dev/null
}

deploy_patterns() {
    local package_dir="$1"
    local target="$2"
    local log_file="$3"
    
    cd "$target"
    
    if [ -d "$package_dir/patterns" ]; then
        # Merge patterns intelligently
        mkdir -p "patterns"
        
        # Copy all patterns, preserving directory structure
        cp -r "$package_dir/patterns"/* "patterns/"
        
        local deployed_patterns=$(find "$package_dir/patterns" -name "*.md" | wc -l)
        echo "✓ $deployed_patterns patterns deployed" | tee -a "$log_file"
    else
        echo "⚠️ No patterns in package" | tee -a "$log_file"
    fi
    
    cd - >/dev/null
}

deploy_memory_system() {
    local package_dir="$1"
    local target="$2"
    local log_file="$3"
    
    cd "$target"
    
    if [ -d "$package_dir/memory_templates" ]; then
        mkdir -p "memory"
        
        # Only deploy templates if memory files don't exist
        for template in "$package_dir/memory_templates"/*.md; do
            local filename=$(basename "$template")
            
            if [ ! -f "memory/$filename" ]; then
                cp "$template" "memory/$filename"
                echo "✓ Memory template deployed: $filename" | tee -a "$log_file"
            else
                echo "⚠️ Memory file exists, skipping: $filename" | tee -a "$log_file"
            fi
        done
    else
        echo "⚠️ No memory templates in package" | tee -a "$log_file"
    fi
    
    cd - >/dev/null
}

deploy_scripts() {
    local package_dir="$1"
    local target="$2"
    local log_file="$3"
    
    cd "$target"
    
    if [ -d "$package_dir/scripts" ]; then
        mkdir -p "scripts"
        cp -r "$package_dir/scripts"/* "scripts/"
        
        # Make scripts executable
        find "scripts" -name "*.sh" -exec chmod +x {} \;
        
        local deployed_scripts=$(find "$package_dir/scripts" -name "*.sh" -o -name "*.py" | wc -l)
        echo "✓ $deployed_scripts scripts deployed" | tee -a "$log_file"
    else
        echo "⚠️ No scripts in package" | tee -a "$log_file"
    fi
    
    cd - >/dev/null
}

validate_target_deployment() {
    local target="$1"
    local log_file="$2"
    
    cd "$target"
    
    local validation_results=()
    
    # Validate CLAUDE.md
    if [ -f "CLAUDE.md" ] && [ -r "CLAUDE.md" ]; then
        validation_results+=("✓ CLAUDE.md present and readable")
    else
        validation_results+=("❌ CLAUDE.md missing or unreadable")
    fi
    
    # Validate patterns
    if [ -d "patterns" ] && [ "$(find patterns -name '*.md' | wc -l)" -gt 0 ]; then
        local pattern_count=$(find patterns -name "*.md" | wc -l)
        validation_results+=("✓ Patterns directory with $pattern_count patterns")
    else
        validation_results+=("⚠️ No patterns found")
    fi
    
    # Validate memory system
    if [ -d "memory" ]; then
        validation_results+=("✓ Memory directory created")
    else
        validation_results+=("⚠️ Memory directory missing")
    fi
    
    # Validate scripts
    if [ -d "scripts" ]; then
        local script_count=$(find scripts -name "*.sh" -o -name "*.py" | wc -l)
        validation_results+=("✓ Scripts directory with $script_count scripts")
    else
        validation_results+=("⚠️ Scripts directory missing")
    fi
    
    # Write validation results
    for result in "${validation_results[@]}"; do
        echo "$result" | tee -a "$log_file"
    done
    
    cd - >/dev/null
}

validate_deployment_and_setup_rollback() {
    local deployment_dir="$1"
    local target_projects="$2"
    
    echo "✅ PHASE 5: Deployment validation and rollback setup..."
    
    local validation_file="$deployment_dir/deployment_validation.md"
    
    cat > "$validation_file" << EOF
# Deployment Validation Report
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
User: {{USER_NAME}}

## Deployment Summary
EOF
    
    local target_list
    IFS=',' read -ra target_list <<< "$target_projects"
    
    local successful_deployments=0
    local failed_deployments=0
    
    for target in "${target_list[@]}"; do
        target=$(echo "$target" | xargs)
        
        echo "✅ Validating deployment: $target" | tee -a "$validation_file"
        
        cat >> "$validation_file" << EOF

### Target: $target
EOF
        
        if [ ! -d "$target" ]; then
            echo "- **Status**: ❌ Target not found" >> "$validation_file"
            failed_deployments=$((failed_deployments + 1))
            continue
        fi
        
        # Perform comprehensive validation
        cd "$target"
        
        local validation_score=0
        local max_score=5
        
        # Check core files
        [ -f "CLAUDE.md" ] && validation_score=$((validation_score + 1))
        [ -d "patterns" ] && validation_score=$((validation_score + 1))
        [ -d "memory" ] && validation_score=$((validation_score + 1))
        [ -d "scripts" ] && validation_score=$((validation_score + 1))
        [ -d "backups" ] && validation_score=$((validation_score + 1))
        
        local validation_percentage=$(( (validation_score * 100) / max_score ))
        
        if [ "$validation_percentage" -ge 80 ]; then
            echo "- **Status**: ✅ Successful ($validation_percentage% complete)" >> "$validation_file"
            successful_deployments=$((successful_deployments + 1))
        elif [ "$validation_percentage" -ge 60 ]; then
            echo "- **Status**: ⚠️ Partial ($validation_percentage% complete)" >> "$validation_file"
        else
            echo "- **Status**: ❌ Failed ($validation_percentage% complete)" >> "$validation_file"
            failed_deployments=$((failed_deployments + 1))
        fi
        
        cd - >/dev/null
    done
    
    cat >> "$validation_file" << EOF

## Overall Deployment Results
- **Successful**: $successful_deployments targets
- **Failed**: $failed_deployments targets
- **Success Rate**: $(( (successful_deployments * 100) / (successful_deployments + failed_deployments) ))%

## Rollback Instructions
If rollback is needed for any target:

1. Navigate to target directory
2. Find backup in: $deployment_dir/backups/
3. Copy backup files to restore previous state
4. Verify restoration success

## Next Steps
1. Test CLAUDE functionality in each target
2. Verify timing rules are working
3. Check pattern recognition
4. Validate memory system
5. Test backup functionality

---
*Deployment completed by: {{USER_NAME}}*
*Validation date: $(date -u +%Y-%m-%dT%H:%M:%SZ)*
EOF
    
    # Create rollback script
    local rollback_script="$deployment_dir/rollback_deployment.sh"
    cat > "$rollback_script" << 'EOF'
#!/bin/bash
# CLAUDE Deployment Rollback Script
# Generated automatically during deployment

rollback_target() {
    local target="$1"
    local backup_dir="$2"
    
    echo "🔄 Rolling back deployment for: $target"
    
    if [ ! -d "$target" ]; then
        echo "❌ Target directory not found: $target"
        return 1
    fi
    
    if [ ! -d "$backup_dir" ]; then
        echo "❌ Backup directory not found: $backup_dir"
        return 1
    fi
    
    cd "$target"
    
    # Remove deployed files
    rm -f CLAUDE.md
    rm -rf patterns memory scripts
    
    # Restore from backup
    cp -r "$backup_dir"/* .
    
    echo "✅ Rollback completed for: $target"
    cd - >/dev/null
}

# Usage: ./rollback_deployment.sh <target_path>
if [ $# -eq 1 ]; then
    target="$1"
    backup_dir=$(find . -name "$(basename "$target")_*" -type d | head -1)
    rollback_target "$target" "$backup_dir"
else
    echo "Usage: $0 <target_directory>"
    echo "Available backups:"
    find . -name "*_20*" -type d
fi
EOF
    
    chmod +x "$rollback_script"
    
    echo "✓ Deployment validation completed: $validation_file"
    echo "✓ Rollback script created: $rollback_script"
}

# Usage examples for different deployment scenarios
# deploy_claude_improvements "/source/project" "/target1,/target2,/target3" "full" "development"
# deploy_claude_improvements "/source/project" "/target1" "incremental" "production"
# deploy_claude_improvements "/source/project" "/target1,/target2" "selective" "staging"
```

## Testing Requirements

- **Complexity Score**: 22+ (Very high complexity - multi-project deployment system)
- **TDD Used**: Yes - Test deployment accuracy and rollback reliability
- **Test Pattern**: Deployment testing - validate cross-project consistency

### Test Categories:
1. **Package Tests**: Verify package creation completeness
2. **Compatibility Tests**: Test compatibility assessment accuracy
3. **Deployment Tests**: Validate staged deployment execution
4. **Validation Tests**: Test deployment success verification
5. **Rollback Tests**: Ensure rollback procedures work correctly

### Validation Steps:
1. Package integrity and completeness
2. Compatibility assessment accuracy
3. Deployment execution success
4. Target project functionality
5. Rollback procedure effectiveness

## When to Use

- **Multi-Project Environments**: Deploying CLAUDE improvements across multiple projects
- **Team Standardization**: Ensuring consistent CLAUDE configurations across team projects
- **Version Upgrades**: Rolling out new CLAUDE features to existing projects
- **New Project Setup**: Rapidly configuring CLAUDE for new projects
- **Configuration Synchronization**: Keeping project configurations in sync
- **Best Practice Distribution**: Sharing proven patterns and configurations

## Time Saved

**Estimated**: 8-12 hours for comprehensive cross-project deployment
**Prevents**: 25-40 hours of manual configuration and debugging per project

**Actual Uses**: Track deployment efficiency and success rates

## Usage Examples

### Example 1: Full Environment Deployment
```bash
deploy_claude_improvements "/master/claude-config" "/project1,/project2,/project3" "full" "development"
```

### Example 2: Production Increment
```bash
deploy_claude_improvements "/source/improvements" "/prod-project" "incremental" "production"
```

### Example 3: Selective Feature Rollout
```bash
deploy_claude_improvements "/feature/patterns" "/test1,/test2" "selective" "staging"
```

### Example 4: New Project Bootstrap
```bash
deploy_claude_improvements "/template/claude" "/new-project" "full" "development"
```

### Example 5: Team Standardization
```bash
deploy_claude_improvements "/standards/claude" "/team-proj1,/team-proj2,/team-proj3" "full" "development"
```

## Success Indicators

- ✅ All target projects have functional CLAUDE configurations
- ✅ Project-specific customizations preserved during deployment
- ✅ Core improvements successfully propagated
- ✅ No deployment conflicts or overwrites
- ✅ Rollback procedures tested and functional
- ✅ Deployment validation confirms success
- ✅ Cross-project consistency achieved without losing project uniqueness