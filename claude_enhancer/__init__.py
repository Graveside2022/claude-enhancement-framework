"""
Claude Enhancement Framework
Version: 1.0.0
Author: Christian

A deployable framework for CLAUDE optimization with 98.5% boot improvement,
pattern-first development, and automated learning systems.
"""

__version__ = "1.0.0"
__author__ = "Christian"

from .core.enhancer import ClaudeEnhancer
from .core.config import Config
from .core.path_manager import PathManager
from .deployment.pattern_deployer import PatternDeployer

__all__ = ["ClaudeEnhancer", "Config", "PathManager", "PatternDeployer"]