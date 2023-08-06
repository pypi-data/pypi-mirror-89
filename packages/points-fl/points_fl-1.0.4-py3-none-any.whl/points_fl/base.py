from functools import wraps
from types import MethodType

import grpc

from points_fl.proto import (
    federated_learning_pb2,
    federated_learning_pb2_grpc,
    permission_pb2_grpc,
    permission_pb2,
    log_provider_pb2_grpc,
    inference_pb2_grpc,
)


def verify_login(cls):
    orig_getattribute = cls.__getattribute__

    def new_getattribute(self, name):
        res = orig_getattribute(self, name)
        # 判断除登录外的其他函数，如果还没有登录，则抛出异常
        if (
            name not in ["login", "admin_login"]
            and isinstance(res, MethodType)
            and orig_getattribute(self, "connected") is False
        ):
            raise BrokenPipeError("未登录")

        return res

    cls.__getattribute__ = new_getattribute
    return cls


def optimization_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        rp = func(*args, **kwargs)
        # 统计grpc接口返回值
        start_count = False
        rp_args = []
        for property in dir(rp):
            if property == "_extensions_by_number":
                start_count = True
                continue
            if start_count:
                rp_args.append(property)

        if len(rp_args) == 0:
            # 若返回为grpc response 无属性，则返回None
            return
        elif len(rp_args) == 1:
            # 若返回为grpc response 仅一个属性，则返回该属性值
            return getattr(rp, rp_args[0])
        else:
            # 若返回 grpc response 有多个属性，则返回response
            return rp

    return wrapper


@verify_login
class Base:
    """
    基类，创建连接，登录及关闭验证
    """

    def __init__(self, grpc_ip_address, flask_ip_address):
        self._grpc_ip_address = grpc_ip_address
        self._flask_ip_address = flask_ip_address
        self.connected = False
        self._token = None
        self._headers = {}

    def __enter__(self):
        # grpc channel 在调用时才真正建立连接
        self._channel = grpc.insecure_channel(self._grpc_ip_address)
        self._federated_learning_stub = federated_learning_pb2_grpc.FederatedLearningServiceStub(self._channel)
        self._permission_stub = permission_pb2_grpc.PermissionStub(self._channel)
        self._log_provider_stub = log_provider_pb2_grpc.LogProviderStub(self._channel)
        self._inference_stub = inference_pb2_grpc.InferenceStub(self._channel)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._channel.close()
        self.connected = False
        self._token = None

    def login(self, username, password):
        request = federated_learning_pb2.LoginRequest(username=username, password=password)
        try:
            response = self._federated_learning_stub.Login(request)
        except Exception as e:
            raise ConnectionError(f"建立连接失败，请检查ip，端口.  {e}")
        self._token = response.token
        self.connected = True
        self._headers = {"Authorization": f"bearer {self._token}"}

    def admin_login(self, username, password):
        request = permission_pb2.BackstageLoginRequest(username=username, password=password)
        response = self._permission_stub.BackstageLogin(request)
        self._token = response.token
        self.connected = True
