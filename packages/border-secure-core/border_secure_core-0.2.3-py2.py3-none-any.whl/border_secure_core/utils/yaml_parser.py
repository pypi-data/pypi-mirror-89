# -*- coding:utf-8 -*-
from border_secure_core import decrypt_ciphertext
from border_secure_core.errors import RequestError
import requests
import yaml
import hmac
import hashlib


class YamlParser(object):
    def __init__(self, path):

        with open(path, 'r') as stream:
            loaded = yaml.safe_load(stream)

        self.loaded = loaded
        self.private_key = loaded['data']['private_key']
        self.salt = loaded['data']['salt']
        self.validate_api = loaded['data']['validate_api']
        self.public_domain = loaded['data']['public_domain']
        self.jsonrpc = loaded['data']['jsonrpc']

    def request_validate_api(self, ticket):
        r = requests.post(self.validate_api, json={'ticket': ticket})
        r.raise_for_status()
        return r.json()

    def decrypt(self, raw_data):
        if isinstance(raw_data, bytes):
            raw_data = raw_data.decode()

        res = decrypt_ciphertext(combined=raw_data, private_key=self.private_key)
        return res

    def signature(self, raw_data):
        if isinstance(raw_data, bytes):
            raw_data = raw_data.decode()

        return hmac.new(self.salt.encode(), raw_data.encode("utf-8"), hashlib.sha256).hexdigest()

    def error_page_redict(self, error_msg=''):
        return self.public_domain + '/error?desc=' + str(error_msg)

    def request_sso_jsonrpc(self, method, **kwargs):
        """发起sso调用请求

        ARGS:
            method(str):
                请求名称

        RETURNS:
            (dict|list)
                提取jsonrpc的result部分

                method:prepare_create_new_username  {'ciphertext':'xx'}

        RAISES:
            RequestError 调用异常/jsonrpc返回码异常

        EXAMPLES:

            >>> # 向sso请求指定uuid返回的加密用户名
            >>> self.request_sso_jsonrpc(method='prepare_create_new_username',sc='jumpserver',uuid='32ff95f1-9f9d-466a-8790-8db4fcd466bf')
            >>> {'ciphertext': 'WTOsO/LnEHSm6PKlQDoyPcpzUM2qjC4H.....'}

        """

        req_data = {
            "method": method,
            "jsonrpc": "2.0",
            "id": 0
        }
        req_data['params'] = (kwargs)

        try:
            r = requests.post(url=self.jsonrpc, json=req_data)
            resp = r.json()
        except Exception as e:
            print('请求{}异常 : {}'.format(self.jsonrpc, e))
            raise RequestError('请求{}异常 : {}'.format(self.jsonrpc, e))

        if resp.get('error'):
            raise RequestError('请求{}返回码异常 : {}'.format(self.jsonrpc, resp['error'].get('message')))

        return resp.get('result')

