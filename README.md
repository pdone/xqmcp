# pysnowball MCP Server

基于 [pysnowball](https://pypi.org/project/pysnowball/) 的雪球股票数据服务器，同时支持 **MCP 协议** 和 **REST API**，可一键部署到 Vercel。

## 功能特性

- **56 个 API 接口** - 覆盖实时行情、财务数据、基金、指数等
- **双协议支持** - MCP 协议（Streamable HTTP）+ REST API（通用调用）
- **Streamable HTTP** - 使用标准 HTTP/HTTPS 协议，更好的兼容性
- **Swagger 文档** - 自动生成，开箱即用
- **API 认证** - 可选的 `x-api-key` 保护
- **Serverless** - Vercel 一键部署，零运维

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 必填：雪球网 token
export XUEQIU_TOKEN=your_xueqiu_token

# 可选：API 访问密钥（设置后需要 x-api-key 认证）
export API_TOKEN=your_api_key
```

> **获取雪球 Token：** 登录 [雪球网](https://xueqiu.com) → F12 开发者工具 → Application → Cookies → `xq_a_token`

### 3. 启动服务

```bash
python server.py
```

- Swagger UI: http://localhost:8000/docs
- MCP 端点: http://localhost:8000/mcp (Streamable HTTP)

## 部署到 Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fpdone%2Fxqmcp)

1. Fork 本项目到你的 GitHub
2. 在 [Vercel](https://vercel.com) 导入项目
3. 添加环境变量：
   - `XUEQIU_TOKEN`（必填）
   - `API_TOKEN`（可选）
4. 完成部署

部署后访问 `https://your-project.vercel.app/docs` 查看 Swagger 文档。

## API 使用

### REST API

每个接口都是独立的 POST 请求：

```bash
# 搜索股票
curl -X POST "https://your-project.vercel.app/api/search_stock" \
  -H "Content-Type: application/json" \
  -d '{"q": "贵州茅台"}'

# 获取实时行情（带认证）
curl -X POST "https://your-project.vercel.app/api/get_quote" \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_api_key" \
  -d '{"symbol": "SH600519"}'
```

### MCP 协议

使用 Streamable HTTP 传输协议，基于标准 HTTP/HTTPS 实现流式通信。

**Claude Desktop (`claude_desktop_config.json`)：**
```json
{
  "mcpServers": {
    "pysnowball": {
      "url": "https://your-project.vercel.app/mcp",
      "headers": {
        "x-api-key": "your_api_key"  // 可选，API_TOKEN 为空时可删除
      }
    }
  }
}
```

**Claude Code CLI：**
```bash
# 无认证
claude mcp add pysnowball --transport http https://your-project.vercel.app/mcp

# 带认证
claude mcp add pysnowball --transport http https://your-project.vercel.app/mcp --header "x-api-key: your_api_key"
```

**Streamable HTTP 优势：**
- 使用标准 HTTP/HTTPS 协议，穿透防火墙和代理
- 支持双向流式传输
- 支持会话管理和断线重连
- 更好的兼容性和稳定性

## 接口分类

| 分类 | 接口数 | 示例接口 |
|------|--------|----------|
| 实时行情 | 4 | `get_quote`, `get_kline`, `get_pankou` |
| 财务数据 | 9 | `get_balance`, `get_income`, `get_cash_flow` |
| 基本面 | 11 | `get_holders`, `get_top_holders`, `get_bonus` |
| 资金流向 | 5 | `get_capital_flow`, `get_margin` |
| 研报数据 | 2 | `get_report`, `get_earningforecast` |
| 基金数据 | 9 | `get_fund_detail`, `get_fund_nav_history` |
| 指数数据 | 6 | `get_index_basic_info`, `get_index_weight_top10` |
| 债券数据 | 1 | `get_convertible_bond` |
| 港股通 | 2 | `get_northbound_shareholding_sh/sz` |
| 用户数据 | 2 | `get_watch_list`, `get_watch_stock` |
| 组合数据 | 4 | `get_nav_daily`, `get_rebalancing_current` |
| 搜索 | 1 | `search_stock` |

> 完整接口文档请访问 Swagger UI: `/docs`

## 项目结构

```
xqmcp/
├── api/
│   └── index.py          # Vercel 入口 + MCP Streamable HTTP 处理
├── tools/                # 工具函数（每个模块对应一个分类）
│   ├── realtime.py       # 实时行情
│   ├── finance.py        # 财务数据
│   ├── f10.py            # 基本面
│   ├── capital.py        # 资金流向
│   ├── report.py         # 研报数据
│   ├── fund.py           # 基金数据
│   ├── index.py          # 指数数据
│   ├── bond.py           # 债券数据
│   ├── hkex.py           # 港股通
│   ├── user.py           # 用户数据
│   ├── cube.py           # 组合数据
│   └── suggest.py        # 搜索
├── mcp_server.py         # MCP 服务器核心
├── server.py             # FastAPI 服务器 + Swagger
├── vercel.json           # Vercel 部署配置
├── requirements.txt      # Python 依赖
└── runtime.txt           # Python 版本
```

## 环境变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `XUEQIU_TOKEN` | 是 | - | 雪球网登录 token |
| `API_TOKEN` | 否 | 空 | API 访问密钥，设置后启用 `x-api-key` 认证 |

## 技术栈

- [pysnowball](https://pypi.org/project/pysnowball/) - 雪球数据接口
- [FastAPI](https://fastapi.tiangolo.com/) - REST API 框架
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) - MCP 协议支持（Streamable HTTP）
- [Vercel](https://vercel.com) - Serverless 部署平台

## License

MIT
