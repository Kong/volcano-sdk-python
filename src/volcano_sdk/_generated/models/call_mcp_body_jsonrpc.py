from typing import Literal

CallMCPBodyJsonrpc = Literal['2.0']

CALL_MCP_BODY_JSONRPC_VALUES: set[CallMCPBodyJsonrpc] = { '2.0',  }

def check_call_mcp_body_jsonrpc(value: str) -> CallMCPBodyJsonrpc:
    if value in CALL_MCP_BODY_JSONRPC_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CALL_MCP_BODY_JSONRPC_VALUES!r}")
