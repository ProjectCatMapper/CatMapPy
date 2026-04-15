# Quickstart

```python
import pandas as pd
from catmappy import list_datasets, search_database, translate_rows

# List available datasets in a database
datasets = list_datasets("SocioMap")

# Search a domain
hits = search_database(
    database="SocioMap",
    domain="ETHNICITY",
    term="Dan",
)

# Translate rows with a property mapping
rows = pd.DataFrame([{"country": "Afghanistan"}])
translated = translate_rows(
    rows=rows,
    database="SocioMap",
    domain="ADM0",
    term="country",
    property="Name",
)
```

Set API overrides with environment variables when needed:

- `CATMAPR_API_URL`
- `CATMAPR_API_KEY`
