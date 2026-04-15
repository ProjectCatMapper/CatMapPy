# Usage

## Configure API URL (optional)

```python
import os
os.environ["CATMAPR_API_URL"] = "https://api.catmapper.org"
```

By default, CatMapPy uses `https://api.catmapper.org`. Set this only when you need to target a different deployment (for example, a staging or local API).

CatMapPy uses `CATMAPR_API_URL` and `CATMAPR_API_KEY` for cross-package compatibility with existing CatMapper tooling, and also supports `CATMAPPER_API_URL`/`CATMAPPER_API_KEY`.

## Configure API key for write endpoints

```python
import os
os.environ["CATMAPR_API_KEY"] = "cmk_your_api_key"
```

CatMapPy reads `CATMAPR_API_KEY` first, and falls back to `CATMAPPER_API_KEY`.

## Quickstart

```python
import pandas as pd
from catmappy import list_datasets, search_database, translate_rows

catalog = list_datasets("SocioMap")
results = search_database(database="SocioMap", domain="ETHNICITY", term="Afghanistan", property="Name")

rows = pd.DataFrame([{"country": "Afghanistan"}])
translated = translate_rows(
    rows=rows,
    database="SocioMap",
    domain="ADM0",
    term="country",
    property="Name",
)
```

## Merge example

```python
from catmappy import propose_merge_links

links = propose_merge_links(
    categoryLabel="ETHNICITY",
    datasetChoices=["SD5", "SD6"],
    database="SocioMap",
    equivalence="standard",
)
```
