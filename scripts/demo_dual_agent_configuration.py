#!/usr/bin/env python3

"""
Dual Agent Configuration Demo Script
Demonstrates the context detection and agent count determination
For: Christian
Created: 2025-06-17
"""

import re
from typing import Tuple, List

class DualAgentConfigurationDemo:
    """Demo class to show how the dual agent configuration system works"""
    
    def __init__(self):
        # Boot context triggers (exact phrases to avoid false positives)
        self.boot_triggers = [
            "hi", "hello", "setup", "startup", "boot", "start", "ready", 
            "i'm christian", "what's up", "bootup", "boot up"
        ]
        
        # Work context triggers
        self.work_triggers = [
            "implement", "create", "build", "analyze", "design", "investigate", 
            "develop", "refactor", "optimize", "test", "debug", "fix"
        ]
        
        # Complex context indicators
        self.complex_indicators = [
            "comprehensive", "system-wide", "architectural", "complete system",
            "full implementation", "end-to-end", "multiple components",
            "complex", "advanced", "enterprise"
        ]
        
        # Agent configurations
        self.agent_config = {
            'boot': 3,
            'work': 5, 
            'complex': 10
        }
    
    def detect_context(self, user_input: str) -> str:
        """
        Detect the context based on user input
        Returns: 'boot', 'work', or 'complex'
        """
        input_lower = user_input.lower()
        
        # Check for manual override first
        agent_match = re.search(r'use\s+(\d+)\s+agents?', input_lower)
        if agent_match:
            return f"manual_{agent_match.group(1)}"
            
        # Check for complex context indicators
        if any(indicator in input_lower for indicator in self.complex_indicators):
            return 'complex'
            
        # Check for boot context (use word boundaries for better matching)
        for trigger in self.boot_triggers:
            # Handle special cases
            if trigger == "what's up" and "what's up" in input_lower:
                return 'boot'
            elif trigger in ["hi", "hello", "setup", "startup", "boot", "start", "ready"]:
                # Use word boundaries for these common words
                if re.search(r'\b' + re.escape(trigger) + r'\b', input_lower):
                    return 'boot'
            elif trigger in input_lower:
                return 'boot'
            
        # Check for work context
        if any(trigger in input_lower for trigger in self.work_triggers):
            return 'work'
            
        # Default to work context
        return 'work'
    
    def get_agent_count(self, context: str) -> int:
        """Get agent count based on context"""
        if context.startswith('manual_'):
            return int(context.split('_')[1])
        return self.agent_config.get(context, 5)
    
    def determine_agents(self, user_input: str) -> Tuple[str, int, List[str]]:
        """
        Determine context, agent count, and reasoning
        Returns: (context, agent_count, reasoning_list)
        """
        context = self.detect_context(user_input)
        agent_count = self.get_agent_count(context)
        
        reasoning = []
        input_lower = user_input.lower()
        
        if context.startswith('manual_'):
            reasoning.append(f"Manual override detected: 'use {context.split('_')[1]} agents'")
        elif context == 'boot':
            found_triggers = [t for t in self.boot_triggers if t in input_lower]
            reasoning.append(f"Boot context detected from triggers: {found_triggers}")
            reasoning.append("Using 3 agents for faster startup")
        elif context == 'work':
            found_triggers = [t for t in self.work_triggers if t in input_lower]
            if found_triggers:
                reasoning.append(f"Work context detected from triggers: {found_triggers}")
            else:
                reasoning.append("Defaulting to work context (no specific triggers found)")
            reasoning.append("Using 5 agents for thorough analysis")
        elif context == 'complex':
            found_indicators = [i for i in self.complex_indicators if i in input_lower]
            reasoning.append(f"Complex context detected from indicators: {found_indicators}")
            reasoning.append("Using 10 agents for comprehensive coverage")
            
        return context, agent_count, reasoning

def demo_examples():
    """Run demonstration with various example inputs"""
    demo = DualAgentConfigurationDemo()
    
    test_cases = [
        # Boot context examples
        "Hi Christian",
        "Hello, please setup the project",
        "Start the boot sequence",
        "Ready to begin startup",
        
        # Work context examples  
        "Analyze the configuration system",
        "Implement the new feature",
        "Create a dual agent system",
        "Design the architecture",
        "Investigate this issue",
        "Debug the performance problem",
        
        # Complex context examples
        "Implement comprehensive dual agent system with error handling",
        "Create complete system architecture with testing",
        "Design enterprise-level solution with full validation",
        "Build complex multi-component system",
        
        # Manual override examples
        "Use 7 agents to analyze this",
        "Please use 12 agents for this task",
        
        # Default/ambiguous examples
        "What do you think about this?",
        "Can you help me with something?",
        "Show me the documentation"
    ]
    
    print("🤖 Dual Agent Configuration Demo")
    print("=" * 50)
    print()
    
    for i, test_input in enumerate(test_cases, 1):
        context, agent_count, reasoning = demo.determine_agents(test_input)
        
        print(f"Example {i}:")
        print(f"  Input: '{test_input}'")
        print(f"  Context: {context}")
        print(f"  Agents: {agent_count}")
        print(f"  Reasoning:")
        for reason in reasoning:
            print(f"    - {reason}")
        print()

def validate_configuration():
    """Validate that the configuration matches the implementation"""
    demo = DualAgentConfigurationDemo()
    
    print("🔍 Configuration Validation")
    print("=" * 30)
    print()
    
    # Test boot context
    boot_test = "Hi Christian, setup"
    context, agents, _ = demo.determine_agents(boot_test)
    assert context == 'boot' and agents == 3, f"Boot test failed: {context}, {agents}"
    print("✅ Boot context validation passed")
    
    # Test work context
    work_test = "Analyze the system"
    context, agents, _ = demo.determine_agents(work_test)  
    assert context == 'work' and agents == 5, f"Work test failed: {context}, {agents}"
    print("✅ Work context validation passed")
    
    # Test complex context
    complex_test = "Implement comprehensive solution"
    context, agents, _ = demo.determine_agents(complex_test)
    assert context == 'complex' and agents == 10, f"Complex test failed: {context}, {agents}"
    print("✅ Complex context validation passed")
    
    # Test manual override
    manual_test = "Use 7 agents to investigate"
    context, agents, _ = demo.determine_agents(manual_test)
    assert context == 'manual_7' and agents == 7, f"Manual test failed: {context}, {agents}"
    print("✅ Manual override validation passed")
    
    # Test default
    default_test = "What do you think?"
    context, agents, _ = demo.determine_agents(default_test)
    assert context == 'work' and agents == 5, f"Default test failed: {context}, {agents}"
    print("✅ Default context validation passed")
    
    print()
    print("🎉 All configuration validations passed!")

if __name__ == "__main__":
    print("🚀 Running Dual Agent Configuration Demo")
    print()
    
    # Run validation first
    validate_configuration()
    print()
    
    # Run examples
    demo_examples()
    
    print("📊 Demo Summary:")
    print("- Boot context: 3 agents (faster startup)")
    print("- Work context: 5 agents (thorough analysis)")  
    print("- Complex context: 10 agents (comprehensive coverage)")
    print("- Manual override: Custom agent count")
    print("- Default: Work context if unclear")
    print()
    print("✅ Dual Agent Configuration System Ready for Use!")