# cafe-llama (library extension)

Optional **advanced** llama.cpp runtime based on [cafe-llama.cpp](https://github.com/quimmedes/cafe-llama.cpp).

Does **not** replace the core `llama-server` service or `LLM_BACKEND=llama-server`.

## Enable

```bash
# From an ODS install tree:
cp -r extensions/library/services/cafe-llama extensions/services/cafe-llama
ods enable cafe-llama
ods start cafe-llama
```

Set in `.env` (also exposed in Dashboard settings via `.env.schema.json`):

```bash
CAFE_LLAMA_MODEL=/models/your-model.gguf
EXT_CAFE_LLAMA_PORT=8081
# Example advanced flags:
# LLAMA_ARG_HOST_MOE=on
# LLAMA_ARG_CACHE_TYPE_K=turbo4
# LLAMA_ARG_CACHE_TYPE_V=turbo4
# LLAMA_ARG_FLASH_ATTN=on
# LLAMA_ARG_SPEC_TYPE=draft-mtp
# LLAMA_ARG_SPEC_DRAFT_N_MAX=4
```

Build the image with a release asset when ready:

```bash
docker build --build-arg CAFE_LLAMA_RELEASE_URL='https://github.com/quimmedes/cafe-llama.cpp/releases/download/<tag>/<asset>' \
  -t ods-cafe-llama:local extensions/services/cafe-llama
```

## Docs

- Operator: `docs/CAFE-LLAMA.md`
- English summary: `docs/integrations/cafe-llama.cpp/README-eng.mkd`
