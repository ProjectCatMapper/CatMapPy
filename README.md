# CatMapPy

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/github/license/ProjectCatMapper/CatMapPy)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-2ea44f)](https://projectcatmapper.github.io/CatMapPy/)
[![ProjectCatMapper](https://img.shields.io/badge/ProjectCatMapper-Organization%20Site-24292f)](https://projectcatmapper.github.io/)

CatMapPy is a Python interface to the CatMapper API for searching datasets, building merge keys, and translating tabular data.

## Package Documentation

Project docs: <https://projectcatmapper.github.io/CatMapPy/>

ProjectCatMapper organization site: <https://projectcatmapper.github.io/>

## Overview

**CatMapPy** provides Python access to [CatMapper](https://catmapper.org) APIs used by `SocioMap` and `ArchaMap`.

It supports:

- Dataset metadata retrieval
- Entity/category search
- Row translation workflows
- Merge-link proposal and dataset joins
- Upload/edit write workflows with API-key authentication

## Installation

```bash
python -m pip install -e .
```

For development:

```bash
python -m pip install -e .[dev,docs]
```

## Quickstart

```python
import pandas as pd
from catmappy import list_datasets, search_database, translate_rows

datasets = list_datasets("SocioMap")
hits = search_database(database="SocioMap", domain="ETHNICITY", term="Dan")

rows = pd.DataFrame([{"country": "Afghanistan"}])
translated = translate_rows(
    rows=rows,
    database="SocioMap",
    domain="ADM0",
    term="country",
    property="Name",
)
```

## Usage highlights

- Search and metadata discovery: `list_datasets`, `search_database`, `get_dataset_metadata`, `get_domains`
- Merge key helpers: `normalize_key`, `build_key`, `build_key_from_columns`
- Translation/upload workflows: `translate_rows`, `prepare_upload_rows`, `upload_rows`

## API reference

See the docs API page for exported functions:
<https://projectcatmapper.github.io/CatMapPy/api-reference/>

## Environment variables

- `CATMAPR_API_URL`: override API base URL.
- `CATMAPR_API_KEY`: API key for authenticated write endpoints.
- `CATMAPPER_API_KEY`: fallback API key variable.

The `CATMAPR_*` names are retained for compatibility with existing CatMapper tooling across packages.

## Contributing

- Issues: <https://github.com/ProjectCatMapper/CatMapPy/issues>
- Pull requests: <https://github.com/ProjectCatMapper/CatMapPy/pulls>

```bash
pytest -q
mkdocs serve
```

## Citation

If CatMapPy supports your work, cite ProjectCatMapper resources and link to:
<https://github.com/ProjectCatMapper/CatMapPy>

## License

GNU General Public License v3.0. See [LICENSE](LICENSE).
