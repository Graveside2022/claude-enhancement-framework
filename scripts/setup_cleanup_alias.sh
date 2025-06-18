#!/bin/bash

# Enhanced Setup script with comprehensive error handling and retry logic
# Usage: ./scripts/setup_cleanup_alias.sh

SCRIPT_PATH="/Users/scarmatrix/Project/CLAUDE_improvement/scripts/cleanup"
PROJECT_ROOT="/Users/scarmatrix/Project/CLAUDE_improvement"
GLOBAL_CLAUDE_DIR="$HOME/.claude"
GLOBAL_CLAUDE_FILE="$GLOBAL_CLAUDE_DIR/CLAUDE.md"
PROJECT_CLAUDE_FILE="$PROJECT_ROOT/CLAUDE.md"

# Enhanced error handling configuration
MAX_RETRY_ATTEMPTS=3
RETRY_DELAY=1
BACKUP_SUFFIX=".setup_backup"
CLEANUP_NEEDED=false

# Error handling functions
handle_error() {
    local error_type="$1"
    local error_message="$2"
    local file_path="$3"
    
    case "$error_type" in
        "permission")
            echo "❌ Permission Error: $error_message"
            echo "💡 Try running with appropriate permissions or check file ownership"
            echo "📁 File: $file_path"
            ;;
        "file_not_found")
            echo "❌ File Not Found: $error_message"
            echo "💡 Verify the file path exists and is accessible"
            echo "📁 Path: $file_path"
            ;;
        "write_failure")
            echo "❌ Write Operation Failed: $error_message"
            echo "💡 Check disk space and file permissions"
            echo "📁 Target: $file_path"
            ;;
        "backup_failure")
            echo "❌ Backup Operation Failed: $error_message"
            echo "💡 Ensure backup location is writable"
            echo "📁 File: $file_path"
            ;;
        "copy_failure")
            echo "❌ File Copy Failed: $error_message"
            echo "💡 Check source file exists and destination is writable"
            echo "📁 Operation: $file_path"
            ;;
        "directory_creation")
            echo "❌ Directory Creation Failed: $error_message"
            echo "💡 Check parent directory permissions"
            echo "📁 Path: $file_path"
            ;;
        *)
            echo "❌ Unknown Error: $error_message"
            echo "📁 Context: $file_path"
            ;;
    esac
}

# Retry mechanism with exponential backoff
retry_operation() {
    local operation="$1"
    local max_attempts="$2"
    local delay="$3"
    local context="$4"
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        echo "🔄 Attempt $attempt of $max_attempts: $context"
        
        if eval "$operation"; then
            echo "✅ Operation succeeded on attempt $attempt"
            return 0
        else
            local exit_code=$?
            echo "⚠️ Attempt $attempt failed (exit code: $exit_code)"
            
            if [ $attempt -lt $max_attempts ]; then
                echo "⏳ Waiting ${delay}s before retry..."
                sleep $delay
                delay=$((delay * 2))  # Exponential backoff
            fi
            
            attempt=$((attempt + 1))
        fi
    done
    
    echo "❌ All $max_attempts attempts failed for: $context"
    return 1
}

# Cleanup function for partial installations
cleanup_partial_installation() {
    if [ "$CLEANUP_NEEDED" = true ]; then
        echo "🧹 Cleaning up partial installation..."
        
        # Remove backup files
        find "$HOME" -name "*${BACKUP_SUFFIX}" -type f 2>/dev/null | while read -r backup_file; do
            if rm "$backup_file" 2>/dev/null; then
                echo "✅ Removed backup file: $backup_file"
            else
                echo "⚠️ Could not remove backup file: $backup_file"
            fi
        done
        
        # Remove incomplete global CLAUDE.md if it was being deployed
        if [ -f "$GLOBAL_CLAUDE_FILE" ] && [ ! -s "$GLOBAL_CLAUDE_FILE" ]; then
            if rm "$GLOBAL_CLAUDE_FILE" 2>/dev/null; then
                echo "✅ Removed incomplete global CLAUDE.md"
            fi
        fi
        
        echo "🧹 Cleanup completed"
        CLEANUP_NEEDED=false
    fi
}

echo "🚀 Enhanced CLAUDE Improvement Setup Script"
echo "============================================="
echo "✨ Features: Comprehensive error handling, retry logic, graceful cleanup"
echo ""

# Enhanced function to backup existing global CLAUDE.md with retry logic
backup_global_claude() {
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local backup_file="${GLOBAL_CLAUDE_DIR}/CLAUDE_backup_${timestamp}.md"
    
    # Validate source file exists and is readable
    if [ ! -f "$GLOBAL_CLAUDE_FILE" ]; then
        handle_error "file_not_found" "Global CLAUDE.md file does not exist" "$GLOBAL_CLAUDE_FILE"
        return 1
    fi
    
    if [ ! -r "$GLOBAL_CLAUDE_FILE" ]; then
        handle_error "permission" "Cannot read global CLAUDE.md file" "$GLOBAL_CLAUDE_FILE"
        return 1
    fi
    
    # Ensure backup directory is writable
    if [ ! -w "$GLOBAL_CLAUDE_DIR" ]; then
        handle_error "permission" "Cannot write to backup directory" "$GLOBAL_CLAUDE_DIR"
        return 1
    fi
    
    # Perform backup with retry logic
    local backup_operation="cp '$GLOBAL_CLAUDE_FILE' '$backup_file'"
    
    if retry_operation "$backup_operation" $MAX_RETRY_ATTEMPTS $RETRY_DELAY "Backing up global CLAUDE.md"; then
        # Verify backup integrity
        if [ -f "$backup_file" ] && [ -s "$backup_file" ]; then
            local original_size=$(wc -c < "$GLOBAL_CLAUDE_FILE" 2>/dev/null || echo "0")
            local backup_size=$(wc -c < "$backup_file" 2>/dev/null || echo "0")
            
            if [ "$original_size" -eq "$backup_size" ] && [ "$original_size" -gt 0 ]; then
                echo "📦 Backup created and verified: $backup_file"
                return 0
            else
                handle_error "backup_failure" "Backup file size mismatch (original: ${original_size}, backup: ${backup_size})" "$backup_file"
                rm -f "$backup_file" 2>/dev/null
                return 1
            fi
        else
            handle_error "backup_failure" "Backup file was not created or is empty" "$backup_file"
            return 1
        fi
    else
        handle_error "backup_failure" "Failed to create backup after $MAX_RETRY_ATTEMPTS attempts" "$backup_file"
        return 1
    fi
}

# Enhanced function to deploy global CLAUDE.md with comprehensive error handling
deploy_global_claude() {
    echo "📋 Deploying global CLAUDE.md configuration..."
    CLEANUP_NEEDED=true
    
    # Validate source file exists and is readable
    if [ ! -f "$PROJECT_CLAUDE_FILE" ]; then
        handle_error "file_not_found" "Project CLAUDE.md file does not exist" "$PROJECT_CLAUDE_FILE"
        return 1
    fi
    
    if [ ! -r "$PROJECT_CLAUDE_FILE" ]; then
        handle_error "permission" "Cannot read project CLAUDE.md file" "$PROJECT_CLAUDE_FILE"
        return 1
    fi
    
    # Create .claude directory with retry logic
    local create_dir_operation="mkdir -p '$GLOBAL_CLAUDE_DIR'"
    if ! retry_operation "$create_dir_operation" $MAX_RETRY_ATTEMPTS $RETRY_DELAY "Creating .claude directory"; then
        handle_error "directory_creation" "Failed to create directory after $MAX_RETRY_ATTEMPTS attempts" "$GLOBAL_CLAUDE_DIR"
        return 1
    fi
    
    # Verify directory permissions
    if [ ! -w "$GLOBAL_CLAUDE_DIR" ]; then
        handle_error "permission" "Created directory is not writable" "$GLOBAL_CLAUDE_DIR"
        return 1
    fi
    
    # Check if global CLAUDE.md already exists
    if [[ -f "$GLOBAL_CLAUDE_FILE" ]]; then
        echo "⚠️  Global CLAUDE.md exists at: $GLOBAL_CLAUDE_FILE"
        read -p "   Overwrite existing file? (y/n): " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # Create backup before overwriting
            if backup_global_claude; then
                # Deploy with retry logic
                local deploy_operation="cp '$PROJECT_CLAUDE_FILE' '$GLOBAL_CLAUDE_FILE'"
                
                if retry_operation "$deploy_operation" $MAX_RETRY_ATTEMPTS $RETRY_DELAY "Updating global CLAUDE.md"; then
                    # Verify deployment integrity
                    if [ -f "$GLOBAL_CLAUDE_FILE" ] && [ -s "$GLOBAL_CLAUDE_FILE" ]; then
                        local source_size=$(wc -c < "$PROJECT_CLAUDE_FILE" 2>/dev/null || echo "0")
                        local deployed_size=$(wc -c < "$GLOBAL_CLAUDE_FILE" 2>/dev/null || echo "0")
                        
                        if [ "$source_size" -eq "$deployed_size" ] && [ "$source_size" -gt 0 ]; then
                            echo "✓ Global CLAUDE.md updated successfully in ~/.claude"
                            CLEANUP_NEEDED=false
                            return 0
                        else
                            handle_error "copy_failure" "Deployment file size mismatch (source: ${source_size}, deployed: ${deployed_size})" "$GLOBAL_CLAUDE_FILE"
                            return 1
                        fi
                    else
                        handle_error "copy_failure" "Deployed file was not created or is empty" "$GLOBAL_CLAUDE_FILE"
                        return 1
                    fi
                else
                    handle_error "copy_failure" "Failed to deploy global CLAUDE.md after $MAX_RETRY_ATTEMPTS attempts" "$GLOBAL_CLAUDE_FILE"
                    return 1
                fi
            else
                echo "❌ Backup failed, aborting global deployment"
                return 1
            fi
        else
            echo "ℹ️  Skipping global CLAUDE.md deployment"
            CLEANUP_NEEDED=false
            return 0
        fi
    else
        # No existing file, deploy directly with retry logic
        local deploy_operation="cp '$PROJECT_CLAUDE_FILE' '$GLOBAL_CLAUDE_FILE'"
        
        if retry_operation "$deploy_operation" $MAX_RETRY_ATTEMPTS $RETRY_DELAY "Deploying global CLAUDE.md"; then
            # Verify deployment integrity
            if [ -f "$GLOBAL_CLAUDE_FILE" ] && [ -s "$GLOBAL_CLAUDE_FILE" ]; then
                local source_size=$(wc -c < "$PROJECT_CLAUDE_FILE" 2>/dev/null || echo "0")
                local deployed_size=$(wc -c < "$GLOBAL_CLAUDE_FILE" 2>/dev/null || echo "0")
                
                if [ "$source_size" -eq "$deployed_size" ] && [ "$source_size" -gt 0 ]; then
                    echo "✓ Global CLAUDE.md deployed successfully in ~/.claude"
                    CLEANUP_NEEDED=false
                    return 0
                else
                    handle_error "copy_failure" "Deployment file size mismatch (source: ${source_size}, deployed: ${deployed_size})" "$GLOBAL_CLAUDE_FILE"
                    return 1
                fi
            else
                handle_error "copy_failure" "Deployed file was not created or is empty" "$GLOBAL_CLAUDE_FILE"
                return 1
            fi
        else
            handle_error "copy_failure" "Failed to deploy global CLAUDE.md after $MAX_RETRY_ATTEMPTS attempts" "$GLOBAL_CLAUDE_FILE"
            return 1
        fi
    fi
}

# Enhanced alias setup with error handling and validation
setup_cleanup_alias() {
    echo "🔧 Setting up cleanup alias with enhanced error handling..."
    
    # Validate cleanup script exists and is executable
    if [ ! -f "$SCRIPT_PATH" ]; then
        handle_error "file_not_found" "Cleanup script not found" "$SCRIPT_PATH"
        return 1
    fi
    
    if [ ! -x "$SCRIPT_PATH" ]; then
        echo "⚠️ Cleanup script is not executable, attempting to fix..."
        local chmod_operation="chmod +x '$SCRIPT_PATH'"
        
        if retry_operation "$chmod_operation" $MAX_RETRY_ATTEMPTS $RETRY_DELAY "Making cleanup script executable"; then
            echo "✅ Made cleanup script executable"
        else
            handle_error "permission" "Cannot make cleanup script executable" "$SCRIPT_PATH"
            return 1
        fi
    fi
    
    # Determine shell profile file
    if [[ $SHELL == *"zsh"* ]]; then
        PROFILE_FILE="$HOME/.zshrc"
    elif [[ $SHELL == *"bash"* ]]; then
        PROFILE_FILE="$HOME/.bashrc"
    else
        PROFILE_FILE="$HOME/.profile"
    fi
    
    echo "🐚 Detected shell profile: $PROFILE_FILE"
    
    # Create profile file if it doesn't exist
    if [ ! -f "$PROFILE_FILE" ]; then
        local profile_dir=$(dirname "$PROFILE_FILE")
        if [ ! -d "$profile_dir" ]; then
            local create_profile_dir_operation="mkdir -p '$profile_dir'"
            if ! retry_operation "$create_profile_dir_operation" $MAX_RETRY_ATTEMPTS $RETRY_DELAY "Creating profile directory"; then
                handle_error "directory_creation" "Failed to create profile directory" "$profile_dir"
                return 1
            fi
        fi
        
        local create_profile_operation="touch '$PROFILE_FILE'"
        if ! retry_operation "$create_profile_operation" $MAX_RETRY_ATTEMPTS $RETRY_DELAY "Creating profile file"; then
            handle_error "write_failure" "Failed to create profile file" "$PROFILE_FILE"
            return 1
        fi
    fi
    
    # Check if profile file is writable
    if [ ! -w "$PROFILE_FILE" ]; then
        handle_error "permission" "Profile file is not writable" "$PROFILE_FILE"
        return 1
    fi
    
    # Check if alias already exists
    if grep -q "alias cleanup=" "$PROFILE_FILE" 2>/dev/null; then
        echo "ℹ️  'cleanup' alias already exists in $PROFILE_FILE"
        
        # Verify existing alias points to correct script
        local existing_alias=$(grep "alias cleanup=" "$PROFILE_FILE" 2>/dev/null | head -1)
        if [[ "$existing_alias" == *"$SCRIPT_PATH"* ]]; then
            echo "✅ Existing alias is correctly configured"
            return 0
        else
            echo "⚠️ Existing alias points to different script, updating..."
            
            # Create backup of profile file
            local profile_backup="${PROFILE_FILE}${BACKUP_SUFFIX}"
            local backup_profile_operation="cp '$PROFILE_FILE' '$profile_backup'"
            
            if retry_operation "$backup_profile_operation" $MAX_RETRY_ATTEMPTS $RETRY_DELAY "Backing up profile file"; then
                echo "💾 Created profile backup: $profile_backup"
                
                # Remove old alias and add new one
                local temp_file=$(mktemp)
                if [ $? -eq 0 ]; then
                    if grep -v "alias cleanup=" "$PROFILE_FILE" > "$temp_file" 2>/dev/null; then
                        local restore_profile_operation="mv '$temp_file' '$PROFILE_FILE'"
                        if retry_operation "$restore_profile_operation" $MAX_RETRY_ATTEMPTS $RETRY_DELAY "Removing old alias"; then
                            echo "✅ Removed old alias"
                        else
                            handle_error "write_failure" "Failed to remove old alias" "$PROFILE_FILE"
                            rm -f "$temp_file"
                            return 1
                        fi
                    else
                        handle_error "write_failure" "Failed to process profile file" "$PROFILE_FILE"
                        rm -f "$temp_file"
                        return 1
                    fi
                else
                    handle_error "write_failure" "Failed to create temporary file" "$PROFILE_FILE"
                    return 1
                fi
            else
                handle_error "backup_failure" "Failed to backup profile file" "$PROFILE_FILE"
                return 1
            fi
        fi
    fi
    
    # Add new alias with retry logic
    local alias_line="alias cleanup='$SCRIPT_PATH'"
    local add_alias_operation="echo '$alias_line' >> '$PROFILE_FILE'"
    
    if retry_operation "$add_alias_operation" $MAX_RETRY_ATTEMPTS $RETRY_DELAY "Adding cleanup alias"; then
        # Verify alias was added successfully
        if grep -q "alias cleanup=" "$PROFILE_FILE" 2>/dev/null; then
            echo "✅ Successfully added 'cleanup' alias to $PROFILE_FILE"
            echo "🔄 Run 'source $PROFILE_FILE' or restart terminal to use 'cleanup' command"
            echo "🧪 Test the alias by running: cleanup --help"
            
            # Remove backup on success
            rm -f "${PROFILE_FILE}${BACKUP_SUFFIX}" 2>/dev/null
            return 0
        else
            handle_error "write_failure" "Alias was not properly written to file" "$PROFILE_FILE"
            return 1
        fi
    else
        handle_error "write_failure" "Failed to add alias after $MAX_RETRY_ATTEMPTS attempts" "$PROFILE_FILE"
        return 1
    fi
}

# Error trap for unexpected failures
trap 'echo "❌ Unexpected error occurred at line $LINENO. Exit code: $?"; cleanup_partial_installation; exit 1' ERR

# Deploy global CLAUDE.md configuration
if [[ -f "$PROJECT_CLAUDE_FILE" ]]; then
    if ! deploy_global_claude; then
        echo "❌ Global CLAUDE.md deployment failed"
        cleanup_partial_installation
        exit 1
    fi
else
    echo "❌ Project CLAUDE.md not found at: $PROJECT_CLAUDE_FILE"
    echo "   Skipping global deployment"
fi

echo ""

# Setup cleanup alias with enhanced error handling
if setup_cleanup_alias; then
    echo ""
    echo "🎉 Enhanced Setup completed successfully!"
    echo "   ✅ Comprehensive error handling implemented"
    echo "   ✅ Retry logic with 3 attempts maximum"
    echo "   ✅ Exponential backoff for failed operations"
    echo "   ✅ File integrity verification"
    echo "   ✅ Graceful cleanup for partial installations"
    echo "   ✅ Specific error messages for different failure types"
    echo "   ✅ Permission error handling"
else
    echo ""
    echo "❌ Setup failed during alias configuration"
    cleanup_partial_installation
    exit 1
fi