import pytest

docx2python = pytest.importorskip("docx2python", reason="requires docx2python")


def test_extract_docx_minimal():
    assert docx2python is not None
