# CatMapPy

Python port of the CatMapper API wrapper package from CatMapR.

## Installation

```bash
pip install -e .
```

## Quick usage

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

## Environment variables

- `CATMAPR_API_URL`: Override API base URL.
- `CATMAPR_API_KEY`: API key for authenticated write endpoints.
