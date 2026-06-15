"""债券数据工具模块"""

import pysnowball
from tools.utils import safe_call, logger
from mcp.types import ToolAnnotations


def get_convertible_bond(page_size: int = 50, page_number: int = 1, response_format: str = "json") -> dict:
    """获取可转债列表

    Args:
        page_size: 每页条数
        page_number: 页码
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取可转债列表: page={page_number}")
    return safe_call(pysnowball.convertible_bond, page_size, page_number, response_format=response_format)


def register(mcp):
    """注册 MCP 工具"""
    annotations = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=True)
    mcp.tool(annotations=annotations)(get_convertible_bond)
