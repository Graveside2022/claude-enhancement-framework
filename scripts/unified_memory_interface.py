#!/usr/bin/env python3
"""
Unified Memory Interface
Provides single access point for all memory operations, eliminating fragmentation
Author: Christian
Created: 2025-06-18
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from pathlib import Path

class UnifiedMemoryInterface:
    """Unified interface for all memory operations"""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.memory_dir = self.project_root / "memory"
        self.unified_file = self.memory_dir / "unified_memory.json"
        self.schema_file = self.memory_dir / "unified_memory_schema.json"
        
        # Initialize if needed
        if not self.unified_file.exists():
            self._initialize_unified_memory()
    
    def _initialize_unified_memory(self):
        """Initialize unified memory structure"""
        initial_data = {
            "metadata": {
                "version": "1.0.0",
                "created": datetime.now(timezone.utc).isoformat(),
                "user": "Christian",
                "last_updated": datetime.now(timezone.utc).isoformat()
            },
            "sessions": {},
            "patterns": {},
            "errors": {},
            "analytics": {
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "totals": {
                    "patterns_available": 0,
                    "patterns_used": 0,
                    "total_applications": 0,
                    "success_rate": 0.0,
                    "average_quality": 0.0,
                    "total_time_saved": 0
                },
                "trends": {
                    "quality_trend": "stable",
                    "usage_trend": "stable", 
                    "error_trend": "stable"
                },
                "recommendations": []
            }
        }
        
        self.memory_dir.mkdir(exist_ok=True)
        with open(self.unified_file, 'w') as f:
            json.dump(initial_data, f, indent=2)
    
    def _load_memory(self) -> Dict:
        """Load unified memory data"""
        with open(self.unified_file, 'r') as f:
            return json.load(f)
    
    def _save_memory(self, data: Dict):
        """Save unified memory data"""
        data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
        with open(self.unified_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def start_session(self, context: str = "work") -> str:
        """Start new session and return session_id"""
        data = self._load_memory()
        session_id = f"{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
        
        data["sessions"][session_id] = {
            "session_id": session_id,
            "start_time": datetime.now(timezone.utc).isoformat(),
            "end_time": None,
            "user": "Christian",
            "context": context,
            "activities": []
        }
        
        self._save_memory(data)
        return session_id
    
    def end_session(self, session_id: str):
        """End session"""
        data = self._load_memory()
        if session_id in data["sessions"]:
            data["sessions"][session_id]["end_time"] = datetime.now(timezone.utc).isoformat()
            self._save_memory(data)
    
    def log_activity(self, session_id: str, activity_type: str, **kwargs) -> str:
        """Log unified activity (replaces fragmented logging)"""
        data = self._load_memory()
        
        activity_id = f"{session_id}_{len(data['sessions'][session_id]['activities']):03d}"
        
        activity = {
            "activity_id": activity_id,
            "type": activity_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "pattern_id": kwargs.get("pattern_id"),
            "context": kwargs.get("context", ""),
            "complexity": kwargs.get("complexity", 5),
            "result": kwargs.get("result", "success"),
            "quality_metrics": kwargs.get("quality_metrics", {}),
            "impact_metrics": kwargs.get("impact_metrics", {}),
            "related_activities": kwargs.get("related_activities", []),
            "notes": kwargs.get("notes", ""),
            "side_effects": kwargs.get("side_effects", [])
        }
        
        data["sessions"][session_id]["activities"].append(activity)
        self._update_analytics(data, activity)
        self._save_memory(data)
        
        return activity_id
    
    def log_pattern_usage(self, session_id: str, pattern_id: str, **kwargs) -> str:
        """Log pattern usage (unified tracking)"""
        return self.log_activity(
            session_id=session_id,
            activity_type="pattern_usage",
            pattern_id=pattern_id,
            **kwargs
        )
    
    def log_error_resolution(self, session_id: str, error_pattern: str, **kwargs) -> str:
        """Log error resolution"""
        activity_id = self.log_activity(
            session_id=session_id,
            activity_type="error_resolution", 
            context=error_pattern,
            **kwargs
        )
        
        # Update error tracking
        data = self._load_memory()
        error_id = f"ERROR_{error_pattern.upper().replace(' ', '_')}"
        
        if error_id not in data["errors"]:
            data["errors"][error_id] = {
                "error_id": error_id,
                "pattern_name": error_pattern,
                "category": kwargs.get("category", "implementation"),
                "frequency": "low",
                "status": "resolved",
                "first_occurrence": datetime.now(timezone.utc).isoformat(),
                "last_occurrence": datetime.now(timezone.utc).isoformat(),
                "root_cause": kwargs.get("root_cause", ""),
                "resolution_activity_id": activity_id,
                "prevention_pattern_id": kwargs.get("prevention_pattern_id"),
                "quality_impact": kwargs.get("quality_impact", 0),
                "resolution_time": kwargs.get("resolution_time", 0)
            }
        else:
            data["errors"][error_id]["status"] = "resolved"
            data["errors"][error_id]["last_occurrence"] = datetime.now(timezone.utc).isoformat()
            data["errors"][error_id]["resolution_activity_id"] = activity_id
        
        self._save_memory(data)
        return activity_id
    
    def log_side_effect(self, session_id: str, effect_description: str, **kwargs) -> str:
        """Log side effects (unified tracking)"""
        return self.log_activity(
            session_id=session_id,
            activity_type="side_effect",
            context=effect_description,
            **kwargs
        )
    
    def update_pattern_status(self, pattern_id: str, **kwargs):
        """Update pattern information"""
        data = self._load_memory()
        
        if pattern_id not in data["patterns"]:
            data["patterns"][pattern_id] = {
                "pattern_id": pattern_id,
                "category": kwargs.get("category", ""),
                "status": "active",
                "creation_date": datetime.now(timezone.utc).isoformat(),
                "usage_count": 0,
                "success_rate": 0.0,
                "average_quality": 0.0,
                "contexts": [],
                "promotion_criteria": {
                    "usage_frequency": False,
                    "success_rate": False,
                    "quality_score": False,
                    "reusability_index": False,
                    "user_satisfaction": False,
                    "technical_debt": False
                },
                "applications": []
            }
        
        # Update with provided kwargs
        for key, value in kwargs.items():
            if key in data["patterns"][pattern_id]:
                data["patterns"][pattern_id][key] = value
        
        self._save_memory(data)
    
    def get_analytics(self) -> Dict:
        """Get current analytics"""
        data = self._load_memory()
        return data["analytics"]
    
    def get_pattern_performance(self, pattern_id: str = None) -> Dict:
        """Get pattern performance data"""
        data = self._load_memory()
        
        if pattern_id:
            return data["patterns"].get(pattern_id, {})
        else:
            return data["patterns"]
    
    def get_error_patterns(self) -> Dict:
        """Get error pattern data"""
        data = self._load_memory()
        return data["errors"]
    
    def get_session_activities(self, session_id: str) -> List[Dict]:
        """Get activities for a session"""
        data = self._load_memory()
        return data["sessions"].get(session_id, {}).get("activities", [])
    
    def search_activities(self, **criteria) -> List[Dict]:
        """Search activities by criteria"""
        data = self._load_memory()
        results = []
        
        for session in data["sessions"].values():
            for activity in session["activities"]:
                match = True
                for key, value in criteria.items():
                    if key not in activity or activity[key] != value:
                        match = False
                        break
                if match:
                    results.append(activity)
        
        return results
    
    def _update_analytics(self, data: Dict, activity: Dict):
        """Update analytics based on new activity"""
        analytics = data["analytics"]
        
        # Update totals
        if activity["type"] == "pattern_usage":
            analytics["totals"]["total_applications"] += 1
            
            # Update success rate
            total_activities = sum(
                len(session["activities"]) 
                for session in data["sessions"].values()
            )
            successful_activities = len([
                a for session in data["sessions"].values()
                for a in session["activities"]
                if a["result"] == "success"
            ])
            
            if total_activities > 0:
                analytics["totals"]["success_rate"] = (successful_activities / total_activities) * 100
            
            # Update average quality
            quality_scores = [
                a.get("quality_metrics", {}).get("overall_score", 0)
                for session in data["sessions"].values()
                for a in session["activities"]
                if a.get("quality_metrics", {}).get("overall_score", 0) > 0
            ]
            
            if quality_scores:
                analytics["totals"]["average_quality"] = sum(quality_scores) / len(quality_scores)
            
            # Update time saved
            time_saved = activity.get("impact_metrics", {}).get("time_saved", 0)
            analytics["totals"]["total_time_saved"] += time_saved
    
    def generate_report(self, report_type: str = "summary") -> str:
        """Generate unified memory report"""
        data = self._load_memory()
        
        if report_type == "summary":
            return self._generate_summary_report(data)
        elif report_type == "patterns":
            return self._generate_pattern_report(data)
        elif report_type == "errors":
            return self._generate_error_report(data)
        else:
            return "Unknown report type"
    
    def _generate_summary_report(self, data: Dict) -> str:
        """Generate summary report"""
        analytics = data["analytics"]
        
        report = f"""# Unified Memory Summary Report
Generated: {datetime.now(timezone.utc).isoformat()}
User: Christian

## Overall Statistics
- Total Pattern Applications: {analytics['totals']['total_applications']}
- Success Rate: {analytics['totals']['success_rate']:.1f}%
- Average Quality Score: {analytics['totals']['average_quality']:.1f}/10
- Total Time Saved: {analytics['totals']['total_time_saved']} minutes

## Active Sessions: {len(data['sessions'])}
## Tracked Patterns: {len(data['patterns'])}
## Error Patterns: {len(data['errors'])}

## Current Trends
- Quality: {analytics['trends']['quality_trend']}
- Usage: {analytics['trends']['usage_trend']}
- Error Rate: {analytics['trends']['error_trend']}
"""
        return report
    
    def migrate_from_legacy(self):
        """Migrate data from legacy fragmented files"""
        # This would contain the migration logic
        pass


# Example usage and testing
if __name__ == "__main__":
    # Initialize interface
    memory = UnifiedMemoryInterface()
    
    # Start session
    session_id = memory.start_session("work")
    print(f"Started session: {session_id}")
    
    # Log some activities
    memory.log_pattern_usage(
        session_id=session_id,
        pattern_id="ARCH-001",
        context="File organization",
        complexity=6,
        quality_metrics={"overall_score": 8.5},
        impact_metrics={"time_saved": 45}
    )
    
    # Generate report
    report = memory.generate_report("summary")
    print(report)
    
    # End session
    memory.end_session(session_id)