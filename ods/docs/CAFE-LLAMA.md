# cafe-llama.cpp optional runtime

**Status:** experimental enable path  
**Upstream:** https://github.com/quimmedes/cafe-llama.cpp  
**Design / evidence rules:** https://github.com/robertosantosx2/LEONES/pull/96

## Role in ODS

cafe-llama.cpp is an **optional advanced** inference runtime. It does **not** replace the default `llama-server` or `LLM_BACKEND=llama-server`.

Use it when you need:

- MoE expert offload to pinned host RAM, system RAM, or SSD streaming
- Turbo low-bit KV cache (with flash-attention)
- Strong MTP speculative decoding and PLE/N-gram controls
- Native safetensors loading (no intermediate GGUF required for some checkpoints)

It remains OpenAI-compatible and GGUF-compatible, so Portal, Open WebUI, Hermes, LiteLLM, and external clients can keep the same API base URL once routing points at this runtime.

## Enable (`ods enable cafe-llama`)

```bash
# From the ODS install tree:
cp -r extensions/library/services/cafe-llama extensions/services/cafe-llama
ods enable cafe-llama
ods start cafe-llama
```

Library recipe: `extensions/library/services/cafe-llama/`

1. Ensure a cafe-llama.cpp `llama-server` binary is available (build image with `CAFE_LLAMA_RELEASE_URL` or set `CAFE_LLAMA_SERVER`).
2. Set `CAFE_LLAMA_MODEL` to a GGUF/safetensors path under the models volume.
3. Optional advanced flags via `.env` / Dashboard (see below).

Default listen: host port **8081** (`EXT_CAFE_LLAMA_PORT`).

## Dashboard / `.env.schema`

Settings surface for operators:

| Key | Purpose |
|-----|---------|
| `CAFE_LLAMA_ENABLED` | Opt-in marker (does not change `LLM_BACKEND`) |
| `CAFE_LLAMA_HOST` / `EXT_CAFE_LLAMA_PORT` | Bind / publish |
| `CAFE_LLAMA_MODEL` | Model path |
| `CAFE_LLAMA_EXTRA_ARGS` | Raw extra CLI flags |
| `LLAMA_ARG_HOST_MOE` / `LLAMA_ARG_N_HOST_MOE` | Host MoE offload |
| `LLAMA_ARG_CPU_MOE` / `LLAMA_ARG_N_CPU_MOE` | CPU MoE offload |
| `LLAMA_ARG_SSD_STREAMING` / `LLAMA_ARG_N_SSD` | SSD expert streaming |
| `LLAMA_ARG_CACHE_TYPE_K` / `V` | KV types (`turbo4`/`turbo3`/`turbo2` on cafe builds) |
| `LLAMA_ARG_FLASH_ATTN` | Required for turbo KV |
| `LLAMA_ARG_SPEC_TYPE` / `LLAMA_ARG_SPEC_DRAFT_N_MAX` | MTP / speculative |
| `LLAMA_ARG_PIPELINE_PARALLEL` | Host→device overlap |
| `LLAMA_ARG_NO_NGRAM` / `LLAMA_ARG_NGRAM_SSD` | Qwen Flash Next PLE |

Schema fragment (merge into `ods/.env.schema.json` `properties` for full Dashboard validation):

`extensions/library/services/cafe-llama/env.schema.fragment.json`

Existing stock keys already present in core schema (e.g. `LLAMA_ARG_N_CPU_MOE`, `LLAMA_ARG_FLASH_ATTN`, `LLAMA_ARG_SPEC_*`) continue to apply.

## Evidence rules

| Class | Meaning |
|-------|---------|
| REPORTED | Published by upstream or third parties |
| OBSERVED | Verified from docs/releases/code |
| ESTIMATED | Pre-run viability guess |
| MEASURED | Produced on target hardware under controlled workload |

Only **MEASURED** results justify local performance claims.

## Out of scope (follow-ups)

- Installer auto-promotion of cafe-llama as a first-class `LLM_BACKEND` value
- Full merge of the schema fragment into root `.env.schema.json` (if not done in the same PR)
- Automatic ICD sweeps / recommended profiles
- Replacement of default `llama-server` paths

## References

- https://github.com/quimmedes/cafe-llama.cpp
- https://github.com/quimmedes/cafe-llama.cpp/releases
- https://huggingface.co/quimmedes/Qwen3.8-Flash-Next-MTP-GGUF
- LEONES design PR: https://github.com/robertosantosx2/LEONES/pull/96
