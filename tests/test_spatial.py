import json

import pandas as pd
import pytest
import requests

import catmappy as cm
from catmappy import core


TOKEN = "a" * 32
DETAILS = [{"feature": 2, "field": "Key", "code": "uses_not_unique", "message": "Missing tie"}]


def response(payload, code=200):
    result = requests.Response()
    result.status_code = code
    result._content = json.dumps(payload).encode()
    return result


@pytest.mark.parametrize("replace_existing", [False, True])
def test_polygon_preflight_sends_file_as_multipart_and_closes_it(monkeypatch, tmp_path, replace_existing):
    path = tmp_path / "polygons.geojson"
    raw = b'{"type":"FeatureCollection","features":[]}'
    path.write_bytes(raw)
    captured = {}

    def post(url, **kwargs):
        captured.update(kwargs)
        assert url == "https://example.test/api/uploads/geojson/polygons/preflight"
        assert "json" not in kwargs
        assert kwargs["data"] == {"database": "archamap", "replaceExisting": str(replace_existing).lower()}
        name, handle, mime = kwargs["files"]["file"]
        assert (name, handle.read(), mime) == (path.name, raw, "application/geo+json")
        # Exercise requests' actual multipart encoder, including the boundary.
        handle.seek(0)
        wire = requests.Request("POST", url, data=kwargs["data"], files=kwargs["files"],
                                headers=kwargs["headers"]).prepare()
        assert wire.headers["Content-Type"].startswith("multipart/form-data; boundary=")
        assert b'name="file"; filename="polygons.geojson"' in wire.body
        assert raw in wire.body
        assert wire.headers["X-API-Key"] == "test-key"
        return response({"valid": True, "token": TOKEN, "warnings": []})

    monkeypatch.setattr(core.requests, "post", post)
    report = cm.preflight_polygon_upload(path, "ArchaMap", replace_existing=replace_existing,
                                         api_key="test-key", url="https://example.test")
    assert report["token"] == TOKEN
    assert captured["files"]["file"][1].closed


def test_preflight_failure_preserves_details_and_never_applies(monkeypatch, tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{}")
    calls = []

    def post(url, **kwargs):
        calls.append(url)
        return response({"error": "Preflight failed", "error_details": DETAILS}, 422)

    monkeypatch.setattr(core.requests, "post", post)
    with pytest.raises(cm.CatMapPyError, match="Preflight failed") as exc:
        cm.preflight_polygon_upload(path, "SocioMap", api_key="test-key")
    assert exc.value.status_code == 422
    assert exc.value.error_details == DETAILS
    assert len(calls) == 1 and calls[0].endswith("/preflight")


def test_apply_then_existing_poller_and_cancel_and_discard(monkeypatch):
    calls = []

    def post(url, **kwargs):
        calls.append((url, kwargs))
        assert kwargs["headers"]["X-API-Key"] == "test-key"
        if url.endswith("/apply"):
            return response({"taskId": "task-1", "status": "queued"}, 202)
        if url.endswith("/cancel"):
            return response({"taskId": "task-1", "status": "running"}, 202)
        return response({"taskId": "task-1", "status": "completed", "file": [{"usesLinks": 1}]})

    monkeypatch.setattr(core.requests, "post", post)
    monkeypatch.setattr(core.requests, "delete", lambda url, **kwargs: (
        calls.append((url, kwargs)) or response({"message": "Polygon upload discarded."})))
    task = cm.apply_polygon_upload(TOKEN, api_key="test-key")
    assert cm.waitForUploadTask(task["taskId"], api_key="test-key")["file"][0]["usesLinks"] == 1
    cm.cancel_upload_task(task["taskId"], cursor=4, api_key="test-key")
    cm.discard_polygon_upload(TOKEN, api_key="test-key")
    assert calls[2][1]["json"] == {"taskId": "task-1", "cursor": 4}
    assert calls[3][0].endswith("/" + TOKEN)
    assert len([url for url, _ in calls if url.endswith("/apply")]) == 1


@pytest.mark.parametrize("state", ["failed", "canceled"])
def test_task_errors_retain_diagnostics(monkeypatch, state):
    payload = {"status": state, "error": "Bad polygon", "message": "Stopped", "error_details": DETAILS}
    monkeypatch.setattr(core, "uploadInputNodesStatus", lambda **kwargs: payload)
    with pytest.raises(cm.CatMapPyError) as exc:
        cm.waitForUploadTask("task-1", api_key="test-key")
    assert exc.value.error_details == DETAILS
    assert exc.value.task_id == "task-1"
    assert exc.value.response["status"] == state


def test_upload_rows_errors_keep_details_without_refresh(monkeypatch):
    monkeypatch.setattr(core, "prepare_upload_rows", lambda **kwargs: {
        "database": "SocioMap", "form_data": {}, "rows": [], "action": "add_node",
        "properties": [], "merging_type": "0"})
    calls = []

    def call(endpoint, *args, **kwargs):
        calls.append(endpoint)
        if endpoint == "uploadInputNodes":
            return {"taskId": "task-1"}
        return {"status": "failed", "error": "Invalid reference", "error_details": DETAILS}

    monkeypatch.setattr(core, "call_api", call)
    with pytest.raises(cm.CatMapPyError) as exc:
        cm.upload_rows([], "SocioMap", api_key="test-key")
    assert exc.value.error_details == DETAILS
    assert exc.value.task_id == "task-1"
    assert "updateWaitingUSES" not in calls


def test_read_only_geometry_and_contextual_policy_payloads(monkeypatch):
    calls = []
    payload = {"polygons": [], "truncated": 3, "sources": ["SD1"]}

    def call(endpoint, parameters, **kwargs):
        calls.append((endpoint, parameters, kwargs))
        return payload

    monkeypatch.setattr(core, "call_api", call)
    assert cm.get_geometry("SocioMap", "SM1") is payload
    assert cm.explore_geometry("ArchaMap", "AM1", layers=["direct", "related"],
                               relations=["CONTAINS"], max_depth=2, polygon_limit=12) is payload
    cm.get_contextual_policy("ArchaMap")
    cm.validate_contextual_rows(pd.DataFrame([{"CMID": "AM1", "parent": ["AM2"]}]), "ArchaMap")
    assert calls[0][:2] == ("api/geometry", {"database": "sociomap", "cmid": "SM1"})
    assert calls[1][:2] == ("api/databases/archamap/nodes/AM1/explore-geometry",
                            {"layers": "direct,related", "relations": "CONTAINS", "maxDepth": 2, "polygonLimit": 12})
    assert calls[2][0] == "api/databases/archamap/metadata/contextual-policy"
    assert calls[3][1] == {"rows": [{"CMID": "AM1", "parent": ["AM2"]}]}
    assert calls[3][2]["request"] == "POST"


def test_invalid_inputs_do_not_send_requests(monkeypatch, tmp_path):
    monkeypatch.setattr(core, "call_api", lambda *args, **kwargs: pytest.fail("unexpected request"))
    with pytest.raises(cm.CatMapPyError):
        cm.preflight_polygon_upload(tmp_path / "missing.geojson", "SocioMap", api_key="test-key")
    with pytest.raises(cm.CatMapPyError):
        cm.apply_polygon_upload("../bad", api_key="test-key")
    with pytest.raises(cm.CatMapPyError):
        cm.discard_polygon_upload("expired")
    with pytest.raises(cm.CatMapPyError):
        cm.cancel_upload_task("task-1", cursor=-1)
    with pytest.raises(cm.CatMapPyError):
        cm.explore_geometry("ArchaMap", "AM1", polygon_limit=1.5)
    with pytest.raises(cm.CatMapPyError):
        cm.validate_contextual_rows([{}] * 1001, "SocioMap")


@pytest.mark.parametrize("code", [401, 403])
def test_admin_auth_errors_keep_server_response(monkeypatch, code):
    payload = {"error": "Admin role required", "error_details": DETAILS}
    monkeypatch.setattr(core.requests, "post", lambda *args, **kwargs: response(payload, code))
    with pytest.raises(cm.CatMapPyError, match="Not authorized") as exc:
        cm.apply_polygon_upload(TOKEN, api_key="test-key")
    assert exc.value.status_code == code
    assert exc.value.response == payload
