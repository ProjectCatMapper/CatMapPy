# API Reference

CatMapPy exports both snake_case and compatibility aliases.

## Core API

- `call_api`
- `list_datasets` / `allDatasets`
- `search_database`
- `get_dataset_metadata` / `datasetInfo`
- `get_domains` / `getDomains`
- `get_properties`

## Merge and translation helpers

- `normalize_key`
- `is_normalized_key`
- `build_key`
- `build_key_from_columns`
- `translate_rows`
- `prepare_upload_rows`
- `propose_merge_links`
- `join_datasets`

## Upload and task helpers

- `upload_rows`
- `uploadInputNodes`
- `uploadInputNodesStatus`
- `waitForUploadTask`
- `submitEditUpload`

For exact signatures, see source code in [`src/catmappy/core.py`](https://github.com/ProjectCatMapper/CatMapPy/blob/main/src/catmappy/core.py).
