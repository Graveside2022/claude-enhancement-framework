#!/bin/bash

# Add cleanup alias to shell profile
SCRIPT_PATH="/Users/scarmatrix/Project/CLAUDE_improvement/scripts/cleanup"

# Check which shell is being used
if [[ $SHELL == *"zsh"* ]]; then
    PROFILE_FILE="$HOME/.zshrc"
elif [[ $SHELL == *"bash"* ]]; then
    PROFILE_FILE="$HOME/.bashrc"
else
    PROFILE_FILE="$HOME/.profile"
fi

# Add alias if it doesn't exist
if ! grep -q "alias cleanup=" "$PROFILE_FILE" 2>/dev/null; then
    echo "alias cleanup='$SCRIPT_PATH'" >> "$PROFILE_FILE"
    echo "✅ Added 'cleanup' alias to $PROFILE_FILE"
    echo "🔄 Run 'source $PROFILE_FILE' or restart terminal to use 'cleanup' command"
else
    echo "ℹ️  'cleanup' alias already exists in $PROFILE_FILE"
fi