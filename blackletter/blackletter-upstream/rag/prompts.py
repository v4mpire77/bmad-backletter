"""Prompt templates for retrieval-augmented generation."""

ANSWER_WITH_CITATIONS = """
You are a helpful assistant that answers questions using the supplied sources.
Each source is tagged as [source_id:page].

Answer the user's question. After every sentence, cite the supporting sources
in the form [source_id:page]. Use at least two distinct citations when the
material allows. If the sources do not provide enough information, respond with
"I don't have enough information to answer that.".

Return your response as JSON with the following structure:
{{
  "answer": string,
  "citations": [
    {{"source_id": string, "page": int, "quote": string}}
  ],
  "confidence": float  # 0 to 1 confidence in the answer
}}

Question: {question}

Sources:
{context}
"""

EXPLAIN_FINDING = """
Given the answer and its citations, explain briefly how each citation supports
the answer. Reference the citations by their [source_id:page] tags.

Answer: {answer}
Citations:
{citations}
"""
