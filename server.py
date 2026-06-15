"""本地开发服务器

启动命令: python server.py
访问 Swagger: http://localhost:8000/docs
访问 MCP: http://localhost:8000/mcp (Streamable HTTP)
"""

import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from starlette.types import ASGIApp, Scope, Receive, Send

from common import register_all_endpoints, ROOT_HTML
from mcp_server import create_mcp_server

# 本地开发服务器使用有状态模式（支持 session 管理）
mcp = create_mcp_server(stateless=False)


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
    description="雪球股票数据接口，提供 A 股/港股/美股的实时行情、财务数据、基金信息等。同时支持 MCP 协议和 REST API。",
    version="1.0.0",
    lifespan=lifespan,
)


# 注册所有 REST API 端点
register_all_endpoints(app)


@app.get("/", tags=["首页"], include_in_schema=False)
async def root():
    return HTMLResponse(ROOT_HTML)


# ============================================================
# MCP 端点 (Streamable HTTP)
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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"启动服务器: http://localhost:{port}")
    print(f"Swagger UI: http://localhost:{port}/docs")
    print(f"MCP 端点: http://localhost:{port}/mcp (Streamable HTTP)")
    uvicorn.run(app, host="0.0.0.0", port=port)
