"""
@Date    : 2020-12-21
@Author  : liyachao
"""
# import json
# import os
# import sys
# def get_file(root_path,all_files=[]):
#     '''
#     递归函数，遍历该文档目录和子目录下的所有文件，获取其path
#     '''
#     files = os.listdir(root_path)
#     for file in files:
#         if not os.path.isdir(root_path + '/' + file):   # not a dir
#             all_files.append(root_path + '/' + file)
#         else:  # is a dir
#             get_file((root_path+'/'+file),all_files)
#     return all_files
#
# root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")
# print(root_path)
# sys.path.extend(get_file(root_path+"/py_ios_device"))  # 指定搜索路径绝对目录
# sys.path.extend(get_file(root_path+"/src"))  # 指定搜索路径绝对目录
# print(json.dumps(sys.path))

__version__ = "0.16"
