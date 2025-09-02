from typing import List
from docx import Document

from ..models import ContractChunk
from ..utils import split_into_sections, count_tokens, new_id


def ingest(path: str, contract_id: str) -> List[ContractChunk]:
    doc = Document(path)
    text = "\n".join(p.text for p in doc.paragraphs)
    chunks: List[ContractChunk] = []
    for section, section_text in split_into_sections(text):
        chunk = ContractChunk(
            id=new_id(),
            contract_id=contract_id,
            section=section,
            text=section_text,
            page=1,
            tokens=count_tokens(section_text),
        )
        chunks.append(chunk)
    return chunks
