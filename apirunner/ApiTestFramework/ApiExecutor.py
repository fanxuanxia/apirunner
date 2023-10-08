import requests
import jsonpath
import json
import re
import operator
import pytest
from apirunner.utils.myTemplate import MyTemplate
from apirunner.utils.logger import logger


def execute(caseinfo, login):
    """
    用例核心执行器
    """
    steps = caseinfo["steps"]
    context = caseinfo["context"]
    msg = ">>>>执行用例【" + caseinfo["baseinfo"]["casename"] + "】>>>>>"
    logger.info(msg)
    for step in steps:
        # 0. 预处理，有些可能需要进行变量替换
        for key in step.keys():
            if not key.startswith("_"):
                # 取值渲染
                target = step.get(key)
                string = MyTemplate(json.dumps(target))
                value = string.substitute(**context)
                obj = json.loads(value)
                # 赋值
                step.update({key: obj})
                logger.info("变量模板替换完成，" + value)
        # 添加一下cookie信息
        # 1. 发送接口请求
        logger.info(">>>>>发送接口请求>>>>>")
        headers = step.get('headers', {})
        headers.update({'Cookie': "userClientMarkKey=04af405d1ed24e19bd07688587615ec8; Hm_lvt_ecc8b50a3122e6d5e09be7a9e5383e07=1694512925,1696748291,1696754282; Authorization=eyJhbGciOiJIUzUxMiJ9.eyJleHAiOjE2OTczNjAzOTEsInN1YiI6IntcImlkXCI6MTYxMzAxMjA3MTYwODA2NjA0OCxcInVzZXJuYW1lXCI6XCIxMzgxMTExMTExMVwiLFwibmlja05hbWVcIjpcIjEzODExMTExMTExXCJ9IiwiY3JlYXRlZCI6MTY5Njc1NTU5MTU2OX0.GkFvLrOK4_Wje6P006yW33otsRooj2m3LyGNKlioMH6jV6NNFPpSHDshokyvS4LO6yjD4qK8_3zRZJlHfT44cA; Hm_lpvt_ecc8b50a3122e6d5e09be7a9e5383e07=1696755618"})
        response = requests.request(method=step.get('method', None),
                                    url=step.get('url', None),
                                    data=step.get('data', None),
                                    params=step.get('params', None),
                                    json=step.get('json', None),
                                    headers=headers,
                                    files=step.get('files', None),
                                    timeout=step.get('timeout', None))
        response_result = json.loads(response.text)
        logger.info(">>>>>请求完成，响应信息如下>>>>>")
        logger.info(response_result)
        # 2. 断言
        assert_options = step.get('assert_options')
        if isinstance(assert_options, list) and len(assert_options) > 0:
            for assert_option in assert_options:
                # 3.1 获取目标值
                target_value = None
                if assert_option["target"].startswith("$."):   # json表达式
                    target_value = jsonpath.jsonpath(response_result, assert_option["target"])
                else:                                          # 正则表达式
                    pattern = re.compile(assert_option["target"])
                    target_value = re.findall(pattern, response.text)[0]

                # 进行判断
                assert_type = assert_option["type"]
                expect_value = assert_option["value"]
                if assert_type == "exists":  # 存在
                    assertResult = target_value != False
                elif assert_type == 'contains':  # 包含
                    assertResult = target_value[0].__contains__(
                        expect_value)
                elif assert_type == 'equals':  # 相同
                    assertResult = str(target_value[0]) == expect_value
                else:
                    assertResult = getattr(operator, assert_type)(
                        float(target_value[0]), float(expect_value))

                # assert assertResult, "断言不通过：" + assert_option["errorMsg"]
                errorMsg = assert_option["errorMsg"]
                assert assertResult, errorMsg
                logger.info(f"执行{assert_type}断言，断言结果：{assertResult}，实际值：{target_value[0]}，期望值：{expect_value}")
                if not assertResult:
                    logger.info(errorMsg)

        # 3. 提取数据保存到上下文中
        for extract_option in step.get("extract_options", []):
            # 定义一个变量用来存放结果
            target_value = None

            # 3.1 json表达式或者正则表达式，获取目标值
            if extract_option['target'].startswith("$."):
                target_value = jsonpath.jsonpath(response_result, extract_option['target'])
            else:
                pattern = re.compile(extract_option["target"])
                target_value = re.findall(pattern, response.text)[0]
            # 3.2 更新上下文变量数据
            context.update({
                extract_option["varname"]: target_value[0]
            })
        logger.info("上下文信息："+json.dumps(context))

if __name__ == '__main__':
    steps = {'context': {'host': 'shop-xo.hctestedu.com', 'port': '80', 'accounts': 'sanfeng',
                         'pwd': 'sanfeng',
                         'desc': '正确的用户名，正确的密码'},
             'steps': [
                 {'assert_options': [
                     {'errorMsg': 'code不等于0', 'target': '$.code', 'type': 'equals', 'value': '0'}],
                     'data': {'accounts': '!accounts',
                              'pwd': '!pwd', 'type': 'username'},
                     'extract_options': [
                         {'target': '$.data.token',
                          'varname': 'login_token'}],
                     'method': 'post',
                     'url': 'http://!host:!port/index.php?s=/api/user/login&application=app'}],
             'ddts': [{'accounts': 'sanfeng', 'pwd': 'ttt', 'desc': '正确的用户名，错误的密码'},
                      {'accounts': 'sanfen', 'pwd': 'sanfeng', 'desc': '错误的用户名，正确的密码'},
                      {'accounts': 'sanfeng', 'pwd': 'sanfeng', 'desc': '正确的用户名，正确的密码'}]}
    execute(steps)
