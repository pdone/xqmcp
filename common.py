"""公共模块 - REST API 和 MCP 共享的逻辑"""

import os
import inspect
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
# 工具分组配置
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


# ============================================================
# REST API 端点注册
# ============================================================

def register_endpoint(app: FastAPI, func, tag: str):
    """将工具函数注册为 FastAPI 端点"""
    func_name = func.__name__

    # 获取函数签名
    sig = inspect.signature(func)

    # 创建包装函数
    async def wrapper(api_key: str = Depends(verify_api_key), **kwargs):
        try:
            return func(**kwargs)
        except Exception as e:
            return {"success": False, "error": str(e), "data": None}

    # 重建签名
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


def register_all_endpoints(app: FastAPI):
    """注册所有工具函数为 REST API 端点"""
    EXCLUDE_NAMES = {"register"}

    for group_name, (tag, module) in TOOL_GROUPS.items():
        for attr_name in dir(module):
            if attr_name.startswith("_") or attr_name in EXCLUDE_NAMES:
                continue
            func = getattr(module, attr_name)
            if callable(func):
                register_endpoint(app, func, tag)


# ============================================================
# 首页 HTML
# ============================================================

ROOT_HTML = """
<html>
    <head><title>pysnowball MCP Server</title></head>
    <body>
        <h1>pysnowball MCP Server</h1>
        <p>雪球股票数据服务器，支持 MCP 协议和 REST API</p>
        <h2>接口</h2>
        <ul>
            <li><a href="/docs">Swagger UI</a> - REST API 文档</li>
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
"""
