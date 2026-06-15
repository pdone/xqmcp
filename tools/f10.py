"""F10 基本面工具模块"""

import pysnowball
from tools.utils import safe_call, logger
from mcp.types import ToolAnnotations


def get_skholderchg(symbol: str, limit: int = 50, offset: int = 0, response_format: str = "json") -> dict:
    """获取股东增减持

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
        limit: 返回条数上限，默认50
        offset: 跳过条数，默认0
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取股东增减持: {symbol}")
    result = safe_call(pysnowball.skholderchg, symbol, response_format="json")
    if result.get("success") and isinstance(result.get("data"), list):
        data = result["data"]
        total = len(data)
        result["data"] = {
            "items": data[offset:offset + limit] if limit else data[offset:],
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total if limit else False,
        }
    if response_format == "markdown":
        from tools.utils import _format_markdown
        return _format_markdown(result.get("data"))
    return result


def get_skholder(symbol: str, response_format: str = "json") -> dict:
    """获取股东信息

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取股东信息: {symbol}")
    result = safe_call(pysnowball.skholder, symbol, response_format="json")
    if response_format == "markdown":
        from tools.utils import _format_markdown
        return _format_markdown(result.get("data"))
    return result


def get_main_indicator(symbol: str, response_format: str = "json") -> dict:
    """获取主要指标

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取主要指标: {symbol}")
    result = safe_call(pysnowball.main_indicator, symbol, response_format="json")
    if response_format == "markdown":
        from tools.utils import _format_markdown
        return _format_markdown(result.get("data"))
    return result


def get_industry(symbol: str, response_format: str = "json") -> dict:
    """获取行业信息

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取行业信息: {symbol}")
    result = safe_call(pysnowball.industry, symbol, response_format="json")
    if response_format == "markdown":
        from tools.utils import _format_markdown
        return _format_markdown(result.get("data"))
    return result


def get_holders(symbol: str, limit: int = 50, offset: int = 0, response_format: str = "json") -> dict:
    """获取股东人数

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
        limit: 返回条数上限，默认50
        offset: 跳过条数，默认0
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取股东人数: {symbol}")
    result = safe_call(pysnowball.holders, symbol, response_format="json")
    if result.get("success") and isinstance(result.get("data"), list):
        data = result["data"]
        total = len(data)
        result["data"] = {
            "items": data[offset:offset + limit] if limit else data[offset:],
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total if limit else False,
        }
    if response_format == "markdown":
        from tools.utils import _format_markdown
        return _format_markdown(result.get("data"))
    return result


def get_bonus(symbol: str, limit: int = 50, offset: int = 0, response_format: str = "json") -> dict:
    """获取分红送转

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
        limit: 返回条数上限，默认50
        offset: 跳过条数，默认0
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取分红送转: {symbol}")
    result = safe_call(pysnowball.bonus, symbol, response_format="json")
    if result.get("success") and isinstance(result.get("data"), list):
        data = result["data"]
        total = len(data)
        result["data"] = {
            "items": data[offset:offset + limit] if limit else data[offset:],
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total if limit else False,
        }
    if response_format == "markdown":
        from tools.utils import _format_markdown
        return _format_markdown(result.get("data"))
    return result


def get_org_holding_change(symbol: str, limit: int = 50, offset: int = 0, response_format: str = "json") -> dict:
    """获取机构持仓变动

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
        limit: 返回条数上限，默认50
        offset: 跳过条数，默认0
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取机构持仓变动: {symbol}")
    result = safe_call(pysnowball.org_holding_change, symbol, response_format="json")
    if result.get("success") and isinstance(result.get("data"), list):
        data = result["data"]
        total = len(data)
        result["data"] = {
            "items": data[offset:offset + limit] if limit else data[offset:],
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total if limit else False,
        }
    if response_format == "markdown":
        from tools.utils import _format_markdown
        return _format_markdown(result.get("data"))
    return result


def get_industry_compare(symbol: str, response_format: str = "json") -> dict:
    """获取行业对比

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取行业对比: {symbol}")
    result = safe_call(pysnowball.industry_compare, symbol, response_format="json")
    if response_format == "markdown":
        from tools.utils import _format_markdown
        return _format_markdown(result.get("data"))
    return result


def get_business_analysis(symbol: str, response_format: str = "json") -> dict:
    """获取经营分析

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取经营分析: {symbol}")
    result = safe_call(pysnowball.business_analysis, symbol, response_format="json")
    if response_format == "markdown":
        from tools.utils import _format_markdown
        return _format_markdown(result.get("data"))
    return result


def get_shareschg(symbol: str, limit: int = 50, offset: int = 0, response_format: str = "json") -> dict:
    """获取股本变动

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
        limit: 返回条数上限，默认50
        offset: 跳过条数，默认0
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取股本变动: {symbol}")
    result = safe_call(pysnowball.shareschg, symbol, response_format="json")
    if result.get("success") and isinstance(result.get("data"), list):
        data = result["data"]
        total = len(data)
        result["data"] = {
            "items": data[offset:offset + limit] if limit else data[offset:],
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total if limit else False,
        }
    if response_format == "markdown":
        from tools.utils import _format_markdown
        return _format_markdown(result.get("data"))
    return result


def get_top_holders(symbol: str, limit: int = 50, offset: int = 0, response_format: str = "json") -> dict:
    """获取十大股东

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
        limit: 返回条数上限，默认50
        offset: 跳过条数，默认0
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取十大股东: {symbol}")
    result = safe_call(pysnowball.top_holders, symbol, response_format="json")
    if result.get("success") and isinstance(result.get("data"), list):
        data = result["data"]
        total = len(data)
        result["data"] = {
            "items": data[offset:offset + limit] if limit else data[offset:],
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total if limit else False,
        }
    if response_format == "markdown":
        from tools.utils import _format_markdown
        return _format_markdown(result.get("data"))
    return result


def register(mcp):
    """注册 MCP 工具"""
    annotations = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=True)
    mcp.tool(annotations=annotations)(get_skholderchg)
    mcp.tool(annotations=annotations)(get_skholder)
    mcp.tool(annotations=annotations)(get_main_indicator)
    mcp.tool(annotations=annotations)(get_industry)
    mcp.tool(annotations=annotations)(get_holders)
    mcp.tool(annotations=annotations)(get_bonus)
    mcp.tool(annotations=annotations)(get_org_holding_change)
    mcp.tool(annotations=annotations)(get_industry_compare)
    mcp.tool(annotations=annotations)(get_business_analysis)
    mcp.tool(annotations=annotations)(get_shareschg)
    mcp.tool(annotations=annotations)(get_top_holders)
