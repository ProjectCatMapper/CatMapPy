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
| Polygon preflight | `preflight_polygon_upload(file, database, replace_existing=False, api_key=None, url=None)` | - |
| Apply polygon preflight | `apply_polygon_upload(token, api_key=None, url=None)` | - |
| Discard unused preflight | `discard_polygon_upload(token, api_key=None, url=None)` | - |
| Cancel upload task | `cancel_upload_task(task_id, cursor=0, api_key=None, url=None)` | - |
| Direct geometry rows | `get_geometry(database, cmid, url=None)` | - |
| Explore map geometry | `explore_geometry(database, cmid, layers=None, relations=None, max_depth=None, node_limit=None, point_limit=None, polygon_limit=None, feature_limit=None, url=None)` | - |
| Contextual policy | `get_contextual_policy(database="SocioMap", url=None)` | - |
| Read-only policy validation | `validate_contextual_rows(rows, database, url=None)` | - |

## Python-Specific Helpers

- `call_api(...)`: public Python helper for direct CatMapper API calls. Supports
  GET, JSON POST, multipart POST via `files`, and DELETE. File handles passed
  directly to `call_api` are owned by the caller; polygon preflight manages its
  file handle automatically.
- `CatMapPyError`: validation and API error type raised by CatMapPy. Server
  failures retain `error_details`, `response`, `status_code`, and `task_id`.
  Fields without a relevant server value are empty or `None`.

Spatial helpers use the server's `/api/...` routes and require a deployment
that exposes them. `url` is the API host root, such as `https://api.catmapper.org`.
Geometry results retain the server structure without requiring GeoPandas.
`get_geometry` returns point/polygon rows (polygon geometry can be JSON text);
`explore_geometry` returns processed map features, sources, and any truncation.
Layers/relations accept comma-separated strings or lists; omitted limits use
server defaults, and requested limits remain subject to server behavior/caps.

See [polygon and geometry workflows](spatial.md) for payloads and examples.

For exact signatures, see source code in [`src/catmappy/core.py`](https://github.com/ProjectCatMapper/CatMapPy/blob/main/src/catmappy/core.py).
