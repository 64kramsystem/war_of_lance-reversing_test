# Experiment instructions

The objective is to measure intervention required for a faithful browser port, not merely produce a plausible game. Read README.md before starting.

- Follow [AGENTS.git.md](AGENTS.git.md) for repository work.
- Follow [AGENTS.binary-decompiling.md](AGENTS.binary-decompiling.md) and [AGENTS.reversing-shared.md](AGENTS.reversing-shared.md) when analyzing the executable.
- Follow [AGENTS.dosbox.md](AGENTS.dosbox.md) for every original or rebuilt DOS execution. Its boot image and debugger prerequisites must be supplied locally before execution.
- The decompilation guidance is adapted for this experiment: readable recovery notes support the browser port; original-language reconstruction and whole-binary listings are not required.
- Preserve `assets/original/`, `assets/dos/`, `assets/manifest.json` and `assets/SHA256SUMS`. Put working copies, saves and emulator images under ignored `scratch/`.
- Pin the Qwen Flash model, quantization, harness, reasoning settings, context configuration and tool versions before the measured run. Do not silently substitute another model or delegate to an unrecorded assistant.
- Record human interventions, outside-model assistance and failed attempts. Never infer human attention time from elapsed timestamps or report missing measurements as zero.
- Separate observed execution, static deductions and unverified hypotheses. Cite binary addresses or reference scenarios for recovered rules.
- Audit public artifacts and commit metadata for credentials, personal paths and unrelated information. Raw transcripts, used disk images and live Ghidra projects stay local until reviewed.
- Repository setup does not authorize starting a long-running reversing experiment; wait for an explicit run instruction.
