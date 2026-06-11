"""F10 基本面工具模块"""

import pysnowball
from tools.utils import safe_call, logger


def get_skholderchg(symbol: str) -> dict:
    """获取股东增减持

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
    """
    logger.info(f"获取股东增减持: {symbol}")
    return safe_call(pysnowball.skholderchg, symbol)


def get_skholder(symbol: str) -> dict:
    """获取股东信息

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
    """
    logger.info(f"获取股东信息: {symbol}")
    return safe_call(pysnowball.skholder, symbol)


def get_main_indicator(symbol: str) -> dict:
    """获取主要指标

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
    """
    logger.info(f"获取主要指标: {symbol}")
    return safe_call(pysnowball.main_indicator, symbol)


def get_industry(symbol: str) -> dict:
    """获取行业信息

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
    """
    logger.info(f"获取行业信息: {symbol}")
    return safe_call(pysnowball.industry, symbol)


def get_holders(symbol: str) -> dict:
    """获取股东人数

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
    """
    logger.info(f"获取股东人数: {symbol}")
    return safe_call(pysnowball.holders, symbol)


def get_bonus(symbol: str) -> dict:
    """获取分红送转

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
    """
    logger.info(f"获取分红送转: {symbol}")
    return safe_call(pysnowball.bonus, symbol)


def get_org_holding_change(symbol: str) -> dict:
    """获取机构持仓变动

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
    """
    logger.info(f"获取机构持仓变动: {symbol}")
    return safe_call(pysnowball.org_holding_change, symbol)


def get_industry_compare(symbol: str) -> dict:
    """获取行业对比

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
    """
    logger.info(f"获取行业对比: {symbol}")
    return safe_call(pysnowball.industry_compare, symbol)


def get_business_analysis(symbol: str) -> dict:
    """获取经营分析

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
    """
    logger.info(f"获取经营分析: {symbol}")
    return safe_call(pysnowball.business_analysis, symbol)


def get_shareschg(symbol: str) -> dict:
    """获取股本变动

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
    """
    logger.info(f"获取股本变动: {symbol}")
    return safe_call(pysnowball.shareschg, symbol)


def get_top_holders(symbol: str) -> dict:
    """获取十大股东

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
    """
    logger.info(f"获取十大股东: {symbol}")
    return safe_call(pysnowball.top_holders, symbol)


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
