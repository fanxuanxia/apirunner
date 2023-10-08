import os
import yaml
from apirunner.utils.assert_method import AssertMethod

class AssertUtil():
    @staticmethod
    def do_assert(rule):
        assert_type = rule.get('type')
        target = rule.get('target')   # 提取到实际值
        value = rule.get('value')     # 预设的期望值

        obj = AssertMethod()
        result = getattr(obj, assert_type)(target, value)
        print(result)
