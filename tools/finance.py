"""财务数据工具模块"""

import pysnowball
from tools.utils import safe_call, logger
from mcp.types import ToolAnnotations


def get_cash_flow(symbol: str, is_annals: int = 0, count: int = 10, response_format: str = "json") -> dict:
    """获取现金流量表

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)、HK00700(港股)、USAAPL(美股)
        is_annals: 是否只看年报，1=是 0=否
        count: 数据条数
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取现金流量表: {symbol}")
    return safe_call(pysnowball.cash_flow, symbol, is_annals, count, response_format=response_format)


def get_cash_flow_v2(symbol: str, count: int = 10, region: str = "cn", type: str = "all", is_detail: bool = True, response_format: str = "json") -> dict:
    """获取现金流量表(详细版)

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)、HK00700(港股)、USAAPL(美股)
        count: 数据条数
        region: 地区 cn/us/hk
        type: 类型 all/Q4
        is_detail: 是否详细
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取现金流量表v2: {symbol}")
    return safe_call(pysnowball.cash_flow_v2, symbol, count, region, type, is_detail, response_format=response_format)


def get_balance(symbol: str, is_annals: int = 0, count: int = 10, response_format: str = "json") -> dict:
    """获取资产负债表

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)、HK00700(港股)、USAAPL(美股)
        is_annals: 是否只看年报，1=是 0=否
        count: 数据条数
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取资产负债表: {symbol}")
    return safe_call(pysnowball.balance, symbol, is_annals, count, response_format=response_format)


def get_balance_v2(symbol: str, count: int = 10, region: str = "cn", type: str = "all", is_detail: bool = True, response_format: str = "json") -> dict:
    """获取资产负债表(详细版)

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)、HK00700(港股)、USAAPL(美股)
        count: 数据条数
        region: 地区 cn/us/hk
        type: 类型 all/Q4
        is_detail: 是否详细
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取资产负债表v2: {symbol}")
    return safe_call(pysnowball.balance_v2, symbol, count, region, type, is_detail, response_format=response_format)


def get_income(symbol: str, is_annals: int = 0, count: int = 10, response_format: str = "json") -> dict:
    """获取利润表

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)、HK00700(港股)、USAAPL(美股)
        is_annals: 是否只看年报，1=是 0=否
        count: 数据条数
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取利润表: {symbol}")
    return safe_call(pysnowball.income, symbol, is_annals, count, response_format=response_format)


def get_income_v2(symbol: str, count: int = 10, region: str = "cn", type: str = "all", is_detail: bool = True, response_format: str = "json") -> dict:
    """获取利润表(详细版)

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)、HK00700(港股)、USAAPL(美股)
        count: 数据条数
        region: 地区 cn/us/hk
        type: 类型 all/Q4
        is_detail: 是否详细
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取利润表v2: {symbol}")
    return safe_call(pysnowball.income_v2, symbol, count, region, type, is_detail, response_format=response_format)


def get_indicator(symbol: str, is_annals: int = 0, count: int = 10, response_format: str = "json") -> dict:
    """获取财务指标

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)、HK00700(港股)、USAAPL(美股)
        is_annals: 是否只看年报，1=是 0=否
        count: 数据条数
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取财务指标: {symbol}")
    return safe_call(pysnowball.indicator, symbol, is_annals, count, response_format=response_format)


def get_indicator_v2(symbol: str, count: int = 10, region: str = "cn", type: str = "all", is_detail: bool = True, response_format: str = "json") -> dict:
    """获取财务指标(详细版)

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)、HK00700(港股)、USAAPL(美股)
        count: 数据条数
        region: 地区 cn/us/hk
        type: 类型 all/Q4
        is_detail: 是否详细
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取财务指标v2: {symbol}")
    return safe_call(pysnowball.indicator_v2, symbol, count, region, type, is_detail, response_format=response_format)


def get_business(symbol: str, is_annals: int = 0, count: int = 10, response_format: str = "json") -> dict:
    """获取主营业务构成

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)、HK00700(港股)、USAAPL(美股)
        is_annals: 是否只看年报，1=是 0=否
        count: 数据条数
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取主营业务构成: {symbol}")
    return safe_call(pysnowball.business, symbol, is_annals, count, response_format=response_format)


def register(mcp):
    """注册 MCP 工具"""
    annotations = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=True)
    mcp.tool(annotations=annotations)(get_cash_flow)
    mcp.tool(annotations=annotations)(get_cash_flow_v2)
    mcp.tool(annotations=annotations)(get_balance)
    mcp.tool(annotations=annotations)(get_balance_v2)
    mcp.tool(annotations=annotations)(get_income)
    mcp.tool(annotations=annotations)(get_income_v2)
    mcp.tool(annotations=annotations)(get_indicator)
    mcp.tool(annotations=annotations)(get_indicator_v2)
    mcp.tool(annotations=annotations)(get_business)
