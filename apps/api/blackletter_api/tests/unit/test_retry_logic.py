from __future__ import annotations

import asyncio

import pytest

from blackletter_api.services.upload_orchestrator import with_retries


@pytest.mark.asyncio
async def test_with_retries_succeeds_after_two_failures():
    attempts = {"n": 0}

    async def flaky():
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise RuntimeError("boom")
        await asyncio.sleep(0)
        return "ok"

    result = await with_retries(lambda: flaky(), timeout_seconds=1.0, retries=2)
    assert result == "ok"
    assert attempts["n"] == 3


@pytest.mark.asyncio
async def test_with_retries_times_out_and_raises():
    async def slow():
        await asyncio.sleep(0.2)
        return "done"

    with pytest.raises(asyncio.TimeoutError):
        await with_retries(lambda: slow(), timeout_seconds=0.01, retries=0)

