"""组合数据工具模块"""

import pysnowball


def get_nav_daily(cube_symbol: str) -> dict:
    """获取组合每日净值

    Args:
        cube_symbol: 组合代码
    """
    return pysnowball.nav_daily(cube_symbol)


def get_rebalancing_history(cube_symbol: str) -> dict:
    """获取组合调仓历史

    Args:
        cube_symbol: 组合代码
    """
    return pysnowball.rebalancing_history(cube_symbol)


def get_rebalancing_current(cube_symbol: str) -> dict:
    """获取组合当前持仓

    Args:
        cube_symbol: 组合代码
    """
    return pysnowball.rebalancing_current(cube_symbol)


def get_quote_current(code: str) -> dict:
    """获取组合当前报价

    Args:
        code: 组合代码
    """
    return pysnowball.quote_current(code)


def register(mcp):
    """注册 MCP 工具"""
    mcp.tool()(get_nav_daily)
    mcp.tool()(get_rebalancing_history)
    mcp.tool()(get_rebalancing_current)
    mcp.tool()(get_quote_current)
