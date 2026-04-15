# Usage

## Configure API URL (optional)

```python
import os
os.environ["CATMAPR_API_URL"] = "https://api.catmapper.org"
```

By default, CatMapPy uses `https://api.catmapper.org`.

## Configure API key for write endpoints

```python
import os
os.environ["CATMAPR_API_KEY"] = "cmk_your_api_key"
```

CatMapPy reads `CATMAPR_API_KEY` first, and falls back to `CATMAPPER_API_KEY`.

## Common workflows

### 1. Search and inspect metadata

Use `list_datasets`, `search_database`, and metadata helpers to understand available keys and domains.

### 2. Build stable merge keys

Use `normalize_key`, `build_key`, and `build_key_from_columns` to create reproducible matching keys.

### 3. Translate tabular rows

Use `translate_rows` for direct row-wise translations, or `generateMergeFiles` for larger merge workflows.

## Error handling

CatMapPy raises `CatMapPyError` for validation failures and API errors, including clear authorization messages for missing or invalid API keys.
