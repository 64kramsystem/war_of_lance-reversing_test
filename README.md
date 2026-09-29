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

This repository's initial preparation used another coding assistant. No human timer was running during that preparation; setup time is **unmeasured**, not zero. The intervention log starts empty. Preserve raw run transcripts locally under ignored `runs/`; review them for personal information and credentials before publishing selected evidence.

## Agent guidance and tools

Read [AGENTS.md](AGENTS.md). The DOSBox guidance is copied unchanged. The decompilation guidance and its shared/Git dependencies are adapted for behavioral fidelity and preserving experiment history, with personal workflow references removed; see [template adaptations](docs/templates.md).

Ghidra and DOSBox MCP configurations are supplied for `.mcp.json`, `.codewhale/mcp.json` and `.codex/config.toml`. They use loopback connections and these relative executables:

```text
../../local/ghidra-mcp-next/.venv/bin/ghidra-mcp-bridge
../../local/dos-mcp/.venv/bin/dos-mcp
```

Those paths fit a checkout under `~/code/` with tools under `~/local/`; other installations must adjust their local configuration. These MCPs supply analysis and emulator control, not model inference. Configure the installed Qwen Flash separately and record the exact resolved model; the source template's Qwen 27B launcher was deliberately omitted.

`dos-mcp` requires the [DOSBox-X remote-debug fork](https://github.com/64kramsystem/dosbox-x), built with `--enable-remotedebug`, and a guest configured with `[dosbox] qmpserver=true` on loopback port 4444. Ghidra's debugger bridge uses loopback port 8099. With CodeWhale, pass an absolute `CODEWHALE_MCP_CONFIG` path:

```sh
export CODEWHALE_MCP_CONFIG="$PWD/.codewhale/mcp.json"
```

Before executing the game, supply a clean `assets/ms_dos_500/ms_dos_500_hdd.img` matching the DOSBox template's geometry and `assets/DEBUG.COM`. These local runtime prerequisites are ignored and are not bundled. Never reuse a disk from another analysis or mount the base image writable; work on a scratch copy under `scratch/`. No emulator or MCP session is started by this repository.
