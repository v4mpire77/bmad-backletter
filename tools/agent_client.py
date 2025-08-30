#!/usr/bin/env python3
"""
AI Agent Client for Independent Orchestration Service

This script allows AI agents to connect to the orchestration service and participate
in code synchronization, conflict resolution, and multi-agent coordination.

Usage:
    python agent_client.py --agent-id <agent_id> --capabilities <cap1,cap2>
    
Example:
    python agent_client.py --agent-id "dev-agent" --capabilities "python,backend,api"
"""

import asyncio
import json
import logging
import argparse
import websockets
import requests
from typing import Dict, List, Optional, Callable
from datetime import datetime
import time
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgentClient:
    """
    Client for AI agents to connect to the orchestration service.
    
    Features:
    - WebSocket connection for real-time communication
    - HTTP API integration for status updates
    - Automatic reconnection handling
    - Message queuing and delivery
    """
    
    def __init__(self, agent_id: str, capabilities: List[str] = None, 
                 base_url: str = "http://localhost:8000"):
        self.agent_id = agent_id
        self.capabilities = capabilities or []
        self.base_url = base_url.rstrip('/')
        self.websocket_url = f"ws://localhost:8000/api/orchestration/ws/agent/{agent_id}"
        
        # Connection state
        self.websocket = None
        self.is_connected = False
        self.reconnect_delay = 1
        self.max_reconnect_delay = 60
        
        # Message handlers
        self.message_handlers: Dict[str, Callable] = {}
        self.default_message_handler = self._default_message_handler
        
        # Status tracking
        self.current_task = None
        self.workload = 0.0
        self.status = "idle"
        
        # Register default message handlers
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Register default message handlers"""
        self.register_handler("ping", self._handle_ping)
        self.register_handler("agent_message", self._handle_agent_message)
        self.register_handler("broadcast_message", self._handle_broadcast)
        self.register_handler("code_sync_started", self._handle_sync_started)
        self.register_handler("code_sync_stopped", self._handle_sync_stopped)
        self.register_handler("agent_registered", self._handle_agent_registered)
        self.register_handler("agent_unregistered", self._handle_agent_unregistered)
        self.register_handler("agent_status_update", self._handle_status_update)
        self.register_handler("conflict_resolved", self._handle_conflict_resolved)
    
    def register_handler(self, message_type: str, handler: Callable):
        """Register a message handler for a specific message type"""
        self.message_handlers[message_type] = handler
        logger.info(f"Registered handler for message type: {message_type}")
    
    async def connect(self):
        """Connect to the orchestration service"""
        try:
            # First register via HTTP API
            await self._register_via_http()
            
            # Then establish WebSocket connection
            await self._connect_websocket()
            
            logger.info(f"Agent {self.agent_id} successfully connected to orchestration service")
            
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise
    
    async def _register_via_http(self):
        """Register agent via HTTP API"""
        try:
            url = f"{self.base_url}/api/orchestration/agents/register"
            data = {
                "agent_id": self.agent_id,
                "capabilities": self.capabilities
            }
            
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"HTTP registration successful: {result['message']}")
            
        except Exception as e:
            logger.error(f"HTTP registration failed: {e}")
            raise
    
    async def _connect_websocket(self):
        """Establish WebSocket connection"""
        try:
            self.websocket = await websockets.connect(self.websocket_url)
            self.is_connected = True
            self.reconnect_delay = 1
            
            # Start listening for messages
            asyncio.create_task(self._listen_for_messages())
            
            logger.info(f"WebSocket connection established to {self.websocket_url}")
            
        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            self.is_connected = False
            raise
    
    async def disconnect(self):
        """Disconnect from the orchestration service"""
        try:
            if self.websocket:
                await self.websocket.close()
                self.websocket = None
            
            self.is_connected = False
            
            # Unregister via HTTP API
            await self._unregister_via_http()
            
            logger.info(f"Agent {self.agent_id} disconnected from orchestration service")
            
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")
    
    async def _unregister_via_http(self):
        """Unregister agent via HTTP API"""
        try:
            url = f"{self.base_url}/api/orchestration/agents/{self.agent_id}"
            response = requests.delete(url)
            response.raise_for_status()
            
            logger.info("HTTP unregistration successful")
            
        except Exception as e:
            logger.warning(f"HTTP unregistration failed: {e}")
    
    async def _listen_for_messages(self):
        """Listen for incoming WebSocket messages"""
        try:
            async for message in self.websocket:
                await self._handle_message(message)
                
        except websockets.exceptions.ConnectionClosed:
            logger.warning("WebSocket connection closed")
            self.is_connected = False
            await self._schedule_reconnect()
            
        except Exception as e:
            logger.error(f"Error in message listener: {e}")
            self.is_connected = False
            await self._schedule_reconnect()
    
    async def _handle_message(self, message: str):
        """Handle incoming WebSocket message"""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            logger.debug(f"Received message: {message_type}")
            
            # Find and execute appropriate handler
            handler = self.message_handlers.get(message_type, self.default_message_handler)
            await handler(data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse message: {e}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def _default_message_handler(self, message: Dict):
        """Default message handler for unhandled message types"""
        logger.info(f"Unhandled message type: {message.get('type')} - {message}")
    
    async def _handle_ping(self, message: Dict):
        """Handle ping messages"""
        response = {
            "type": "pong",
            "timestamp": datetime.now().isoformat()
        }
        await self._send_message(response)
    
    async def _handle_agent_message(self, message: Dict):
        """Handle direct agent messages"""
        logger.info(f"Received direct message: {message.get('payload')}")
        
        # Acknowledge receipt
        response = {
            "type": "message_ack",
            "original_message": message,
            "timestamp": datetime.now().isoformat()
        }
        await self._send_message(response)
    
    async def _handle_broadcast(self, message: Dict):
        """Handle broadcast messages"""
        logger.info(f"Received broadcast: {message.get('payload')}")
    
    async def _handle_sync_started(self, message: Dict):
        """Handle code sync started notification"""
        logger.info("Code synchronization monitoring has started")
    
    async def _handle_sync_stopped(self, message: Dict):
        """Handle code sync stopped notification"""
        logger.info("Code synchronization monitoring has stopped")
    
    async def _handle_agent_registered(self, message: Dict):
        """Handle agent registration notification"""
        agent_id = message.get("agent_id")
        if agent_id != self.agent_id:
            logger.info(f"New agent registered: {agent_id}")
    
    async def _handle_agent_unregistered(self, message: Dict):
        """Handle agent unregistration notification"""
        agent_id = message.get("agent_id")
        if agent_id != self.agent_id:
            logger.info(f"Agent unregistered: {agent_id}")
    
    async def _handle_status_update(self, message: Dict):
        """Handle agent status update notification"""
        agent_id = message.get("agent_id")
        status = message.get("status")
        task = message.get("task")
        
        if agent_id != self.agent_id:
            logger.info(f"Agent {agent_id} status: {status} - {task}")
    
    async def _handle_conflict_resolved(self, message: Dict):
        """Handle conflict resolution notification"""
        conflict_id = message.get("conflict_id")
        resolved_by = message.get("resolved_by")
        logger.info(f"Conflict {conflict_id} resolved by {resolved_by}")
    
    async def _send_message(self, message: Dict):
        """Send message via WebSocket"""
        if self.is_connected and self.websocket:
            try:
                await self.websocket.send(json.dumps(message))
            except Exception as e:
                logger.error(f"Failed to send message: {e}")
                self.is_connected = False
                await self._schedule_reconnect()
        else:
            logger.warning("Cannot send message - not connected")
    
    async def _schedule_reconnect(self):
        """Schedule reconnection attempt"""
        if not self.is_connected:
            logger.info(f"Scheduling reconnection in {self.reconnect_delay} seconds")
            await asyncio.sleep(self.reconnect_delay)
            
            # Exponential backoff
            self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
            
            try:
                await self.connect()
            except Exception as e:
                logger.error(f"Reconnection failed: {e}")
                # Schedule another attempt
                asyncio.create_task(self._schedule_reconnect())
    
    async def update_status(self, status: str, task: str = None, workload: float = 0.0):
        """Update agent status"""
        try:
            self.status = status
            self.current_task = task
            self.workload = workload
            
            # Send status update via WebSocket
            status_message = {
                "type": "status_update",
                "status": status,
                "task": task,
                "workload": workload,
                "timestamp": datetime.now().isoformat()
            }
            await self._send_message(status_message)
            
            # Also update via HTTP API
            await self._update_status_via_http(status, task, workload)
            
            logger.info(f"Status updated: {status} - {task} (workload: {workload})")
            
        except Exception as e:
            logger.error(f"Failed to update status: {e}")
    
    async def _update_status_via_http(self, status: str, task: str = None, workload: float = 0.0):
        """Update status via HTTP API"""
        try:
            url = f"{self.base_url}/api/orchestration/agents/{self.agent_id}/status"
            data = {
                "status": status,
                "task": task,
                "workload": workload
            }
            
            response = requests.post(url, json=data)
            response.raise_for_status()
            
        except Exception as e:
            logger.warning(f"HTTP status update failed: {e}")
    
    async def report_code_change(self, file_path: str, change_type: str = "modified"):
        """Report a code change to the orchestration service"""
        try:
            change_message = {
                "type": "code_change",
                "file_path": file_path,
                "change_type": change_type,
                "timestamp": datetime.now().isoformat()
            }
            
            await self._send_message(change_message)
            logger.info(f"Reported code change: {change_type} on {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to report code change: {e}")
    
    async def send_message_to_agent(self, target_agent_id: str, message: Dict):
        """Send a message to a specific agent via HTTP API"""
        try:
            url = f"{self.base_url}/api/orchestration/agents/{target_agent_id}/message"
            data = {
                "message": message
            }
            
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Message sent to {target_agent_id}: {result['message']}")
            
        except Exception as e:
            logger.error(f"Failed to send message to {target_agent_id}: {e}")
    
    async def broadcast_message(self, message: Dict):
        """Broadcast a message to all agents via HTTP API"""
        try:
            url = f"{self.base_url}/api/orchestration/broadcast"
            data = {
                "message": message
            }
            
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Message broadcasted: {result['message']}")
            
        except Exception as e:
            logger.error(f"Failed to broadcast message: {e}")
    
    async def get_system_status(self) -> Dict:
        """Get current system status via HTTP API"""
        try:
            url = f"{self.base_url}/api/orchestration/sync/status"
            response = requests.get(url)
            response.raise_for_status()
            
            result = response.json()
            return result.get("sync_status", {})
            
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return {}
    
    async def get_agent_list(self) -> List[Dict]:
        """Get list of all registered agents via HTTP API"""
        try:
            url = f"{self.base_url}/api/orchestration/agents"
            response = requests.get(url)
            response.raise_for_status()
            
            result = response.json()
            return result.get("agents", [])
            
        except Exception as e:
            logger.error(f"Failed to get agent list: {e}")
            return []


async def main():
    """Main function for standalone agent client"""
    parser = argparse.ArgumentParser(description="AI Agent Client for Orchestration Service")
    parser.add_argument("--agent-id", required=True, help="Unique identifier for this agent")
    parser.add_argument("--capabilities", help="Comma-separated list of capabilities")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Base URL of orchestration service")
    parser.add_argument("--status", default="idle", help="Initial agent status")
    parser.add_argument("--task", help="Initial agent task")
    parser.add_argument("--workload", type=float, default=0.0, help="Initial workload (0.0 to 1.0)")
    
    args = parser.parse_args()
    
    # Parse capabilities
    capabilities = []
    if args.capabilities:
        capabilities = [cap.strip() for cap in args.capabilities.split(",")]
    
    # Create agent client
    client = AgentClient(
        agent_id=args.agent_id,
        capabilities=capabilities,
        base_url=args.base_url
    )
    
    try:
        # Connect to orchestration service
        await client.connect()
        
        # Set initial status
        await client.update_status(args.status, args.task, args.workload)
        
        # Keep the client running
        logger.info(f"Agent {args.agent_id} is now running. Press Ctrl+C to stop.")
        
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Shutting down agent client...")
    except Exception as e:
        logger.error(f"Agent client error: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
