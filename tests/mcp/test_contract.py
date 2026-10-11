"""Contract test: the public tool surface must only change on purpose.

Clients and prompts depend on tool names, arguments and the envelope. If this
test fails after an intended change, review the diff and refresh the baseline:

    UPDATE_MCP_CONTRACT=1 pytest tests/mcp/test_contract.py
"""

import json
import os
from pathlib import Path

import pytest

BASELINE = Path(__file__).parent / "baseline" / "tool_contracts.json"


def describe(tool) -> dict:
    """Reduce a tool to the parts of its contract that callers rely on."""
    schema = tool.input_schema
    return {
        "name": tool.name,
        "title": tool.annotations.title,
        "read_only": tool.annotations.read_only_hint,
        "required": sorted(schema.get("required", [])),
        "parameters": {
            name: {k: v for k, v in sorted(spec.items()) if k != "description"}
            for name, spec in sorted(schema.get("properties", {}).items())
        },
        "result": sorted(tool.output_schema.get("properties", {})),
    }


@pytest.mark.asyncio
async def test_tool_contract_matches_baseline(mcp_client):
    """Test tool names, arguments and result shape match the recorded contract."""
    tools = sorted(await mcp_client.list_tools(), key=lambda t: t.name)
    contract = {"tools": [describe(t) for t in tools]}

    if os.environ.get("UPDATE_MCP_CONTRACT"):
        BASELINE.write_text(json.dumps(contract, indent=2) + "\n")

    assert contract == json.loads(BASELINE.read_text())


@pytest.mark.asyncio
async def test_no_debug_tools_are_exposed(mcp_client):
    """Test the public server offers only data tools."""
    names = {t.name for t in await mcp_client.list_tools()}
    assert not {n for n in names if n.startswith("debug") or "cache" in n}


@pytest.mark.asyncio
async def test_every_tool_is_marked_read_only(mcp_client):
    """Test clients can tell that no tool changes anything."""
    for tool in await mcp_client.list_tools():
        assert tool.annotations.read_only_hint is True, tool.name
