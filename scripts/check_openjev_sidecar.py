#!/usr/bin/env python3
"""Dependency-free live smoke for a running OpenJev helper."""
from __future__ import annotations
import argparse, json, os, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from hermes_jev.reflex.openjev import OpenJevClient

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--base-url',default=os.getenv('HERMES_REFLEX_OPENJEV_BASE_URL','http://127.0.0.1:3000'))
    p.add_argument('--token',default=os.getenv('HERMES_REFLEX_OPENJEV_TOKEN',''))
    p.add_argument('--expected-identity',default=os.getenv('HERMES_REFLEX_OPENJEV_EXPECTED_IDENTITY',''))
    p.add_argument('--timeout',type=float,default=10.0)
    a=p.parse_args()
    c=OpenJevClient(base_url=a.base_url,token=a.token or None,expected_identity=a.expected_identity or None,timeout=a.timeout)
    version=c.version()
    r=c.system_one(state={'message':'duplicate charge; please refund today'},questions={
        'route':{'type':'choice','instructions':'Which team?','criteria':{'billing':'charges/refunds','technical':'bugs'}},
        'urgent':{'type':'noul','instructions':'Does this need prompt handling?'}
    })
    assert r.provider=='OpenJev' and r.transport=='openjev-local-http' and not r.live_provider_call
    assert set(r.answers)=={'route','urgent'}
    print(json.dumps({'ok':True,'provider':r.provider,'model':r.model,'version':version,'usage':r.usage,'latency_ms':round(r.latency_ms,3)},sort_keys=True,default=str))
    return 0
if __name__=='__main__': raise SystemExit(main())
