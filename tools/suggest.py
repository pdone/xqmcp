"""搜索工具模块"""

import pysnowball
from tools.utils import safe_call, logger
from mcp.types import ToolAnnotations


def search_stock(q: str, response_format: str = "json") -> dict:
    """搜索股票（支持模糊搜索，可用股票名称、代码或简称）

    Args:
        q: 搜索关键词，如 贵州茅台、茅台、600519、SH600519
        response_format: 响应格式 json/markdown
    """
    logger.info(f"搜索股票: {q}")
    return safe_call(pysnowball.suggest_stock, q, response_format=response_format)


def register(mcp):
    """注册 MCP 工具"""
    annotations = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=True)
    mcp.tool(annotations=annotations)(search_stock)
