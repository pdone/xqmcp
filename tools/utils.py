"""工具模块公共函数"""

import json
import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pysnowball")

# 响应字符限制（约 100KB，防止 MCP 响应过大）
CHARACTER_LIMIT = 100000


def convert_timestamps(data):
    """递归将毫秒时间戳转为可读日期字符串"""
    if isinstance(data, dict):
        for key, value in list(data.items()):
            if key == 'timestamp' and isinstance(value, (int, float)) and value > 1e12:
                data[key] = datetime.datetime.fromtimestamp(value / 1000).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, (dict, list)):
                convert_timestamps(value)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            data[i] = convert_timestamps(item)
    return data


def process_data(data):
    """统一数据处理入口"""
    return convert_timestamps(data)


def paginate(data, limit=None, offset=None):
    """对列表数据进行分页

    Args:
        data: 原始数据（应为 list）
        limit: 返回条数上限
        offset: 跳过条数

    Returns:
        分页后的数据，附带分页元信息
    """
    if not isinstance(data, list):
        return data

    total = len(data)
    start = offset or 0
    end = (start + limit) if limit else total
    items = data[start:end]

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": start,
        "has_more": end < total,
    }


def _truncate_data(data, limit):
    """截断数据使其 JSON 序列化不超过字符限制

    优先截断列表项，保持数据结构完整
    """
    json_str = json.dumps(data, ensure_ascii=False)
    if len(json_str) <= limit:
        return data, False

    # 如果是列表，逐步减少条数
    if isinstance(data, list) and len(data) > 1:
        truncated = data[:]
        while len(json.dumps(truncated, ensure_ascii=False)) > limit and len(truncated) > 1:
            truncated = truncated[:len(truncated) // 2]
        return truncated, True

    # 如果是字典，尝试截断其中的列表值
    if isinstance(data, dict):
        result = dict(data)
        for key, value in result.items():
            if isinstance(value, list) and len(value) > 1:
                while len(json.dumps(result, ensure_ascii=False)) > limit and len(value) > 1:
                    result[key] = value[:len(value) // 2]
                    value = result[key]
        return result, True

    return data, True


def _format_markdown(data):
    """将数据格式化为 Markdown 文本"""
    if data is None:
        return "无数据"

    if isinstance(data, dict):
        # 检查是否为分页格式
        if "items" in data and "total" in data:
            lines = [f"共 {data['total']} 条，显示 {len(data['items'])} 条"]
            if data.get("has_more"):
                lines.append(f"（还有更多数据，offset={data.get('offset', 0) + len(data['items'])}）")
            lines.append("")
            lines.append(_format_markdown(data["items"]))
            return "\n".join(lines)

        lines = []
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                lines.append(f"**{k}:**")
                lines.append(_format_markdown(v))
            else:
                lines.append(f"**{k}:** {v}")
        return "\n".join(lines)

    if isinstance(data, list):
        if not data:
            return "空列表"
        if isinstance(data[0], dict):
            # 表格格式
            keys = list(data[0].keys())
            lines = ["| " + " | ".join(keys) + " |"]
            lines.append("| " + " | ".join(["---"] * len(keys)) + " |")
            for row in data:
                vals = [str(row.get(k, "")) for k in keys]
                lines.append("| " + " | ".join(vals) + " |")
            return "\n".join(lines)
        return "\n".join(f"- {item}" for item in data)

    return str(data)


def make_response(data, error=None, response_format="json"):
    """统一返回格式

    Args:
        data: 响应数据
        error: 错误信息
        response_format: 响应格式 "json" 或 "markdown"
    """
    if error:
        result = {"success": False, "error": error, "data": None}
    else:
        processed = process_data(data)
        # 应用分页（如果 safe_call 传入了分页参数，数据已被包装）
        result = {"success": True, "error": None, "data": processed}

    # 字符限制截断
    result, truncated = _truncate_data(result, CHARACTER_LIMIT)
    if truncated:
        logger.warning("响应数据超过字符限制，已截断")
        if isinstance(result.get("data"), dict):
            result["data"]["_truncated"] = True
        elif result.get("data") is not None:
            result["data"] = {"_truncated": True, "original_type": type(result["data"]).__name__, "partial": result["data"]}

    # 格式转换
    if response_format == "markdown":
        if error:
            return f"❌ 错误: {error}"
        return _format_markdown(data)

    return result


def safe_call(func, *args, response_format="json", **kwargs):
    """安全调用 pysnowball 函数，捕获异常

    Args:
        func: 要调用的函数
        args: 位置参数
        response_format: 响应格式 "json" 或 "markdown"
        kwargs: 关键字参数
    """
    try:
        result = func(*args, **kwargs)
        return make_response(result, response_format=response_format)
    except ConnectionError as e:
        error_msg = "网络连接失败，请检查网络状态后重试"
        logger.error(f"调用 {func.__name__} 网络错误: {e}")
        return make_response(None, error=error_msg, response_format=response_format)
    except TimeoutError as e:
        error_msg = "请求超时，雪球服务器响应过慢，请稍后重试"
        logger.error(f"调用 {func.__name__} 超时: {e}")
        return make_response(None, error=error_msg, response_format=response_format)
    except Exception as e:
        error_msg = str(e)
        if "TOKEN" in error_msg or "token" in error_msg.lower():
            error_msg = "未设置雪球TOKEN。请设置环境变量 XUEQIU_TOKEN（获取方式：登录雪球网 → F12 → Application → Cookies → xq_a_token）"
        elif "403" in error_msg:
            error_msg = "访问被拒绝（403），TOKEN 可能已过期，请重新获取"
        elif "404" in error_msg:
            error_msg = "接口不存在（404），请检查股票代码格式是否正确"
        elif "500" in error_msg:
            error_msg = "雪球服务器内部错误（500），请稍后重试"
        elif "JSON" in error_msg or "json" in error_msg.lower():
            error_msg = "数据解析失败，返回的数据格式异常，请检查参数或稍后重试"
        logger.error(f"调用 {func.__name__} 失败: {error_msg}")
        return make_response(None, error=error_msg, response_format=response_format)
