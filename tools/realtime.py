"""实时行情工具模块"""

import pysnowball


def get_quote(symbol: str) -> dict:
    """获取股票实时报价

    Args:
        symbol: 股票代码，如 SH600519, SZ000001
    """
    return pysnowball.quotec(symbol)


def get_kline(symbol: str, begin: int, period: str = "day", count: int = 100) -> dict:
    """获取K线数据

    Args:
        symbol: 股票代码
        begin: 开始时间戳(毫秒)
        period: 周期 day/week/month/quarter/year
        count: 数据条数
    """
    return pysnowball.kline(symbol, begin, period, count)


def get_pankou(symbol: str) -> dict:
    """获取盘口数据(五档买卖)

    Args:
        symbol: 股票代码
    """
    return pysnowball.pankou(symbol)


def get_quote_detail(symbol: str) -> dict:
    """获取股票详细行情

    Args:
        symbol: 股票代码
    """
    return pysnowball.quote_detail(symbol)


def register(mcp):
    """注册 MCP 工具"""
    mcp.tool()(get_quote)
    mcp.tool()(get_kline)
    mcp.tool()(get_pankou)
    mcp.tool()(get_quote_detail)
