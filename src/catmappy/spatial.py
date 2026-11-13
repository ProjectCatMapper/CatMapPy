"""Polygon uploads and read-only geometry/contextual policy endpoints.

Geometry responses retain the server structure; no GIS dependency is required.
"""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any
from urllib.parse import quote

from . import core


def _database(database: str) -> str:
    return core._validate_database(database).lower()


def _token(token: str) -> str:
    if not isinstance(token, str) or not re.fullmatch(r"[a-f0-9]{32}", token):
        raise core.CatMapPyError("`token` must be the 32-character token returned by polygon preflight.")
    return token


def preflight_polygon_upload(file: str | Path, database: str, replace_existing: bool = False,
                             api_key: str | None = None, url: str | None = None) -> dict[str, Any]:
    """Validate a GeoJSON file without graph writes; return its report and apply token.

    Requires an administrator API key. Features must identify an existing USES
    tie through string properties CMID, Key and datasetID. Replacement is opt-in.
    The server checks topology, target identity, ownership and configured limits.
    """
    database = _database(database)
    core._validate_bool(replace_existing, "replace_existing")
    path = Path(file)
    if not path.is_file() or path.suffix.lower() not in {".geojson", ".json"}:
        raise core.CatMapPyError("`file` must be an existing .geojson or .json file.")
    headers = {"X-API-Key": core._api_key(api_key)}
    with path.open("rb") as handle:
        return core.call_api(
            "api/uploads/geojson/polygons/preflight",
            {"database": database, "replaceExisting": str(replace_existing).lower()},
            request="POST", url=url, headers=headers,
            files={"file": (path.name, handle, "application/geo+json")},
        )


def apply_polygon_upload(token: str, api_key: str | None = None, url: str | None = None) -> dict[str, Any]:
    """Revalidate and queue a preflighted file; return taskId for waitForUploadTask.

    Tokens are single-use, belong to the preflighting user, and expire (one hour
    by default). This function does not retry apply requests automatically.
    """
    return core.call_api(f"api/uploads/geojson/polygons/{_token(token)}/apply", {},
                         request="POST", url=url, headers={"X-API-Key": core._api_key(api_key)})


def discard_polygon_upload(token: str, api_key: str | None = None, url: str | None = None) -> dict[str, Any]:
    """Delete an unused preflight token and its staged file; does not undo an upload."""
    return core.call_api(f"api/uploads/geojson/polygons/{_token(token)}", {},
                         request="DELETE", url=url, headers={"X-API-Key": core._api_key(api_key)})


def cancel_upload_task(task_id: str, cursor: int = 0, api_key: str | None = None,
                       url: str | None = None) -> dict[str, Any]:
    """Request cancellation of a tabular or polygon upload; poll for final status.

    Cancellation is cooperative, so a task can finish before it takes effect.
    """
    task_id = core._validate_string(task_id, "task_id")
    if isinstance(cursor, bool) or not isinstance(cursor, int) or cursor < 0:
        raise core.CatMapPyError("`cursor` must be a non-negative integer.")
    return core.call_api("api/uploads/input-nodes/cancel", {"taskId": task_id, "cursor": cursor},
                         request="POST", url=url, headers={"X-API-Key": core._api_key(api_key)})


def get_geometry(database: str, cmid: str, url: str | None = None) -> dict[str, Any]:
    """Return direct point/polygon rows, including server-selected simplifications.

    Polygon row geometry may be JSON-encoded text. Use explore_geometry for the
    map payload with processed features and source information.
    """
    return core.call_api("api/geometry", {"database": _database(database),
                                         "cmid": core._validate_string(cmid, "cmid")}, url=url)


def explore_geometry(database: str, cmid: str, layers: str | list[str] | None = None,
                     relations: str | list[str] | None = None, max_depth: int | None = None,
                     node_limit: int | None = None, point_limit: int | None = None,
                     polygon_limit: int | None = None, feature_limit: int | None = None,
                     url: str | None = None) -> dict[str, Any]:
    """Return the map geometry payload, retaining sources and truncation metadata.

    Omitted options use server defaults. Layers/relations accept comma-separated
    strings or lists. Limits are requests subject to server caps and behavior.
    """
    database = _database(database)
    cmid = quote(core._validate_string(cmid, "cmid"), safe="")
    parameters = {}
    for name, value in (("layers", layers), ("relations", relations)):
        if value is not None:
            if isinstance(value, list) and value:
                value = ",".join(core._validate_string(item, name) for item in value)
            parameters[name] = core._validate_string(value, name)
    for name, value in (("maxDepth", max_depth), ("nodeLimit", node_limit),
                        ("pointLimit", point_limit), ("polygonLimit", polygon_limit),
                        ("featureLimit", feature_limit)):
        if value is not None:
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise core.CatMapPyError(f"`{name}` must be a positive integer.")
            parameters[name] = value
    return core.call_api(f"api/databases/{database}/nodes/{cmid}/explore-geometry", parameters, url=url)


def get_contextual_policy(database: str = "SocioMap", url: str | None = None) -> dict[str, Any]:
    """Fetch the server's current metadata-driven contextual relationship policy."""
    return core.call_api(f"api/databases/{_database(database)}/metadata/contextual-policy", {}, url=url)


def validate_contextual_rows(rows: Any, database: str, url: str | None = None) -> dict[str, Any]:
    """Read-only policy validation of up to 1,000 proposed assertion row objects.

    Accepts a DataFrame or list of dicts. This checks contextual policy only; the
    upload endpoint still checks all other requirements and mutable conditions.
    """
    database = _database(database)
    records = core._records(rows)
    if len(records) > 1000:
        raise core.CatMapPyError("Contextual validation accepts at most 1000 rows per request.")
    return core.call_api(f"api/databases/{database}/metadata/contextual-policy/validate",
                         {"rows": records}, request="POST", url=url)
