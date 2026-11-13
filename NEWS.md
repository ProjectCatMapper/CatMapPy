# CatMapPy 0.1.1 (2026-11-13)

- Added `preflight_polygon_upload`, `apply_polygon_upload`, and
  `discard_polygon_upload` for the administrator GeoJSON upload workflow.
  Preflight validates the entire file without graph writes; applying is an
  explicit separate step, and replacement defaults to disabled.
- Added `cancel_upload_task` for polygon and tabular tasks. Existing task
  status and waiting helpers also support polygon uploads.
- Added `get_geometry` and `explore_geometry` for direct geometry and map
  payloads, preserving server source and truncation information.
- Added `get_contextual_policy` and `validate_contextual_rows` for current
  policy discovery and read-only validation of up to 1,000 proposed rows.
- `CatMapPyError` now retains `error_details`, `response`, `status_code`
  (for HTTP failures), and `task_id` (for task failures). Error messages now
  use the server's message rather than raw JSON. Previously, error handling
  provided no structured access to actionable feature/field diagnostics.
- Extended `call_api` with multipart POST and DELETE support; JSON-only
  transport previously prevented use of the polygon endpoints.
- Added examples and mocked tests for multipart encoding, task completion,
  cancellation, structured failures, and read-only spatial requests.
- Existing public function signatures remain compatible.
