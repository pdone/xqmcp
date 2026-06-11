"""研报数据工具模块"""

import pysnowball
from tools.utils import safe_call, logger


def get_report(symbol: str) -> dict:
    """获取研究报告

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
    """
    logger.info(f"获取研究报告: {symbol}")
    return safe_call(pysnowball.report, symbol)


def get_earningforecast(symbol: str) -> dict:
    """获取盈利预测

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
    """
    logger.info(f"获取盈利预测: {symbol}")
    return safe_call(pysnowball.earningforecast, symbol)


def register(mcp):
    """注册 MCP 工具"""
    mcp.tool()(get_report)
    mcp.tool()(get_earningforecast)
