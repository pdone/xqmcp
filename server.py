"""本地开发服务器

启动命令: python server.py
访问 Swagger: http://localhost:8000/docs
访问 MCP: http://localhost:8000/mcp (Streamable HTTP)
"""

import os
import inspect
import uvicorn
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.responses import HTMLResponse
from typing import Optional

import pysnowball

from tools import (
    realtime,
    finance,
    f10,
    capital,
    report,
    fund,
    index,
    bond,
    hkex,
    user,
    cube,
    suggest,
)

# 环境变量
XUEQIU_TOKEN = os.environ.get("XUEQIU_TOKEN", "")
API_TOKEN = os.environ.get("API_TOKEN", "")

# 设置雪球 token
if XUEQIU_TOKEN:
    pysnowball.set_token(XUEQIU_TOKEN)


# ============================================================
# API 认证
# ============================================================

async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """验证 API Key（当 API_TOKEN 不为空时启用）"""
    if not API_TOKEN:
        return  # 未设置 API_TOKEN，跳过验证
    if x_api_key != API_TOKEN:
        raise HTTPException(status_code=401, detail="无效的 API Key")


# ============================================================
# FastAPI 应用
# ============================================================

app = FastAPI(
    title="pysnowball MCP Server",
    description="雪球股票数据接口，提供 A 股/港股/美股的实时行情、财务数据、基金信息等。同时支持 MCP 协议和 REST API。",
    version="1.0.0",
)


# ============================================================
# 自动注册所有工具函数为 REST API 端点
# ============================================================

TOOL_GROUPS = {
    "realtime": ("实时行情", realtime),
    "finance": ("财务数据", finance),
    "f10": ("基本面", f10),
    "capital": ("资金流向", capital),
    "report": ("研报数据", report),
    "fund": ("基金数据", fund),
    "index": ("指数数据", index),
    "bond": ("债券数据", bond),
    "hkex": ("港股通", hkex),
    "user": ("用户数据", user),
    "cube": ("组合数据", cube),
    "suggest": ("搜索", suggest),
}


def register_endpoint(func, tag: str):
    """将工具函数注册为 FastAPI 端点"""
    func_name = func.__name__

    # 获取函数签名
    sig = inspect.signature(func)

    # 创建包装函数，保持原始函数名
    async def wrapper(api_key: str = Depends(verify_api_key), **kwargs):
        try:
            return func(**kwargs)
        except Exception as e:
            return {"error": str(e)}

    # 重建签名（排除 api_key 参数）
    new_params = []
    for name, param in sig.parameters.items():
        annotation = param.annotation if param.annotation != inspect.Parameter.empty else str
        default = param.default if param.default != inspect.Parameter.empty else ...
        new_params.append(inspect.Parameter(
            name, inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default=default, annotation=annotation
        ))
    wrapper.__signature__ = inspect.Signature(new_params)
    wrapper.__name__ = func_name
    wrapper.__qualname__ = func_name
    wrapper.__doc__ = func.__doc__

    # 注册路由
    app.post(
        f"/api/{func_name}",
        tags=[tag],
        summary=func_name,
        description=func.__doc__,
        name=func_name,
        dependencies=[Depends(verify_api_key)],
    )(wrapper)


# 遍历所有模块，注册每个函数
EXCLUDE_NAMES = {"register"}  # 排除的函数名

for group_name, (tag, module) in TOOL_GROUPS.items():
    for attr_name in dir(module):
        if attr_name.startswith("_") or attr_name in EXCLUDE_NAMES:
            continue
        func = getattr(module, attr_name)
        if callable(func):
            register_endpoint(func, tag)


# ============================================================
# MCP 端点
# ============================================================

@app.post("/api/mcp", tags=["MCP"], summary="MCP JSON-RPC 端点", dependencies=[Depends(verify_api_key)])
async def mcp_endpoint(request: dict):
    """MCP 协议端点，用于 Claude 等 AI 客户端调用"""
    return {"message": "请使用 MCP 客户端连接此端点", "protocol": "MCP Streamable HTTP"}


@app.get("/", tags=["首页"], include_in_schema=False)
async def root():
    return HTMLResponse("""
    <html>
        <head><title>pysnowball MCP Server</title></head>
        <body>
            <h1>pysnowball MCP Server</h1>
            <p>雪球股票数据服务器，支持 MCP 协议和 REST API</p>
            <h2>接口</h2>
            <ul>
                <li><a href="/docs">Swagger UI</a> - REST API 文档</li>
                <li><a href="/redoc">ReDoc</a> - API 文档（备用）</li>
                <li><strong>MCP 端点:</strong> <code>/mcp</code> (Streamable HTTP)</li>
            </ul>
            <h2>MCP 客户端配置</h2>
            <pre><code>{
  "mcpServers": {
    "pysnowball": {
      "url": "https://your-domain/mcp"
    }
  }
}</code></pre>
        </body>
    </html>
    """)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"启动服务器: http://localhost:{port}")
    print(f"Swagger UI: http://localhost:{port}/docs")
    print(f"MCP 端点: http://localhost:{port}/mcp (Streamable HTTP)")
    if API_TOKEN:
        print(f"API 认证: 已启用 (需要 x-api-key)")
    else:
        print(f"API 认证: 未启用")
    uvicorn.run(app, host="0.0.0.0", port=port)
