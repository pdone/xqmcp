"""Vercel API 入口

支持 REST API 和 MCP Streamable HTTP 协议
"""

import os
import sys
import inspect
from contextlib import asynccontextmanager

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Header, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from typing import Optional
from starlette.types import ASGIApp, Scope, Receive, Send

import pysnowball

from tools import (
    realtime,
    finance,
    f10,
    capital,
    report,
    fund,
    index,
    bond,
    hkex,
    user,
    cube,
    suggest,
)
from mcp_server import mcp

# 环境变量
XUEQIU_TOKEN = os.environ.get("XUEQIU_TOKEN", "")
API_TOKEN = os.environ.get("API_TOKEN", "")

# 设置雪球 token
if XUEQIU_TOKEN:
    pysnowball.set_token(XUEQIU_TOKEN)


# ============================================================
# API 认证
# ============================================================

async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """验证 API Key（当 API_TOKEN 不为空时启用）"""
    if not API_TOKEN:
        return  # 未设置 API_TOKEN，跳过验证
    if x_api_key != API_TOKEN:
        raise HTTPException(status_code=401, detail="无效的 API Key")


# ============================================================
# FastAPI 应用（带 MCP lifespan）
# ============================================================

@asynccontextmanager
async def lifespan(app):
    """启动 MCP session manager"""
    async with mcp.session_manager.run():
        yield


app = FastAPI(
    title="pysnowball MCP Server",
    description="雪球股票数据接口，支持 MCP 协议和 REST API",
    version="1.0.0",
    lifespan=lifespan,
)


# ============================================================
# 首页
# ============================================================

@app.get("/", tags=["首页"], include_in_schema=False)
async def root():
    """首页"""
    return HTMLResponse("""
    <html>
        <head><title>pysnowball MCP Server</title></head>
        <body>
            <h1>pysnowball MCP Server</h1>
            <p>雪球股票数据服务器，支持 MCP 协议和 REST API</p>
            <h2>接口</h2>
            <ul>
                <li><a href="/docs">Swagger UI</a> - REST API 文档</li>
                <li><strong>MCP 端点:</strong> <code>/mcp</code> (Streamable HTTP)</li>
            </ul>
            <h2>MCP 客户端配置</h2>
            <pre><code>{
  "mcpServers": {
    "pysnowball": {
      "url": "https://your-domain/mcp"
    }
  }
}</code></pre>
        </body>
    </html>
    """)


# ============================================================
# REST API 端点
# ============================================================

TOOL_GROUPS = {
    "realtime": ("实时行情", realtime),
    "finance": ("财务数据", finance),
    "f10": ("基本面", f10),
    "capital": ("资金流向", capital),
    "report": ("研报数据", report),
    "fund": ("基金数据", fund),
    "index": ("指数数据", index),
    "bond": ("债券数据", bond),
    "hkex": ("港股通", hkex),
    "user": ("用户数据", user),
    "cube": ("组合数据", cube),
    "suggest": ("搜索", suggest),
}


def register_endpoint(func, tag: str):
    """将工具函数注册为 FastAPI 端点"""
    func_name = func.__name__

    # 获取函数签名
    sig = inspect.signature(func)

    # 创建包装函数，保持原始函数名
    async def wrapper(api_key: str = Depends(verify_api_key), **kwargs):
        try:
            return func(**kwargs)
        except Exception as e:
            return {"error": str(e)}

    # 重建签名（排除 api_key 参数）
    new_params = []
    for name, param in sig.parameters.items():
        annotation = param.annotation if param.annotation != inspect.Parameter.empty else str
        default = param.default if param.default != inspect.Parameter.empty else ...
        new_params.append(inspect.Parameter(
            name, inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default=default, annotation=annotation
        ))
    wrapper.__signature__ = inspect.Signature(new_params)
    wrapper.__name__ = func_name
    wrapper.__qualname__ = func_name
    wrapper.__doc__ = func.__doc__

    # 注册路由
    app.post(
        f"/api/{func_name}",
        tags=[tag],
        summary=func_name,
        description=func.__doc__,
        name=func_name,
        dependencies=[Depends(verify_api_key)],
    )(wrapper)


# 遍历所有模块，注册每个函数
EXCLUDE_NAMES = {"register"}  # 排除的函数名

for group_name, (tag, module) in TOOL_GROUPS.items():
    for attr_name in dir(module):
        if attr_name.startswith("_") or attr_name in EXCLUDE_NAMES:
            continue
        func = getattr(module, attr_name)
        if callable(func):
            register_endpoint(func, tag)


# ============================================================
# MCP 端点
# ============================================================

# 创建 MCP streamable_http_app
mcp_app = mcp.streamable_http_app()

# 找到 MCP ASGI handler
_mcp_asgi_handler = None
for route in mcp_app.routes:
    if hasattr(route, 'endpoint'):
        _mcp_asgi_handler = route.endpoint
        break


class MCPMountMiddleware:
    """ASGI 中间件，将 /mcp 请求直接转发给 MCP handler，避免 307 重定向"""

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope.get("type") == "http" and scope.get("path", "").rstrip("/") == "/mcp":
            # 直接转发给 MCP handler，修改路径为 /
            scope = dict(scope)
            scope["path"] = "/"
            scope["raw_path"] = b"/"
            await _mcp_asgi_handler(scope, receive, send)
        else:
            await self.app(scope, receive, send)


app.add_middleware(MCPMountMiddleware)
