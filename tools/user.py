"""用户数据工具模块"""

import pysnowball
from tools.utils import safe_call, logger
from mcp.types import ToolAnnotations


def get_watch_list(limit: int = 50, offset: int = 0, response_format: str = "json") -> dict:
    """获取自选股列表

    Args:
        limit: 返回条数上限
        offset: 跳过条数
        response_format: 响应格式 json/markdown
    """
    logger.info("获取自选股列表")
    return safe_call(pysnowball.watch_list, response_format=response_format)


def get_watch_stock(pid: str, response_format: str = "json") -> dict:
    """获取自选股详情

    Args:
        pid: 组合ID
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取自选股详情: {pid}")
    return safe_call(pysnowball.watch_stock, pid, response_format=response_format)


def register(mcp):
    """注册 MCP 工具"""
    annotations = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=True)
    mcp.tool(annotations=annotations)(get_watch_list)
    mcp.tool(annotations=annotations)(get_watch_stock)
