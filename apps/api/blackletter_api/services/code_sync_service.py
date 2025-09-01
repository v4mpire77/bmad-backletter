"""
Code Synchronization Service for Independent Orchestration Agent

This service provides real-time code monitoring, conflict detection, and 
synchronization across multiple AI agents working on the same codebase.
"""

import asyncio
import json
import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent, FileDeletedEvent
import hashlib
import difflib

logger = logging.getLogger(__name__)

@dataclass
class CodeChange:
    """Represents a code change detected by the sync service"""
    file_path: str
    agent_id: str
    timestamp: datetime
    change_type: str  # 'created', 'modified', 'deleted'
    file_hash: str
    previous_hash: Optional[str] = None
    conflict_level: str = 'low'  # 'low', 'medium', 'high', 'critical'
    affected_agents: List[str] = field(default_factory=list)

@dataclass
class CodeConflict:
    """Represents a code conflict between multiple agents"""
    conflict_id: str
    file_path: str
    conflicting_agents: List[str]
    conflict_type: str  # 'merge', 'deletion', 'addition'
    severity: str  # 'low', 'medium', 'high', 'critical'
    detected_at: datetime
    resolution_status: str = 'pending'  # 'pending', 'resolving', 'resolved', 'escalated'
    resolution_strategy: Optional[str] = None

@dataclass
class AgentStatus:
    """Represents the current status of an AI agent"""
    agent_id: str
    status: str  # 'active', 'idle', 'busy', 'error', 'offline'
    last_activity: datetime = field(default_factory=datetime.now)
    current_task: Optional[str] = None
    workload: float = 0.0  # 0.0 to 1.0
    capabilities: List[str] = field(default_factory=list)

class CodeSyncService:
    """
    Main service for coordinating code synchronization across AI agents.
    
    Features:
    - Real-time file system monitoring
    - Conflict detection and analysis
    - Automatic conflict resolution coordination
    - Agent workload balancing
    - Code quality validation
    """
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.agents: Dict[str, AgentStatus] = {}
        self.active_changes: Dict[str, CodeChange] = {}
        self.conflicts: Dict[str, CodeConflict] = {}
        self.file_hashes: Dict[str, str] = {}
        self.observer: Optional[Observer] = None
        self.is_monitoring = False
        
        # Configuration
        self.conflict_thresholds = {
            'low': 0.1,      # 10% change overlap
            'medium': 0.3,   # 30% change overlap
            'high': 0.6,     # 60% change overlap
            'critical': 0.8  # 80% change overlap
        }
        
        # File patterns to monitor
        self.monitored_extensions = {
            '.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.cpp', '.c',
            '.h', '.hpp', '.cs', '.go', '.rs', '.php', '.rb', '.swift'
        }
        
        # Initialize file hashes
        self._initialize_file_hashes()
    
    def _initialize_file_hashes(self):
        """Initialize file hashes for all monitored files"""
        logger.info("Initializing file hashes for code synchronization")
        for file_path in self._get_monitored_files():
            self.file_hashes[str(file_path)] = self._calculate_file_hash(file_path)
    
    def _get_monitored_files(self) -> List[Path]:
        """Get all monitored files in the project"""
        monitored_files = []
        for root, dirs, files in os.walk(self.project_root):
            # Skip common directories that shouldn't be monitored
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if any(file.endswith(ext) for ext in self.monitored_extensions):
                    monitored_files.append(Path(root) / file)
        
        return monitored_files
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of a file"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return hashlib.sha256(content).hexdigest()
        except Exception as e:
            logger.warning(f"Could not calculate hash for {file_path}: {e}")
            return ""
    
    def start_monitoring(self):
        """Start monitoring the file system for changes"""
        if self.is_monitoring:
            logger.warning("File monitoring is already active")
            return
        
        logger.info("Starting code synchronization monitoring")
        
        # Create file system observer
        self.observer = Observer()
        event_handler = CodeChangeHandler(self)
        self.observer.schedule(event_handler, str(self.project_root), recursive=True)
        self.observer.start()
        
        self.is_monitoring = True
        logger.info(f"Code synchronization monitoring started for {self.project_root}")
    
    def stop_monitoring(self):
        """Stop monitoring the file system"""
        if not self.is_monitoring:
            return
        
        logger.info("Stopping code synchronization monitoring")
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
        
        self.is_monitoring = False
        logger.info("Code synchronization monitoring stopped")
    
    def register_agent(self, agent_id: str, capabilities: List[str] = None):
        """Register a new AI agent with the sync service"""
        if agent_id in self.agents:
            logger.warning(f"Agent {agent_id} is already registered")
            return
        
        self.agents[agent_id] = AgentStatus(
            agent_id=agent_id,
            status='active',
            last_activity=datetime.now(),
            capabilities=capabilities or []
        )
        
        logger.info(f"Registered agent {agent_id} with capabilities: {capabilities}")
    
    def unregister_agent(self, agent_id: str):
        """Unregister an AI agent from the sync service"""
        if agent_id not in self.agents:
            return
        
        del self.agents[agent_id]
        logger.info(f"Unregistered agent {agent_id}")
    
    def update_agent_status(self, agent_id: str, status: str, task: str = None, workload: float = 0.0):
        """Update the status of a registered agent"""
        if agent_id not in self.agents:
            logger.warning(f"Cannot update status for unregistered agent {agent_id}")
            return
        
        self.agents[agent_id].status = status
        self.agents[agent_id].current_task = task
        self.agents[agent_id].workload = workload
        self.agents[agent_id].last_activity = datetime.now()
        
        logger.debug(f"Updated agent {agent_id} status: {status}, task: {task}, workload: {workload}")
    
    def process_code_change(self, file_path: str, agent_id: str, change_type: str) -> Optional[CodeChange]:
        """Process a detected code change and return change details"""
        file_path_obj = Path(file_path)
        
        # Check if file should be monitored
        if not any(file_path_obj.suffix == ext for ext in self.monitored_extensions):
            return None
        
        # Calculate new hash
        new_hash = self._calculate_file_hash(file_path_obj)
        previous_hash = self.file_hashes.get(str(file_path), "")
        
        # Create change record
        change = CodeChange(
            file_path=str(file_path),
            agent_id=agent_id,
            timestamp=datetime.now(),
            change_type=change_type,
            file_hash=new_hash,
            previous_hash=previous_hash
        )
        
        # Update file hash
        self.file_hashes[str(file_path)] = new_hash
        
        # Analyze change impact
        self._analyze_change_impact(change)
        
        # Store change
        change_id = f"{file_path}_{int(time.time())}"
        self.active_changes[change_id] = change
        
        logger.info(f"Processed code change: {change_type} on {file_path} by agent {agent_id}")
        
        return change
    
    def _analyze_change_impact(self, change: CodeChange):
        """Analyze the impact of a code change and identify affected agents"""
        affected_agents = []
        
        # Check if other agents are working on related files
        for agent_id, agent in self.agents.items():
            if agent_id == change.agent_id:
                continue
            
            # Check if agent is currently working on related tasks
            if agent.current_task and self._is_related_task(agent.current_task, change.file_path):
                affected_agents.append(agent_id)
                change.conflict_level = 'medium'
        
        # Check for actual file conflicts
        if change.previous_hash:
            conflict_level = self._detect_conflict_level(change)
            if conflict_level != 'low':
                change.conflict_level = conflict_level
                self._create_conflict_record(change)
        
        change.affected_agents = affected_agents
    
    def _is_related_task(self, task: str, file_path: str) -> bool:
        """Check if a task is related to a specific file"""
        # Simple heuristic: check if task description contains file-related keywords
        file_keywords = file_path.lower().replace('_', ' ').replace('-', ' ').split('.')[0]
        return file_keywords in task.lower()
    
    def _detect_conflict_level(self, change: CodeChange) -> str:
        """Detect the level of conflict for a code change"""
        if not change.previous_hash:
            return 'low'
        
        # This is a simplified conflict detection
        # In a real implementation, you'd do more sophisticated diff analysis
        return 'low'  # Placeholder for now
    
    def _create_conflict_record(self, change: CodeChange):
        """Create a conflict record when conflicts are detected"""
        conflict = CodeConflict(
            conflict_id=f"conflict_{int(time.time())}",
            file_path=change.file_path,
            conflicting_agents=[change.agent_id] + change.affected_agents,
            conflict_type='merge',
            severity=change.conflict_level,
            detected_at=datetime.now()
        )
        
        self.conflicts[conflict.conflict_id] = conflict
        logger.warning(f"Created conflict record: {conflict.conflict_id} for {change.file_path}")
    
    def get_agent_recommendations(self, file_path: str) -> List[str]:
        """Get recommendations for which agents should work on a file"""
        recommendations = []
        
        # Find agents with relevant capabilities
        for agent_id, agent in self.agents.items():
            if agent.status != 'active':
                continue
            
            # Check if agent has relevant capabilities
            if self._agent_can_handle_file(agent, file_path):
                recommendations.append(agent_id)
        
        # Sort by workload (prefer less busy agents)
        recommendations.sort(key=lambda aid: self.agents[aid].workload)
        
        return recommendations
    
    def _agent_can_handle_file(self, agent: AgentStatus, file_path: str) -> bool:
        """Check if an agent can handle a specific file type"""
        file_ext = Path(file_path).suffix.lower()
        
        # Map file extensions to capabilities
        extension_capabilities = {
            '.py': ['python', 'backend', 'api'],
            '.js': ['javascript', 'frontend', 'web'],
            '.ts': ['typescript', 'frontend', 'web'],
            '.tsx': ['typescript', 'react', 'frontend'],
            '.jsx': ['javascript', 'react', 'frontend'],
            '.java': ['java', 'backend', 'android'],
            '.cpp': ['cpp', 'backend', 'system'],
            '.c': ['c', 'backend', 'system'],
            '.go': ['go', 'backend', 'system'],
            '.rs': ['rust', 'backend', 'system']
        }
        
        required_capabilities = extension_capabilities.get(file_ext, [])
        
        # Check if agent has any of the required capabilities
        return any(cap in agent.capabilities for cap in required_capabilities)
    
    def get_sync_status(self) -> Dict:
        """Get current synchronization status"""
        return {
            'monitoring_active': self.is_monitoring,
            'registered_agents': len(self.agents),
            'active_changes': len(self.active_changes),
            'active_conflicts': len([c for c in self.conflicts.values() if c.resolution_status == 'pending']),
            'resolved_conflicts': len([c for c in self.conflicts.values() if c.resolution_status == 'resolved']),
            'total_files_monitored': len(self.file_hashes)
        }
    
    def get_agent_status(self) -> List[Dict]:
        """Get status of all registered agents"""
        return [asdict(agent) for agent in self.agents.values()]
    
    def get_conflicts(self, status: str = None) -> List[Dict]:
        """Get list of conflicts, optionally filtered by status"""
        conflicts = self.conflicts.values()
        if status:
            conflicts = [c for c in conflicts if c.resolution_status == status]
        
        return [asdict(conflict) for conflict in conflicts]
    
    def resolve_conflict(self, conflict_id: str, resolution_strategy: str, resolved_by: str):
        """Mark a conflict as resolved"""
        if conflict_id not in self.conflicts:
            logger.warning(f"Conflict {conflict_id} not found")
            return
        
        conflict = self.conflicts[conflict_id]
        conflict.resolution_status = 'resolved'
        conflict.resolution_strategy = resolution_strategy
        
        logger.info(f"Conflict {conflict_id} resolved by {resolved_by} using strategy: {resolution_strategy}")
    
    def cleanup_old_changes(self, max_age_hours: int = 24):
        """Clean up old change records"""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        changes_to_remove = []
        for change_id, change in self.active_changes.items():
            if change.timestamp < cutoff_time:
                changes_to_remove.append(change_id)
        
        for change_id in changes_to_remove:
            del self.active_changes[change_id]
        
        if changes_to_remove:
            logger.info(f"Cleaned up {len(changes_to_remove)} old change records")


class CodeChangeHandler(FileSystemEventHandler):
    """File system event handler for code changes"""
    
    def __init__(self, sync_service: CodeSyncService):
        self.sync_service = sync_service
    
    def on_created(self, event):
        if not event.is_directory:
            self.sync_service.process_code_change(
                str(event.src_path), 
                'system', 
                'created'
            )
    
    def on_modified(self, event):
        if not event.is_directory:
            self.sync_service.process_code_change(
                str(event.src_path), 
                'system', 
                'modified'
            )
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.sync_service.process_code_change(
                str(event.src_path), 
                'system', 
                'deleted'
            )


# Global instance for easy access
code_sync_service = CodeSyncService()
