# War of the Lance reversing test

Measure the human intervention needed for a local Qwen Flash model to reverse engineer the DOS version of **War of the Lance** and reproduce its rules and rendering in a browser.

The motivating [article](https://this.os.isfine.org/blog/posts/what-reverse-engineering-and-modernising-an-old-war-game-tells-us-about-the-econ/) reports a Qwen3.8-Flash-Next port in about a week with less than four hours of dedicated human attention. This repository prepares a repeatable experiment; no reversing run has started and no gameplay fidelity has been established. The exact model, quantization, harness, hardware and context settings must be recorded before a run; differences from the author's setup limit direct comparison.

## Inputs

- `assets/original/War-of-The-Lance_DOS.zip`: the unchanged DOS archive from [My Abandonware](https://www.myabandonware.com/game/war-of-the-lance-11z), 195,214 bytes.
- `assets/dos/`: all 48 files extracted from that archive; `START.EXE` is 317,720 bytes. These files have not been executed.
- `assets/original/War-of-The-Lance_Manual_DOS_EN.pdf`: the 24-page manual supplied by the same site.
- `assets/manifest.json`: download URLs, retrieval time, sizes and SHA-256 hashes. This identifies the downloaded distribution, not a verified pristine retail release.

Verify the inputs from the repository root:

```sh
sha256sum -c assets/SHA256SUMS
```

The original game and manual remain third-party copyrighted material. Their inclusion does not grant a new license to them.

## Experiment

The target is a browser implementation of the original game, with recovered game logic and rendering. Browser-hosted DOS emulation is a reference, not the finished port. Modernisation is outside the initial experiment.

Before starting, freeze the task prompt, environment settings and a set of reference scenarios covering loading, movement, combat, diplomacy, quests, AI turns, victory conditions and save/load. Record observable states and results from the original game. Report fidelity per scenario and unresolved behavior; successful screenshots or the model's own tests alone do not establish equivalence.

Use `experiments/interventions.csv` to log human help, including setup, prompt writing, reading progress, verification, corrections, restarts and time spent diagnosing tools. Record active human time separately from elapsed time and model usage. Count corrections against the original run even if they lead to a successful retry. Log help from other models separately, with the supplied prompt and output, so it cannot be mistaken for Qwen working alone.

This repository's initial preparation used another coding assistant. No human timer was running during that preparation; setup time is **unmeasured**, not zero. Preserve raw run transcripts locally under ignored `runs/`; review them for personal information and credentials before publishing selected evidence.

Run 001 is recorded under [experiments/run-001](experiments/run-001), with its frozen task prompt and reference-scenario definitions. `scripts/run_session.py` owns the local model, DOSBox and Ghidra processes, records their lifecycle, and starts one CodeWhale attempt after preflight. Create `runs/run-001/stop` to request shutdown; it also shuts down its child processes when the attempt ends or fails. Raw transcripts and model prompts remain under ignored `runs/run-001/`. The lifecycle script expects the prepared scratch disk and isolated Ghidra profile for this run; it is not a fresh-clone installer.

## Agent guidance and tools

Read [AGENTS.md](AGENTS.md). The DOSBox guidance is copied unchanged. The decompilation guidance and its shared/Git dependencies are adapted for behavioral fidelity and preserving experiment history, with personal workflow references removed; see [template adaptations](docs/templates.md).

Ghidra and DOSBox MCP configurations are supplied for `.mcp.json`, `.codewhale/mcp.json` and `.codex/config.toml`. They use loopback connections and these relative executables:

```text
../../local/ghidra-mcp-next/.venv/bin/ghidra-mcp-bridge
../../local/dos-mcp/.venv/bin/dos-mcp
```

Those paths fit a checkout under `~/code/` with tools under `~/local/`; other installations must adjust their local configuration. These MCPs supply analysis and emulator control, not model inference. The selected model is **Qwen3.8 Flash NVFP4 + Q8_0**, pinned in [experiments/model.json](experiments/model.json), with a [launch command and CodeWhale profile](docs/model.md). The configuration uses the previously tuned 131,072-token context and `xhigh` reasoning.

`dos-mcp` requires the [DOSBox-X remote-debug fork](https://github.com/64kramsystem/dosbox-x), built with `--enable-remotedebug`, and a guest configured with `[dosbox] qmpserver=true` on loopback port 4444. Ghidra's debugger bridge uses loopback port 8099. With CodeWhale, pass an absolute `CODEWHALE_MCP_CONFIG` path:

```sh
export CODEWHALE_MCP_CONFIG="$PWD/.codewhale/mcp.json"
```

The local checkout now has `assets/ms_dos_500/ms_dos_500_hdd.img` and `assets/DEBUG.COM`, copied from an unchanged tracked DOS baseline after inspecting its file listing and startup commands. They are ignored and are not included in the public repository. Fresh clones must supply matching local prerequisites; verify them with `sha256sum -c assets/runtime-SHA256SUMS`. The image is 33,546,240 bytes and matches geometry `512,63,2,520`; its FAT partition begins at byte 32,256. Never reuse a modified working disk or mount the base image writable; work on a scratch copy under `scratch/`. The local base image is read-only. No emulator or model inference session has been started for this experiment.
