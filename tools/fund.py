"""基金数据工具模块"""

import pysnowball
from tools.utils import safe_call, logger
from mcp.types import ToolAnnotations


def get_fund_detail(symbol: str, response_format: str = "json") -> dict:
    """获取基金详情

    Args:
        symbol: 基金代码，如 000001、110011
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取基金详情: {symbol}")
    return safe_call(pysnowball.fund_detail, symbol, response_format=response_format)


def get_fund_info(symbol: str, response_format: str = "json") -> dict:
    """获取基金信息

    Args:
        symbol: 基金代码，如 000001、110011
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取基金信息: {symbol}")
    return safe_call(pysnowball.fund_info, symbol, response_format=response_format)


def get_fund_growth(symbol: str, day: str = "ty", response_format: str = "json") -> dict:
    """获取基金增长数据

    Args:
        symbol: 基金代码，如 000001、110011
        day: 时间范围 ty/1y/3y/5y
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取基金增长数据: {symbol}")
    return safe_call(pysnowball.fund_growth, symbol, day, response_format=response_format)


def get_fund_nav_history(symbol: str, page: int = 1, size: int = 20, response_format: str = "json") -> dict:
    """获取基金净值历史

    Args:
        symbol: 基金代码，如 000001、110011
        page: 页码
        size: 每页条数
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取基金净值历史: {symbol}")
    return safe_call(pysnowball.fund_nav_history, symbol, page, size, response_format=response_format)


def get_fund_derived(symbol: str, response_format: str = "json") -> dict:
    """获取基金衍生数据

    Args:
        symbol: 基金代码，如 000001、110011
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取基金衍生数据: {symbol}")
    return safe_call(pysnowball.fund_derived, symbol, response_format=response_format)


def get_fund_asset(symbol: str, response_format: str = "json") -> dict:
    """获取基金持仓

    Args:
        symbol: 基金代码，如 000001、110011
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取基金持仓: {symbol}")
    return safe_call(pysnowball.fund_asset, symbol, response_format=response_format)


def get_fund_manager(symbol: str, response_format: str = "json") -> dict:
    """获取基金经理信息

    Args:
        symbol: 基金代码，如 000001、110011
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取基金经理信息: {symbol}")
    return safe_call(pysnowball.fund_manager, symbol, response_format=response_format)


def get_fund_achievement(symbol: str, response_format: str = "json") -> dict:
    """获取基金业绩

    Args:
        symbol: 基金代码，如 000001、110011
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取基金业绩: {symbol}")
    return safe_call(pysnowball.fund_achievement, symbol, response_format=response_format)


def get_fund_trade_date(symbol: str, response_format: str = "json") -> dict:
    """获取基金交易日

    Args:
        symbol: 基金代码，如 000001、110011
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取基金交易日: {symbol}")
    return safe_call(pysnowball.fund_trade_date, symbol, response_format=response_format)


def register(mcp):
    """注册 MCP 工具"""
    annotations = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=True)
    mcp.tool(annotations=annotations)(get_fund_detail)
    mcp.tool(annotations=annotations)(get_fund_info)
    mcp.tool(annotations=annotations)(get_fund_growth)
    mcp.tool(annotations=annotations)(get_fund_nav_history)
    mcp.tool(annotations=annotations)(get_fund_derived)
    mcp.tool(annotations=annotations)(get_fund_asset)
    mcp.tool(annotations=annotations)(get_fund_manager)
    mcp.tool(annotations=annotations)(get_fund_achievement)
    mcp.tool(annotations=annotations)(get_fund_trade_date)
