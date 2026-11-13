# Polygon and geometry workflows


Polygon uploads attach geometry to an **existing** dataset-to-category `USES`
relationship. They do not create categories, datasets, or ties. Each feature's
`properties` must contain nonblank strings `CMID`, `Key`, and `datasetID` matching
exactly one tie. Use a normalized source expression such as `Code == 1` for
`Key`, and use one `MultiPolygon` feature if a tie has several polygon parts.

The input must be a `.geojson` or `.json` `FeatureCollection` containing valid,
nonempty `Polygon` or `MultiPolygon` geometries in WGS84 longitude/latitude
order, with no `crs` member. Default server limits are 50 MiB, 10,000 features,
and 2,000,000 coordinate positions; deployments can override these limits.
For example (replace the identifiers with your existing target tie):

```json
{
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "properties": {"CMID": "SM1", "datasetID": "SD1", "Key": "Code == 1"},
    "geometry": {"type": "Polygon", "coordinates": [[[0,0],[1,0],[1,1],[0,0]]]}
  }]
}
```

An administrator API key is required for polygon preflight, apply, and discard.
Preflight checks the entire file and database targets without graph writes.
It returns counts, warnings, a digest, and a token bound to the acting user.
Tokens are single-use and expire after one hour by default. Inspect the report
before applying. Existing references are rejected unless `replace_existing`
is explicitly enabled **at preflight**.

```python
import catmappy as cm

# Uses CATMAPR_API_KEY (or CATMAPPER_API_KEY) and CATMAPR_API_URL when set.
report = cm.preflight_polygon_upload("polygons.geojson", "SocioMap")
print(report)

# After reviewing report, submit this explicit write request:
task = cm.apply_polygon_upload(report["token"])
result = cm.waitForUploadTask(task["taskId"], timeout_seconds=1800)
print(result["file"])  # feature count, geometry count, USES links and upload ID

# Alternative: discard an unused report rather than applying it.
# cm.discard_polygon_upload(report["token"])
```

Apply revalidates and queues the upload. The worker rechecks the file digest and
targets, stages geometry in `gisdb`, updates `USES.geoPolygon`, and verifies the
result. Failures trigger compensating restoration/cleanup across the two
databases. The package does not retry apply automatically.

Polling timeouts do not cancel the server job. Resume polling using its task ID,
or request cooperative cancellation with `cm.cancel_upload_task(task["taskId"])`
and poll `cm.uploadInputNodesStatus(task["taskId"])` for the final status. A task
may finish before cancellation takes effect. Expired tokens require new preflight.

```python
try:
    report = cm.preflight_polygon_upload("polygons.geojson", "SocioMap")
except cm.CatMapPyError as error:
    print(error.status_code)
    print(error.error_details)  # feature, field, code, message, when supplied
    print(error.task_id)        # present on failed/canceled task errors
```

## Retrieve geometry and inspect contextual policy

```python
geometry = cm.get_geometry("SocioMap", "SM1")
map_data = cm.explore_geometry("SocioMap", "SM1", layers="direct", polygon_limit=100)
policy = cm.get_contextual_policy("SocioMap")
validation = cm.validate_contextual_rows(
    [{"CMID": "SM1", "parent": ["SM2"]}], "SocioMap"
)
```

Geometry helpers preserve the API response without a GIS dependency. Direct
polygon rows may contain JSON-encoded geometry and use server-selected
simplifications; explore results contain processed features, sources, and
truncation metadata. Requested limits remain subject to server caps/behavior.

Contextual validation is read-only and accepts a DataFrame or list of row
objects (at most 1,000). It checks contextual policy, not the complete upload
contract. The server rechecks edit requirements when a write is submitted.
Rows are validated together; the client does not silently split larger edits,
which could hide conflicts between proposed domain changes. The endpoint can
reject validation when contextual enforcement is disabled on the server.
