# Qwen3.8 Flash NVFP4 + Q8_0

The selected weights are the [CompiledThoughts NVFP4 + Q8_0 GGUF conversion](https://huggingface.co/CompiledThoughts/Qwen3.8-Flash-Next-NVFP4-Q8_0/tree/d0f5c6667cea078100caea35835ed08f6ed66608). [The model record](../experiments/model.json) pins its revision, size, SHA-256 and the locally measured runtime settings. The existing download receipt verified the full hash; repository preparation checked the installed file's size and GGUF header without repeating the 119 GiB hash read.

This conversion preserves NVFP4 routed experts and uses Q8_0 for other quantized weights. It has no vision encoder or MTP head. Q8_0 in the model name describes weights; the runtime also independently uses Q8_0 for both KV caches. Native context is 262,144 tokens; the previously tuned single-slot configuration serves 131,072.

Start the model server in the foreground:

```sh
llama serve \
  --model "$HOME/models/Qwen3.8-Flash-Next-NVFP4-Q8_0/Qwen3.8-Flash-Next-NVFP4-Q8_0.gguf" \
  --alias qwen3.8-flash-next-nvfp4 --host 127.0.0.1 --port 8081 \
  --ctx-size 131072 --parallel 1 --threads 16 --threads-batch 16 \
  --ubatch-size 1024 --load-mode none --fit-target 2048 \
  --cache-type-k q8_0 --cache-type-v q8_0 --flash-attn on --jinja \
  --no-context-shift --log-verbosity 4 \
  --reasoning on --reasoning-effort xhigh --reasoning-budget -1 \
  --reasoning-format deepseek \
  --temp 1 --top-p 0.95 --top-k 20 --min-p 0
```

This command matches the recorded benchmark launch settings. Its automatic GPU placement depends on available memory; record actual placement, model metadata, software versions and sampler settings at run start. The prior measured weight-buffer placement was CUDA 24,793.18 MiB, CUDA host 45,204.52 MiB and CPU mapped 51,880.13 MiB. This is not a measurement of current RSS or total VRAM usage.

Use the checked-in CodeWhale profile with an absolute MCP configuration path, from the repository root:

```sh
export CODEWHALE_MCP_CONFIG="$PWD/.codewhale/mcp.json"
codewhale --config "$PWD/.codewhale/qwen-local.toml" \
  --provider qwen-local --model qwen3.8-flash-next-nvfp4 --workspace "$PWD" \
  exec --auto --output-format stream-json "<frozen task prompt>"
```

Replace the placeholder with the frozen task prompt when starting the run. The profile declares the served context and requests compaction at 80%. Before a measured run, verify a reasoning/tool round trip and context compaction with this harness; the earlier coding benchmark used a different harness. Keep the frozen task prompt and complete run record. Selecting this configuration does not start the experiment.

DOSBox can capture screens, but this text-only model cannot directly interpret image inputs. Use binary/state evidence and programmed image comparisons where useful; separately record any human interpretation or outside vision-model assistance.
