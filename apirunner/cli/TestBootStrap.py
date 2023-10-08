import pytest
from apirunner.cli.DataCenter import DataCenter
from apirunner.ApiTestFramework.ApiExecutor import execute

class TestBootStrap():
    """
    pytest用例参数化驱动
    """
    @pytest.mark.parametrize("caseinfo", DataCenter.caseinfos)
    def test(self, caseinfo, login):
        execute(caseinfo, login)