# API Reference

CatMapPy mirrors the CatMapR public API where practical. Preferred Python
functions use `snake_case`; compatibility aliases preserve the names used by
existing CatMapR workflows.

## Shared CatMapR/CatMapPy Surface

| Workflow | Preferred function | Compatibility aliases |
| --- | --- | --- |
| Dataset catalog metadata | `list_datasets(database)` | `allDatasets(database)`, `listDatasetMetadata(database)` |
| Dataset metadata by CMID | `get_dataset_metadata(database, cmid, domain="CATEGORY", children=None)` | `datasetInfo(database, CMID, ...)`, `getDatasetMetadata(database, CMID, ...)` |
| CMID details | `get_cmid_info(database, cmid)` | `CMIDinfo(database, cmid)` |
| Search | `search_database(...)` | - |
| Translation | `translate_rows(rows, ...)` | - |
| Merge-link proposal | `propose_merge_links(...)` | `createLinkfile(...)` |
| Dataset join | `join_datasets(database, joinLeft, joinRight, domain="CATEGORY")` | - |
| Domain metadata | `get_domains(database="SocioMap", advanced=False)` | `getDomains(database, advanced)` |
| Flattened property metadata | `get_properties(database="SocioMap", url=None)` | - |
| Upload property metadata | `get_upload_properties(database="SocioMap", url=None)` | - |
| Merge template rows | `get_merge_template(database, dataset_id, url=None)` | - |
| Merge template summary | `get_merge_template_summary(database, cmid, url=None)` | - |
| Downloadable merging template | `getMergingTemplate(cmid, database="SocioMap", url=None)` | - |
| Downloadable merging summary | `getMergingTemplateSummary(cmid, database="SocioMap", url=None)` | - |
| Merging template classifier | `findMergingTemplate(cmid, database="SocioMap", url=None)` | - |
| Merging template workbook | `downloadMergingTemplateWorkbook(...)` | - |
| Link-file workbook | `downloadLinkFileWorkbook(...)` | - |
| Generate merge syntax | `build_merge_syntax(template, database, url=None)` | - |
| Generate merge files | `generateMergeFiles(...)` | - |
| Download merge zip | `downloadMergeZip(hash_id, ...)` | - |
| Build key expression | `build_key(field, value)` | - |
| Build key column | `build_key_from_columns(data, columns, key_column="Key", drop_source=False)` | - |
| Normalize key expression | `normalize_key(key)` | - |
| Check normalized keys | `is_normalized_key(key)` | - |
| Prepare upload rows | `prepare_upload_rows(...)` | - |
| Start edit upload | `uploadInputNodes(...)` | - |
| Refresh waiting USES | `updateWaitingUSES(database, ...)` | - |
| Upload task status | `uploadInputNodesStatus(task_id, ...)` | - |
| Wait for upload task | `waitForUploadTask(task_id, ...)` | - |
| Submit edit upload | `submitEditUpload(...)` | - |
| Upload and poll rows | `upload_rows(...)` | - |

## Python-Specific Helpers

- `call_api(...)`: public Python helper for direct CatMapper API calls.
- `CatMapPyError`: validation and API error type raised by CatMapPy.

For exact signatures, see source code in [`src/catmappy/core.py`](https://github.com/ProjectCatMapper/CatMapPy/blob/main/src/catmappy/core.py).
