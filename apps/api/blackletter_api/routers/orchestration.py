"""
Orchestration API Router for Independent Orchestration Agent

This router provides endpoints for:
- Agent registration and status management
- Code synchronization monitoring
- Conflict resolution coordination
- Real-time agent communication
"""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional
import json
import logging
from datetime import datetime

from ..services.code_sync_service import code_sync_service, AgentStatus
from ..models.entities import Base
from ..database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/orchestration", tags=["orchestration"])

# WebSocket connection manager for real-time agent communication
class OrchestrationConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.agent_connections: Dict[str, str] = {}  # agent_id -> connection_id
    
    async def connect(self, websocket: WebSocket, agent_id: str = None):
        await websocket.accept()
        connection_id = f"conn_{len(self.active_connections)}"
        self.active_connections[connection_id] = websocket
        
        if agent_id:
            self.agent_connections[agent_id] = connection_id
            logger.info(f"Agent {agent_id} connected via WebSocket {connection_id}")
        
        return connection_id
    
    def disconnect(self, connection_id: str):
        if connection_id in self.active_connections:
            # Remove agent mapping if exists
            agent_id = None
            for aid, cid in self.agent_connections.items():
                if cid == connection_id:
                    agent_id = aid
                    break
            
            if agent_id:
                del self.agent_connections[agent_id]
                logger.info(f"Agent {agent_id} disconnected from WebSocket {connection_id}")
            
            del self.active_connections[connection_id]
    
    async def send_personal_message(self, message: str, connection_id: str):
        if connection_id in self.active_connections:
            try:
                await self.active_connections[connection_id].send_text(message)
            except Exception as e:
                logger.error(f"Failed to send message to {connection_id}: {e}")
                self.disconnect(connection_id)
    
    async def send_to_agent(self, message: str, agent_id: str):
        """Send message to a specific agent"""
        if agent_id in self.agent_connections:
            connection_id = self.agent_connections[agent_id]
            await self.send_personal_message(message, connection_id)
        else:
            logger.warning(f"Agent {agent_id} not connected via WebSocket")
    
    async def broadcast(self, message: str, exclude_agent: str = None):
        """Broadcast message to all connected agents"""
        for agent_id, connection_id in self.agent_connections.items():
            if agent_id != exclude_agent:
                await self.send_personal_message(message, connection_id)

# Global connection manager
orchestration_manager = OrchestrationConnectionManager()

# Agent Management Endpoints

@router.post("/agents/register")
async def register_agent(agent_id: str, capabilities: List[str] = None):
    """Register a new AI agent with the orchestration service"""
    try:
        code_sync_service.register_agent(agent_id, capabilities)
        
        # Send welcome message via WebSocket if connected
        welcome_message = {
            "type": "agent_registered",
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat(),
            "message": f"Agent {agent_id} successfully registered with capabilities: {capabilities or []}"
        }
        
        await orchestration_manager.broadcast(json.dumps(welcome_message))
        
        return {
            "status": "success",
            "agent_id": agent_id,
            "message": "Agent registered successfully",
            "capabilities": capabilities or []
        }
    except Exception as e:
        logger.error(f"Failed to register agent {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to register agent: {str(e)}")

@router.post("/agents/{agent_id}/status")
async def update_agent_status(
    agent_id: str, 
    status: str, 
    task: Optional[str] = None, 
    workload: float = 0.0
):
    """Update the status of a registered agent"""
    try:
        code_sync_service.update_agent_status(agent_id, status, task, workload)
        
        # Broadcast status update
        status_message = {
            "type": "agent_status_update",
            "agent_id": agent_id,
            "status": status,
            "task": task,
            "workload": workload,
            "timestamp": datetime.now().isoformat()
        }
        
        await orchestration_manager.broadcast(json.dumps(status_message))
        
        return {
            "status": "success",
            "agent_id": agent_id,
            "message": "Agent status updated successfully"
        }
    except Exception as e:
        logger.error(f"Failed to update agent {agent_id} status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update agent status: {str(e)}")

@router.delete("/agents/{agent_id}")
async def unregister_agent(agent_id: str):
    """Unregister an AI agent from the orchestration service"""
    try:
        code_sync_service.unregister_agent(agent_id)
        
        # Broadcast unregistration
        unregister_message = {
            "type": "agent_unregistered",
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat(),
            "message": f"Agent {agent_id} has been unregistered"
        }
        
        await orchestration_manager.broadcast(json.dumps(unregister_message))
        
        return {
            "status": "success",
            "agent_id": agent_id,
            "message": "Agent unregistered successfully"
        }
    except Exception as e:
        logger.error(f"Failed to unregister agent {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to unregister agent: {str(e)}")

@router.get("/agents")
async def list_agents():
    """Get list of all registered agents and their status"""
    try:
        agents = code_sync_service.get_agent_status()
        return {
            "status": "success",
            "agents": agents,
            "total_agents": len(agents)
        }
    except Exception as e:
        logger.error(f"Failed to list agents: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list agents: {str(e)}")

@router.get("/agents/{agent_id}")
async def get_agent_status(agent_id: str):
    """Get status of a specific agent"""
    try:
        agents = code_sync_service.get_agent_status()
        agent = next((a for a in agents if a["agent_id"] == agent_id), None)
        
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
        
        return {
            "status": "success",
            "agent": agent
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get agent {agent_id} status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get agent status: {str(e)}")

# Code Synchronization Endpoints

@router.post("/sync/start")
async def start_code_sync():
    """Start code synchronization monitoring"""
    try:
        code_sync_service.start_monitoring()
        
        # Broadcast sync start
        sync_message = {
            "type": "code_sync_started",
            "timestamp": datetime.now().isoformat(),
            "message": "Code synchronization monitoring has been started"
        }
        
        await orchestration_manager.broadcast(json.dumps(sync_message))
        
        return {
            "status": "success",
            "message": "Code synchronization monitoring started",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to start code sync: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start code sync: {str(e)}")

@router.post("/sync/stop")
async def stop_code_sync():
    """Stop code synchronization monitoring"""
    try:
        code_sync_service.stop_monitoring()
        
        # Broadcast sync stop
        sync_message = {
            "type": "code_sync_stopped",
            "timestamp": datetime.now().isoformat(),
            "message": "Code synchronization monitoring has been stopped"
        }
        
        await orchestration_manager.broadcast(json.dumps(sync_message))
        
        return {
            "status": "success",
            "message": "Code synchronization monitoring stopped",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to stop code sync: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to stop code sync: {str(e)}")

@router.get("/sync/status")
async def get_sync_status():
    """Get current code synchronization status"""
    try:
        status = code_sync_service.get_sync_status()
        return {
            "status": "success",
            "sync_status": status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get sync status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get sync status: {str(e)}")

@router.get("/sync/changes")
async def get_code_changes():
    """Get list of recent code changes"""
    try:
        # This would need to be implemented in the service
        # For now, return a placeholder
        return {
            "status": "success",
            "changes": [],
            "message": "Code changes endpoint - implementation pending",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get code changes: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get code changes: {str(e)}")

# Conflict Management Endpoints

@router.get("/conflicts")
async def get_conflicts(status: Optional[str] = None):
    """Get list of code conflicts, optionally filtered by status"""
    try:
        conflicts = code_sync_service.get_conflicts(status)
        return {
            "status": "success",
            "conflicts": conflicts,
            "total_conflicts": len(conflicts),
            "filtered_by": status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get conflicts: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get conflicts: {str(e)}")

@router.post("/conflicts/{conflict_id}/resolve")
async def resolve_conflict(
    conflict_id: str, 
    resolution_strategy: str, 
    resolved_by: str
):
    """Mark a conflict as resolved"""
    try:
        code_sync_service.resolve_conflict(conflict_id, resolution_strategy, resolved_by)
        
        # Broadcast conflict resolution
        resolve_message = {
            "type": "conflict_resolved",
            "conflict_id": conflict_id,
            "resolution_strategy": resolution_strategy,
            "resolved_by": resolved_by,
            "timestamp": datetime.now().isoformat(),
            "message": f"Conflict {conflict_id} resolved by {resolved_by}"
        }
        
        await orchestration_manager.broadcast(json.dumps(resolve_message))
        
        return {
            "status": "success",
            "conflict_id": conflict_id,
            "message": "Conflict marked as resolved",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to resolve conflict {conflict_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to resolve conflict: {str(e)}")

# Agent Communication Endpoints

@router.post("/agents/{agent_id}/message")
async def send_agent_message(agent_id: str, message: Dict):
    """Send a message to a specific agent"""
    try:
        # Add metadata to message
        full_message = {
            "type": "agent_message",
            "from": "orchestrator",
            "to": agent_id,
            "payload": message,
            "timestamp": datetime.now().isoformat()
        }
        
        # Send via WebSocket if connected
        await orchestration_manager.send_to_agent(json.dumps(full_message), agent_id)
        
        return {
            "status": "success",
            "agent_id": agent_id,
            "message": "Message sent successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to send message to agent {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")

@router.post("/broadcast")
async def broadcast_message(message: Dict):
    """Broadcast a message to all connected agents"""
    try:
        # Add metadata to message
        full_message = {
            "type": "broadcast_message",
            "from": "orchestrator",
            "payload": message,
            "timestamp": datetime.now().isoformat()
        }
        
        # Broadcast via WebSocket
        await orchestration_manager.broadcast(json.dumps(full_message))
        
        return {
            "status": "success",
            "message": "Message broadcasted successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to broadcast message: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to broadcast message: {str(e)}")

# WebSocket Endpoints for Real-time Communication

@router.websocket("/ws/orchestrator")
async def websocket_orchestrator(websocket: WebSocket):
    """Main orchestration WebSocket endpoint"""
    connection_id = None
    try:
        connection_id = await orchestration_manager.connect(websocket)
        
        # Send welcome message
        welcome_message = {
            "type": "connection_established",
            "connection_id": connection_id,
            "message": "Connected to orchestration service",
            "timestamp": datetime.now().isoformat()
        }
        await websocket.send_text(json.dumps(welcome_message))
        
        # Keep connection alive and handle messages
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            await handle_orchestration_message(message, connection_id)
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket connection {connection_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        if connection_id:
            orchestration_manager.disconnect(connection_id)

@router.websocket("/ws/agent/{agent_id}")
async def websocket_agent(websocket: WebSocket, agent_id: str):
    """Direct agent communication WebSocket endpoint"""
    connection_id = None
    try:
        connection_id = await orchestration_manager.connect(websocket, agent_id)
        
        # Send welcome message
        welcome_message = {
            "type": "agent_connection_established",
            "agent_id": agent_id,
            "connection_id": connection_id,
            "message": f"Agent {agent_id} connected to orchestration service",
            "timestamp": datetime.now().isoformat()
        }
        await websocket.send_text(json.dumps(welcome_message))
        
        # Keep connection alive and handle messages
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle agent-specific messages
            await handle_agent_message(message, agent_id, connection_id)
            
    except WebSocketDisconnect:
        logger.info(f"Agent {agent_id} WebSocket connection {connection_id} disconnected")
    except Exception as e:
        logger.error(f"Agent {agent_id} WebSocket error: {e}")
    finally:
        if connection_id:
            orchestration_manager.disconnect(connection_id)

async def handle_orchestration_message(message: Dict, connection_id: str):
    """Handle messages from the main orchestration WebSocket"""
    try:
        message_type = message.get("type")
        
        if message_type == "ping":
            # Respond to ping
            response = {
                "type": "pong",
                "timestamp": datetime.now().isoformat()
            }
            await orchestration_manager.send_personal_message(
                json.dumps(response), connection_id
            )
        
        elif message_type == "get_status":
            # Send current status
            status = code_sync_service.get_sync_status()
            response = {
                "type": "status_response",
                "status": status,
                "timestamp": datetime.now().isoformat()
            }
            await orchestration_manager.send_personal_message(
                json.dumps(response), connection_id
            )
        
        else:
            logger.info(f"Received orchestration message: {message_type}")
            
    except Exception as e:
        logger.error(f"Error handling orchestration message: {e}")

async def handle_agent_message(message: Dict, agent_id: str, connection_id: str):
    """Handle messages from agent WebSocket connections"""
    try:
        message_type = message.get("type")
        
        if message_type == "status_update":
            # Update agent status
            status = message.get("status", "active")
            task = message.get("task")
            workload = message.get("workload", 0.0)
            
            code_sync_service.update_agent_status(agent_id, status, task, workload)
            
            # Acknowledge status update
            response = {
                "type": "status_update_ack",
                "agent_id": agent_id,
                "timestamp": datetime.now().isoformat()
            }
            await orchestration_manager.send_personal_message(
                json.dumps(response), connection_id
            )
        
        elif message_type == "code_change":
            # Process code change from agent
            file_path = message.get("file_path")
            change_type = message.get("change_type", "modified")
            
            if file_path:
                change = code_sync_service.process_code_change(file_path, agent_id, change_type)
                
                # Acknowledge code change
                response = {
                    "type": "code_change_ack",
                    "file_path": file_path,
                    "change_type": change_type,
                    "timestamp": datetime.now().isoformat()
                }
                await orchestration_manager.send_personal_message(
                    json.dumps(response), connection_id
                )
        
        else:
            logger.info(f"Received agent message from {agent_id}: {message_type}")
            
    except Exception as e:
        logger.error(f"Error handling agent message from {agent_id}: {e}")

# Health Check Endpoint

@router.get("/health")
async def health_check():
    """Health check endpoint for the orchestration service"""
    try:
        # Check if code sync service is running
        sync_status = code_sync_service.get_sync_status()
        
        return {
            "status": "healthy",
            "service": "orchestration",
            "timestamp": datetime.now().isoformat(),
            "sync_service": {
                "monitoring_active": sync_status["monitoring_active"],
                "registered_agents": sync_status["registered_agents"]
            },
            "websocket_connections": len(orchestration_manager.active_connections)
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")
