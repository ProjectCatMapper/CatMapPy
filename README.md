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
- Upload/edit write workflows with API-key authentication. See the [Standard Upload/Edit Options Table](#standard-uploadedit-options) below for a summary of available upload/edit actions.

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

### Standard Upload/Edit Options

The following table summarizes the available upload/edit actions and their meanings. Refer to this table when preparing data for upload or when using the `upload_rows()` function:

| Option Key      | Label                                                              | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| --------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| add_node        | Adding new node for every row                                      | Create a new node for each row. Use when each row represents a distinct new node.                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| node_add        | Updating existing Node properties--add or add to properties        | Update existing node properties by adding values without replacing current values.                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| node_replace    | Updating existing Node properties--replace one property            | Update one existing node property by replacing its value. Replace mode supports one property column.                                                                                                                                                                                                                                                                                                                                                                                                                             |
| add_uses        | Adding new uses ties (with old or new nodes)                       | Create USES ties for rows and include new or existing nodes. Rows can be aggregated by datasetID, CMID, and Key.                                                                                                                                                                                                                                                                                                                                                                                                                 |
| update_add      | Updating existing USES only--add or add to properties              | Update existing USES ties by adding values without removing current values.                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| update_replace  | Updating existing USES only--replace one property                  | Replace one property on existing USES ties. Replace mode supports one property column.                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| add_merging     | Adding new merging ties for every row                              | Create merging ties for rows in the upload file. Requires mergingID and datasetID. Variable-merging uploads also require Key so the DATASET-to-VARIABLE MERGING tie can be scoped to a specific dataset key without changing the dataset itself. If a stackID column is also provided, no new STACK node is created — the existing STACK node is used and MERGING ties are created from the MERGING node to that STACK and from that STACK to the DATASET. If stackID is omitted, a new STACK node is auto-created for each row. |
| merging_add     | Updating existing Merging tie properties--add or add to properties | Update existing merging tie properties by adding values without replacing current values.                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| merging_replace | Updating existing Merging tie properties--replace one property     | Replace one property on an existing merging tie. Replace mode supports one property column.                                                                                                                                                                                                                                                                                                                                                                                                                                      |

When using edit/upload workflows, select the appropriate option key from this table to control the upload behavior.

## API reference

See the docs API page for exported functions:
<https://projectcatmapper.github.io/CatMapPy/api-reference/>

## Environment variables

- `CATMAPR_API_URL`: Override API base URL.
- `CATMAPR_API_KEY`: API key for authenticated write endpoints.
- `CATMAPPER_API_KEY`: fallback API key variable.

The `CATMAPR_*` names are retained for compatibility with existing CatMapper API deployments.

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
