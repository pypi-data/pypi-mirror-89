"""
by tacey@XARC on 20-10-30
"""

import logging
import threading
from urllib.parse import urljoin
from functools import wraps
from requests import Session
from xacs.common.exceptions import XACSClientException
from xacs.common.token import decode_token
from xacs.common.client import XACSClientSingle

logger = logging.getLogger(__file__)

get_user_token = XACSClientSingle.get_user_token

get_app_token = XACSClientSingle.get_app_token


class DataCenterClient:
    REPEAT_TIMES = 3
    TIMEOUT = 60 * 3

    def __init__(self, user_token=None, app_token=None,
                 impersonator=None, debug=True, url_base=None):

        self.debug = debug
        self.user = dict()
        self.app = None
        self.user_token = user_token
        self.app_token = app_token
        self.impersonator = impersonator
        if url_base is not None:
            self.url_base = url_base
        elif debug:  # TODO: DEV&PRODUCTION ENV
            self.url_base = "http://127.0.0.1:5050/api/v1/"
        else:
            self.url_base = "http://127.0.0.1:5050/api/v1/"
        self.headers = dict()
        self.new_auth(user_token, app_token, impersonator)
        self.client = Session()

    def init_auth(self):
        pass

    def __repeat_try(self, repeat=REPEAT_TIMES):
        pass

    def do_request(self, path, json_data=None, method="GET"):
        request_url = urljoin(self.url_base, path)
        respond = None
        error = None
        for i in range(self.REPEAT_TIMES):
            try:
                with Session() as s:
                    # json-param将会自动携带json-content-type的http header
                    respond = s.request(method=method, url=request_url,
                                        json=json_data, headers=self.headers)
            except Exception as e:
                error = str(e)
                logger.warning(e)
                continue
            break
        if not respond:
            return False, error
        resp_json = respond.json()
        if resp_json.get("code") != 1:
            return False, resp_json.get("error", "")
        return True, resp_json

    def __verify_auth_condition(self, user_token: str = None, app_token: str = None,
                                impersonator: int = None) -> None:
        if user_token is None and app_token is None:
            raise XACSClientException("user-token&app-token二者必须有其一")
        if user_token and impersonator and not app_token:
            logger.warning("impersonator只有在app-token存在的情况下才有作用")
        if user_token and app_token:
            logger.warning("user-token和app-token同时存在的情况下app-token将失效")

    def new_auth(self, user_token=None, app_token=None, impersonator=None):
        """重新设置client的auth信息

        :param user_token: 用户Token
        :param app_token:  应用Token
        :param impersonator: 扮演者ID
        :return: client自身
        """
        self.__verify_auth_condition(user_token, app_token, impersonator)
        self.user_token = user_token
        self.app_token = app_token
        self.impersonator = impersonator
        if self.user_token:
            self.get_user_info()
            self.headers["XACS-USER-TOKEN"] = self.user_token
        if self.app_token:
            self.headers["XACS-APP-TOKEN"] = self.app_token
        if self.impersonator:
            self.headers["XACS-IMPERSONATOR"] = self.impersonator
        return self

    def get_user_info(self):
        """ 获取user信息（根据user-token或者扮演者ID）
        :return: None
        """
        if not self.user_token:
            logger.warning("仅在使用user_token的时候此方法方才有效")
            return
        token_content = dict()
        try:
            token_content, _ = decode_token(self.user_token)
        except Exception as e:
            logger.warning(e)
            return
        if not token_content:
            return
        if token_content.get("token_type", "") != "user":
            logger.warning("user-token不合法")
            return
        self.user = token_content


class DataCenterClientSingle(DataCenterClient):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(DataCenterClientSingle, "_instance"):
            with  DataCenterClientSingle._instance_lock:
                if not hasattr(DataCenterClientSingle, "_instance"):
                    DataCenterClientSingle._instance = object.__new__(cls)
        return DataCenterClientSingle._instance


class DataCenterSession:
    """DataCenter-Client with上下文协议 和 类装饰器 实现

        形式一——with上下文::

            with DataCenterSession() as ctx:
                x_datacenter_action(ctx)

        形式二——装饰器::

            DataCenterSession()(x_datacenter_action)(**kwargs)
            # 或(下面用于SDK代码，非SDK调用者使用)
            @DataCenterSession()
            def x_datacenter_action():
                pass

        形式四——实例参数::

            session = DataCenterSession()
            x_datacenter_action(session=session)
    """

    def __init__(self, *args, **kwargs):
        client = kwargs.get("client")
        if client and isinstance(client, DataCenterClient):
            self.datacenter_client = client
            user_token = kwargs.get("user_token")
            app_token = kwargs.get("app_token")
            impersonator = kwargs.get("impersonator")
            try:
                self.datacenter_client.new_auth(user_token=user_token,
                                                app_token=app_token,
                                                impersonator=impersonator)
            except:
                pass
        else:
            self.datacenter_client = DataCenterClientSingle(*args, **kwargs)

    def __enter__(self):
        return self.datacenter_client

    def __exit__(self, type, value, traceback):
        self.datacenter_client = None

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            kwargs["session"] = self.datacenter_client
            func(*args, **kwargs)

        return wrapper
