# CatMapPy

Python package interface for the CatMapper API.

## Package Documentation

Project page (package docs): <https://projectcatmapper.github.io/CatMapPy/>

## Overview

**CatMapPy** provides Python access to [CatMapper](https://catmapper.org) APIs used by `SocioMap` and `ArchaMap`.

It supports:

- Dataset metadata retrieval
- Entity/category search
- Row translation workflows
- Merge-link proposal and dataset joins
- Upload/edit write workflows with API-key authentication

## Install

```bash
pip install git+https://github.com/ProjectCatMapper/CatMapPy.git
```

For development:

```bash
pip install -e .[dev]
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

## Usage

### Environment variables

- `CATMAPR_API_URL`: override API base URL.
- `CATMAPR_API_KEY`: API key for authenticated write endpoints.
- `CATMAPPER_API_KEY`: fallback API key variable.

See full usage and API coverage in the docs site.

## Contributing

- Issues: <https://github.com/ProjectCatMapper/CatMapPy/issues>
- Pull requests: <https://github.com/ProjectCatMapper/CatMapPy/pulls>

## License

GNU General Public License v3.0. See [LICENSE](LICENSE).
