from collections import defaultdict
from database.redis.database_redis import *

"""STATE INSTRUCTIONS
# 服务端 #
0: 关闭连接，具体原因见返回内容
1: 请求成功
2: 错误状态，具体原因见返回内容

# 客户端 #
w11: p2p
w12: p2g
w21: create one group
w22: add to one group

# 测试码 #
99999: return 'hello world'
"""
state_code = ['w11', 'w12', 'w21', 'w22', 'w99999']

ERROR_COUNT = 2

KEY_MAP = {}
VAL_MAP = {}


class Connector:
    def __init__(self, snow_key, request, client_address):
        self.snow_key = snow_key
        self.request = request
        self.client_address = ':'.join([str(i) for i in client_address])
        self.user_name = str(redis_handler.hget(REDIS_USER_SNOW_ID, snow_key))


class ConnectManager:
    connectors = defaultdict(dict)
    groups = defaultdict(dict)

    @classmethod
    def online(cls):
        return len(cls.connectors)

    @classmethod
    def clear(cls, name, key):
        try:
            cls.connectors[name].pop(key)
        except:
            pass

    @classmethod
    def add_connector(cls, name, key, value):
        cls.connectors[name][key] = value

    @classmethod
    def add_group(cls, name, key, value):
        # cls.groups[key].append(value)
        cls.groups[name][key] = value

    @classmethod
    def group_exist(cls, key):
        return key in cls.groups
