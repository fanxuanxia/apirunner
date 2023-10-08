import os
import yaml
from apirunner.utils.logger import logger
class AssertMethod():
    def equals(self, actual_value, expect_value):
        # assert expect_value == actual_value
        logger.info("相等断言，期望值为"+expect_value+"，实际值为："+actual_value)
        assert actual_value== expect_value
    def not_equals(self, actual_value, expect_value):
        return actual_value + expect_value

    def contain(self, actual_value, expect_value):
        assert expect_value in actual_value

