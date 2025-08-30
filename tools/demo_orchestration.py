#!/usr/bin/env python3
"""
Demo Script for Independent Orchestration Agent

This script demonstrates how multiple AI agents can work together
through the orchestration service for code synchronization and coordination.

Usage:
    python demo_orchestration.py
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import the agent client
import sys
sys.path.append(str(Path(__file__).parent))
from agent_client import AgentClient

class DemoAgent:
    """Demo agent that simulates real AI agent behavior"""
    
    def __init__(self, agent_id: str, capabilities: List[str], base_url: str = "http://localhost:8000"):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.client = AgentClient(agent_id, capabilities, base_url)
        self.is_running = False
        
        # Register custom message handlers
        self.client.register_handler("agent_message", self._handle_agent_message)
        self.client.register_handler("broadcast_message", self._handle_broadcast)
    
    async def start(self):
        """Start the demo agent"""
        try:
            await self.client.connect()
            await self.client.update_status("active", "Ready for tasks", 0.0)
            self.is_running = True
            
            logger.info(f"Demo agent {self.agent_id} started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start demo agent {self.agent_id}: {e}")
            raise
    
    async def stop(self):
        """Stop the demo agent"""
        try:
            self.is_running = False
            await self.client.disconnect()
            logger.info(f"Demo agent {self.agent_id} stopped")
            
        except Exception as e:
            logger.error(f"Error stopping demo agent {self.agent_id}: {e}")
    
    async def simulate_work(self, task: str, duration: int = 5):
        """Simulate agent working on a task"""
        try:
            logger.info(f"Agent {self.agent_id} starting task: {task}")
            
            # Update status to busy
            await self.client.update_status("busy", task, 0.8)
            
            # Simulate work duration
            await asyncio.sleep(duration)
            
            # Simulate code changes
            await self._simulate_code_changes(task)
            
            # Update status to idle
            await self.client.update_status("idle", "Task completed", 0.2)
            
            logger.info(f"Agent {self.agent_id} completed task: {task}")
            
        except Exception as e:
            logger.error(f"Error in simulate_work for {self.agent_id}: {e}")
    
    async def _simulate_code_changes(self, task: str):
        """Simulate code changes during task execution"""
        try:
            # Generate fake file paths based on task
            if "authentication" in task.lower():
                files = [
                    "apps/api/blackletter_api/models/user.py",
                    "apps/api/blackletter_api/routers/auth.py",
                    "apps/api/blackletter_api/services/auth_service.py"
                ]
            elif "database" in task.lower():
                files = [
                    "apps/api/blackletter_api/database.py",
                    "apps/api/blackletter_api/models/base.py",
                    "apps/api/blackletter_api/migrations/"
                ]
            elif "testing" in task.lower():
                files = [
                    "tests/test_auth.py",
                    "tests/test_models.py",
                    "tests/conftest.py"
                ]
            else:
                files = [
                    f"src/{self.agent_id}/main.py",
                    f"src/{self.agent_id}/config.py"
                ]
            
            # Report code changes
            for file_path in files:
                await self.client.report_code_change(file_path, "modified")
                await asyncio.sleep(0.5)  # Small delay between changes
            
        except Exception as e:
            logger.error(f"Error simulating code changes: {e}")
    
    async def _handle_agent_message(self, message: Dict):
        """Handle direct messages from other agents"""
        try:
            payload = message.get("payload", {})
            action = payload.get("action")
            sender = message.get("from")
            
            logger.info(f"Agent {self.agent_id} received message from {sender}: {action}")
            
            # Respond based on action type
            if action == "request_review":
                await self._handle_review_request(sender, payload)
            elif action == "request_help":
                await self._handle_help_request(sender, payload)
            elif action == "coordinate_merge":
                await self._handle_merge_coordination(sender, payload)
            
        except Exception as e:
            logger.error(f"Error handling agent message: {e}")
    
    async def _handle_broadcast(self, message: Dict):
        """Handle broadcast messages"""
        try:
            payload = message.get("payload", {})
            logger.info(f"Agent {self.agent_id} received broadcast: {payload}")
            
        except Exception as e:
            logger.error(f"Error handling broadcast: {e}")
    
    async def _handle_review_request(self, sender: str, payload: Dict):
        """Handle code review requests"""
        try:
            file_path = payload.get("file_path")
            message = payload.get("message", "")
            
            logger.info(f"Agent {self.agent_id} reviewing {file_path} for {sender}")
            
            # Simulate review process
            await asyncio.sleep(2)
            
            # Send review feedback
            review_message = {
                "action": "review_feedback",
                "file_path": file_path,
                "feedback": f"Code review completed by {self.agent_id}. All looks good!",
                "status": "approved"
            }
            
            await self.client.send_message_to_agent(sender, review_message)
            
        except Exception as e:
            logger.error(f"Error handling review request: {e}")
    
    async def _handle_help_request(self, sender: str, payload: Dict):
        """Handle help requests"""
        try:
            message = payload.get("message", "")
            
            logger.info(f"Agent {self.agent_id} providing help to {sender}: {message}")
            
            # Simulate help process
            await asyncio.sleep(1)
            
            # Send help response
            help_message = {
                "action": "help_response",
                "message": f"Here's some help from {self.agent_id} for: {message}",
                "suggestions": [
                    "Check the documentation",
                    "Review similar implementations",
                    "Consider using the established patterns"
                ]
            }
            
            await self.client.send_message_to_agent(sender, help_message)
            
        except Exception as e:
            logger.error(f"Error handling help request: {e}")
    
    async def _handle_merge_coordination(self, sender: str, payload: Dict):
        """Handle merge coordination requests"""
        try:
            file_path = payload.get("file_path")
            
            logger.info(f"Agent {self.agent_id} coordinating merge for {file_path} with {sender}")
            
            # Simulate merge coordination
            await asyncio.sleep(1)
            
            # Send merge approval
            merge_message = {
                "action": "merge_approved",
                "file_path": file_path,
                "message": f"Merge approved by {self.agent_id}",
                "status": "ready_to_merge"
            }
            
            await self.client.send_message_to_agent(sender, merge_message)
            
        except Exception as e:
            logger.error(f"Error handling merge coordination: {e}")


class OrchestrationDemo:
    """Main demo orchestrator"""
    
    def __init__(self):
        self.agents = {}
        self.demo_scenarios = [
            {
                "name": "Multi-Agent Development",
                "description": "Multiple agents working on different features",
                "duration": 30
            },
            {
                "name": "Code Review Workflow",
                "description": "Agents requesting and providing code reviews",
                "duration": 20
            },
            {
                "name": "Conflict Resolution",
                "description": "Simulating and resolving code conflicts",
                "duration": 25
            }
        ]
    
    async def setup_agents(self):
        """Set up demo agents"""
        try:
            logger.info("Setting up demo agents...")
            
            # Create different types of agents
            agent_configs = [
                {
                    "id": "dev-agent",
                    "capabilities": ["python", "backend", "api"],
                    "base_url": "http://localhost:8000"
                },
                {
                    "id": "architect-agent",
                    "capabilities": ["system-design", "scalability", "architecture"],
                    "base_url": "http://localhost:8000"
                },
                {
                    "id": "qa-agent",
                    "capabilities": ["testing", "quality-assurance", "automation"],
                    "base_url": "http://localhost:8000"
                },
                {
                    "id": "ux-agent",
                    "capabilities": ["ui-design", "user-experience", "frontend"],
                    "base_url": "http://localhost:8000"
                }
            ]
            
            # Create and start agents
            for config in agent_configs:
                agent = DemoAgent(
                    agent_id=config["id"],
                    capabilities=config["capabilities"],
                    base_url=config["base_url"]
                )
                
                await agent.start()
                self.agents[config["id"]] = agent
                
                logger.info(f"Agent {config['id']} created and started")
            
            logger.info(f"All {len(self.agents)} demo agents are ready")
            
        except Exception as e:
            logger.error(f"Failed to setup agents: {e}")
            raise
    
    async def run_demo_scenarios(self):
        """Run the demo scenarios"""
        try:
            logger.info("Starting demo scenarios...")
            
            for i, scenario in enumerate(self.demo_scenarios, 1):
                logger.info(f"\n{'='*60}")
                logger.info(f"SCENARIO {i}: {scenario['name']}")
                logger.info(f"Description: {scenario['description']}")
                logger.info(f"Duration: {scenario['duration']} seconds")
                logger.info(f"{'='*60}\n")
                
                await self._run_scenario(scenario)
                
                # Brief pause between scenarios
                if i < len(self.demo_scenarios):
                    logger.info("Pausing between scenarios...")
                    await asyncio.sleep(3)
            
            logger.info("\nAll demo scenarios completed!")
            
        except Exception as e:
            logger.error(f"Error running demo scenarios: {e}")
    
    async def _run_scenario(self, scenario: Dict):
        """Run a specific demo scenario"""
        try:
            if scenario["name"] == "Multi-Agent Development":
                await self._run_multi_agent_development(scenario["duration"])
            elif scenario["name"] == "Code Review Workflow":
                await self._run_code_review_workflow(scenario["duration"])
            elif scenario["name"] == "Conflict Resolution":
                await self._run_conflict_resolution(scenario["duration"])
            else:
                logger.warning(f"Unknown scenario: {scenario['name']}")
                
        except Exception as e:
            logger.error(f"Error running scenario {scenario['name']}: {e}")
    
    async def _run_multi_agent_development(self, duration: int):
        """Run multi-agent development scenario"""
        try:
            logger.info("Starting multi-agent development scenario...")
            
            # Define tasks for each agent
            tasks = {
                "dev-agent": "Implementing user authentication system",
                "architect-agent": "Designing microservices architecture",
                "qa-agent": "Creating automated test suite",
                "ux-agent": "Designing user interface components"
            }
            
            # Start all agents working simultaneously
            work_tasks = []
            for agent_id, task in tasks.items():
                if agent_id in self.agents:
                    work_tasks.append(
                        self.agents[agent_id].simulate_work(task, duration // 2)
                    )
            
            # Wait for all work to complete
            await asyncio.gather(*work_tasks)
            
            # Simulate coordination between agents
            await self._simulate_agent_coordination()
            
            logger.info("Multi-agent development scenario completed")
            
        except Exception as e:
            logger.error(f"Error in multi-agent development scenario: {e}")
    
    async def _run_code_review_workflow(self, duration: int):
        """Run code review workflow scenario"""
        try:
            logger.info("Starting code review workflow scenario...")
            
            # Simulate code review requests
            review_requests = [
                ("dev-agent", "architect-agent", "user authentication model"),
                ("dev-agent", "qa-agent", "test coverage for auth system"),
                ("ux-agent", "dev-agent", "frontend authentication flow"),
                ("architect-agent", "dev-agent", "database schema design")
            ]
            
            for requester, reviewer, description in review_requests:
                if requester in self.agents and reviewer in self.agents:
                    # Request review
                    review_message = {
                        "action": "request_review",
                        "file_path": f"src/{requester}/main.py",
                        "message": f"Please review {description}"
                    }
                    
                    await self.agents[requester].client.send_message_to_agent(
                        reviewer, review_message
                    )
                    
                    await asyncio.sleep(2)
            
            # Wait for reviews to complete
            await asyncio.sleep(duration // 2)
            
            logger.info("Code review workflow scenario completed")
            
        except Exception as e:
            logger.error(f"Error in code review workflow scenario: {e}")
    
    async def _run_conflict_resolution(self, duration: int):
        """Run conflict resolution scenario"""
        try:
            logger.info("Starting conflict resolution scenario...")
            
            # Simulate conflicting code changes
            conflict_files = [
                "apps/api/blackletter_api/models/user.py",
                "apps/api/blackletter_api/database.py",
                "tests/test_auth.py"
            ]
            
            # Have multiple agents report changes to the same files
            for file_path in conflict_files:
                # Agent 1 reports change
                await self.agents["dev-agent"].client.report_code_change(file_path, "modified")
                await asyncio.sleep(0.5)
                
                # Agent 2 reports change to same file
                await self.agents["architect-agent"].client.report_code_change(file_path, "modified")
                await asyncio.sleep(0.5)
                
                # Agent 3 reports change to same file
                await self.agents["qa-agent"].client.report_code_change(file_path, "modified")
                await asyncio.sleep(0.5)
            
            # Simulate conflict resolution coordination
            await self._simulate_conflict_resolution()
            
            logger.info("Conflict resolution scenario completed")
            
        except Exception as e:
            logger.error(f"Error in conflict resolution scenario: {e}")
    
    async def _simulate_agent_coordination(self):
        """Simulate coordination between agents"""
        try:
            logger.info("Simulating agent coordination...")
            
            # Have agents communicate with each other
            coordination_tasks = [
                self.agents["dev-agent"].client.send_message_to_agent("architect-agent", {
                    "action": "request_help",
                    "message": "Need guidance on database schema design"
                }),
                self.agents["qa-agent"].client.send_message_to_agent("dev-agent", {
                    "action": "request_review",
                    "file_path": "tests/test_auth.py",
                    "message": "Please review the test coverage"
                }),
                self.agents["ux-agent"].client.send_message_to_agent("dev-agent", {
                    "action": "coordinate_merge",
                    "file_path": "src/frontend/auth.js",
                    "message": "Ready to merge frontend authentication changes"
                })
            ]
            
            await asyncio.gather(*coordination_tasks)
            
        except Exception as e:
            logger.error(f"Error simulating agent coordination: {e}")
    
    async def _simulate_conflict_resolution(self):
        """Simulate conflict resolution process"""
        try:
            logger.info("Simulating conflict resolution...")
            
            # Have agents coordinate on conflict resolution
            resolution_tasks = [
                self.agents["dev-agent"].client.send_message_to_agent("architect-agent", {
                    "action": "coordinate_merge",
                    "file_path": "apps/api/blackletter_api/models/user.py",
                    "message": "Need to coordinate merge for user model changes"
                }),
                self.agents["qa-agent"].client.send_message_to_agent("dev-agent", {
                    "action": "request_help",
                    "message": "Need help resolving test conflicts"
                })
            ]
            
            await asyncio.gather(*resolution_tasks)
            
        except Exception as e:
            logger.error(f"Error simulating conflict resolution: {e}")
    
    async def cleanup(self):
        """Clean up demo resources"""
        try:
            logger.info("Cleaning up demo resources...")
            
            # Stop all agents
            stop_tasks = []
            for agent in self.agents.values():
                stop_tasks.append(agent.stop())
            
            await asyncio.gather(*stop_tasks)
            
            logger.info("Demo cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


async def main():
    """Main demo function"""
    try:
        logger.info("🚀 Starting Independent Orchestration Agent Demo")
        logger.info("=" * 60)
        
        # Create demo orchestrator
        demo = OrchestrationDemo()
        
        # Setup agents
        await demo.setup_agents()
        
        # Wait a moment for everything to settle
        logger.info("Waiting for agents to stabilize...")
        await asyncio.sleep(3)
        
        # Run demo scenarios
        await demo.run_demo_scenarios()
        
        # Cleanup
        await demo.cleanup()
        
        logger.info("\n🎉 Demo completed successfully!")
        logger.info("Check the logs above to see the orchestration in action.")
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Demo interrupted by user")
    except Exception as e:
        logger.error(f"\n❌ Demo failed: {e}")
    finally:
        logger.info("Demo finished")


if __name__ == "__main__":
    asyncio.run(main())
