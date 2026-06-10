"""财务数据工具模块"""

import pysnowball


def get_cash_flow(symbol: str, is_annals: int = 0, count: int = 10) -> dict:
    """获取现金流量表

    Args:
        symbol: 股票代码
        is_annals: 是否只看年报，1=是 0=否
        count: 数据条数
    """
    return pysnowball.cash_flow(symbol, is_annals, count)


def get_cash_flow_v2(symbol: str, count: int = 10, region: str = "cn", type: str = "all", is_detail: bool = True) -> dict:
    """获取现金流量表(详细版)

    Args:
        symbol: 股票代码
        count: 数据条数
        region: 地区 cn/us/hk
        type: 类型 all/Q4
        is_detail: 是否详细
    """
    return pysnowball.cash_flow_v2(symbol, count, region, type, is_detail)


def get_balance(symbol: str, is_annals: int = 0, count: int = 10) -> dict:
    """获取资产负债表

    Args:
        symbol: 股票代码
        is_annals: 是否只看年报，1=是 0=否
        count: 数据条数
    """
    return pysnowball.balance(symbol, is_annals, count)


def get_balance_v2(symbol: str, count: int = 10, region: str = "cn", type: str = "all", is_detail: bool = True) -> dict:
    """获取资产负债表(详细版)

    Args:
        symbol: 股票代码
        count: 数据条数
        region: 地区 cn/us/hk
        type: 类型 all/Q4
        is_detail: 是否详细
    """
    return pysnowball.balance_v2(symbol, count, region, type, is_detail)


def get_income(symbol: str, is_annals: int = 0, count: int = 10) -> dict:
    """获取利润表

    Args:
        symbol: 股票代码
        is_annals: 是否只看年报，1=是 0=否
        count: 数据条数
    """
    return pysnowball.income(symbol, is_annals, count)


def get_income_v2(symbol: str, count: int = 10, region: str = "cn", type: str = "all", is_detail: bool = True) -> dict:
    """获取利润表(详细版)

    Args:
        symbol: 股票代码
        count: 数据条数
        region: 地区 cn/us/hk
        type: 类型 all/Q4
        is_detail: 是否详细
    """
    return pysnowball.income_v2(symbol, count, region, type, is_detail)


def get_indicator(symbol: str, is_annals: int = 0, count: int = 10) -> dict:
    """获取财务指标

    Args:
        symbol: 股票代码
        is_annals: 是否只看年报，1=是 0=否
        count: 数据条数
    """
    return pysnowball.indicator(symbol, is_annals, count)


def get_indicator_v2(symbol: str, count: int = 10, region: str = "cn", type: str = "all", is_detail: bool = True) -> dict:
    """获取财务指标(详细版)

    Args:
        symbol: 股票代码
        count: 数据条数
        region: 地区 cn/us/hk
        type: 类型 all/Q4
        is_detail: 是否详细
    """
    return pysnowball.indicator_v2(symbol, count, region, type, is_detail)


def get_business(symbol: str, is_annals: int = 0, count: int = 10) -> dict:
    """获取主营业务构成

    Args:
        symbol: 股票代码
        is_annals: 是否只看年报，1=是 0=否
        count: 数据条数
    """
    return pysnowball.business(symbol, is_annals, count)


def register(mcp):
    """注册 MCP 工具"""
    mcp.tool()(get_cash_flow)
    mcp.tool()(get_cash_flow_v2)
    mcp.tool()(get_balance)
    mcp.tool()(get_balance_v2)
    mcp.tool()(get_income)
    mcp.tool()(get_income_v2)
    mcp.tool()(get_indicator)
    mcp.tool()(get_indicator_v2)
    mcp.tool()(get_business)
