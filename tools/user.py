"""用户数据工具模块"""

import pysnowball


def get_watch_list() -> dict:
    """获取自选股列表"""
    return pysnowball.watch_list()


def get_watch_stock(pid: str) -> dict:
    """获取自选股详情

    Args:
        pid: 组合ID
    """
    return pysnowball.watch_stock(pid)


def register(mcp):
    """注册 MCP 工具"""
    mcp.tool()(get_watch_list)
    mcp.tool()(get_watch_stock)
