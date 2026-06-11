"""本地 stdio 模式 MCP 服务器

适用于 Claude Desktop、Cursor 等支持 stdio 传输的 MCP 客户端。

启动方式: python stdio_server.py
"""

import os
import sys

# 确保项目根目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_server import create_mcp_server


def main():
    mcp = create_mcp_server()
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
