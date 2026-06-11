"""Vercel API 入口

支持 REST API 和 MCP Streamable HTTP 协议
"""

import os
import sys
from contextlib import asynccontextmanager

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from starlette.types import ASGIApp, Scope, Receive, Send

from common import register_all_endpoints, verify_api_key, ROOT_HTML
from mcp_server import mcp


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


# 注册所有 REST API 端点
register_all_endpoints(app)


# ============================================================
# 首页
# ============================================================

@app.get("/", tags=["首页"], include_in_schema=False)
async def root():
    """首页"""
    return HTMLResponse(ROOT_HTML)


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
