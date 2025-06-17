#!/usr/bin/env python3
"""
Quick validation script for Christian's persistent memory system
"""

import os
from pathlib import Path
from datetime import datetime

def validate_memory_system():
    """Quick validation of the persistent memory system"""
    
    print("🧠 PERSISTENT MEMORY SYSTEM - QUICK VALIDATION")
    print("=" * 55)
    
    project_root = Path(__file__).parent.parent
    session_file = project_root / "SESSION_CONTINUITY.md"
    
    if not session_file.exists():
        print("❌ SESSION_CONTINUITY.md not found")
        return False
    
    content = session_file.read_text()
    
    # Check for Christian's agent execution rule
    checks = {
        "Agent Execution Rule": "AGENT_EXECUTION_RULE" in content,
        "Parallel Enforcement": "Parallel execution mandatory" in content,
        "Never Sequential": "NEVER use" in content and "sequential" in content,
        "5 Agent Rule": "5 agents" in content,
        "10 Agent Rule": "10 agents" in content,
        "Boot Integration": "Boot Loading" in content,
        "Binding Rule": "binding" in content.lower(),
        "Christian User": "Christian" in content
    }
    
    passed = 0
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}: {result}")
        if result:
            passed += 1
    
    # Check file age
    mod_time = datetime.fromtimestamp(session_file.stat().st_mtime)
    age_minutes = (datetime.now() - mod_time).total_seconds() / 60
    within_120 = age_minutes <= 120
    
    print(f"⏰ File Age: {age_minutes:.1f} min ({'✅' if within_120 else '❌'} within 120-min rule)")
    
    # Check project config consistency
    project_config = project_root / "CLAUDE.md"
    if project_config.exists():
        config_content = project_config.read_text().lower()
        no_sequential = "sequential" not in config_content
        print(f"🔧 No Sequential Conflicts: {'✅' if no_sequential else '❌'}")
        if no_sequential:
            passed += 1
    
    score = (passed / (len(checks) + 1)) * 100
    overall_pass = score >= 80
    
    print("-" * 55)
    print(f"📊 Overall Score: {score:.1f}%")
    print(f"🎯 Status: {'✅ OPERATIONAL' if overall_pass else '❌ NEEDS ATTENTION'}")
    
    return overall_pass

if __name__ == "__main__":
    success = validate_memory_system()
    exit(0 if success else 1)