"""债券数据工具模块"""

import pysnowball


def get_convertible_bond(page_size: int = 50, page_number: int = 1) -> dict:
    """获取可转债列表

    Args:
        page_size: 每页条数
        page_number: 页码
    """
    return pysnowball.convertible_bond(page_size, page_number)


def register(mcp):
    """注册 MCP 工具"""
    mcp.tool()(get_convertible_bond)
