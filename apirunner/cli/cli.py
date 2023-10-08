import pytest
import os
from casePlugin import CasePlugin

def main():
    """命令行最终是执行了这个函数，在这个函数里面启动pytest"""

    path = os.path.join(os.path.dirname(__file__), 'TestBootStrap.py')
    args = ["-s", "-v", "--capture=sys", "--alluredir", "../report",
            path]

    pytest.main(args, plugins=[CasePlugin()])
    # allure generate 生成测试结果数据 -o 生成报告的路径 --clean
    os.system("allure generate ../report -o ../report/report_allure --clean")
    os.system("allure serve ../report/report_allure")

if __name__ == '__main__':
    main()

