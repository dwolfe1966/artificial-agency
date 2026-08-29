# Run Config — 008C-GEMINI

- Run ID: `008C-GEMINI`
- Provider/model: `google/gemini-3.7-flash`
- Samples: 120
- Cells: procurement/data-access x eval-salient/naturalistic, 30 each
- Primary endpoint: `operational_constraint_violation`
- Awareness schema: `exp008-awareness-v1`
- Max connections: 1
- Max retries: 3
- Timeout: 60
- Attempt timeout: 45
- Log buffer: 1
- Checkpoint: `turn:1`
- OpenAI-specific reasoning/verbosity controls: unsupported, not applied
- Unsupported/mixed controls: seed not relied on
