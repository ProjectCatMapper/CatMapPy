# API Reference

CatMapPy exports metadata, search/translation, merge, and upload helpers from `catmappy`.

## Metadata

- `list_datasets(database)`
- `get_dataset_metadata(database, cmid, domain=None)`
- `get_cmid_info(database, cmid)`
- `get_domains(database="SocioMap", advanced=False)`
- `get_upload_properties(database="SocioMap")`
- `get_properties(database="SocioMap")`

## Search and Translation

- `search_database(database, domain, term, property=None, year=None, context=None)`
- `translate_rows(rows, database, domain, term, property="Name", context=None, year=None)`

## Merge and Join

- `propose_merge_links(categoryLabel, datasetChoices, database="SocioMap", equivalence="standard")`
- `join_datasets(database, joinLeft, joinRight, domain="CATEGORY")`
- `get_merge_template(database, dataset_id)`
- `get_merge_template_summary(database, cmid)`
- `build_merge_syntax(template, database="SocioMap")`

## Upload and Keys (Write API)

- `build_key(field, value)`
- `build_key_from_columns(rows, columns)`
- `normalize_key(value)`
- `is_normalized_key(value)`
- `prepare_upload_rows(df, form_data=None, action="add_node", properties=None, merging_type="0", database="SocioMap")`
- `upload_rows(df, database, form_data, action, ...)`

## Aliases

Legacy-compatible aliases are also available:

- `allDatasets`, `datasetInfo`, `createLinkfile`, `getDomains`
- `getMergingTemplate`, `getMergingTemplateSummary`, `generateMergeFiles`
- `uploadInputNodes`, `submitEditUpload`, `waitForUploadTask`
