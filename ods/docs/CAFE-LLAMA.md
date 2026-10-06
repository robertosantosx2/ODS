# cafe-llama.cpp optional runtime

**Status:** experimental scaffold  
**Upstream:** https://github.com/quimmedes/cafe-llama.cpp  
**Design / evidence rules:** https://github.com/robertosantosx2/LEONES/pull/96

## Role in ODS

cafe-llama.cpp is an **optional advanced** inference runtime. It does **not** replace the default `llama-server`.

Use it when you need:

- MoE expert offload to pinned host RAM, system RAM, or SSD streaming
- Turbo low-bit KV cache (with flash-attention)
- Strong MTP speculative decoding and PLE/N-gram controls
- Native safetensors loading (no intermediate GGUF required for some checkpoints)

It remains OpenAI-compatible and GGUF-compatible, so Portal, Open WebUI, Hermes, LiteLLM, and external clients can keep the same API base URL once routing points at this runtime.

## Activation (planned)

```bash
ods enable cafe-llama
# or select runtime per model / profile in Dashboard → Models (advanced)
```

Binary preference:

1. Official prebuilt releases from https://github.com/quimmedes/cafe-llama.cpp/releases
2. Controlled source build when a platform/backend is not covered by releases

## Priority parameters

These should map into Dashboard advanced settings and/or `LLAMA_ARG_*` / Model Switchboard:

| Setting | Flag | Notes |
|---------|------|--------|
| GPU layers | `-ngl` | existing |
| Host MoE | `-hmoe` / `-nhmoe` | pinned CUDA host |
| CPU MoE | `-cmoe` / `-ncmoe` | system RAM |
| SSD streaming | `-ssd` / `-nssd` | mmap on-demand experts |
| Context | `-c` | existing |
| KV type | `-ctk` / `-ctv` | include `turbo4` / `turbo3` / `turbo2` |
| Flash attention | `-fa` | required for turbo KV |
| Spec type | `--spec-type` | e.g. `draft-mtp` |
| Spec draft depth | `--spec-draft-n-max` | recommended `4` |
| Draft model | `-md` | MTP GGUF path |
| PLE / N-gram | `--no-ngram` / `--ngram-ssd` | Qwen Flash Next |
| Pipeline parallel | `--pipeline-parallel` | host→device overlap |

## Service layout

```text
ods/services/cafe-llama/
├── README.md
├── manifest.yaml
└── entrypoint.sh
```

## Evidence rules

Do not claim local performance from upstream or community numbers alone.

| Class | Meaning |
|-------|---------|
| REPORTED | Published by upstream or third parties |
| OBSERVED | Verified from docs/releases/code |
| ESTIMATED | Pre-run viability guess |
| MEASURED | Produced on target hardware under controlled workload |

Only **MEASURED** results justify local performance claims.

## Out of scope for this scaffold

- Full installer wiring and `ods enable` implementation
- Dashboard UI changes
- Automatic ICD sweeps / recommended profiles
- Replacement of default `llama-server` paths

## References

- https://github.com/quimmedes/cafe-llama.cpp
- https://github.com/quimmedes/cafe-llama.cpp/releases
- https://huggingface.co/quimmedes/Qwen3.8-Flash-Next-MTP-GGUF
- LEONES design PR: https://github.com/robertosantosx2/LEONES/pull/96
