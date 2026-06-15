# 更新日志

## 2026-06-15: 代码重构与 Vercel 无状态模式支持

### 一、核心架构改进

#### 1. Vercel Serverless 无状态模式

**问题**: Vercel 部署的 MCP 服务在调用时提示 session 错误。

**原因**: Vercel Serverless 环境是无状态的，而 MCP 协议的 session 管理需要服务器端保持状态。

**解决方案**: 启用 MCP SDK 的 `stateless_http` 模式。

**修改文件**:
- [mcp_server.py](mcp_server.py) - 添加 `stateless` 参数
- [server.py](server.py) - 本地开发使用有状态模式 (`stateless=False`)
- [api/index.py](api/index.py) - Vercel 部署使用无状态模式 (`stateless=True`)

**技术细节**:
| 模式 | 参数 | 特点 | 适用场景 |
|------|------|------|----------|
| 无状态 | `stateless_http=True` | 每个请求独立处理，不返回 `Mcp-Session-Id` | Vercel Serverless |
| 有状态 | `stateless_http=False` | 维护 session 状态，支持断线重连 | 本地开发服务器 |

#### 2. 环境变量支持

- [server.py](server.py) - 添加 `python-dotenv` 支持，自动加载 `.env` 文件
- [stdio.py](stdio.py) - 同样添加 `.env` 加载支持
- [requirements.txt](requirements.txt) - 添加 `python-dotenv>=1.0.0` 依赖

### 二、工具模块增强

#### 1. ToolAnnotations 注解

所有工具模块添加了 MCP `ToolAnnotations` 注解，提供更丰富的元数据：

```python
from mcp.types import ToolAnnotations

annotations = ToolAnnotations(
    readOnlyHint=True,      # 只读操作
    destructiveHint=False,  # 非破坏性操作
    idempotentHint=True,    # 幂等操作
    openWorldHint=True      # 访问外部世界
)
mcp.tool(annotations=annotations)(func)
```

**修改的工具模块**:
- [tools/realtime.py](tools/realtime.py) - 实时行情
- [tools/finance.py](tools/finance.py) - 财务数据
- [tools/f10.py](tools/f10.py) - 基本面数据
- [tools/capital.py](tools/capital.py) - 资金流向
- [tools/report.py](tools/report.py) - 研报数据
- [tools/fund.py](tools/fund.py) - 基金数据
- [tools/index.py](tools/index.py) - 指数数据
- [tools/bond.py](tools/bond.py) - 债券数据
- [tools/hkex.py](tools/hkex.py) - 港股通
- [tools/user.py](tools/user.py) - 用户数据
- [tools/suggest.py](tools/suggest.py) - 搜索

#### 2. 响应格式支持

所有工具添加 `response_format` 参数，支持 JSON 和 Markdown 两种格式：

```python
def get_quote(symbol: str, response_format: str = "json") -> dict:
    """获取股票实时报价

    Args:
        symbol: 股票代码
        response_format: 响应格式 json/markdown
    """
```

#### 3. 分页支持

部分工具添加了分页参数 (`limit`, `offset`)：

```python
def get_margin(symbol: str, limit: int = 50, offset: int = 0) -> dict:
    """获取融资融券

    Args:
        symbol: 股票代码
        limit: 返回条数上限，默认50
        offset: 跳过条数，默认0
    """
```

### 三、工具函数增强

[tools/utils.py](tools/utils.py) 新增功能：

| 函数 | 功能 |
|------|------|
| `paginate()` | 列表数据分页 |
| `_format_markdown()` | 数据转 Markdown 格式 |
| `_truncate_data()` | 字符限制截断（约 100KB） |
| `make_response()` | 统一响应格式，支持格式转换和截断 |

### 四、错误处理优化

[common.py](common.py) 统一错误响应格式：

```python
# 旧格式
return {"error": str(e)}

# 新格式
return {"success": False, "error": str(e), "data": None}
```

### 五、文件结构变更

#### 删除的文件
- `stdio_server.py` → 重命名为 [stdio.py](stdio.py)
- `test_import.py` → 移至 [tests/test_import.py](tests/test_import.py)
- `test_mcp.py` → 移至 [tests/test_mcp.py](tests/test_mcp.py)
- `test_stdio.py` → 移至 [tests/test_stdio.py](tests/test_stdio.py)

#### 新增的文件
- [CHANGELOG.md](CHANGELOG.md) - 更新日志
- [tests/](tests/) - 测试目录

### 六、文档更新

[README.md](README.md) 更新内容：
- API 接口数量：56 → 51（移除了组合数据工具）
- 实时行情接口：4 → 3（移除 `get_kline`）
- 移除"组合数据"分类
- 更新 Vercel 部署说明（支持无状态模式）
- 更新文件结构说明

### 七、使用方式

#### Vercel 部署（无状态模式）

```bash
# Claude Code CLI
claude mcp add pysnowball --transport http https://your-project.vercel.app/mcp

# Claude Desktop
{
  "mcpServers": {
    "pysnowball": {
      "url": "https://your-project.vercel.app/mcp"
    }
  }
}
```

#### 本地开发（有状态模式）

```bash
python server.py
```

#### 本地 stdio 模式（推荐）

```bash
python stdio.py
```

### 八、测试验证

本地验证无状态模式：

```bash
# 启动测试服务器
python -c "
from mcp_server import create_mcp_server
from server import *
mcp = create_mcp_server(stateless=True)
# ... 启动服务器
"

# 测试请求
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

验证要点：
- ✅ 不返回 `Mcp-Session-Id` header
- ✅ 连续请求不需要携带 session ID
- ✅ 每个请求独立处理
