"""Vercel API 入口"""

import os
import sys

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from starlette.routing import Route
from mcp.server.streamable_http import StreamableHTTPServerTransport
from server import app, mcp

# 创建 Streamable HTTP 传输实例
streamable_transport = StreamableHTTPServerTransport("/mcp")


async def handle_streamable_http(request):
    """处理 Streamable HTTP 请求"""
    async with streamable_transport.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await mcp._mcp_server.run(
            streams[0],
            streams[1],
            mcp._mcp_server.create_initialization_options(),
        )


# 添加 MCP 路由到应用
app.routes.extend([
    Route("/mcp", endpoint=handle_streamable_http, methods=["GET", "POST"]),
])

# Vercel Python Runtime 会自动处理 ASGI 应用
