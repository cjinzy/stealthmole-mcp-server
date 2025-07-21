# StealthMole MCP Server

[![smithery badge](https://smithery.ai/badge/@cjinzy/mole-mcp-server)](https://smithery.ai/server/@cjinzy/mole-mcp-server)

An MCP server for StealthMole search that helps with search and analysis across various StealthMole services.

### Version History

##### 1.0.0 (2025-07-18)

- Initial release

### Prerequisites

- StealthMole API Key (Access Key, Secret Key)
- Python 12 or higher
- uv package manager
- Node.js 18 or higher
- NPM 8 or higher
- Docker (optional, for container deployment)

### Tool Details

#### Available Tools

- **search_combo_binder**: CB(Combo Binder) search tool
- **search_compromised_dataset**: CDS(Compromised DataSet) search tool
- **search_credentials**: CL(Credentials Lookout) search tool
- **search_darkweb**: DT(Darkweb Tracker) search tool
- **search_government_monitoring**: GM(Government Monitoring) search tool
- **search_leaked_monitoring**: LM(Leaked Monitoring) search tool
- **search_pagination**: Tool used for searching next pages
- **search_ransomware**: RM(Ransomware Monitoring) search tool
- **search_telegram**: TT(Telegram Tracker) search tool
- **search_ulp_binder**: ULP(ULP Binder) search tool
- **get_compromised_dataset_node**: Retrieves detailed information of CDS nodes
- **get_node_details**: Retrieves detailed information of nodes
- **get_targets**: Retrieves target information of queried nodes
- **get_user_quotas**: Retrieves user's API usage status
- **download_file**: Downloads files
- **export_data**: Exports information of queried nodes by inputting service (cl, cds, cb, ub) and search query. For large datasets, please contact the vendor.

### Installation

#### Automatic Installation via Smithery (Recommended)

For Claude Desktop users:

```bash
npx -y @smithery/cli@latest install @cjinzy/mole-mcp-server --client claude
```

During installation, the following information will be required:

- StealthMole API Access key
- StealthMole API Secret key

#### Manual Configuration for Claude Desktop

```json
{
  "mcpServers": {
    "mole-mcp-server": {
      "command": "npx",
      "args": ["-y", "@smithery/cli@latest", "run", "@cjinzy/mole-mcp-server"],
      "env": {
        "STEALTHMOLE_API_ACCESS_KEY": "your_access_key",
        "STEALTHMOLE_API_SECRET_KEY": "your_secret_key"
      }
    }
  }
}
```

## License

MIT License
