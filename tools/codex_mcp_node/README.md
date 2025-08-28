Codex MCP Node Server

Overview
- Exposes workspace-scoped tools over Model Context Protocol (MCP) so MCP clients can interact with this repo similarly to Codex CLI: read/write files, list/search, and run commands with an allowlist.

Tools
- read_file: Read a UTF-8 text file at a path relative to workspace root.
- write_file: Write/overwrite a UTF-8 text file; creates parent folders.
- list_files: Recursively list files with basic ignores and optional limit.
- search: Simple substring search across text files with limits and ignores.
- run: Execute an allowed command in the workspace with timeouts and size limits.

Workspace Scoping
- Root is resolved from env `CODEX_MCP_ROOT`; defaults to `process.cwd()`.
- All paths are resolved safely under the root. Requests outside the root are rejected.

Install
1) Node.js 18+.
2) From repo root:
   - cd tools/codex_mcp_node
   - npm install

Run (direct)
- node src/server.js

MCP Client Config (example)
Add to your MCP client configuration:

{
  "mcpServers": {
    "codex-mcp-node": {
      "command": "node",
      "args": ["tools/codex_mcp_node/src/server.js"],
      "env": {
        "CODEX_MCP_ROOT": "${workspaceRoot}",
        "CODEX_MCP_RUN_ALLOW": "rg,pytest,python,uvicorn,node"
      }
    }
  }
}

Environment Variables
- CODEX_MCP_ROOT: Absolute path to workspace root. Defaults to current working directory.
- CODEX_MCP_RUN_ALLOW: Comma-separated command allowlist for `run` (default: empty/none).
- CODEX_MCP_RUN_TIMEOUT_MS: Default run timeout in ms (default: 30000).
- CODEX_MCP_RUN_MAX_BYTES: Max stdout/stderr bytes to capture (default: 200000).

Security Notes
- The server enforces path sandboxing under the workspace root.
- `run` is disabled unless the command is explicitly allowlisted.
- This server does not read environment secrets or make network calls.

Limitations
- `search` is a naive substring scan and may skip large/binary files.
- `apply_patch` is not implemented; use `write_file`/`read_file` or request it to be added.

