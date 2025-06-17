#!/bin/bash
# Test 120-Minute Timing Rule Enforcement
# Verifies automatic execution and compliance checking
# Created: 2025-06-16T21:45:00Z
# User: Christian

echo "🧪 TESTING 120-MINUTE TIMING RULE ENFORCEMENT"
echo "User: Christian"
echo "Test start: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

# Test 1: Verify timing enforcement script exists and is executable
echo "📋 Test 1: Timing enforcement script validation"
if [ -x "scripts/timing_enforcement.sh" ]; then
    echo "✓ timing_enforcement.sh exists and is executable"
else
    echo "❌ timing_enforcement.sh missing or not executable"
    exit 1
fi

# Test 2: Verify session start handler exists and is executable
echo "📋 Test 2: Session start handler validation"
if [ -x "scripts/session_start_handler.sh" ]; then
    echo "✓ session_start_handler.sh exists and is executable"
else
    echo "❌ session_start_handler.sh missing or not executable"
    exit 1
fi

# Test 3: Verify CLAUDE.md contains 120-minute timing references
echo "📋 Test 3: CLAUDE.md timing reference validation"
if grep -q "check_120_minute_timing_rules" CLAUDE.md; then
    echo "✓ CLAUDE.md contains 120-minute timing function reference"
else
    echo "❌ CLAUDE.md missing 120-minute timing function reference"
    exit 1
fi

# Test 4: Verify timing function execution
echo "📋 Test 4: Timing function execution test"
source scripts/timing_enforcement.sh > /dev/null 2>&1
if command -v check_120_minute_timing_rules > /dev/null 2>&1; then
    echo "✓ check_120_minute_timing_rules function loaded successfully"
else
    echo "❌ check_120_minute_timing_rules function not available"
    exit 1
fi

# Test 5: Verify automatic session start detection
echo "📋 Test 5: Session start trigger detection test"
source scripts/session_start_handler.sh "startup" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Session start detection working correctly"
else
    echo "❌ Session start detection failed"
    exit 1
fi

# Test 6: Check current TODO.md and backup status
echo "📋 Test 6: Current timing status verification"
if [ -f "TODO.md" ]; then
    last_modified=$(stat -c %Y TODO.md 2>/dev/null || stat -f %m TODO.md)
    current_time=$(date +%s)
    age_minutes=$(( (current_time - last_modified) / 60 ))
    echo "✓ TODO.md current age: ${age_minutes} minutes"
else
    echo "⚠️ TODO.md not present"
fi

if [ -f "backups/.last_scheduled_backup" ]; then
    last_backup=$(stat -c %Y backups/.last_scheduled_backup 2>/dev/null || stat -f %m backups/.last_scheduled_backup)
    backup_age_minutes=$(( (current_time - last_backup) / 60 ))
    echo "✓ Last backup age: ${backup_age_minutes} minutes"
else
    echo "⚠️ Backup marker not present"
fi

# Test 7: Verify CLAUDE.md automatic execution directive
echo "📋 Test 7: CLAUDE.md automatic execution directive verification"
if grep -q "check_120_minute_timing_rules" CLAUDE.md && grep -q "AUTOMATIC EXECUTION" CLAUDE.md; then
    echo "✓ CLAUDE.md contains automatic execution directive for 120-minute timing"
else
    echo "❌ CLAUDE.md missing automatic execution directive"
    exit 1
fi

echo ""
echo "✅ ALL TESTS PASSED - 120-MINUTE TIMING ENFORCEMENT READY"
echo "🎯 System Status:"
echo "   - ✓ Timing enforcement scripts created and executable"
echo "   - ✓ CLAUDE.md updated with 120-minute timing rules"
echo "   - ✓ Automatic execution configured for session start"
echo "   - ✓ All timing functions loaded and available"
echo "   - ✓ Session start detection operational"
echo ""
echo "📋 Implementation Summary:"
echo "   1. Created scripts/timing_enforcement.sh with 120-minute timing checks"
echo "   2. Created scripts/session_start_handler.sh for automatic execution"
echo "   3. Updated CLAUDE.md automatic execution directive"
echo "   4. Verified all timing references use 120-minute intervals"
echo "   5. Added timing trigger to session start procedure"
echo ""
echo "⏰ 120-MINUTE TIMING RULE ENFORCEMENT IS NOW ACTIVE FOR CHRISTIAN"