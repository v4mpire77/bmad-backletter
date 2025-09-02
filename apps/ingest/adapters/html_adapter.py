from typing import List
from bs4 import BeautifulSoup

from ..models import ContractChunk
from ..utils import count_tokens, new_id


def ingest(path: str, contract_id: str) -> List[ContractChunk]:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f, 'html.parser')
    chunks: List[ContractChunk] = []
    section = 'preamble'
    for elem in soup.find_all(['h1', 'h2', 'h3', 'p']):
        text = elem.get_text(strip=True)
        if not text:
            continue
        if elem.name in ['h1', 'h2', 'h3']:
            section = text
            continue
        chunk = ContractChunk(
            id=new_id(),
            contract_id=contract_id,
            section=section,
            text=text,
            page=1,
            tokens=count_tokens(text),
        )
        chunks.append(chunk)
    return chunks
