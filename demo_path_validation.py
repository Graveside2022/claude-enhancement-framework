#!/usr/bin/env python3
"""
Path Validation System Demonstration
Interactive demonstration of the comprehensive path validation system.

Created for: Christian - Agent 8 Implementation  
Purpose: Demonstrate path validation features for user-specified installation directories
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add framework to path
framework_path = Path(__file__).parent
sys.path.insert(0, str(framework_path))

from claude_enhancer.core.path_manager import PathManager


def demo_path_validation():
    """Interactive demonstration of path validation features."""
    print("🛡️ Path Validation System Demonstration")
    print("Comprehensive validation for user-specified installation directories")
    print("=" * 70)
    
    path_manager = PathManager("demo_user", "demo_project")
    temp_dir = None
    
    try:
        # Create test environment
        temp_dir = Path(tempfile.mkdtemp(prefix="claude_demo_"))
        print(f"🔧 Demo environment: {temp_dir}")
        
        # Demo 1: Valid existing directory
        print("\n📁 Demo 1: Valid Existing Directory")
        print("-" * 40)
        
        valid_dir = temp_dir / "valid_directory"
        valid_dir.mkdir(exist_ok=True)
        
        is_valid, errors, validated_path = path_manager.validate_path(
            valid_dir,
            check_exists=True,
            check_writable=True,
            create_if_missing=False,
            require_confirmation=False
        )
        
        print(f"✅ Directory: {valid_dir}")
        print(f"   Valid: {is_valid}")
        print(f"   Errors: {errors if errors else 'None'}")
        print(f"   Validated path: {validated_path}")
        
        # Demo 2: Non-existent directory with creation
        print("\n📁 Demo 2: Non-existent Directory (with creation)")
        print("-" * 50)
        
        new_dir = temp_dir / "new_directory"
        print(f"Directory to create: {new_dir}")
        print("This will prompt for user confirmation...")
        
        is_valid, errors, validated_path = path_manager.validate_path(
            new_dir,
            check_exists=True,
            check_writable=True,
            create_if_missing=True,
            require_confirmation=True
        )
        
        print(f"   Valid: {is_valid}")
        print(f"   Directory created: {new_dir.exists()}")
        print(f"   Errors: {errors if errors else 'None'}")
        
        # Demo 3: Invalid path characters
        print("\n📁 Demo 3: Invalid Path Characters")
        print("-" * 40)
        
        invalid_path = str(temp_dir / "invalid\x00path")  # Null byte
        
        is_valid, errors, validated_path = path_manager.validate_path(
            invalid_path,
            check_exists=False,
            check_writable=False,
            create_if_missing=False,
            require_confirmation=False
        )
        
        print(f"❌ Invalid path: {repr(invalid_path)}")
        print(f"   Valid: {is_valid}")
        print(f"   Errors: {errors}")
        
        # Demo 4: Relative path handling
        print("\n📁 Demo 4: Relative Path Handling")
        print("-" * 40)
        
        relative_path = "~/claude_demo_test"
        
        is_valid, errors, validated_path = path_manager.validate_path(
            relative_path,
            check_exists=True,
            check_writable=True,
            create_if_missing=True,
            require_confirmation=False  # Auto-create for demo
        )
        
        print(f"🏠 Relative path: {relative_path}")
        print(f"   Expanded to: {validated_path}")
        print(f"   Valid: {is_valid}")
        print(f"   Directory created: {validated_path.exists() if validated_path else False}")
        
        # Cleanup relative path test
        if validated_path and validated_path.exists():
            validated_path.rmdir()
            print(f"   Cleaned up: {validated_path}")
        
        # Demo 5: Safe directory path with fallback
        print("\n📁 Demo 5: Safe Directory Path with Fallback")
        print("-" * 50)
        
        invalid_input = "/totally/invalid/nonexistent/path"
        default_path = temp_dir / "safe_default"
        default_path.mkdir(exist_ok=True)
        
        print(f"❌ Invalid input: {invalid_input}")
        print(f"🛡️ Default fallback: {default_path}")
        
        # This will automatically decline creation and fall back
        result_path = path_manager.get_safe_directory_path(
            invalid_input,
            default_path,
            "demo installation"
        )
        
        print(f"   Result path: {result_path}")
        print(f"   Used fallback: {result_path == default_path}")
        
        # Demo 6: Platform-specific validation
        print("\n📁 Demo 6: Platform-Specific Validation")
        print("-" * 45)
        
        test_dir = temp_dir / "platform_test"
        test_dir.mkdir(exist_ok=True)
        
        platform_errors = path_manager._validate_platform_specific(test_dir)
        
        print(f"🖥️  Platform: {path_manager.platform}")
        print(f"   Test directory: {test_dir}")
        print(f"   Platform-specific errors: {platform_errors if platform_errors else 'None'}")
        
        # Demo 7: Write permission testing
        print("\n📁 Demo 7: Write Permission Testing")
        print("-" * 42)
        
        can_write = path_manager._check_write_permission(test_dir)
        
        print(f"✍️ Write permission test: {test_dir}")
        print(f"   Can write: {can_write}")
        print(f"   Method: Temporary file creation test")
        
        print("\n" + "=" * 70)
        print("🎯 PATH VALIDATION DEMONSTRATION COMPLETE")
        print("=" * 70)
        
        print("\n📋 Features Demonstrated:")
        print("   ✅ Path existence validation")
        print("   ✅ Write permission checking")
        print("   ✅ Directory creation with user confirmation")
        print("   ✅ Invalid character detection")
        print("   ✅ Relative path expansion")
        print("   ✅ Safe fallback mechanism")
        print("   ✅ Platform-specific validation")
        print("   ✅ Write permission testing")
        
        print("\n🚀 The path validation system is fully operational and ready for")
        print("   deployment in the Claude Enhancement Framework setup process!")
        
    except Exception as e:
        print(f"\n💥 Demo crashed: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)
            print(f"\n🧹 Demo environment cleaned up: {temp_dir}")


if __name__ == "__main__":
    try:
        demo_path_validation()
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo cancelled by user")
    except Exception as e:
        print(f"\n💥 Demo failed: {e}")
        sys.exit(1)