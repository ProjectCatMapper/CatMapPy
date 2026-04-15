# CatMapPy

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/github/license/ProjectCatMapper/CatMapPy)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-2ea44f)](https://projectcatmapper.github.io/CatMapPy/)
[![ProjectCatMapper](https://img.shields.io/badge/ProjectCatMapper-Organization%20Site-24292f)](https://projectcatmapper.github.io/)

CatMapPy is a Python interface to the CatMapper API for searching datasets, building merge keys, and translating tabular data.

## Documentation

- Project docs: <https://projectcatmapper.github.io/CatMapPy/>
- ProjectCatMapper organization site: <https://projectcatmapper.github.io/>

## Installation

```bash
python -m pip install -e .
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

## Contributing

```bash
python -m pip install -e .[dev,docs]
pytest -q
mkdocs serve
```

## Citation

If CatMapPy supports your work, cite ProjectCatMapper resources and link to:
<https://github.com/ProjectCatMapper/CatMapPy>

## License

This project is licensed under the terms in [LICENSE](LICENSE).

## Environment variables

- `CATMAPR_API_URL`: Override API base URL.
- `CATMAPR_API_KEY`: API key for authenticated write endpoints.
