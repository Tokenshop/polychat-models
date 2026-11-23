#!/usr/bin/env python3
"""Validate models.json before it reaches the app. Run: python3 validate.py"""
import json, re, sys

REQUIRED = {
    "id": str, "name": str, "params": str, "quant": str, "repo": str, "revision": str,
    "sizeBytes": int, "architecture": str, "capabilities": list, "tags": list,
    "description": str, "license": str, "minRamGB": (int, float), "minAppVersion": str, "pro": bool,
}
CAPABILITIES = {"text", "vision", "audio", "reasoning"}
errors = []

def err(msg):
    errors.append(msg)

with open("models.json") as f:
    data = json.load(f)

if data.get("schemaVersion") != 1:
    err("schemaVersion must be 1")
models = data.get("models")
if not isinstance(models, list) or not models:
    err("models must be a non-empty list")
    models = []
ids = set()
for i, m in enumerate(models):
    where = f"models[{i}] ({m.get('id', '?')})"
    for key, typ in REQUIRED.items():
        if key not in m:
            err(f"{where}: missing '{key}'")
        elif not isinstance(m[key], typ) or (typ is int and isinstance(m[key], bool)):
            err(f"{where}: '{key}' has the wrong type")
    if m.get("id") in ids:
        err(f"{where}: duplicate id")
    ids.add(m.get("id"))
    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]*", str(m.get("id", ""))):
        err(f"{where}: id must be lowercase letters, digits, '.', '_' or '-'")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", str(m.get("repo", ""))):
        err(f"{where}: repo must look like 'owner/name'")
    if not re.fullmatch(r"[0-9a-f]{40}", str(m.get("revision", ""))):
        err(f"{where}: revision must be a full 40-character commit hash (pin the exact files)")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(m.get("minAppVersion", ""))):
        err(f"{where}: minAppVersion must look like 1.1.0")
    bad = set(m.get("capabilities", [])) - CAPABILITIES
    if bad:
        err(f"{where}: unknown capabilities {sorted(bad)}")
    if "text" not in m.get("capabilities", []):
        err(f"{where}: every model needs the 'text' capability")
    if "vendor" in m and not re.fullmatch(r"[a-z0-9-]+", str(m["vendor"])):
        err(f"{where}: vendor must be lowercase letters/digits (e.g. qwen, gemma, llama)")
    if isinstance(m.get("sizeBytes"), int) and m["sizeBytes"] <= 0:
        err(f"{where}: sizeBytes must be positive")

if data.get("defaultModelId") not in ids:
    err("defaultModelId must be the id of a model in the list")

if errors:
    print("models.json is NOT valid:\n  - " + "\n  - ".join(errors))
    sys.exit(1)
print(f"models.json is valid: {len(models)} models, default '{data['defaultModelId']}'.")
