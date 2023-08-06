# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
try:
    from typing import List
except ImportError:
    pass


class Config(TeaModel):
    """
    Model for initing client
    """
    def __init__(self, access_key_id=None, access_key_secret=None, security_token=None, protocol=None,
                 read_timeout=None, connect_timeout=None, http_proxy=None, https_proxy=None, endpoint=None, no_proxy=None,
                 max_idle_conns=None, user_agent=None, socks_5proxy=None, socks_5net_work=None):
        # accesskey id
        self.access_key_id = access_key_id  # type: str
        # accesskey secret
        self.access_key_secret = access_key_secret  # type: str
        # security token
        self.security_token = security_token  # type: str
        # http protocol
        self.protocol = protocol        # type: str
        # read timeout
        self.read_timeout = read_timeout  # type: int
        # connect timeout
        self.connect_timeout = connect_timeout  # type: int
        # http proxy
        self.http_proxy = http_proxy    # type: str
        # https proxy
        self.https_proxy = https_proxy  # type: str
        # endpoint
        self.endpoint = endpoint        # type: str
        # proxy white list
        self.no_proxy = no_proxy        # type: str
        # max idle conns
        self.max_idle_conns = max_idle_conns  # type: int
        # user agent
        self.user_agent = user_agent    # type: str
        # socks5 proxy
        self.socks_5proxy = socks_5proxy  # type: str
        # socks5 network
        self.socks_5net_work = socks_5net_work  # type: str

    def validate(self):
        pass

    def to_map(self):
        result = {}
        if self.access_key_id is not None:
            result['accessKeyId'] = self.access_key_id
        if self.access_key_secret is not None:
            result['accessKeySecret'] = self.access_key_secret
        if self.security_token is not None:
            result['securityToken'] = self.security_token
        if self.protocol is not None:
            result['protocol'] = self.protocol
        if self.read_timeout is not None:
            result['readTimeout'] = self.read_timeout
        if self.connect_timeout is not None:
            result['connectTimeout'] = self.connect_timeout
        if self.http_proxy is not None:
            result['httpProxy'] = self.http_proxy
        if self.https_proxy is not None:
            result['httpsProxy'] = self.https_proxy
        if self.endpoint is not None:
            result['endpoint'] = self.endpoint
        if self.no_proxy is not None:
            result['noProxy'] = self.no_proxy
        if self.max_idle_conns is not None:
            result['maxIdleConns'] = self.max_idle_conns
        if self.user_agent is not None:
            result['userAgent'] = self.user_agent
        if self.socks_5proxy is not None:
            result['socks5Proxy'] = self.socks_5proxy
        if self.socks_5net_work is not None:
            result['socks5NetWork'] = self.socks_5net_work
        return result

    def from_map(self, map={}):
        if map.get('accessKeyId') is not None:
            self.access_key_id = map.get('accessKeyId')
        if map.get('accessKeySecret') is not None:
            self.access_key_secret = map.get('accessKeySecret')
        if map.get('securityToken') is not None:
            self.security_token = map.get('securityToken')
        if map.get('protocol') is not None:
            self.protocol = map.get('protocol')
        if map.get('readTimeout') is not None:
            self.read_timeout = map.get('readTimeout')
        if map.get('connectTimeout') is not None:
            self.connect_timeout = map.get('connectTimeout')
        if map.get('httpProxy') is not None:
            self.http_proxy = map.get('httpProxy')
        if map.get('httpsProxy') is not None:
            self.https_proxy = map.get('httpsProxy')
        if map.get('endpoint') is not None:
            self.endpoint = map.get('endpoint')
        if map.get('noProxy') is not None:
            self.no_proxy = map.get('noProxy')
        if map.get('maxIdleConns') is not None:
            self.max_idle_conns = map.get('maxIdleConns')
        if map.get('userAgent') is not None:
            self.user_agent = map.get('userAgent')
        if map.get('socks5Proxy') is not None:
            self.socks_5proxy = map.get('socks5Proxy')
        if map.get('socks5NetWork') is not None:
            self.socks_5net_work = map.get('socks5NetWork')
        return self


class DemoClass(TeaModel):
    def __init__(self, some_string=None, some_date=None, some_boolean=None, some_int=None, some_list=None):
        # 字符串测试
        self.some_string = some_string  # type: str
        # 日期测试
        self.some_date = some_date      # type: str
        # Boolean测试
        self.some_boolean = some_boolean  # type: bool
        # 整数测试
        self.some_int = some_int        # type: int
        # 列表测试
        self.some_list = some_list      # type: List[str]

    def validate(self):
        if self.some_date is not None:
            self.validate_pattern(self.some_date, 'some_date', '\\d{4}[-]\\d{1,2}[-]\\d{1,2}[T]\\d{2}:\\d{2}:\\d{2}[Z]')

    def to_map(self):
        result = {}
        if self.some_string is not None:
            result['someString'] = self.some_string
        if self.some_date is not None:
            result['someDate'] = self.some_date
        if self.some_boolean is not None:
            result['someBoolean'] = self.some_boolean
        if self.some_int is not None:
            result['someInt'] = self.some_int
        if self.some_list is not None:
            result['someList'] = self.some_list
        return result

    def from_map(self, map={}):
        if map.get('someString') is not None:
            self.some_string = map.get('someString')
        if map.get('someDate') is not None:
            self.some_date = map.get('someDate')
        if map.get('someBoolean') is not None:
            self.some_boolean = map.get('someBoolean')
        if map.get('someInt') is not None:
            self.some_int = map.get('someInt')
        if map.get('someList') is not None:
            self.some_list = map.get('someList')
        return self


class AnotherClass(TeaModel):
    def __init__(self, bar=None, ref=None, ref_list=None):
        # 测试字段
        self.bar = bar                  # type: str
        # 引用字段
        self.ref = ref                  # type: DemoClass
        # 列表引用Struct
        self.ref_list = ref_list        # type: List[DemoClass]

    def validate(self):
        if self.ref:
            self.ref.validate()
        if self.ref_list:
            for k in self.ref_list:
                if k:
                    k.validate()

    def to_map(self):
        result = {}
        if self.bar is not None:
            result['bar'] = self.bar
        if self.ref is not None:
            result['ref'] = self.ref.to_map()
        result['refList'] = []
        if self.ref_list is not None:
            for k in self.ref_list:
                result['refList'].append(k.to_map() if k else None)
        return result

    def from_map(self, map={}):
        if map.get('bar') is not None:
            self.bar = map.get('bar')
        if map.get('ref') is not None:
            temp_model = DemoClass()
            self.ref = temp_model.from_map(map['ref'])
        self.ref_list = []
        if map.get('refList') is not None:
            for k in map.get('refList'):
                temp_model = DemoClass()
                self.ref_list.append(temp_model.from_map(k))
        return self


class StatusDemoGatewayCheckRequest(TeaModel):
    def __init__(self, auth_token=None, product_instance_id=None, region_name=None, aaaa=None, same=None):
        self.auth_token = auth_token    # type: str
        self.product_instance_id = product_instance_id  # type: str
        self.region_name = region_name  # type: str
        # ffff
        self.aaaa = aaaa                # type: int
        # ddddd
        self.same = same                # type: List[DemoClass]

    def validate(self):
        if self.same:
            for k in self.same:
                if k:
                    k.validate()

    def to_map(self):
        result = {}
        if self.auth_token is not None:
            result['auth_token'] = self.auth_token
        if self.product_instance_id is not None:
            result['product_instance_id'] = self.product_instance_id
        if self.region_name is not None:
            result['region_name'] = self.region_name
        if self.aaaa is not None:
            result['aaaa'] = self.aaaa
        result['same'] = []
        if self.same is not None:
            for k in self.same:
                result['same'].append(k.to_map() if k else None)
        return result

    def from_map(self, map={}):
        if map.get('auth_token') is not None:
            self.auth_token = map.get('auth_token')
        if map.get('product_instance_id') is not None:
            self.product_instance_id = map.get('product_instance_id')
        if map.get('region_name') is not None:
            self.region_name = map.get('region_name')
        if map.get('aaaa') is not None:
            self.aaaa = map.get('aaaa')
        self.same = []
        if map.get('same') is not None:
            for k in map.get('same'):
                temp_model = DemoClass()
                self.same.append(temp_model.from_map(k))
        return self


class StatusDemoGatewayCheckResponse(TeaModel):
    def __init__(self, req_msg_id=None, result_code=None, result_msg=None):
        self.req_msg_id = req_msg_id    # type: str
        self.result_code = result_code  # type: str
        self.result_msg = result_msg    # type: str

    def validate(self):
        pass

    def to_map(self):
        result = {}
        if self.req_msg_id is not None:
            result['req_msg_id'] = self.req_msg_id
        if self.result_code is not None:
            result['result_code'] = self.result_code
        if self.result_msg is not None:
            result['result_msg'] = self.result_msg
        return result

    def from_map(self, map={}):
        if map.get('req_msg_id') is not None:
            self.req_msg_id = map.get('req_msg_id')
        if map.get('result_code') is not None:
            self.result_code = map.get('result_code')
        if map.get('result_msg') is not None:
            self.result_msg = map.get('result_msg')
        return self


class EchoDemoGatewayCheckRequest(TeaModel):
    def __init__(self, auth_token=None, product_instance_id=None, region_name=None):
        self.auth_token = auth_token    # type: str
        self.product_instance_id = product_instance_id  # type: str
        self.region_name = region_name  # type: str

    def validate(self):
        pass

    def to_map(self):
        result = {}
        if self.auth_token is not None:
            result['auth_token'] = self.auth_token
        if self.product_instance_id is not None:
            result['product_instance_id'] = self.product_instance_id
        if self.region_name is not None:
            result['region_name'] = self.region_name
        return result

    def from_map(self, map={}):
        if map.get('auth_token') is not None:
            self.auth_token = map.get('auth_token')
        if map.get('product_instance_id') is not None:
            self.product_instance_id = map.get('product_instance_id')
        if map.get('region_name') is not None:
            self.region_name = map.get('region_name')
        return self


class EchoDemoGatewayCheckResponse(TeaModel):
    def __init__(self, req_msg_id=None, result_code=None, result_msg=None, ddd=None):
        self.req_msg_id = req_msg_id    # type: str
        self.result_code = result_code  # type: str
        self.result_msg = result_msg    # type: str
        # aaa
        self.ddd = ddd                  # type: int

    def validate(self):
        pass

    def to_map(self):
        result = {}
        if self.req_msg_id is not None:
            result['req_msg_id'] = self.req_msg_id
        if self.result_code is not None:
            result['result_code'] = self.result_code
        if self.result_msg is not None:
            result['result_msg'] = self.result_msg
        if self.ddd is not None:
            result['ddd'] = self.ddd
        return result

    def from_map(self, map={}):
        if map.get('req_msg_id') is not None:
            self.req_msg_id = map.get('req_msg_id')
        if map.get('result_code') is not None:
            self.result_code = map.get('result_code')
        if map.get('result_msg') is not None:
            self.result_msg = map.get('result_msg')
        if map.get('ddd') is not None:
            self.ddd = map.get('ddd')
        return self
