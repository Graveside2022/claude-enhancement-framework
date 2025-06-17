#!/bin/bash
# Test script to demonstrate the new backup retention logic
# This shows how the fixed pruning keeps the last 5 backups

echo "=== Testing Backup Retention Logic ==="
echo "Creating test backup directory structure..."

# Create test directory
mkdir -p test_backups

# Simulate 8 backups to test retention
for i in {1..8}; do
    mkdir -p "test_backups/2024-01-0${i}_v1"
    echo "Created backup: 2024-01-0${i}_v1"
    sleep 0.1  # Small delay to ensure different timestamps
done

echo ""
echo "Current backups:"
ls -1d test_backups/20*_v*

echo ""
echo "Running retention logic (keeping last 5)..."
# This is the fixed retention logic from CLAUDE.md
ls -1dr test_backups/20*_v* 2>/dev/null | tail -n +6 | xargs -r rm -rf 2>/dev/null || true

echo ""
echo "Remaining backups after pruning:"
ls -1d test_backups/20*_v*

echo ""
echo "✅ Test complete - should show exactly 5 most recent backups"

# Cleanup
rm -rf test_backups
echo "Cleaned up test directory"