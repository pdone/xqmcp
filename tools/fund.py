"""基金数据工具模块"""

import pysnowball


def get_fund_detail(symbol: str) -> dict:
    """获取基金详情

    Args:
        symbol: 基金代码，如 000001
    """
    return pysnowball.fund_detail(symbol)


def get_fund_info(symbol: str) -> dict:
    """获取基金信息

    Args:
        symbol: 基金代码
    """
    return pysnowball.fund_info(symbol)


def get_fund_growth(symbol: str, day: str = "ty") -> dict:
    """获取基金增长数据

    Args:
        symbol: 基金代码
        day: 时间范围 ty/1y/3y/5y
    """
    return pysnowball.fund_growth(symbol, day)


def get_fund_nav_history(symbol: str, page: int = 1, size: int = 20) -> dict:
    """获取基金净值历史

    Args:
        symbol: 基金代码
        page: 页码
        size: 每页条数
    """
    return pysnowball.fund_nav_history(symbol, page, size)


def get_fund_derived(symbol: str) -> dict:
    """获取基金衍生数据

    Args:
        symbol: 基金代码
    """
    return pysnowball.fund_derived(symbol)


def get_fund_asset(symbol: str) -> dict:
    """获取基金持仓

    Args:
        symbol: 基金代码
    """
    return pysnowball.fund_asset(symbol)


def get_fund_manager(symbol: str) -> dict:
    """获取基金经理信息

    Args:
        symbol: 基金代码
    """
    return pysnowball.fund_manager(symbol)


def get_fund_achievement(symbol: str) -> dict:
    """获取基金业绩

    Args:
        symbol: 基金代码
    """
    return pysnowball.fund_achievement(symbol)


def get_fund_trade_date(symbol: str) -> dict:
    """获取基金交易日

    Args:
        symbol: 基金代码
    """
    return pysnowball.fund_trade_date(symbol)


def register(mcp):
    """注册 MCP 工具"""
    mcp.tool()(get_fund_detail)
    mcp.tool()(get_fund_info)
    mcp.tool()(get_fund_growth)
    mcp.tool()(get_fund_nav_history)
    mcp.tool()(get_fund_derived)
    mcp.tool()(get_fund_asset)
    mcp.tool()(get_fund_manager)
    mcp.tool()(get_fund_achievement)
    mcp.tool()(get_fund_trade_date)
