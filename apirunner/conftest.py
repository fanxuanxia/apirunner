import pytest
import requests
import jsonpath
import time
from apirunner.utils.logger import logger
from requests.utils import dict_from_cookiejar


@pytest.fixture(scope="function", autouse=True)
def ceshi():
    yield
    logger.info("-----------------------")


@pytest.fixture()
def login():
    """
    登录获取cookie, cookie全项目都需要使用并且进行接口关联，整个项目这个fix只运行一次
    :return: 工具类ak ; 用户的cookie
    """
    # 完成登录操作并返回token
    url = "http://shop-xo.hctestedu.com/index.php?s=/api/user/login"
    params = {"application": "web"}
    data = {"accounts": "fxx", "pwd": "12345678", "type": "username"}

    res = requests.post(url=url, params=params, data=data)

    # 将CookieJar转换为字典, 然后转换为cookie字符串
    cookie_dict = dict_from_cookiejar(res.cookies)
    cookie_str = '; '.join([f'{key}={value}' for key, value in cookie_dict.items()])
    # ----------------------------------------
    # 获取响应数据
    result = res.json()

    return cookie_str





if __name__ == '__main__':
    login()
