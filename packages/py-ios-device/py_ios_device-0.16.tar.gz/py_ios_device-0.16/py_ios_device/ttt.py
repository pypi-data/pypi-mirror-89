"""
@Date    : 2020-12-21
@Author  : liyachao
"""
import json
import os
import sys

root_path = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/"
print(root_path)
syspath = sys.path
sys.path = []
sys.path.append(root_path)  # 指定搜索路径绝对目录

sys.path.extend([root_path + i for i in os.listdir(root_path) if i[0] != "."])  # 将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)
print(json.dumps(sys.path))

