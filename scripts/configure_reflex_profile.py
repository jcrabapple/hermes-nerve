#!/usr/bin/env python3
"""Patch one Hermes profile's hermes-nerve Reflex settings reproducibly."""
from __future__ import annotations
import argparse, os
from pathlib import Path
try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required for this operator script (run with the Hermes venv Python)") from exc


def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument('profile')
    p.add_argument('--backend',choices=['jev','laya','openjev','shadow'],required=True)
    p.add_argument('--shadow-backend',choices=['laya','openjev'],default='laya')
    p.add_argument('--laya-base-url',default=os.getenv('HERMES_REFLEX_LAYA_BASE_URL','http://127.0.0.1:8765'))
    p.add_argument('--laya-model',default=os.getenv('HERMES_REFLEX_LAYA_MODEL','convaiinnovations/laya-typed-decisions'))
    p.add_argument('--openjev-base-url',default=os.getenv('HERMES_REFLEX_OPENJEV_BASE_URL','http://127.0.0.1:3000'))
    p.add_argument('--openjev-model',default=os.getenv('HERMES_REFLEX_OPENJEV_MODEL','openjev'))
    p.add_argument('--openjev-expected-identity',default=os.getenv('HERMES_REFLEX_OPENJEV_EXPECTED_IDENTITY',''))
    p.add_argument('--shadow-sync',action='store_true',help='Make shadow calls synchronous for benchmark reproducibility')
    p.add_argument('--orchestrator-reviewer',default=os.getenv('HERMES_NERVE_ORCHESTRATOR_REVIEWER',''),help='Profile that owns final Nerve budget review authority')
    a=p.parse_args()
    home=Path(os.environ.get('HERMES_HOME') or Path.home()/'.hermes')
    path=home/'profiles'/a.profile/'config.yaml'
    if not path.exists(): raise SystemExit(f"profile config not found: {path}")
    data=yaml.safe_load(path.read_text()) or {}
    plugins=data.setdefault('plugins',{})
    entries=plugins.setdefault('entries',{})
    entry=entries.setdefault('nerve',{})
    settings=entry.setdefault('settings',{})
    settings.update({
        'reflex_backend':a.backend,
        'reflex_shadow_backend':a.shadow_backend,
        'reflex_laya_base_url':a.laya_base_url,
        'reflex_laya_model':a.laya_model,
        'reflex_openjev_base_url':a.openjev_base_url,
        'reflex_openjev_model':a.openjev_model,
        'reflex_openjev_expected_identity':a.openjev_expected_identity,
        'reflex_shadow_async':not a.shadow_sync,
        'work_reviewer':a.orchestrator_reviewer or settings.get('work_reviewer',''),
    })
    path.write_text(yaml.safe_dump(data,sort_keys=False))
    print(f"configured profile={a.profile} backend={a.backend} shadow_backend={a.shadow_backend} path={path}")
    return 0
if __name__=='__main__': raise SystemExit(main())
