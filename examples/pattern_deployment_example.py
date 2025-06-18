#!/usr/bin/env python3
"""
Pattern Deployment Example
Part of Claude Enhancement Framework by Christian

Demonstrates pattern deployment functionality:
- Full pattern deployment
- Selective deployment by category
- Specific pattern deployment
- Template variable substitution
- Deployment validation
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from claude_enhancer.core.enhancer import ClaudeEnhancer


def main():
    """Demonstrate pattern deployment capabilities."""
    print("🚀 Claude Enhancement Framework - Pattern Deployment Example")
    print("=" * 65)
    
    # Initialize ClaudeEnhancer with user details
    enhancer = ClaudeEnhancer(username="Christian", project_name="MyProject")
    
    # Example 1: Get available patterns
    print("\n📋 Available Patterns in Framework:")
    patterns_info = enhancer.get_available_patterns()
    
    print(f"Total patterns available: {patterns_info['total_patterns']}")
    
    for category, info in patterns_info['categories'].items():
        print(f"\n🏷️  {category.title()} ({info['pattern_count']} patterns):")
        print(f"   {info['description']}")
        for pattern in info['patterns']:
            print(f"   • {pattern['name']} ({pattern['size']} bytes)")
    
    # Example 2: Deploy all patterns to current project
    print(f"\n🔧 Deploying All Patterns to Current Directory:")
    
    # Deploy all patterns
    deployment_result = enhancer.deploy_patterns()
    
    if deployment_result['success']:
        print("✅ Deployment successful!")
        print(f"   Patterns deployed: {len(deployment_result['patterns_deployed'])}")
        print(f"   Patterns updated: {len(deployment_result['patterns_updated'])}")
        print(f"   Directories created: {len(deployment_result['directories_created'])}")
        
        for pattern in deployment_result['patterns_deployed']:
            print(f"   ✨ Deployed: {pattern}")
            
    else:
        print("❌ Deployment failed:")
        for error in deployment_result['errors']:
            print(f"   • {error}")
    
    # Example 3: Selective deployment by category
    print(f"\n🎯 Selective Deployment Example (Architecture Only):")
    
    # Create example target directory
    target_dir = Path("example_architecture_project")
    target_dir.mkdir(exist_ok=True)
    
    selective_result = enhancer.deploy_patterns(
        target_project=target_dir,
        categories=["architecture"],
        force=True  # Overwrite existing patterns
    )
    
    if selective_result['success']:
        print("✅ Selective deployment successful!")
        print(f"   Architecture patterns deployed: {len(selective_result['patterns_deployed'])}")
        
        for pattern in selective_result['patterns_deployed']:
            print(f"   🏗️  {pattern}")
    
    # Example 4: Deploy specific patterns
    print(f"\n🔍 Specific Pattern Deployment Example:")
    
    specific_result = enhancer.deploy_patterns(
        target_project=target_dir,
        specific_patterns=["null_pointer_prevention", "microservice_pattern"],
        force=True
    )
    
    if specific_result['success']:
        print("✅ Specific pattern deployment successful!")
        for pattern in specific_result['patterns_deployed']:
            print(f"   🎯 {pattern}")
    
    # Example 5: Validate deployment
    print(f"\n🔍 Validating Pattern Deployment:")
    
    validation_result = enhancer.validate_pattern_deployment(target_dir)
    
    if validation_result['valid']:
        print("✅ Deployment validation passed!")
        print(f"   Patterns found: {len(validation_result['patterns_found'])}")
        print(f"   Index valid: {validation_result['index_valid']}")
        
        if validation_result.get('index_data'):
            index = validation_result['index_data']
            print(f"   Framework version: {index.get('framework_version')}")
            print(f"   Deployment timestamp: {index.get('deployment_timestamp')}")
    else:
        print("❌ Deployment validation failed:")
        for error in validation_result['errors']:
            print(f"   • {error}")
    
    # Example 6: Template variable demonstration
    print(f"\n📝 Template Variable Substitution Example:")
    
    # Check a deployed pattern for variable substitution
    patterns_dir = target_dir / "patterns"
    sample_pattern = None
    
    for pattern_file in patterns_dir.rglob("*.md"):
        sample_pattern = pattern_file
        break
    
    if sample_pattern:
        with open(sample_pattern, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"   Sample pattern: {sample_pattern.name}")
        
        # Check for substituted variables
        variables_found = []
        if "Christian" in content:
            variables_found.append("USER_NAME → Christian")
        if "MyProject" in content:
            variables_found.append("PROJECT_NAME → MyProject")
        if str(target_dir.resolve()) in content:
            variables_found.append(f"PROJECT_PATH → {target_dir.resolve()}")
        
        if variables_found:
            print("   ✅ Variables substituted:")
            for var in variables_found:
                print(f"      • {var}")
        
        # Check for protected variables
        protected_found = []
        for protected in ["{{IMPLEMENTATION}}", "{{CUSTOM_LOGIC}}", "{{PATTERN_CONTENT}}"]:
            if protected in content:
                protected_found.append(protected)
        
        if protected_found:
            print("   🔒 Protected variables preserved:")
            for prot in protected_found:
                print(f"      • {prot}")
    
    # Example 7: Rollback demonstration
    print(f"\n🔙 Rollback Demonstration:")
    
    rollback_result = enhancer.rollback_pattern_deployment(target_dir)
    
    if rollback_result['success']:
        print("✅ Rollback successful!")
        print(f"   Patterns removed: {len(rollback_result['patterns_removed'])}")
        
        # Verify rollback
        remaining_patterns = list(patterns_dir.rglob("*.md")) if patterns_dir.exists() else []
        print(f"   Remaining patterns: {len(remaining_patterns)}")
    
    # Cleanup
    if target_dir.exists():
        import shutil
        shutil.rmtree(target_dir)
        print(f"   🧹 Cleaned up: {target_dir}")
    
    print("\n🎉 Pattern Deployment Example Complete!")
    print("=" * 65)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Example failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)