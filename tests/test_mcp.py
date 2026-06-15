"""测试 MCP 服务是否可用

使用 MCP 客户端 SDK 测试 Streamable HTTP 连接。
支持有状态和无状态两种模式。

用法:
    # 测试本地有状态模式
    python tests/test_mcp.py

    # 测试远程无状态模式（Vercel）
    python tests/test_mcp.py https://your-project.vercel.app/mcp
"""

import asyncio
import sys

# 修复 Windows 控制台编码
sys.stdout.reconfigure(encoding='utf-8')

from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def test_mcp(url: str = "http://localhost:8000/mcp"):
    """测试 MCP 服务连接

    Args:
        url: MCP 服务地址
    """
    print(f"连接 MCP 服务: {url}")
    print("-" * 50)

    async with streamablehttp_client(url) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            # 初始化
            await session.initialize()
            print("[OK] MCP 连接成功!")

            # 列出工具
            tools = await session.list_tools()
            print(f"\n[INFO] 可用工具数量: {len(tools.tools)}")
            print("\n工具列表:")
            for tool in tools.tools:
                desc = tool.description[:50] if tool.description else "无描述"
                print(f"  - {tool.name}: {desc}...")

            # 测试调用搜索工具
            print("\n[TEST] 测试调用 search_stock('贵州茅台'):")
            result = await session.call_tool("search_stock", {"q": "贵州茅台"})
            print(f"   结果: {result.content[0].text[:200]}...")

            # 测试获取行情
            print("\n[TEST] 测试调用 get_quote('SH600519'):")
            result = await session.call_tool("get_quote", {"symbol": "SH600519"})
            print(f"   结果: {result.content[0].text[:200]}...")

    print("\n" + "-" * 50)
    print("测试完成!")


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/mcp"
    asyncio.run(test_mcp(url))
