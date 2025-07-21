# StealthMole MCP Server

[![smithery badge](https://smithery.ai/badge/@cjinzy/mole-mcp-server)](https://smithery.ai/server/@cjinzy/mole-mcp-server)

StealthMole 검색을 위한 MCP 서버로 다양한 StealthMole의 서비스에서 검색 및 분석을 도와줍니다.

### 버전 히스토리

##### 1.0.0 (2025-07-18)

- 오픈

### 필수 요구 사항

- StealthMole API Key (Access Key, Secret Key)
- python 12 이상
- uv 패키지 매니저
- Node.js 18 이상
- NPM 8 이상
- Docker (선택 사항, 컨테이너 배포용)

### 도구 세부 정보

#### 사용 가능한 도구

- **search_combo_binder**: CB(Combo Binder) 검색 도구
- **search_compromised_dataset**: CDS(Compromised DataSet) 검색 도구
- **search_credentials**: CL(Credentials Lookout) 검색 도구
- **search_darkweb**: DT(Darkweb Tracker) 검색 도구
- **search_government_monitoring**: GM(Government Monitoring) 검색 도구
- **search_leaked_monitoring**: LM(Leaked Monitoring) 검색 도구
- **search_pagination**: 다음 페이지 검색에 사용되는 도구
- **search_ransomware**: RM(Ransomware Monitoring) 검색 도구
- **search_telegram**: TT(Telegram Tracker) 검색 도구
- **search_ulp_binder**: ULP(ULP Binder) 검색 도구
- **get_compromised_dataset_node**: CDS 노드의 상세 정보를 조회 합니다.
- **get_node_details**: 노드의 상세 정보를 조회 합니다.
- **get_targets**: 조회된 노드의 타겟 정보를 조회 합니다.
- **get_user_quotas** : 사용자의 API 현황을 조회 합니다.
- **download_file**: 파일을 다운로드 합니다.
- **export_data**: 서비스(cl, cds, cb, ub)와 검색 쿼리를 입력하여 조회된 노드의 정보를 내보내기 합니다. 데이터가 큰 경우 업체에 문의 하세요.

### 설치

#### Smithery를 통한 자동 설치 (권장)

Claude Desktop 사용시:

```bash
npx -y @smithery/cli@latest install @cjinzy/mole-mcp-server --client claude
```

설치시 다음 정보를 요구합니다.

- StealthMole API Access key
- StealthMole API Secret key

#### Claude Desktop 수동 구성

```json
{
  "mcpServers": {
    "mole-mcp-server": {
      "command": "npx",
      "args": [
        "-y",
        "@smithery/cli@latest",
        "run",
        "@cjinzy/mole-mcp-server"
      ]
      "env": {
        "STEALTHMOLE_API_ACCESS_KEY": "your_access_key",
        "STEALTHMOLE_API_SECRET_KEY": "your_secret_key"
      }
    }
  }
}
```

## 라이선스

MIT License
