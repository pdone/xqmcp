"""组合数据工具模块

注意：组合相关工具（get_nav_daily, get_rebalancing_history, get_rebalancing_current, get_quote_current）
因雪球API问题已移除。这些工具需要真实的雪球组合代码（ZH开头），且当前返回数据异常。
"""

from mcp.types import ToolAnnotations


def register(mcp):
    """注册 MCP 工具"""
    # 组合相关工具已移除，暂无可注册的工具
    pass
