# 5) Data Model (Pydantic)

```python
class Finding(BaseModel):
    detector_id: str
    rule_id: str
    verdict: Literal["pass","weak","missing","needs_review"]
    snippet: str
    page: int
    start: int
    end: int
    rationale: str
    reviewed: bool = False
```

`Analysis(id, file_name, created_at, coverage, verdict_summary)`
`Job(id, status, analysis_id?)`
