from fastapi.testclient import TestClient

from blackletter_api.main import app
from blackletter_api.orchestrator.state import orchestrator, AnalysisState

client = TestClient(app)


def test_websocket_progress_broadcast_ordered_messages():
    analysis_id = orchestrator.intake("contract.pdf")

    with client.websocket_connect(f"/ws/analysis/{analysis_id}") as ws1, \
         client.websocket_connect(f"/ws/analysis/{analysis_id}") as ws2:
        assert ws1.receive_json()["type"] == "connection"
        assert ws2.receive_json()["type"] == "connection"

        states = [
            AnalysisState.QUEUED,
            AnalysisState.EXTRACTING,
            AnalysisState.DETECTING,
            AnalysisState.REPORTING,
            AnalysisState.DONE,
        ]

        for state in states:
            orchestrator.advance(analysis_id, state)

        received1 = [ws1.receive_json()["state"] for _ in states]
        received2 = [ws2.receive_json()["state"] for _ in states]

        def dedupe(seq: list[str]) -> list[str]:
            out: list[str] = []
            for item in seq:
                if not out or out[-1] != item:
                    out.append(item)
            return out

        assert dedupe(received1) == [s.value for s in states]
        assert dedupe(received2) == [s.value for s in states]
