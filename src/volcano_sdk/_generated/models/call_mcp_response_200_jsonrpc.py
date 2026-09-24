from typing import Literal

CallMCPResponse200Jsonrpc = Literal['2.0']

CALL_MCP_RESPONSE_200_JSONRPC_VALUES: set[CallMCPResponse200Jsonrpc] = { '2.0',  }

def check_call_mcp_response_200_jsonrpc(value: str) -> CallMCPResponse200Jsonrpc:
    if value in CALL_MCP_RESPONSE_200_JSONRPC_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CALL_MCP_RESPONSE_200_JSONRPC_VALUES!r}")
