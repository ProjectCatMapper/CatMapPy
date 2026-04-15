from __future__ import annotations

import os
import re
import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests

VALID_DATABASES = {"SocioMap", "ArchaMap"}


class CatMapPyError(ValueError):
    pass


def _validate_string(value: Any, arg: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CatMapPyError(f"`{arg}` must be a non-empty string.")
    return value


def _validate_database(database: str) -> str:
    database = _validate_string(database, "database")
    if database not in VALID_DATABASES:
        raise CatMapPyError("`database` must be one of: SocioMap, ArchaMap.")
    return database


def _validate_bool(value: Any, arg: str) -> bool:
    if not isinstance(value, bool):
        raise CatMapPyError(f"`{arg}` must be True or False.")
    return value


def _resolve_api_url(url: str | None = None) -> str:
    if isinstance(url, str) and url.strip():
        return url
    return os.getenv("CATMAPR_API_URL", "").strip() or "https://api.catmapper.org"


def call_api(
    endpoint: str,
    parameters: dict[str, Any] | None = None,
    request: str = "GET",
    url: str | None = None,
    type: str = "default",
    headers: dict[str, str] | None = None,
) -> Any:
    endpoint = _validate_string(endpoint, "endpoint")
    base_url = _resolve_api_url(url)
    final_url = f"{base_url.rstrip('/')}/{endpoint}"
    request = _validate_string(request, "request").upper()
    type = _validate_string(type, "type")
    if request not in {"GET", "POST"}:
        raise CatMapPyError("`request` must be GET or POST.")
    if type not in {"default", "stream"}:
        raise CatMapPyError("`type` must be default or stream.")

    try:
        if request == "GET":
            response = requests.get(final_url, params=parameters or {}, headers=headers or {}, timeout=120)
        else:
            response = requests.post(final_url, json=parameters or {}, headers=headers or {}, timeout=120)
    except requests.RequestException as exc:
        raise CatMapPyError(f"API request failed: {exc}") from exc

    if not response.ok:
        text = response.text.strip() or f"HTTP {response.status_code}"
        if response.status_code in (401, 403):
            text = (
                "Not authorized: missing or invalid API key/token. "
                f"Server response: {text} See https://help.catmapper.org/API.html"
            )
        raise CatMapPyError(text)

    if type == "stream":
        return response.text
    if not response.text.strip():
        return None
    try:
        return response.json()
    except ValueError:
        return response.text


def _to_df(value: Any) -> pd.DataFrame:
    if value is None:
        return pd.DataFrame()
    if isinstance(value, pd.DataFrame):
        return value
    if isinstance(value, list):
        return pd.DataFrame(value)
    if isinstance(value, dict):
        try:
            return pd.DataFrame(value)
        except ValueError:
            return pd.DataFrame([value])
    return pd.DataFrame({"value": [value]})


def _records(df: Any) -> list[dict[str, Any]]:
    if isinstance(df, pd.DataFrame):
        return df.to_dict(orient="records")
    if isinstance(df, list) and all(isinstance(i, dict) for i in df):
        return df
    raise CatMapPyError("Expected pandas DataFrame or list[dict].")


def _api_key(api_key: str | None = None) -> str:
    if isinstance(api_key, str) and api_key.strip():
        return api_key
    for env in ("CATMAPR_API_KEY", "CATMAPPER_API_KEY"):
        value = os.getenv(env, "").strip()
        if value:
            return value
    raise CatMapPyError("An API key is required for write operations.")


def list_datasets(database: str) -> Any:
    return call_api("allDatasets", {"database": _validate_database(database)})


def allDatasets(database: str) -> Any:
    return list_datasets(database)


def get_cmid_info(database: str, cmid: str) -> Any:
    return call_api(f"CMID/{_validate_database(database)}/{_validate_string(cmid, 'cmid')}", {})


def CMIDinfo(database: str, cmid: str) -> Any:
    return get_cmid_info(database, cmid)


def get_dataset_metadata(database: str, cmid: str, domain: str = "CATEGORY", children: bool | None = None) -> Any:
    if children is not None:
        _validate_bool(children, "children")
    return call_api(
        "dataset",
        {
            "database": _validate_database(database),
            "cmid": _validate_string(cmid, "cmid"),
            "domain": _validate_string(domain, "domain"),
            "children": children,
        },
    )


def datasetInfo(database: str, CMID: str, domain: str = "CATEGORY", children: bool | None = None) -> Any:
    return get_dataset_metadata(database, CMID, domain, children)


def getDatasetMetadata(database: str, CMID: str, domain: str = "CATEGORY", children: bool | None = None) -> Any:
    return get_dataset_metadata(database, CMID, domain, children)


def search_database(
    database: str,
    domain: str | None = None,
    term: str | None = None,
    property: str = "Name",
    yearStart: int | None = None,
    yearEnd: int | None = None,
    country: str | None = None,
    context: str | None = None,
    dataset: str | None = None,
    query: str = "false",
    limit: int = 1000,
) -> Any:
    if limit < 1:
        raise CatMapPyError("`limit` must be a positive number.")
    return call_api(
        "search",
        {
            "database": _validate_database(database),
            "domain": domain,
            "term": term,
            "property": _validate_string(property, "property"),
            "yearStart": yearStart,
            "yearEnd": yearEnd,
            "country": country,
            "context": context,
            "dataset": dataset,
            "query": query,
            "limit": limit,
        },
    )


def translate_rows(
    rows: pd.DataFrame,
    database: str,
    term: str,
    property: str = "Name",
    domain: str = "CATEGORY",
    context: str | None = None,
    country: str | None = None,
    dataset: str | None = None,
    yearStart: int | None = None,
    yearEnd: int | None = None,
    key: str = "false",
    query: str = "false",
    countsamename: bool = False,
    unique_rows: bool = True,
) -> Any:
    _validate_bool(countsamename, "countsamename")
    _validate_bool(unique_rows, "unique_rows")
    if not isinstance(rows, pd.DataFrame):
        raise CatMapPyError("`rows` must be a pandas DataFrame.")
    return call_api(
        "translate",
        {
            "table": rows.to_dict(orient="records"),
            "database": _validate_database(database),
            "term": _validate_string(term, "term"),
            "property": _validate_string(property, "property"),
            "domain": _validate_string(domain, "domain"),
            "context": context,
            "country": country,
            "dataset": dataset,
            "yearStart": yearStart,
            "yearEnd": yearEnd,
            "key": key,
            "query": query,
            "countsamename": countsamename,
            "uniqueRows": unique_rows,
        },
        request="POST",
    )


def join_datasets(database: str, joinLeft: pd.DataFrame, joinRight: pd.DataFrame, domain: str = "CATEGORY") -> Any:
    return call_api(
        "joinDatasets",
        {
            "database": _validate_database(database),
            "joinLeft": _records(joinLeft),
            "joinRight": _records(joinRight),
            "domain": _validate_string(domain, "domain"),
        },
        request="POST",
    )


def propose_merge_links(
    categoryLabel: str,
    datasetChoices: list[str] | str,
    database: str = "SocioMap",
    intersection: bool = False,
    equivalence: str = "standard",
    mergelevel: int = 2,
    resultFormat: str = "key-to-key",
    selectedKeyvariable: dict[str, Any] | None = None,
) -> Any:
    _validate_bool(intersection, "intersection")
    if isinstance(datasetChoices, list):
        datasetChoices = ",".join(datasetChoices)
    return call_api(
        "proposeMergeSubmit",
        {
            "database": _validate_database(database),
            "datasetChoices": _validate_string(datasetChoices, "datasetChoices"),
            "categoryLabel": _validate_string(categoryLabel, "categoryLabel"),
            "intersection": intersection,
            "mergelevel": mergelevel,
            "equivalence": equivalence,
            "resultFormat": resultFormat,
            "selectedKeyvariable": selectedKeyvariable or {},
        },
        request="POST",
    )


def createLinkfile(*args: Any, **kwargs: Any) -> Any:
    return propose_merge_links(*args, **kwargs)


def get_domains(database: str = "SocioMap", advanced: bool = False) -> pd.DataFrame:
    _validate_bool(advanced, "advanced")
    out = _to_df(call_api("getTranslatedomains", {"database": _validate_database(database)}))
    for col in ("domain", "subdomain", "description"):
        if col not in out.columns:
            out[col] = pd.NA
    return out if advanced else out[["domain", "subdomain", "description"]]


def getDomains(database: str = "SocioMap", advanced: bool = False) -> pd.DataFrame:
    return get_domains(database, advanced)


def get_properties(database: str = "SocioMap", url: str | None = None) -> pd.DataFrame:
    out = call_api(f"metadata/properties/{_validate_database(database).lower()}", {}, url=url)
    out_df = _to_df(out.get("table") if isinstance(out, dict) else out)
    for col in ("nodeID", "CMName", "property", "value"):
        if col not in out_df.columns:
            out_df[col] = pd.NA
    return out_df


def get_upload_properties(database: str = "SocioMap", url: str | None = None) -> dict[str, Any]:
    out = call_api(f"metadata/uploadProperties/{_validate_database(database).lower()}", {}, url=url)
    out = out if isinstance(out, dict) else {}
    return {
        "database": str(out.get("database", database)),
        "nodeProperties": _to_df(out.get("nodeProperties")),
        "usesProperties": _to_df(out.get("usesProperties")),
    }


def get_merge_template(database: str, dataset_id: str, url: str | None = None) -> Any:
    return call_api(f"merge/template/{_validate_database(database)}/{_validate_string(dataset_id, 'dataset_id')}", {}, url=url)


def get_merge_template_summary(database: str, cmid: str, url: str | None = None) -> Any:
    return call_api(f"merge/template/summary/{_validate_database(database)}/{_validate_string(cmid, 'cmid')}", {}, url=url)


def getMergingTemplate(cmid: str, database: str = "SocioMap", url: str | None = None) -> pd.DataFrame:
    return _to_df(call_api(f"merge/template/{_validate_database(database).lower()}/{_validate_string(cmid, 'cmid')}", {}, url=url))


def getMergingTemplateSummary(cmid: str, database: str = "SocioMap", url: str | None = None) -> dict[str, Any]:
    out = call_api(f"merge/template/summary/{_validate_database(database).lower()}/{_validate_string(cmid, 'cmid')}", {}, url=url)
    out = out if isinstance(out, dict) else {}
    for key in ("stackSummary", "datasetSummary", "mergingTies", "equivalenceTies"):
        out[key] = _to_df(out.get(key))
    return out


def findMergingTemplate(cmid: str, database: str = "SocioMap", url: str | None = None) -> dict[str, Any]:
    summary = getMergingTemplateSummary(cmid=cmid, database=database, url=url)
    template = getMergingTemplate(cmid=cmid, database=database, url=url)
    node_type = str(summary.get("nodeType", "")).upper()
    variable_count = float((summary.get("stackSummaryTotals") or {}).get("variableCount", 0) or 0)
    eq_count = len(summary.get("equivalenceTies", pd.DataFrame()))
    status = {
        "nodeType": node_type,
        "isMergingTemplate": node_type == "MERGING",
        "hasVariableMappings": variable_count > 0,
        "canDownloadLinkFile": node_type == "MERGING" and eq_count > 0,
        "variableCount": variable_count,
        "equivalenceTieCount": eq_count,
    }
    return {"cmid": cmid, "database": database, "status": status, "summary": summary, "template": template}


def downloadMergingTemplateWorkbook(cmid: str, database: str = "SocioMap", path: str | None = None, overwrite: bool = False, url: str | None = None) -> dict[str, Any]:
    _validate_bool(overwrite, "overwrite")
    template = getMergingTemplate(cmid=cmid, database=database, url=url)
    out = Path(path or f"merging_template_{cmid}.xlsx").resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and not overwrite:
        raise CatMapPyError(f"File already exists: {out}")
    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        template.to_excel(writer, sheet_name="MergingTemplate", index=False)
    return {"path": str(out), "template": template}


def downloadLinkFileWorkbook(cmid: str, database: str = "SocioMap", path: str | None = None, overwrite: bool = False, url: str | None = None) -> dict[str, Any]:
    _validate_bool(overwrite, "overwrite")
    result = findMergingTemplate(cmid=cmid, database=database, url=url)
    if not result["status"]["isMergingTemplate"]:
        raise CatMapPyError(f"\"{cmid}\" is not a merging template.")
    if result["status"]["hasVariableMappings"]:
        raise CatMapPyError(f"Merging template \"{cmid}\" has variable mappings. Download the merge template workbook instead.")
    if not result["status"]["canDownloadLinkFile"]:
        raise CatMapPyError(f"Merging template \"{cmid}\" has no equivalence ties to build a link file.")
    out = Path(path or f"link_file_{cmid}.xlsx").resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and not overwrite:
        raise CatMapPyError(f"File already exists: {out}")
    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        _to_df(result["summary"].get("equivalenceTies")).to_excel(writer, sheet_name="LinkFileLong", index=False)
        _to_df(result["template"]).to_excel(writer, sheet_name="LinkFileWide", index=False)
    return {"path": str(out), "status": result["status"]}


def build_merge_syntax(template: Any, database: str, url: str | None = None) -> Any:
    return call_api(f"merge/syntax/{_validate_database(database)}", {"template": _records(template)}, request="POST", url=url)


def generateMergeFiles(template: Any, database: str = "SocioMap", download_zip: bool = True, zip_path: str | None = None, overwrite: bool = False, url: str | None = None) -> dict[str, Any]:
    _validate_bool(download_zip, "download_zip")
    _validate_bool(overwrite, "overwrite")
    rows = _records(template)
    response = call_api(f"merge/syntax/{_validate_database(database)}", {"template": rows}, request="POST", url=url)
    out: dict[str, Any] = {"response": response, "template": pd.DataFrame(rows)}
    hash_id = (response.get("download") or {}).get("hash") if isinstance(response, dict) else None
    if download_zip and hash_id:
        out["zip_path"] = downloadMergeZip(hash_id=hash_id, path=zip_path, overwrite=overwrite, url=url)
    return out


def downloadMergeZip(hash_id: str, path: str | None = None, overwrite: bool = False, url: str | None = None) -> str:
    _validate_bool(overwrite, "overwrite")
    out = Path(path or f"merged_output_{_validate_string(hash_id, 'hash_id')}.zip").resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and not overwrite:
        raise CatMapPyError(f"File already exists: {out}")
    response = requests.get(f"{_resolve_api_url(url).rstrip('/')}/download/zip/{hash_id}", timeout=120)
    if not response.ok:
        raise CatMapPyError(response.text.strip() or f"HTTP {response.status_code}")
    out.write_bytes(response.content)
    return str(out)


def build_key(field: str | list[str], value: str | list[str]) -> list[str]:
    fields = [field] if isinstance(field, str) else list(field)
    values = [value] if isinstance(value, str) else list(value)
    if len(fields) == 0 or len(values) == 0:
        return []
    if len(fields) != len(values):
        if len(fields) == 1:
            fields *= len(values)
        elif len(values) == 1:
            values *= len(fields)
        else:
            raise CatMapPyError("`field` and `value` must have the same length or length 1.")
    return [f"{str(f).strip()} == {str(v).strip()}" for f, v in zip(fields, values)]


def build_key_from_columns(data: pd.DataFrame, columns: list[str], key_column: str = "Key", drop_source: bool = False) -> pd.DataFrame:
    _validate_bool(drop_source, "drop_source")
    if not isinstance(data, pd.DataFrame):
        raise CatMapPyError("`data` must be a pandas DataFrame.")
    if not columns:
        raise CatMapPyError("`columns` must be a non-empty character vector.")
    _validate_string(key_column, "key_column")
    missing = [c for c in columns if c not in data.columns]
    if missing:
        raise CatMapPyError(f"Source key column(s) not found in `data`: {', '.join(missing)}.")
    out = data.copy()
    keys = []
    bad_rows = []
    for i, row in out.iterrows():
        parts: list[str] = []
        for col in columns:
            raw = row[col]
            text = "" if pd.isna(raw) else str(raw).strip()
            if text:
                parts.append(f"{col} == {text}")
        key = " && ".join(parts)
        if not key:
            bad_rows.append(i + 1)
        keys.append(key)
    if bad_rows:
        raise CatMapPyError(f"Cannot build Key values for row(s) with empty source values across selected columns: {', '.join(map(str, bad_rows))}.")
    out[key_column] = keys
    return out.drop(columns=columns) if drop_source else out


def normalize_key(key: str | list[str]) -> list[str]:
    values = [key] if isinstance(key, str) else list(key)
    output = []
    for value in values:
        text = re.sub(r"^\s*Key\s*==\s*", "", str(value).strip())
        segments = [s.strip() for s in re.split(r"\s*&&\s*", text) if s.strip()]
        normalized = []
        for seg in segments:
            if "==" in seg:
                left, right = seg.split("==", 1)
                normalized.append(f"{left.strip()} == {right.strip()}")
            else:
                normalized.append(seg)
        output.append(" && ".join(normalized))
    return output


def is_normalized_key(key: str | list[str]) -> list[bool]:
    values = [key] if isinstance(key, str) else list(key)
    normalized = normalize_key(values)
    pattern = re.compile(r"^.+?\s==\s.+?(?:\s&&\s.+?\s==\s.+?)*$")
    return [n == str(v) and bool(pattern.match(n)) for v, n in zip(values, normalized)]


def prepare_upload_rows(df: Any, form_data: dict[str, Any] | None = None, action: str = "add_node", properties: list[str] | None = None, merging_type: str = "0", database: str = "SocioMap") -> dict[str, Any]:
    return {
        "database": _validate_database(database),
        "form_data": form_data or {},
        "action": _validate_string(action, "action"),
        "properties": properties or [],
        "merging_type": _validate_string(merging_type, "merging_type"),
        "rows": _records(df),
    }


def uploadInputNodes(df: Any, database: str, formData: dict[str, Any] | None = None, so: str = "standard", ao: str = "add_node", addoptions: dict[str, Any] | None = None, allContext: list[str] | None = None, mergingType: str = "0", api_key: str | None = None, url: str | None = None) -> Any:
    return call_api(
        "uploadInputNodes",
        {
            "formData": formData or {},
            "database": _validate_database(database),
            "df": _records(df),
            "so": _validate_string(so, "so"),
            "ao": _validate_string(ao, "ao"),
            "addoptions": {"district": bool((addoptions or {}).get("district")), "recordyear": bool((addoptions or {}).get("recordyear"))},
            "allContext": allContext or [],
            "mergingType": _validate_string(mergingType, "mergingType"),
        },
        request="POST",
        url=url,
        headers={"X-API-Key": _api_key(api_key)},
    )


def updateWaitingUSES(database: str, api_key: str | None = None, url: str | None = None) -> Any:
    return call_api("updateWaitingUSES", {"database": _validate_database(database)}, request="POST", url=url, headers={"X-API-Key": _api_key(api_key)})


def uploadInputNodesStatus(task_id: str, cursor: int = 0, api_key: str | None = None, url: str | None = None) -> Any:
    if cursor < 0:
        raise CatMapPyError("`cursor` must be a non-negative number.")
    return call_api("uploadInputNodesStatus", {"taskId": _validate_string(task_id, "task_id"), "cursor": int(cursor)}, request="POST", url=url, headers={"X-API-Key": _api_key(api_key)})


def waitForUploadTask(task_id: str, poll_seconds: float = 2, timeout_seconds: float = 600, cursor: int = 0, api_key: str | None = None, url: str | None = None, quiet: bool = True) -> Any:
    _validate_bool(quiet, "quiet")
    start = time.time()
    next_cursor = int(cursor)
    while True:
        status = uploadInputNodesStatus(task_id=task_id, cursor=next_cursor, api_key=api_key, url=url)
        if isinstance(status, dict):
            if not quiet:
                for event in status.get("events", []):
                    print(f"[{task_id}] {event}")
            next_cursor = int(status.get("nextCursor", next_cursor))
            state = str(status.get("status", "")).lower()
            if state == "completed":
                return status
            if state == "failed":
                raise CatMapPyError(str(status.get("error", "Upload task failed.")))
            if state == "canceled":
                raise CatMapPyError(str(status.get("message", "Upload task was canceled.")))
        if time.time() - start > timeout_seconds:
            raise CatMapPyError(f"Timed out waiting for upload task {task_id} after {timeout_seconds:.1f} seconds.")
        time.sleep(poll_seconds)


def submitEditUpload(df: Any, database: str, formData: dict[str, Any] | None = None, so: str = "standard", ao: str = "add_node", addoptions: dict[str, Any] | None = None, allContext: list[str] | None = None, mergingType: str = "0", api_key: str | None = None, refresh_waiting_uses: bool = True, url: str | None = None) -> dict[str, Any]:
    _validate_bool(refresh_waiting_uses, "refresh_waiting_uses")
    upload = uploadInputNodes(df=df, database=database, formData=formData, so=so, ao=ao, addoptions=addoptions, allContext=allContext, mergingType=mergingType, api_key=api_key, url=url)
    waiting_uses = updateWaitingUSES(database=database, api_key=api_key, url=url) if refresh_waiting_uses else None
    return {"upload": upload, "waiting_uses": waiting_uses}


def upload_rows(df: Any, database: str, form_data: dict[str, Any] | None = None, action: str = "add_node", add_options: dict[str, Any] | None = None, properties: list[str] | None = None, merging_type: str = "0", api_key: str | None = None, poll_interval_seconds: float = 1, timeout_seconds: float = 600, url: str | None = None) -> pd.DataFrame:
    prepared = prepare_upload_rows(df=df, form_data=form_data, action=action, properties=properties, merging_type=merging_type, database=database)
    start = call_api(
        "uploadInputNodes",
        {
            "formData": prepared["form_data"],
            "database": prepared["database"],
            "df": prepared["rows"],
            "so": "standard",
            "ao": prepared["action"],
            "addoptions": {"district": bool((add_options or {}).get("district")), "recordyear": bool((add_options or {}).get("recordyear"))},
            "optionalProperties": prepared["properties"],
            "mergingType": prepared["merging_type"],
        },
        request="POST",
        url=url,
        headers={"X-API-Key": _api_key(api_key)},
    )
    task_id = str((start or {}).get("taskId", "")) if isinstance(start, dict) else ""
    if not task_id:
        raise CatMapPyError("Upload start response did not include `taskId`; cannot poll task completion.")
    start_time = time.time()
    cursor = 0
    status: dict[str, Any] = {}
    while True:
        status = call_api("uploadInputNodesStatus", {"taskId": task_id, "cursor": cursor}, request="POST", url=url, headers={"X-API-Key": _api_key(api_key)})
        if isinstance(status, dict):
            cursor = int(status.get("nextCursor", cursor))
            state = str(status.get("status", "")).lower()
            if state == "completed":
                break
            if state in {"failed", "canceled"}:
                raise CatMapPyError(f"Upload task `{task_id}` ended with status `{state}`: {status.get('error') or status.get('message')}")
        if time.time() - start_time >= timeout_seconds:
            raise CatMapPyError(f"Timed out waiting for upload task `{task_id}` after {timeout_seconds:.0f} seconds.")
        time.sleep(poll_interval_seconds)
    try:
        call_api("updateWaitingUSES", {"database": prepared["database"]}, request="POST", url=url)
    except Exception:
        pass
    table = None
    if isinstance(status, dict):
        table = status.get("file") or status.get("resultFile") or status.get("data") or status.get("rows") or status.get("result")
    out = _to_df(table)
    order = status.get("order") if isinstance(status, dict) else None
    if isinstance(order, list):
        selected = [c for c in order if c in out.columns]
        out = out[selected + [c for c in out.columns if c not in selected]]
    out.attrs["upload_task"] = status
    return out
