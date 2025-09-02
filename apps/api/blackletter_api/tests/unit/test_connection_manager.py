from __future__ import annotations

import logging
from unittest.mock import AsyncMock

import pytest

import sys
from types import ModuleType
from fastapi import APIRouter

# Stub router modules to avoid heavy dependencies during import
for _module in [
    "blackletter_api.routers.rules",
    "blackletter_api.routers.analyses",
    "blackletter_api.routers.contracts",
    "blackletter_api.routers.jobs",
    "blackletter_api.routers.reports",
    "blackletter_api.routers.risk_analysis",
    "blackletter_api.routers.admin",
    "blackletter_api.routers.orchestration",
    "blackletter_api.routers.gemini",
    "blackletter_api.routers.document_qa",
    "blackletter_api.routers.auth",
]:
    module = ModuleType(_module)
    module.router = APIRouter()
    sys.modules[_module] = module

from blackletter_api.main import ConnectionManager


@pytest.mark.asyncio
async def test_broadcast_removes_dead_connections(caplog: pytest.LogCaptureFixture) -> None:
    manager = ConnectionManager()

    good_ws = AsyncMock()
    bad_ws = AsyncMock()
    good_ws.send_text = AsyncMock()
    bad_ws.send_text = AsyncMock(side_effect=Exception("boom"))

    manager.active_connections.extend([good_ws, bad_ws])

    with caplog.at_level(logging.WARNING):
        await manager.broadcast("hi")

    assert good_ws in manager.active_connections
    assert bad_ws not in manager.active_connections
    assert "Failed to send message" in caplog.text
