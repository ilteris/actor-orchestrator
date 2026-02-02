# Soul Protocol (Systems 2, 4, 5)

## S2: Interleaved Reflection (Audit)
- **Mandatory**: Every turn MUST begin with an 'Interleaved Reflection' block.
- **Function**: Primary mechanism for architectural audit and anomaly detection. 
- **Rule**: Never act without confirmation.

## S4: Glass Box (Injection)
- **Mandatory**: Always 'inject' relevant file contents or technical evidence into the final response using '### [ Glass Box Review ]'.
- **Reason**: Ensures rendering fidelity and architectural transparency.

## S5: Atomic Contribution (Git)
- **Branching**: `task-<ID>-<short-description>`.
- **Mapping**: 1:1 relationship between PR and Task ID.
- **Closure**: Delete remote branches post-merge.