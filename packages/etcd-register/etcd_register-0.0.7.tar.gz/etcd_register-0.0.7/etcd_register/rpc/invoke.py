import json

import grpc

from etcd_register.proto import rpc_pb2, rpc_pb2_grpc
from etcd_register.util.config import Config


class RpcClient(object):
    conf = None

    def __init__(self, config):
        self.conf = Config.get_config(config)

    @staticmethod
    def encode(data):
        return json.dumps(data).encode('utf-8')

    @staticmethod
    def decode(data):
        return data.decode('utf-8')

    def invoke(self, service, method, args=None, version='v1', origin=False):
        try:
            addr = self.conf.get('rpc')
            channel = grpc.insecure_channel(addr)
            stub = rpc_pb2_grpc.RpcServiceStub(channel)
            request = rpc_pb2.Args()
            request.version = version
            request.service = service
            request.method = method
            request.args = args
            response = stub.Invoke(request)
            if origin:
                return Response(response.code, response.resultJson, response.msg)
            data = response.resultJson.decode('utf-8')
            return Response(response.code, data, response.msg)
        except Exception as e:
            return Response(101, None, str(e))


class Response(object):
    code = None
    data = None
    msg = None

    def __init__(self, code, data, msg):
        self.code = code
        self.data = data
        self.msg = msg

    def marshal(self):
        return {"code": self.code, "data": self.data, "msg": self.msg}
