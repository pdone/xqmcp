"""资金流向工具模块"""

import pysnowball
from tools.utils import safe_call, logger


def get_margin(symbol: str) -> dict:
    """获取融资融券

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
    """
    logger.info(f"获取融资融券: {symbol}")
    return safe_call(pysnowball.margin, symbol)


def get_blocktrans(symbol: str) -> dict:
    """获取大宗交易

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
    """
    logger.info(f"获取大宗交易: {symbol}")
    return safe_call(pysnowball.blocktrans, symbol)


def get_capital_assort(symbol: str) -> dict:
    """获取资金搭配

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
    """
    logger.info(f"获取资金搭配: {symbol}")
    return safe_call(pysnowball.capital_assort, symbol)


def get_capital_flow(symbol: str) -> dict:
    """获取资金流向

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
    """
    logger.info(f"获取资金流向: {symbol}")
    return safe_call(pysnowball.capital_flow, symbol)


def get_capital_history(symbol: str) -> dict:
    """获取资金历史

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
    """
    logger.info(f"获取资金历史: {symbol}")
    return safe_call(pysnowball.capital_history, symbol)


def register(mcp):
    """注册 MCP 工具"""
    mcp.tool()(get_margin)
    mcp.tool()(get_blocktrans)
    mcp.tool()(get_capital_assort)
    mcp.tool()(get_capital_flow)
    mcp.tool()(get_capital_history)
