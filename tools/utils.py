"""工具模块公共函数"""

import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pysnowball")


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


def make_response(data, error=None):
    """统一返回格式"""
    if error:
        return {"success": False, "error": error, "data": None}
    return {"success": True, "error": None, "data": process_data(data)}


def safe_call(func, *args, **kwargs):
    """安全调用 pysnowball 函数，捕获异常"""
    try:
        result = func(*args, **kwargs)
        return make_response(result)
    except Exception as e:
        error_msg = str(e)
        # 优化 TOKEN 错误提示
        if "TOKEN" in error_msg or "token" in error_msg.lower():
            error_msg = "未设置雪球TOKEN。请设置环境变量 XUEQIU_TOKEN（获取方式：登录雪球网 → F12 → Application → Cookies → xq_a_token）"
        logger.error(f"调用 {func.__name__} 失败: {error_msg}")
        return make_response(None, error=error_msg)
