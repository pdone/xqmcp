"""F10 基本面工具模块"""

import pysnowball


def get_skholderchg(symbol: str) -> dict:
    """获取股东增减持

    Args:
        symbol: 股票代码
    """
    return pysnowball.skholderchg(symbol)


def get_skholder(symbol: str) -> dict:
    """获取股东信息

    Args:
        symbol: 股票代码
    """
    return pysnowball.skholder(symbol)


def get_main_indicator(symbol: str) -> dict:
    """获取主要指标

    Args:
        symbol: 股票代码
    """
    return pysnowball.main_indicator(symbol)


def get_industry(symbol: str) -> dict:
    """获取行业信息

    Args:
        symbol: 股票代码
    """
    return pysnowball.industry(symbol)


def get_holders(symbol: str) -> dict:
    """获取股东人数

    Args:
        symbol: 股票代码
    """
    return pysnowball.holders(symbol)


def get_bonus(symbol: str) -> dict:
    """获取分红送转

    Args:
        symbol: 股票代码
    """
    return pysnowball.bonus(symbol)


def get_org_holding_change(symbol: str) -> dict:
    """获取机构持仓变动

    Args:
        symbol: 股票代码
    """
    return pysnowball.org_holding_change(symbol)


def get_industry_compare(symbol: str) -> dict:
    """获取行业对比

    Args:
        symbol: 股票代码
    """
    return pysnowball.industry_compare(symbol)


def get_business_analysis(symbol: str) -> dict:
    """获取经营分析

    Args:
        symbol: 股票代码
    """
    return pysnowball.business_analysis(symbol)


def get_shareschg(symbol: str) -> dict:
    """获取股本变动

    Args:
        symbol: 股票代码
    """
    return pysnowball.shareschg(symbol)


def get_top_holders(symbol: str) -> dict:
    """获取十大股东

    Args:
        symbol: 股票代码
    """
    return pysnowball.top_holders(symbol)


def register(mcp):
    """注册 MCP 工具"""
    mcp.tool()(get_skholderchg)
    mcp.tool()(get_skholder)
    mcp.tool()(get_main_indicator)
    mcp.tool()(get_industry)
    mcp.tool()(get_holders)
    mcp.tool()(get_bonus)
    mcp.tool()(get_org_holding_change)
    mcp.tool()(get_industry_compare)
    mcp.tool()(get_business_analysis)
    mcp.tool()(get_shareschg)
    mcp.tool()(get_top_holders)
