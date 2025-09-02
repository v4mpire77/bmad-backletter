from dataclasses import dataclass

@dataclass
class ContractChunk:
    id: str
    contract_id: str
    section: str
    text: str
    page: int
    tokens: int
