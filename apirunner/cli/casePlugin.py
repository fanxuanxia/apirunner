import os
import copy
import pytest
import time
from apirunner.utils.yaml_util import YamlUtil
from apirunner.cli.DataCenter import DataCenter
from apirunner.utils.logger import logger
class CasePlugin():
    """
    自定义插件，收集和处理测试用例数据，这个里面的函数，必须是pytest定义好的钩子函数
    """

    def pytest_addoption(self, parser):
        """
        添加一个命令行参数
        :param parser:
        :return:
        """
        parser.addoption("--caseDir",        # 命令
                         action="store",
                         default="../../case",  # 没有指定参数时的默认值
                         help="指定测试用例的目录")# help命令显示的信息

    def pytest_configure(self, config):
        """
        pytest插件的配置钩子，pytest配置过程中，把用例数据读取到DataCenter对象里面去
        :param config:
        :return:
        """
        # 配置pytest
        config_path = os.path.abspath(config.getoption("--caseDir"))

        DataCenter.caseinfos = []
        for file in os.listdir(config_path):
            # 1. 只收集以test开头，并以yaml结尾的文件，作为用例的文件
            if not file.startswith('test') or not file.endswith('yaml'):
                continue
            path = os.path.join(config_path, file)
            case_info = YamlUtil.read_data(path)

            # 2. 是否有数据驱动
            ddts = case_info.get('ddts', [])
            if len(ddts) > 0:
                # 2.1 获取到接口的基本信息
                case_info.pop('ddts')
                for ddt in ddts:
                    # 2.2 深拷贝一个对象出来，再把ddt数据放到上下文中，再核心执行器里面会进行统一的替换
                    new_case = copy.deepcopy(case_info)
                    context = new_case.get('context', {})
                    ddt.update(context)
                    new_case.update({'context': ddt})
                    DataCenter.caseinfos.append(new_case)

            else:
                DataCenter.caseinfos.append(case_info)
        print("caseinfo", DataCenter.caseinfos)

    @pytest.hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_runtest_makereport(self, item, call):
        out = yield
        res = out.get_result()
        if res.when == "call":
            logger.info(f"用例ID：{res.nodeid}")
            logger.info(f"测试结果：{res.outcome}")
            logger.info(f"故障表示：{res.longrepr}")
            logger.info(f"异常：{call.excinfo}")
            logger.info(f"用例耗时：{res.duration}")
            logger.info("**************************************")

    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        '''收集测试结果'''
        print(terminalreporter.stats)
        print("total:", terminalreporter._numcollected)
        print('passed:', len(terminalreporter.stats.get('passed', [])))
        print('failed:', len(terminalreporter.stats.get('failed', [])))
        print('error:', len(terminalreporter.stats.get('error', [])))
        print('skipped:', len(terminalreporter.stats.get('skipped', [])))
        # terminalreporter._sessionstarttime 会话开始时间
        duration = time.time() - terminalreporter._sessionstarttime
        print('total times:', duration, 'seconds')



