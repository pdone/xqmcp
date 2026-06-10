"""港股通数据工具模块"""

import pysnowball


def get_northbound_shareholding_sh(date: str = None) -> dict:
    """获取沪股通持股数据

    Args:
        date: 日期，格式 YYYY/MM/DD，默认今天
    """
    return pysnowball.northbound_shareholding_sh(date)


def get_northbound_shareholding_sz(date: str = None) -> dict:
    """获取深股通持股数据

    Args:
        date: 日期，格式 YYYY/MM/DD，默认今天
    """
    return pysnowball.northbound_shareholding_sz(date)


def register(mcp):
    """注册 MCP 工具"""
    mcp.tool()(get_northbound_shareholding_sh)
    mcp.tool()(get_northbound_shareholding_sz)
