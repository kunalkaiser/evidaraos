# EvidaraOS Workflow Lifecycle

Every EvidenceOS module should be explainable through the same governed lifecycle.

| Stage | Purpose | Example Artifacts |
|---|---|---|
| Question | Capture the clinical, economic, payer, regulatory, or translational question. | Intake, PICO/PECO, model scope, dossier scope, regulatory context |
| Protocol | Convert the question into explicit criteria and assumptions. | Search protocol, inclusion/exclusion criteria, model assumptions, benefit-risk scope |
| Retrieval | Collect evidence from approved sources. | PubMed query, source logs, claim evidence files, input source tables |
| Evidence Map | Organize records and claims into traceable evidence signals. | Evidence signals, evidence map, evidence path explanations |
| Human Review | Route uncertain or high-impact outputs for expert review. | Review queue, reviewer decision, adjudication summary |
| Extraction | Produce structured domain-specific outputs. | Study extraction, model input table, claim matrix, benefit-risk table |
| Validation | Check quality, completeness, reviewer agreement, and fixture limitations. | Validation report, audit completeness, performance metrics |
| Report | Generate a final traceable deliverable. | SLR report, HEOR input appendix, payer dossier, regulatory briefing, repurposing report |
| Audit | Preserve provenance and repeatability. | Project manifest, audit trail, source provenance, script metadata |

## Product Rule

The website and workspace should show this lifecycle consistently across modules. Do not imply live execution, validated performance, or data network coverage unless the underlying backend and human-labeled benchmark data exist.
