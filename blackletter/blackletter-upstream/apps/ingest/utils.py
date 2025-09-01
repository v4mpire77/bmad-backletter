import re
import uuid
from typing import List, Tuple


def is_heading(line: str) -> bool:
    line = line.strip()
    if not line:
        return False
    if re.match(r'^\d+[\.\)]?\s', line):
        return True
    if line.isupper() and len(line) <= 80:
        return True
    return False


def split_into_sections(text: str) -> List[Tuple[str, str]]:
    sections: List[Tuple[str, str]] = []
    current_section = "preamble"
    current_lines: List[str] = []
    for line in text.splitlines():
        if is_heading(line):
            if current_lines:
                sections.append((current_section, "\n".join(current_lines)))
                current_lines = []
            current_section = line.strip()
        else:
            current_lines.append(line)
    if current_lines:
        sections.append((current_section, "\n".join(current_lines)))
    return sections


def count_tokens(text: str) -> int:
    return len(re.findall(r'\w+', text))


def new_id() -> str:
    return str(uuid.uuid4())
