"""研报数据工具模块"""

import pysnowball
from tools.utils import safe_call, logger
from mcp.types import ToolAnnotations


def get_report(symbol: str, limit: int = 50, offset: int = 0, response_format: str = "json") -> dict:
    """获取研究报告

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
        limit: 返回条数上限，默认50
        offset: 跳过条数，默认0
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取研究报告: {symbol}")
    result = safe_call(pysnowball.report, symbol, response_format="json")
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


def get_earningforecast(symbol: str, limit: int = 50, offset: int = 0, response_format: str = "json") -> dict:
    """获取盈利预测

    Args:
        symbol: 股票代码，格式为 市场前缀+代码，如 SH600519(上海)、SZ000001(深圳)
        limit: 返回条数上限，默认50
        offset: 跳过条数，默认0
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取盈利预测: {symbol}")
    result = safe_call(pysnowball.earningforecast, symbol, response_format="json")
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
    mcp.tool(annotations=annotations)(get_report)
    mcp.tool(annotations=annotations)(get_earningforecast)
