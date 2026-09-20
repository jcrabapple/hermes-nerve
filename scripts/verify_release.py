#!/usr/bin/env python3
"""Offline source checks for Hermes-Jev v0.2.2.dev4."""
from __future__ import annotations

import csv
import importlib.util
import sys
try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "0.2.2.dev4"


class FakeCtx:
    def __init__(self):
        self.tools = []
        self.hooks = []
        self.engine = None
        self.schemas = {}

    def get_config(self, key, default=None):
        return default

    def register_tool(self, *, name, schema=None, **kwargs):
        self.tools.append(name)
        self.schemas[name] = schema

    def register_hook(self, name, callback):
        self.hooks.append(name)

    def register_context_engine(self, engine):
        self.engine = engine


def main():
    manifest = yaml.safe_load((ROOT / "plugin.yaml").read_text())
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    catalog = yaml.safe_load((ROOT / "packaging/hermes-catalog/jev.yaml").read_text())

    spec = importlib.util.spec_from_file_location(
        "hermes_jev_plugin_root", ROOT / "__init__.py", submodule_search_locations=[str(ROOT)]
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    ctx = FakeCtx()
    module.register(ctx)

    assert manifest["version"] == EXPECTED_VERSION
    assert pyproject["project"]["version"] == EXPECTED_VERSION
    catalog_version = str(catalog["version"])
    if ".dev" in EXPECTED_VERSION:
        assert ".dev" not in catalog_version, (catalog_version, "catalog entries must remain stable releases")
        assert catalog_version != EXPECTED_VERSION, (catalog_version, "development builds must not publish themselves to the catalog")
    else:
        assert catalog_version == EXPECTED_VERSION
    assert module.VERSION == EXPECTED_VERSION
    assert set(ctx.tools) == set(manifest["provides_tools"]), (ctx.tools, manifest["provides_tools"])
    assert set(ctx.hooks) == set(manifest["provides_hooks"]), (ctx.hooks, manifest["provides_hooks"])
    assert ctx.engine is not None

    assess = ctx.schemas["jev_assess"]["parameters"]["properties"]["questions"]["additionalProperties"]
    variants = assess["oneOf"]
    by_type = {item["properties"]["type"]["enum"][0]: item for item in variants}
    assert by_type["choice"]["properties"]["criteria"]["minProperties"] == 2
    assert by_type["score"]["properties"]["criteria"]["minItems"] == 2
    assert "criteria" not in by_type["noul"]["required"]

    trace = ROOT / "planning/vnext-1119/IMPLEMENTATION_TRACE_1119.csv"
    with trace.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    ids = [int(r["point_id"]) for r in rows]
    assert ids == list(range(1, 1120))
    assert len({r["verification_id"] for r in rows}) == 1119
    assert all(r["implementation_status"] for r in rows)

    print(
        f"PASS version={EXPECTED_VERSION} tools={len(set(ctx.tools))} "
        f"hook_names={len(set(ctx.hooks))} hook_callbacks={len(ctx.hooks)} requirements={len(rows)} "
        f"catalog_version={catalog_version}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
