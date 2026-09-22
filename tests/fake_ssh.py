#!/usr/bin/env python3
import json, os, sys, time

mode = os.getenv("FAKE_SSH_MODE", "success")
log = os.getenv("FAKE_SSH_LOG", "")
if log:
    with open(log, "w", encoding="utf-8") as h:
        json.dump({"argv": sys.argv[1:]}, h)
task = sys.stdin.read()
if log:
    with open(log + ".stdin", "w", encoding="utf-8") as h:
        h.write(task)
if mode == "sleep":
    print(json.dumps({"type":"system","subtype":"init","session_id":"fake-session"}), flush=True)
    time.sleep(60)
    raise SystemExit(0)
if mode == "rate_limit":
    print(json.dumps({"type":"system","subtype":"init","session_id":"fake-session"}), flush=True)
    print(json.dumps({"type":"result","session_id":"fake-session","exit_code":75,"text":"rate limited","tokens":{"total_tokens":10}}), flush=True)
    raise SystemExit(75)
print(json.dumps({"type":"system","subtype":"init","session_id":"fake-session"}), flush=True)
print(json.dumps({"type":"tool_use","name":"terminal","input":{"command":"pytest -q"}}), flush=True)
print(json.dumps({"type":"tool_result","name":"terminal","output":"3 passed","is_error":False}), flush=True)
print(json.dumps({"type":"result","session_id":"fake-session","exit_code":0,"text":"REMOTE_OK","tokens":{"input_tokens":100,"output_tokens":20,"total_tokens":120},"duration_ms":12}), flush=True)
