"""
Memory System Templates for Claude Enhancement Framework

This module provides template files for the memory system components:
- learning_archive_template.md: Solution tracking and pattern promotion
- error_patterns_template.md: Error tracking and prevention
- side_effects_log_template.md: Automated side effects tracking  
- solution_candidates_template.md: Solution candidate management

Templates use variables like {{USER_NAME}}, {{PROJECT_NAME}} for customization.
"""

import os
from pathlib import Path

def get_template_path(template_name: str) -> Path:
    """Get the full path to a memory template file."""
    templates_dir = Path(__file__).parent
    return templates_dir / template_name

def list_available_templates() -> list:
    """List all available memory template files."""
    templates_dir = Path(__file__).parent
    return [f.name for f in templates_dir.glob("*_template.md")]

# Template file mappings
MEMORY_TEMPLATES = {
    'learning_archive': 'learning_archive_template.md',
    'error_patterns': 'error_patterns_template.md', 
    'side_effects_log': 'side_effects_log_template.md',
    'solution_candidates': 'solution_candidates_template.md'
}

__all__ = ['get_template_path', 'list_available_templates', 'MEMORY_TEMPLATES']