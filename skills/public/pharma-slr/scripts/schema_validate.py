#!/usr/bin/env python3
"""Small dependency-free JSON Schema validator for pharma-slr artifacts.

This intentionally supports the subset used by the local schemas: required,
properties, type, enum, items, minimum, and additionalProperties=false.
It is not a full JSON Schema Draft 2020-12 implementation.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


TYPE_MAP = {
    "object": dict,
    "array": list,
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "null": type(None),
}


def _type_ok(value: Any, expected: str | list[str]) -> bool:
    expected_types = expected if isinstance(expected, list) else [expected]
    for item in expected_types:
        py_type = TYPE_MAP.get(item)
        if py_type and isinstance(value, py_type):
            if item == "integer" and isinstance(value, bool):
                continue
            return True
    return False


def validate_instance(instance: Any, schema: dict, path: str = "$") -> list[str]:
    errors: list[str] = []
    expected_type = schema.get("type")
    if expected_type and not _type_ok(instance, expected_type):
        errors.append(f"{path}: expected type {expected_type}, got {type(instance).__name__}")
        return errors

    enum = schema.get("enum")
    if enum is not None and instance not in enum:
        errors.append(f"{path}: value {instance!r} not in enum {enum}")

    if isinstance(instance, (int, float)) and "minimum" in schema and instance < schema["minimum"]:
        errors.append(f"{path}: value {instance} below minimum {schema['minimum']}")

    if isinstance(instance, dict):
        for field in schema.get("required", []):
            if field not in instance:
                errors.append(f"{path}.{field}: missing required field")
        properties = schema.get("properties", {})
        for field, value in instance.items():
            if field in properties:
                errors.extend(validate_instance(value, properties[field], f"{path}.{field}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}.{field}: additional property not allowed")

    if isinstance(instance, list) and "items" in schema:
        for index, item in enumerate(instance):
            errors.extend(validate_instance(item, schema["items"], f"{path}[{index}]"))

    return errors


def validate_payload(payload: Any, schema: dict, items_key: str | None = None) -> dict:
    if items_key:
        if not isinstance(payload, dict):
            return {"valid": False, "errors": [f"$: --items-key {items_key!r} requires a JSON object payload"]}
        if items_key not in payload:
            return {"valid": False, "errors": [f"$.{items_key}: items key not found"]}
        payload = payload[items_key]
        if not isinstance(payload, list):
            return {"valid": False, "errors": [f"$.{items_key}: expected array, got {type(payload).__name__}"]}

    if isinstance(payload, list):
        item_schema = schema.get("items") or schema
        errors = []
        for index, item in enumerate(payload):
            errors.extend(validate_instance(item, item_schema, f"$[{index}]"))
    else:
        errors = validate_instance(payload, schema)
    return {"valid": not errors, "errors": errors}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate JSON against a local pharma-slr schema subset.")
    parser.add_argument("--schema", required=True)
    parser.add_argument("--json", required=True)
    parser.add_argument("--items-key", help="optional object key containing an array of records to validate with the schema")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
        payload = json.loads(Path(args.json).read_text(encoding="utf-8"))
        result = validate_payload(payload, schema, args.items_key)
    except Exception as exc:
        print(f"schema_validate.py: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if result["valid"] else 2


if __name__ == "__main__":
    sys.exit(main())
