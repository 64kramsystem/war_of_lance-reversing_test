# Template adaptations

These files were adapted from local agent and reversing templates for this public experiment. Private source locations are intentionally omitted.

- `AGENTS.dosbox.md` is an unchanged copy.
- `AGENTS.binary-decompiling.md` replaces original-language/function-structure reconstruction with evidence-based recovery for a faithful browser port. It adds reference-scenario validation and explicit handling of unknowns.
- `AGENTS.git.md` removes an employer-specific branch prefix and replaces mandatory worktrees and history rewriting with run branches and preservation of measured history.
- `AGENTS.reversing-shared.md` removes a dependency on a private development skill, simplifies target-specific control-flow rules, and replaces full-listing export requirements with saved evidence relevant to the port.
- `AGENTS.md` is a project-specific entry point; the source entry point contained personal paths and unrelated tooling instructions.
- Ghidra MCP configurations are copied from the reversing template. Matching `dos-mcp` entries were added using the locally installed server's documented interface. Executable paths are relative; no credentials are included.
- The source Qwen launcher targets a different model and was not copied. Model configuration belongs in the recorded experiment setup.

The DOSBox template expects a separately supplied clean DOS boot image and `DEBUG.COM`. Used images from other projects were not copied into this repository.
