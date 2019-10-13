from pyws import Pyws
from pyws.route import route
from pyws.public import AuthenticationError, ERROR_FLAG
from pyws.middlewares import DaemonMiddleware, RadioMiddleware, DataMiddleware
from pyws.connector import ConnectManager
import json

"""
每个开发人员应可以创建自己的数据字段
那么我就又需要类似一种field的机制咯，这玩意该怎么写呀
"""  # todo


# 单点测试
@route('/p2p/test/example/1')
def p2p_test_example_1(request, data):
    """
    Client Code:
    ws =new WebSocket("ws://127.0.0.1:8866/p2p/test/example/1");
    ws.onmessage = function (ev) {
        console.log(JSON.parse(ev.data));
    }
    ws.onclose = function (ev) {
        console.log('断开连接')
    }
    ws.send('hello world')
    """
    print('Has Receive: ', data)
    return data + ' - data from Pyws'


# 点对点交互
@route('/p2p/test/example/2')
def p2p_test_example_2(request, data):
    """
    Client Code:
    ws =new WebSocket("ws://127.0.0.1:8866/p2p/test/example/2");
    ws.onmessage = function (ev) {
        console.log(JSON.parse(ev.data));
    }
    ws.onclose = function (ev) {
        console.log('断开连接')
    }
    ws.send(JSON.stringify({'name': 'xxx', 'msg': 'xxx'}))
    """
    data = json.loads(data)
    if 'name' in data and 'msg' in data:
        if ConnectManager.send_to_connector(data['name'], data['msg']):
            msg = {'state': 1, 'msg': 'success'}
        else:
            msg = {'state': 0, 'msg': '用户不存在或系统内部异常'}
    else:
        request.ws_send({'state': 0, 'msg': '请求数据参数错误'})
        msg = ERROR_FLAG
    return msg


# 点对多交互


# 广播轮询
class Radio(RadioMiddleware):
    def process_data(cls):
        return 'Hello, Welcome To Pysw'


@route('/radio/test/example/4')
def radio_test_example_4(request, data):
    """Client Code:
    ws =new WebSocket("ws://127.0.0.1:8866/radio/test/example/4");
    ws.onmessage = function (ev) {
        console.log(JSON.parse(ev.data));
    }
    ws.onclose = function (ev) {
        console.log('断开连接')
    }
    """


# 加入验证机制
class AuthenticationMiddleware(DaemonMiddleware):

    def process_input(self, request, input_msg):
        json_data = json.loads(input_msg)
        if 'name' not in json_data:
            raise AuthenticationError
        return str(json_data['name'])


# 加入数据处理
class DataProcessMiddleware(DataMiddleware):

    def process_input(self, request, input_msg):
        json_data = json.loads(input_msg)
        if 'name' not in json_data:
            raise AuthenticationError
        return str(json_data['name'])


if __name__ == '__main__':
    test = Pyws(__name__)
    # test.add_middleware([CookieMiddleware, Radio])
    # test.add_middleware(Radio)
    test.serve_forever()

"""
ws =new WebSocket("ws://127.0.0.1:8866");
ws.onmessage = function (ev) {
    console.log(JSON.parse(ev.data));
}
ws.onclose = function (ev) {
    console.log('断开连接')
}
"""
