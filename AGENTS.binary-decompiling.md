# Binary decompilation for a faithful browser port

Read [AGENTS.git.md](AGENTS.git.md) and [AGENTS.reversing-shared.md](AGENTS.reversing-shared.md).

## Goal

Recover the original game's rules and rendering well enough to implement and validate a browser port. Readable pseudocode and analysis notes are intermediate artifacts; reproducing the original language, function structure or binary is not required.

## Procedure

- Map the executable format, entry point, segments and data files before import. Identify the language/runtime only when evidence supports it and it helps the current question.
- Use Ghidra through MCP to recover behavior and improve names, types and comments. Record addresses for recovered rules so another investigator can check them.
- Analyze game logic and rendering dependencies; summarize standard library and runtime routines. Do not pursue a whole-binary annotated listing unless a concrete correctness question requires it.
- Check uncertain decompiler output against instructions. Compare material behavior with the original in DOSBox-X under the DOSBox rules. The manual documents intended behavior; execution and binary evidence establish implemented behavior.
- Mark unknowns explicitly. Do not replace a missing rule with a plausible approximation and describe it as faithful.
- Keep game rules distinguishable from rendering and input code where that makes comparison easier; avoid speculative architecture or feature additions.
- Save analysis at material milestones. Review archives for local paths and debugger traces before publication.

## Final review

- Evaluate the frozen reference scenarios against both the original game and the browser port. Record matching behavior, deviations and untested areas, including random behavior and timing assumptions.
- Tests written by the porting model and visually similar output are supporting evidence, not independent proof of fidelity.
- Report incomplete work honestly. Preserve the intervention and assistance record even when a later attempt succeeds.
