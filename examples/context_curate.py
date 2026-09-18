"""v0.1.5.5 context-governor example. Requires the credential for the selected HERMES_JEV_PROVIDER."""

from hermes_jev.context import curate_context

result = curate_context(
    goal="Fix the failing test without changing generated code.",
    items=[
        {"id": "constraint", "kind": "user_text", "content": "Never edit src/generated."},
        {
            "id": "old-read",
            "kind": "tool_result",
            "content": "old source listing ...",
            "recoverable": True,
            "metadata": {"tool_name": "read_file"},
        },
        {
            "id": "failure",
            "kind": "tool_result",
            "content": "AssertionError at tests/test_x.py:42",
            "recoverable": False,
        },
    ],
    preserve_tail=0,
    mode="shadow",  # inspect proposed_action before enabling apply mode
    contract="context-curation/v2",
)
print(result)
