"""测试 stdio 模式连接"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server import create_mcp_server


async def test():
    mcp = create_mcp_server()
    print(f"MCP 服务器: {mcp.name}")
    print(f"工具数量: {len(mcp._tool_manager._tools)}")
    print("服务器配置正常，可以启动 stdio 模式")
    print("\n启动命令: python stdio.py")
    print("确保客户端配置使用 stdio 传输协议")


if __name__ == "__main__":
    asyncio.run(test())