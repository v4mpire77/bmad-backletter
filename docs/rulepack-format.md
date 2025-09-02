# Rulepack Format and Detection Flow

## Rulepack Structure

Rulepacks are YAML files that define detectors and lexicons. A minimal example:

```yaml
name: example-pack
version: v1
Detectors:
  - id: D001
    type: lexicon
    lexicon: weak-language
  - id: R001
    type: regex
    pattern: "review"
Lexicons:
  weak_language:
    - may
    - might
```

Each detector entry includes an `id` and a `type` (`lexicon` or `regex`).
Lexicon detectors reference a lexicon by name; regex detectors supply a
regular expression pattern. Lexicons map names to term lists.

## Detection Flow

1. **Extraction**: The pipeline produces an `extraction.json` artifact with
   sentence entries. Each sentence may include optional `lexicon` metadata
   describing matched terms and their categories and confidence scores.
2. **Detector Runner**: `run_detectors` loads the active rulepack and iterates
   over each sentence.
   - For lexicon detectors, the runner first looks for matching entries in the
     sentence's `lexicon` metadata. If present, findings are created with the
     provided `category` and `confidence` values. When metadata is missing, the
     detector falls back to a simple term search using the lexicon terms.
   - Regex detectors apply their compiled pattern directly to the sentence text.
3. **Post‑processing**: Findings pass through `postprocess_weak_language` to
   downgrade verdicts when weak language appears without counter‑anchors.
4. **Persistence**: All findings are written to `findings.json` under the
   analysis directory.

This flow allows both lexicon‑based and regex‑based rules to be evaluated in a
single pass while surfacing detector metadata in results.
