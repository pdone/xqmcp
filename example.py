"""使用示例 - 展示如何调用 MCP 工具"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置 token
os.environ.setdefault("XUEQIU_TOKEN", "")

from mcp_server import mcp


async def example_direct_call():
    """直接调用工具函数示例"""
    print("=" * 50)
    print("直接调用工具函数示例")
    print("=" * 50)

    # 获取工具列表
    tools = mcp._tool_manager._tools
    print(f"\n可用工具数量: {len(tools)}")

    # 示例: 搜索股票
    print("\n1. 搜索股票 '贵州茅台':")
    try:
        from tools.suggest import search_stock
        result = search_stock("贵州茅台")
        print(f"   结果: {result}")
    except Exception as e:
        print(f"   错误: {e}")

    # 示例: 获取实时行情 (需要有效 token)
    print("\n2. 获取 SH600519 实时行情:")
    try:
        from tools.realtime import get_quote
        result = get_quote("SH600519")
        print(f"   结果: {result}")
    except Exception as e:
        print(f"   错误: {e}")


async def example_mcp_protocol():
    """通过 MCP 协议调用示例"""
    print("\n" + "=" * 50)
    print("MCP 协议调用示例")
    print("=" * 50)

    # 创建 MCP 客户端
    from mcp.client.session import ClientSession
    from mcp.client.streamable_http import streamablehttp_client

    # 这里需要服务器运行才能测试
    print("\n注意: 需要先启动服务器才能测试 MCP 协议调用")
    print("启动命令: python server.py")
    print("然后使用 MCP 客户端连接: http://localhost:8000/mcp")


async def main():
    print("pysnowball MCP Server 使用示例")
    print()

    # 检查 token
    token = os.environ.get("XUEQIU_TOKEN")
    if not token:
        print("警告: 未设置 XUEQIU_TOKEN 环境变量")
        print("部分功能可能无法使用")
        print()

    await example_direct_call()
    await example_mcp_protocol()

    print("\n" + "=" * 50)
    print("更多信息请参考 README.md")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
