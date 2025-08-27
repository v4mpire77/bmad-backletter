# 10) Quality Gates & Testing

* **Unit**: detectors (≥3 pos + ≥3 hard neg per rule), extraction, windower.
* **Integration**: upload→findings→export happy path.
* **E2E**: web covers drag-drop, table view, export.
* **Gold set**: scorer CLI returns Precision/Recall per detector; gates: P≥0.85 / R≥0.90.
* **Performance**: p95 ≤ 60s/doc; cost ≤ £0.10/doc.
