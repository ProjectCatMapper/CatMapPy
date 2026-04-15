# CatMapPy

## Package Documentation

Project page (package docs): <https://projectcatmapper.github.io/CatMapPy/>

This site contains CatMapPy package documentation, including usage guidance and API reference.

**CatMapPy** is a Python package that provides an interface to the [CatMapper API](https://catmapper.org), enabling access to dataset catalog metadata, category entities, and translation and merge workflows used in `SocioMap` and `ArchaMap`.

This package allows you to:

- Retrieve dataset catalog metadata from CatMapper databases.
- Search for categories or entities and inspect details.
- Translate terms in tabular data using CatMapper domains/properties.
- Discover domain/property metadata for CatMapper deployments.
- Propose merge links and join aligned datasets.
- Submit authenticated edit/upload operations with API-key-based write access.

## Installation

CatMapPy is currently installed from GitHub:

```bash
pip install git+https://github.com/ProjectCatMapper/CatMapPy.git
```

For local development:

```bash
pip install -e .[dev]
```

## Package Overview

### Preferred public functions

- `list_datasets()`
- `get_dataset_metadata()`
- `get_cmid_info()`
- `search_database()`
- `translate_rows()`
- `propose_merge_links()`
- `join_datasets()`
- `get_domains()`
- `get_upload_properties()`
- `get_properties()`
- `build_key()`
- `build_key_from_columns()`
- `normalize_key()`
- `is_normalized_key()`
- `prepare_upload_rows()`
- `upload_rows()`

### Legacy-compatible aliases

- `allDatasets()`
- `datasetInfo()`
- `createLinkfile()`
- `getDomains()`

### Internal helper

- `call_api()` is an internal helper used by exported wrappers.

## License

CatMapPy is licensed under the GNU General Public License v3.0. See the [LICENSE](https://github.com/ProjectCatMapper/CatMapPy/blob/main/LICENSE) file.
