"""指数数据工具模块"""

import pysnowball
from tools.utils import safe_call, logger
from mcp.types import ToolAnnotations


def get_index_basic_info(index_code: str, response_format: str = "json") -> dict:
    """获取指数基本信息

    Args:
        index_code: 指数代码，如 000300(沪深300)、000001(上证指数)、399001(深证成指)
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取指数基本信息: {index_code}")
    return safe_call(pysnowball.index_basic_info, index_code, response_format=response_format)


def get_index_details_data(index_code: str, response_format: str = "json") -> dict:
    """获取指数详细数据

    Args:
        index_code: 指数代码，如 000300(沪深300)、000001(上证指数)、399001(深证成指)
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取指数详细数据: {index_code}")
    return safe_call(pysnowball.index_details_data, index_code, response_format=response_format)


def get_index_weight_top10(index_code: str, response_format: str = "json") -> dict:
    """获取指数前10大权重股

    Args:
        index_code: 指数代码，如 000300(沪深300)、000001(上证指数)、399001(深证成指)
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取指数前10权重: {index_code}")
    return safe_call(pysnowball.index_weight_top10, index_code, response_format=response_format)


def get_index_perf_7(index_code: str, response_format: str = "json") -> dict:
    """获取指数近7天表现

    Args:
        index_code: 指数代码，如 000300(沪深300)、000001(上证指数)、399001(深证成指)
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取指数7天表现: {index_code}")
    return safe_call(pysnowball.index_perf_7, index_code, response_format=response_format)


def get_index_perf_30(index_code: str, response_format: str = "json") -> dict:
    """获取指数近30天表现

    Args:
        index_code: 指数代码，如 000300(沪深300)、000001(上证指数)、399001(深证成指)
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取指数30天表现: {index_code}")
    return safe_call(pysnowball.index_perf_30, index_code, response_format=response_format)


def get_index_perf_90(index_code: str, response_format: str = "json") -> dict:
    """获取指数近90天表现

    Args:
        index_code: 指数代码，如 000300(沪深300)、000001(上证指数)、399001(深证成指)
        response_format: 响应格式 json/markdown
    """
    logger.info(f"获取指数90天表现: {index_code}")
    return safe_call(pysnowball.index_perf_90, index_code, response_format=response_format)


def register(mcp):
    """注册 MCP 工具"""
    annotations = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=True)
    mcp.tool(annotations=annotations)(get_index_basic_info)
    mcp.tool(annotations=annotations)(get_index_details_data)
    mcp.tool(annotations=annotations)(get_index_weight_top10)
    mcp.tool(annotations=annotations)(get_index_perf_7)
    mcp.tool(annotations=annotations)(get_index_perf_30)
    mcp.tool(annotations=annotations)(get_index_perf_90)
