"""实时行情工具模块"""

import pysnowball
from tools.utils import safe_call, logger


def get_quote(symbol: str) -> dict:
    """获取股票实时报价

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)、HK00700(港股)、USAAPL(美股)
    """
    logger.info(f"获取行情: {symbol}")
    return safe_call(pysnowball.quotec, symbol)


def get_kline(symbol: str, period: str = "day", count: int = 100) -> dict:
    """获取K线数据

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)、HK00700(港股)、USAAPL(美股)
        period: 周期 day/week/month/quarter/year
        count: 数据条数
    """
    logger.info(f"获取K线: {symbol}, period={period}, count={count}")
    return safe_call(pysnowball.kline, symbol, period, count)


def get_pankou(symbol: str) -> dict:
    """获取盘口数据(五档买卖)

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)、HK00700(港股)、USAAPL(美股)
    """
    logger.info(f"获取盘口: {symbol}")
    return safe_call(pysnowball.pankou, symbol)


def get_quote_detail(symbol: str) -> dict:
    """获取股票详细行情

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)、HK00700(港股)、USAAPL(美股)
    """
    logger.info(f"获取详细行情: {symbol}")
    return safe_call(pysnowball.quote_detail, symbol)


def register(mcp):
    """注册 MCP 工具"""
    mcp.tool()(get_quote)
    mcp.tool()(get_kline)
    mcp.tool()(get_pankou)
    mcp.tool()(get_quote_detail)
