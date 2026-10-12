# cafe-llama (library extension)

Optional **advanced** llama.cpp runtime based on [cafe-llama.cpp](https://github.com/quimmedes/cafe-llama.cpp).

Does **not** replace the core `llama-server` service or `LLM_BACKEND=llama-server`.

## Capabilities (OBSERVED)

- MoE expert offload to pinned host RAM (`-hmoe`), system RAM (`-cmoe`) or SSD streaming (`-ssd`)
- Turbo low-bit KV cache (`turbo4` / `turbo3` / `turbo2`) + Flash Attention
- MTP speculative decoding (`--spec-type draft-mtp`, recommended `--spec-draft-n-max 4`)
- PLE / N-gram control for Qwen 3.8 Flash Next
- Native safetensors loading
- OpenAI-compatible API (same clients as core llama-server)

## Enable

```bash
# From an ODS install tree:
cp -r extensions/library/services/cafe-llama extensions/services/cafe-llama
ods enable cafe-llama
ods start cafe-llama
```

Set in `.env` (also exposed in Dashboard settings):

```bash
CAFE_LLAMA_MODEL=/models/your-model.gguf
EXT_CAFE_LLAMA_PORT=8081

# Recommended starting point for MoE + long context on 8–24 GB GPUs:
LLAMA_ARG_HOST_MOE=on
LLAMA_ARG_CACHE_TYPE_K=turbo4
LLAMA_ARG_CACHE_TYPE_V=turbo4
LLAMA_ARG_FLASH_ATTN=on
LLAMA_ARG_SPEC_TYPE=draft-mtp
LLAMA_ARG_SPEC_DRAFT_N_MAX=4
```

### Image build

By default the Dockerfile downloads the **0.75 Linux x64 CUDA 12.4** binary.
Override for other platforms:

```bash
docker build \
  --build-arg CAFE_LLAMA_RELEASE_URL='https://github.com/quimmedes/cafe-llama.cpp/releases/download/0.75/llama-bin-ubuntu-x64-cpu.zip' \
  -t ods-cafe-llama:local \
  extensions/services/cafe-llama
```

Or set `CAFE_LLAMA_RELEASE_URL` in the environment before `ods start`.

## Evidence rules (LEONES)

| Class     | Meaning                                      |
|-----------|----------------------------------------------|
| REPORTED  | Published by upstream / third parties        |
| OBSERVED  | Verified from docs / releases / code         |
| ESTIMATED | Pre-run viability guess                      |
| MEASURED  | Produced on target hardware under controlled workload |

Only **MEASURED** results justify local performance claims.

## Docs

- Operator: `docs/CAFE-LLAMA.md`
- Design / ICD: LEONES `docs/integrations/cafe-llama.cpp/README.md`
