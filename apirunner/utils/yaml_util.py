import os
import yaml

class YamlUtil():
    @staticmethod
    def read_data(file):
        if os.path.exists(file):
            with open(file=file, mode='r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f)
                return yaml_data
        else:
            print("文件不存在")
if __name__ == '__main__':
    YamlUtil.read_data(r'F:\projects\a2023\python_project\apirun\case\testLogin.yaml')