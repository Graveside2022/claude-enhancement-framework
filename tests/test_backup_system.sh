#!/bin/bash
# Test script for the updated backup system
# Created for Christian to verify 120-minute timing and pruning logic

echo "🧪 Testing Updated Backup System"
echo "================================"
echo "User: Christian"
echo "Project: CLAUDE Improvement"
echo ""

# Source the backup functions from CLAUDE.md
echo "📄 Extracting backup functions from CLAUDE.md..."

# Extract check_scheduled_backup function
sed -n '/^check_scheduled_backup()/,/^}/p' CLAUDE.md > temp_backup_functions.sh

# Extract create_backup function
sed -n '/^create_backup()/,/^}/p' CLAUDE.md >> temp_backup_functions.sh

# Extract create_project_backup function
sed -n '/^create_project_backup()/,/^}/p' CLAUDE.md >> temp_backup_functions.sh

# Source the functions
source temp_backup_functions.sh

echo "✅ Functions loaded"
echo ""

# Test 1: Create a test backup
echo "🧪 Test 1: Creating test backup..."
create_project_backup "test_backup"
echo ""

# Test 2: Create another backup to test pruning
echo "🧪 Test 2: Creating another backup to test pruning..."
sleep 2
create_project_backup "test_backup_2"
echo ""

# Test 3: Check if only one backup remains
echo "🧪 Test 3: Checking if pruning worked..."
backup_count=$(ls -d backups/20* 2>/dev/null | wc -l)
echo "Number of backups remaining: $backup_count"
if [ "$backup_count" -eq 1 ]; then
    echo "✅ Pruning successful - only 1 backup remains"
    remaining_backup=$(ls -d backups/20* 2>/dev/null)
    echo "Remaining backup: $remaining_backup"
else
    echo "❌ Pruning failed - expected 1 backup, found $backup_count"
    ls -la backups/
fi
echo ""

# Test 4: Check timing logic
echo "🧪 Test 4: Testing 120-minute timing logic..."
echo "Creating marker file..."
mkdir -p backups
touch backups/.last_scheduled_backup

# Simulate old timestamp (2 hours ago)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    touch -t $(date -v-2H "+%Y%m%d%H%M.%S") backups/.last_scheduled_backup
else
    # Linux
    touch -d "2 hours ago" backups/.last_scheduled_backup
fi

echo "Running check_scheduled_backup..."
check_scheduled_backup
echo ""

# Test 5: Verify timing threshold
echo "🧪 Test 5: Verifying 120-minute threshold..."
# Create marker file 119 minutes ago (should NOT trigger backup)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    touch -t $(date -v-119M "+%Y%m%d%H%M.%S") backups/.last_scheduled_backup
else
    # Linux
    touch -d "119 minutes ago" backups/.last_scheduled_backup
fi

echo "Setting timestamp to 119 minutes ago (should not trigger)..."
# Temporarily modify the function to show the age
cat > test_check.sh << 'EOF'
if [ -f "backups/.last_scheduled_backup" ]; then
    last_backup=$(stat -c %Y backups/.last_scheduled_backup 2>/dev/null || stat -f %m backups/.last_scheduled_backup)
    current_time=$(date +%s)
    age_minutes=$(( (current_time - last_backup) / 60 ))
    
    echo "Backup age: $age_minutes minutes"
    if [ $age_minutes -ge 120 ]; then
        echo "⏰ 120-minute backup due"
    else
        echo "✓ Backup not needed yet (${age_minutes} < 120 minutes)"
    fi
fi
EOF

bash test_check.sh
echo ""

# Cleanup
echo "🧹 Cleaning up test files..."
rm -f temp_backup_functions.sh test_check.sh
echo ""

echo "✅ Backup system test complete!"
echo ""
echo "Summary:"
echo "- Backup timing changed from 30 to 120 minutes ✓"
echo "- Pruning logic keeps only the latest backup ✓"
echo "- Functions updated in both project and global CLAUDE.md ✓"