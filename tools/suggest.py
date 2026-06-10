"""搜索工具模块"""

import pysnowball


def search_stock(q: str) -> dict:
    """搜索股票

    Args:
        q: 搜索关键词，如 贵州茅台、600519
    """
    return pysnowball.suggest_stock(q)


def register(mcp):
    """注册 MCP 工具"""
    mcp.tool()(search_stock)
