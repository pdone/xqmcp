"""MCP 服务器核心模块"""

import os
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

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


def create_mcp_server() -> FastMCP:
    """创建并配置 MCP 服务器"""

    mcp = FastMCP(
        "pysnowball",
        instructions="雪球股票数据接口 MCP 服务器，提供 A 股/港股/美股的实时行情、财务数据、基金信息等",
        streamable_http_path="/",
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=False,
        ),
    )

    # 设置 token
    token = os.environ.get("XUEQIU_TOKEN", "")
    if token:
        pysnowball.set_token(token)

    # 注册所有工具模块
    realtime.register(mcp)
    finance.register(mcp)
    f10.register(mcp)
    capital.register(mcp)
    report.register(mcp)
    fund.register(mcp)
    index.register(mcp)
    bond.register(mcp)
    hkex.register(mcp)
    user.register(mcp)
    cube.register(mcp)
    suggest.register(mcp)

    return mcp


# 创建全局 MCP 实例
mcp = create_mcp_server()
