"""指数数据工具模块"""

import pysnowball


def get_index_basic_info(index_code: str) -> dict:
    """获取指数基本信息

    Args:
        index_code: 指数代码，如 000300
    """
    return pysnowball.index_basic_info(index_code)


def get_index_details_data(index_code: str) -> dict:
    """获取指数详细数据

    Args:
        index_code: 指数代码
    """
    return pysnowball.index_details_data(index_code)


def get_index_weight_top10(index_code: str) -> dict:
    """获取指数前10大权重股

    Args:
        index_code: 指数代码
    """
    return pysnowball.index_weight_top10(index_code)


def get_index_perf_7(index_code: str) -> dict:
    """获取指数近7天表现

    Args:
        index_code: 指数代码
    """
    return pysnowball.index_perf_7(index_code)


def get_index_perf_30(index_code: str) -> dict:
    """获取指数近30天表现

    Args:
        index_code: 指数代码
    """
    return pysnowball.index_perf_30(index_code)


def get_index_perf_90(index_code: str) -> dict:
    """获取指数近90天表现

    Args:
        index_code: 指数代码
    """
    return pysnowball.index_perf_90(index_code)


def register(mcp):
    """注册 MCP 工具"""
    mcp.tool()(get_index_basic_info)
    mcp.tool()(get_index_details_data)
    mcp.tool()(get_index_weight_top10)
    mcp.tool()(get_index_perf_7)
    mcp.tool()(get_index_perf_30)
    mcp.tool()(get_index_perf_90)
