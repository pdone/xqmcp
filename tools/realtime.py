"""实时行情工具模块"""

import pysnowball
from tools.utils import safe_call, logger
from mcp.types import ToolAnnotations


def get_quote(symbol: str, response_format: str = "json") -> dict:
    """获取股票实时报价

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)、HK00700(港股)、USAAPL(美股)
        response_format: 响应格式 json/markdown

    Note:
        港股(HK)和美股(USA)在非交易时间或权限不足时，data.data[0] 可能返回 null，
        这是雪球 API 的正常行为，调用方需自行判断数据是否为 null。
    """
    logger.info(f"获取行情: {symbol}")
    return safe_call(pysnowball.quotec, symbol, response_format=response_format)


def get_pankou(symbol: str, response_format: str = "json") -> dict:
    """获取盘口数据(五档买卖)

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)、HK00700(港股)、USAAPL(美股)
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取盘口: {symbol}")
    return safe_call(pysnowball.pankou, symbol, response_format=response_format)


def get_quote_detail(symbol: str, response_format: str = "json") -> dict:
    """获取股票详细行情

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)、HK00700(港股)、USAAPL(美股)
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取详细行情: {symbol}")
    return safe_call(pysnowball.quote_detail, symbol, response_format=response_format)


def register(mcp):
    """注册 MCP 工具"""
    annotations = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=True)
    mcp.tool(annotations=annotations)(get_quote)
    mcp.tool(annotations=annotations)(get_pankou)
    mcp.tool(annotations=annotations)(get_quote_detail)
