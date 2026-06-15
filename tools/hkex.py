"""港股通数据工具模块"""

import pysnowball
from tools.utils import safe_call, logger
from mcp.types import ToolAnnotations


def get_northbound_shareholding_sh(date: str = None, limit: int = 50, offset: int = 0, response_format: str = "json") -> dict:
    """获取沪股通持股数据

    Args:
        date: 日期，格式 YYYY/MM/DD，默认今天
        limit: 返回条数上限
        offset: 跳过条数
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取沪股通持股: {date}")
    return safe_call(pysnowball.northbound_shareholding_sh, date, response_format=response_format)


def get_northbound_shareholding_sz(date: str = None, limit: int = 50, offset: int = 0, response_format: str = "json") -> dict:
    """获取深股通持股数据

    Args:
        date: 日期，格式 YYYY/MM/DD，默认今天
        limit: 返回条数上限
        offset: 跳过条数
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取深股通持股: {date}")
    return safe_call(pysnowball.northbound_shareholding_sz, date, response_format=response_format)


def register(mcp):
    """注册 MCP 工具"""
    annotations = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=True)
    mcp.tool(annotations=annotations)(get_northbound_shareholding_sh)
    mcp.tool(annotations=annotations)(get_northbound_shareholding_sz)
