# Shared binary reversing rules

## Analysis

- State the concrete behavioral question before expanding analysis; stop when it is answered.
- Keep reference searches targeted and read only the passages relevant to the question being investigated.

- Improve MCPs or other tools only for a concrete, substantial benefit to the current task, including making existing workflows simpler, faster, or more reliable.
  Pause reversing, check tool history for related changes, make the smallest necessary change without speculative generalization, then deploy and verify before resuming.
  Keep reusable helpers in the repo and list them briefly in README.md; keep sample-specific scripts and assignments outside it.

- When a script can help future analyses, generalize and verify it, store it in the project, and list it briefly in README.md.
  Parameterize target-specific inputs; avoid speculative generalization.

- Follow materially distinct branches and indirect calls that affect the rule under investigation. Explain relevant input, register, stack and state assumptions; a named function alone does not establish its behavior.
- Do not expand into exhaustive path combinations without a concrete behavioral question. Record unresolved paths that could affect fidelity.

## Debugger

- GDB's flat EBP unwinder can fabricate real-mode callers. Limit backtraces to the current frame when segmented unwinding is unsupported.
- Successful Ghidra MCP commands can hide asynchronous TraceRMI errors. Inspect terminal output after operations and shutdown.
- Keep each emulator a child of its driving process; never share an instance; terminate it on every exit or failure.
  Concurrent runs require separate writable images, debugger sessions, ports and MCP connections; otherwise run sequentially.
  GDB detach can resume a guest before cleanup; terminate a stopped guest through the debugger before detaching.

## Saved evidence

- Save before exporting a project archive. Keep recovered rules tied to input hashes, addresses and reference observations. A complete assembly listing is not a required artifact for this experiment.
- Archives can include debugger traces and host paths. Inspect exported evidence and publish only intended artifacts.
