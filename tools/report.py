"""研报数据工具模块"""

import pysnowball


def get_report(symbol: str) -> dict:
    """获取研究报告

    Args:
        symbol: 股票代码
    """
    return pysnowball.report(symbol)


def get_earningforecast(symbol: str) -> dict:
    """获取盈利预测

    Args:
        symbol: 股票代码
    """
    return pysnowball.earningforecast(symbol)


def register(mcp):
    """注册 MCP 工具"""
    mcp.tool()(get_report)
    mcp.tool()(get_earningforecast)
