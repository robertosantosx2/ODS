# Strata (optional inference runtime)

Optional ODS extension that runs **[Strata](https://github.com/Niko1221/Strata)** for **Qwen3.8-Flash-Next** on a consumer **NVIDIA** GPU (≥ 12 GB VRAM, 32–64 GB system RAM, ~80 GB disk for weights).

- **Category:** optional — not enabled by default
- **Does not replace** core `llama-server`
- **Design workshop:** [LEONES docs/integrations/strata](https://github.com/robertosantosx2/LEONES/tree/docs/strata-ods-integration/docs/integrations/strata)

## Enable

```bash
ods enable strata
```

Before first start:

1. Set a **pinned** `STRATA_IMAGE` (or configure the source build in `compose.nvidia.yaml`).
2. Ensure free disk (~80 GB) and envelope hardware.
3. Accept model download (~70 GB) on first run — product UX should require explicit consent.

## Environment (host → container)

| Host env | Container | Default |
|----------|-----------|--------|
| `STRATA_MODEL` | `MODEL` | `IQ2_XS` |
| `STRATA_FAMILY` | `FAMILY` | (empty) |
| `STRATA_CONTEXT` | `CONTEXT` | `8192` |
| `STRATA_VISION` | `VISION` | `no` |
| `STRATA_LOW_RAM` | `LOW_RAM` | `auto` |
| `STRATA_API_KEY` | `API_KEY` | (empty; required off loopback) |
| `STRATA_PORT` | host publish | `8088` |
| `STRATA_START_PERIOD` | health start | `600s` |

Data directory: `data/strata` (not the GGUF catalog under `data/models`).

## Health

- Path: `/health` (available before API key gate upstream)
- First start can take **1–3+ minutes** while the model loads; do not shorten `start_period` aggressively.

## Out of scope (this scaffold)

- Unified proxy routing / ICD profiles / Dashboard form (follow-up PRs)
- AMD HIP as default
- Multi-GPU as default
