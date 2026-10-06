# cafe-llama service (scaffold)

Optional advanced inference runtime based on [cafe-llama.cpp](https://github.com/quimmedes/cafe-llama.cpp).

This directory is a **scaffold**. It defines the intended service contract; full installer and Dashboard integration are follow-up work.

## Intent

- Opt-in only (`ods enable cafe-llama` or explicit runtime selection)
- Same OpenAI-compatible surface as `llama-server` where possible
- Expose MoE offload, Turbo KV, MTP, and PLE-related flags
- Prefer upstream prebuilt binaries from cafe-llama.cpp releases

## Files

| File | Purpose |
|------|---------|
| `manifest.yaml` | Capability and config contract |
| `entrypoint.sh` | Placeholder process launcher |
| `README.md` | This file |

Operator documentation: `ods/docs/CAFE-LLAMA.md`

## Non-goals

- Do not disable or replace the default `llama-server` service
- Do not treat upstream benchmarks as MEASURED local evidence
