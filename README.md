# PolyChat models

The list of on-device AI models the PolyChat iOS app offers. The app downloads
`models.json` from this repo when it launches (and keeps a cached copy for
offline use), so **editing this file changes the app's model lineup without an
App Store update**.

## How to change the lineup

1. Edit `models.json` (the GitHub web editor is fine).
2. Commit. A check runs automatically (`validate.py`); fix anything it reports.
3. Apps pick up the change the next time they launch (GitHub may take a few
   minutes to serve the new file).

- **Change the default model:** set `defaultModelId` to another model's `id`.
- **Add a model:** copy an entry and update it. The model must be an MLX
  conversion on Hugging Face (usually `mlx-community/...`), and its
  `architecture` must be one the app supports. If it isn't, the app hides the
  model until an app update adds that architecture.
- **Remove a model:** delete its entry. People who already downloaded it keep it.

## Fields

| Field | Meaning |
|---|---|
| `id` | Stable identifier. Never reuse or rename an id. |
| `name`, `params`, `quant` | Shown in the app, e.g. "Qwen 3", "1.7B", "4-bit". |
| `repo` | Hugging Face repo with the MLX files. |
| `revision` | Exact commit hash on Hugging Face, so the files can't change under us. Find it on the repo's "Files" page (commit history) or via `https://huggingface.co/api/models/<repo>` (`sha`). |
| `sizeBytes` | Total download size, shown before downloading. |
| `architecture` | The model's `model_type` from its `config.json` (e.g. `qwen3`, `qwen3_5`, `lfm2`). |
| `capabilities` | Any of `text`, `vision`, `audio`, `reasoning`. |
| `tags` | Labels shown in the app (General, Writing, Creative, Reason, ...). |
| `description` | One sentence shown in the model list. |
| `license` | The model's license. Check it allows commercial use. |
| `minRamGB` | Hide the model on iPhones with less RAM than this. |
| `minAppVersion` | Hide the model on older app versions. |
| `pro` | Requires PolyChat PRO. |
