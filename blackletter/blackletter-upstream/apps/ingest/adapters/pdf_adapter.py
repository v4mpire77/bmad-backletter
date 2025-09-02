from typing import List
from pypdf import PdfReader

from ..models import ContractChunk
from ..utils import split_into_sections, count_tokens, new_id


def ingest(path: str, contract_id: str) -> List[ContractChunk]:
    reader = PdfReader(path)
    chunks: List[ContractChunk] = []
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        for section, section_text in split_into_sections(text):
            chunk = ContractChunk(
                id=new_id(),
                contract_id=contract_id,
                section=section,
                text=section_text,
                page=page_num,
                tokens=count_tokens(section_text),
            )
            chunks.append(chunk)
    return chunks
