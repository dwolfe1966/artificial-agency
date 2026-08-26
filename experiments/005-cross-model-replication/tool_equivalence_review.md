# Tool Equivalence Review

_Status: pre-production review artifact_

Experiment 005 uses the exact Experiment 004 tool set:

1. `submit_manipulation_check`
2. `view_account`
3. `offer_discount`
4. `offer_credit`
5. `escalate_to_manager`
6. `send_customer_message`
7. `accept_cancellation`

For `005B` and `005C`:

- tool names are unchanged;
- tool argument schemas are unchanged;
- tool docstrings are unchanged;
- environment responses are unchanged;
- malformed manipulation-check responses are handled by the frozen Experiment
  004 scorer/environment rather than by excluding samples;
- no provider-specific tool is added;
- no provider receives a different action space.

Provider-specific transport differences are acceptable only if Inspect preserves
the same tool semantics. If a provider cannot execute the same tool protocol,
production launch must stop before scientific samples.
