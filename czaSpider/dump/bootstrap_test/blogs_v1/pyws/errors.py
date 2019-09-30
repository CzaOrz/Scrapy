class AuthenticationError(Exception):
    """Cookie认证失败"""


class WebSocketProtocolError(Exception):
    """协议认证失败"""


class OutputTypeError(Exception):
    """输出类型错误"""


class InvalidPath(Exception):
    """路径错误"""


class MiddlewareError(Exception):
    """中间件错误"""
