## Summary

Describe the change and why it is needed.

## Scope

- [ ] This PR is narrowly scoped.
- [ ] Public tool/hook/provider behavior changes are documented.
- [ ] No secrets, credentials, or private traces are included.

## Verification

List the exact commands run and their results.

```text
python -m unittest discover -s tests -v
python -m compileall -q .
python scripts/verify_release.py
```

## Provider / live testing

- [ ] Not applicable
- [ ] Offline/wire-contract only
- [ ] Live provider tested with synthetic state only

If live-tested, identify provider/transport/version and sanitize all IDs or errors as appropriate. Never paste credentials.

## AI assistance

If AI substantially assisted with implementation, review, test generation, or the PR text, disclose it here and state what was independently verified.
