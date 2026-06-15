"""测试脚本 - 验证 MCP 服务器导入和工具注册"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """测试导入"""
    print("[1/3] 测试导入...")
    try:
        from mcp_server import mcp
        print("  OK - mcp_server 导入成功")
    except Exception as e:
        print(f"  FAIL - {e}")
        return False
    return True


def test_tools():
    """测试工具注册"""
    print("[2/3] 测试工具注册...")
    try:
        from mcp_server import mcp
        tools = mcp._tool_manager._tools
        count = len(tools)
        print(f"  OK - 已注册 {count} 个工具")

        # 核心工具列表（每个分类至少一个代表）
        expected_tools = [
            "get_quote",           # 实时行情
            "get_balance",         # 财务数据
            "get_income",          # 财务数据
            "get_fund_detail",     # 基金数据
            "search_stock",        # 搜索
            "get_convertible_bond", # 债券数据
            "get_capital_flow",    # 资金流向
        ]

        for tool in expected_tools:
            if tool in tools:
                print(f"    OK - {tool}")
            else:
                print(f"    MISSING - {tool}")
                return False

    except Exception as e:
        print(f"  FAIL - {e}")
        return False
    return True


def test_app():
    """测试 ASGI 应用创建"""
    print("[3/3] 测试 ASGI 应用...")
    try:
        from mcp_server import mcp
        app = mcp.streamable_http_app()
        print(f"  OK - 应用类型: {type(app).__name__}")
    except Exception as e:
        print(f"  FAIL - {e}")
        return False
    return True


if __name__ == "__main__":
    print("=" * 50)
    print("pysnowball MCP Server 测试")
    print("=" * 50)
    print()

    results = []
    results.append(test_imports())
    results.append(test_tools())
    results.append(test_app())

    print()
    print("=" * 50)
    if all(results):
        print("所有测试通过!")
    else:
        print("部分测试失败")
    print("=" * 50)
