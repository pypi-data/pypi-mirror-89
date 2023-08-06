# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import time

from Tea.exceptions import TeaException, UnretryableException
from Tea.request import TeaRequest
from Tea.core import TeaCore

from alibabacloud_tea_util.client import Client as UtilClient
from antchain_alipay_util.client import Client as AlipayUtilClient
from alibabacloud_rpc_util.client import Client as RPCUtilClient
from antchain_sdk_demo import models as demo_models
from alibabacloud_tea_util import models as util_models


class Client(object):
    def __init__(self, config, _endpoint=None, _region_id=None, _access_key_id=None, _access_key_secret=None,
                 _protocol=None, _user_agent=None, _read_timeout=None, _connect_timeout=None, _http_proxy=None,
                 _https_proxy=None, _socks_5proxy=None, _socks_5net_work=None, _no_proxy=None, _max_idle_conns=None,
                 _security_token=None):
        """
        Init client with Config

        @param config: config contains the necessary information to create a client
        """
        self._endpoint = _endpoint      # type: str
        self._region_id = _region_id    # type: str
        self._access_key_id = _access_key_id  # type: str
        self._access_key_secret = _access_key_secret  # type: str
        self._protocol = _protocol      # type: str
        self._user_agent = _user_agent  # type: str
        self._read_timeout = _read_timeout  # type: int
        self._connect_timeout = _connect_timeout  # type: int
        self._http_proxy = _http_proxy  # type: str
        self._https_proxy = _https_proxy  # type: str
        self._socks_5proxy = _socks_5proxy  # type: str
        self._socks_5net_work = _socks_5net_work  # type: str
        self._no_proxy = _no_proxy      # type: str
        self._max_idle_conns = _max_idle_conns  # type: int
        self._security_token = _security_token  # type: str
        if UtilClient.is_unset(config):
            raise TeaException({
                'code': 'ParameterMissing',
                'message': "'config' can not be unset"
            })
        self._access_key_id = config.access_key_id
        self._access_key_secret = config.access_key_secret
        self._security_token = config.security_token
        self._endpoint = config.endpoint
        self._protocol = config.protocol
        self._user_agent = config.user_agent
        self._read_timeout = config.read_timeout
        self._connect_timeout = config.connect_timeout
        self._http_proxy = config.http_proxy
        self._https_proxy = config.https_proxy
        self._no_proxy = config.no_proxy
        self._socks_5proxy = config.socks_5proxy
        self._socks_5net_work = config.socks_5net_work
        self._max_idle_conns = config.max_idle_conns

    def do_request(self, version, action, protocol, method, pathname, request, runtime):
        """
        Encapsulate the request and invoke the network

        @type action: str
        @param action: api name

        @type protocol: str
        @param protocol: http or https

        @type method: str
        @param method: e.g. GET

        @type pathname: str
        @param pathname: pathname of every api

        @type request: dict
        @param request: which contains request params

        @param runtime: which controls some details of call api, such as retry times

        @rtype: dict
        @return: the response
        """
        runtime.validate()
        _runtime = {
            'timeouted': 'retry',
            'readTimeout': UtilClient.default_number(runtime.read_timeout, self._read_timeout),
            'connectTimeout': UtilClient.default_number(runtime.connect_timeout, self._connect_timeout),
            'httpProxy': UtilClient.default_string(runtime.http_proxy, self._http_proxy),
            'httpsProxy': UtilClient.default_string(runtime.https_proxy, self._https_proxy),
            'noProxy': UtilClient.default_string(runtime.no_proxy, self._no_proxy),
            'maxIdleConns': UtilClient.default_number(runtime.max_idle_conns, self._max_idle_conns),
            'retry': {
                'retryable': runtime.autoretry,
                'maxAttempts': UtilClient.default_number(runtime.max_attempts, 3)
            },
            'backoff': {
                'policy': UtilClient.default_string(runtime.backoff_policy, 'no'),
                'period': UtilClient.default_number(runtime.backoff_period, 1)
            },
            'ignoreSSL': runtime.ignore_ssl
        }
        _last_request = None
        _last_exception = None
        _now = time.time()
        _retry_times = 0
        while TeaCore.allow_retry(_runtime.get('retry'), _retry_times, _now):
            if _retry_times > 0:
                _backoff_time = TeaCore.get_backoff_time(_runtime.get('backoff'), _retry_times)
                if _backoff_time > 0:
                    TeaCore.sleep(_backoff_time)
            _retry_times = _retry_times + 1
            try:
                _request = TeaRequest()
                _request.protocol = UtilClient.default_string(self._protocol, protocol)
                _request.method = method
                _request.pathname = pathname
                _request.query = {
                    'method': action,
                    'version': version,
                    'sign_type': 'HmacSHA1',
                    'req_time': AlipayUtilClient.get_timestamp(),
                    'req_msg_id': UtilClient.get_nonce(),
                    'access_key': self._access_key_id,
                    'charset': 'UTF-8',
                    'baseSdkVersion': 'Tea-SDK',
                    'sdkVersion': 'Tea-SDK-20201229'
                }
                if not UtilClient.empty(self._security_token):
                    _request.query['security_token'] = self._security_token
                _request.headers = {
                    'host': self._endpoint,
                    'user-agent': self.get_user_agent()
                }
                tmp = UtilClient.anyify_map_value(RPCUtilClient.query(request))
                _request.body = UtilClient.to_form_string(tmp)
                _request.headers['content-type'] = 'application/x-www-form-urlencoded'
                signed_param = TeaCore.merge(_request.query,
                    RPCUtilClient.query(request))
                _request.query['sign'] = AlipayUtilClient.get_signature(signed_param, self._access_key_secret)
                _last_request = _request
                _response = TeaCore.do_action(_request, _runtime)
                obj = UtilClient.read_as_json(_response.body)
                res = UtilClient.assert_as_map(obj)
                resp = UtilClient.assert_as_map(res.get('response'))
                if AlipayUtilClient.has_error(res):
                    raise TeaException({
                        'message': resp.get('result_msg'),
                        'data': resp,
                        'code': resp.get('result_code')
                    })
                return resp
            except Exception as e:
                if TeaCore.is_retryable(e):
                    _last_exception = e
                    continue
                raise e
        raise UnretryableException(_last_request, _last_exception)

    def get_user_agent(self):
        """
        Get user agent

        @rtype: str
        @return: user agent
        """
        user_agent = 'TeaClient/1.0.0'
        return UtilClient.get_user_agent(user_agent)

    def status_demo_gateway_check(self, request):
        """
        Description: Demo接口，返回当前服务器当前状态
        Summary: 检查服务状态
        """
        runtime = util_models.RuntimeOptions()
        return self.status_demo_gateway_check_ex(request, runtime)

    def status_demo_gateway_check_ex(self, request, runtime):
        """
        Description: Demo接口，返回当前服务器当前状态
        Summary: 检查服务状态
        """
        UtilClient.validate_model(request)
        return demo_models.StatusDemoGatewayCheckResponse().from_map(self.do_request('1.0', 'demo.gateway.check.status', 'HTTPS', 'POST', '/gateway.do', TeaCore.to_map(request), runtime))

    def echo_demo_gateway_check(self, request):
        """
        Description: Demo接口，返回当输入的值
        Summary: 返回输入值
        """
        runtime = util_models.RuntimeOptions()
        return self.echo_demo_gateway_check_ex(request, runtime)

    def echo_demo_gateway_check_ex(self, request, runtime):
        """
        Description: Demo接口，返回当输入的值
        Summary: 返回输入值
        """
        UtilClient.validate_model(request)
        return demo_models.EchoDemoGatewayCheckResponse().from_map(self.do_request('1.0', 'demo.gateway.check.echo', 'HTTPS', 'POST', '/gateway.do', TeaCore.to_map(request), runtime))
