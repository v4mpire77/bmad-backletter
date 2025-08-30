import asyncio

from blackletter_api.services.document_qa import DocumentQAService


async def _run_answer():
    svc = DocumentQAService(embed_fn=lambda _: [0.0], llm_fn=lambda _: "stub")
    return await svc.answer_simple("doc", "question")


def test_injected_functions_used() -> None:
    """DocumentQAService should use injected LLM function."""
    result = asyncio.run(_run_answer())
    assert result.answer == "stub"
