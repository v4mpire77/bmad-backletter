from pathlib import Path
from typing import List

from ..models import ContractChunk
from . import pdf_adapter, docx_adapter, txt_adapter, html_adapter

ADAPTERS = {
    '.pdf': pdf_adapter,
    '.docx': docx_adapter,
    '.txt': txt_adapter,
    '.html': html_adapter,
    '.htm': html_adapter,
}


def ingest_file(path: str, contract_id: str) -> List[ContractChunk]:
    ext = Path(path).suffix.lower()
    adapter = ADAPTERS.get(ext)
    if not adapter:
        raise ValueError(f"No adapter for {ext}")
    return adapter.ingest(path, contract_id)
