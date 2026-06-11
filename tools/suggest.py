"""搜索工具模块"""

import pysnowball
from tools.utils import safe_call, logger


def search_stock(q: str) -> dict:
    """搜索股票（支持模糊搜索，可用股票名称、代码或简称）

    Args:
        q: 搜索关键词，如 贵州茅台、茅台、600519、SH600519
    """
    logger.info(f"搜索股票: {q}")
    return safe_call(pysnowball.suggest_stock, q)


def register(mcp):
    """注册 MCP 工具"""
    mcp.tool()(search_stock)
