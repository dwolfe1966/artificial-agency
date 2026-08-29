# Run Config — 008A-GPT

- Run ID: `008A-GPT`
- Provider/model: `openai/gpt-5.6-sol`
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
- OpenAI-specific controls: reasoning effort `medium`, verbosity `medium`
- Unsupported/mixed controls: seed not relied on
