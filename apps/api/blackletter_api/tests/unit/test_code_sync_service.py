from datetime import datetime

from blackletter_api.services.code_sync_service import AgentStatus, CodeChange


def test_code_change_defaults():
    change = CodeChange(
        file_path="file.py",
        agent_id="agent1",
        timestamp=datetime.utcnow(),
        change_type="modified",
        file_hash="abc123",
    )
    assert change.previous_hash is None
    assert change.conflict_level == "low"
    assert change.affected_agents == []


def test_agent_status_defaults_are_isolated():
    agent1 = AgentStatus(agent_id="a", status="active")
    agent2 = AgentStatus(agent_id="b", status="idle")

    assert agent1.capabilities == []
    assert agent2.capabilities == []

    agent1.capabilities.append("x")
    assert agent2.capabilities == []

    now = datetime.utcnow()
    assert (now - agent1.last_activity).total_seconds() < 5
