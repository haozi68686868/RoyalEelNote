#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, sys
from posixpath import basename



result_str = ""
flag = "* "
tab = "  "

# 定义递归方法
def find_files(rel_path, n = 0, dir = ""):
    global result_str
    path = os.path.join(dir,rel_path)
    basename = os.path.basename(path)
    if (basename == "node_modules" or basename == "_book" or basename == ".DS_Store"):
        return
    if os.path.isdir(path):
        # path是文件夹
        if rel_path != "":
            title_file = os.path.join(rel_path,"README.md")
            if(not os.path.exists(os.path.join(dir,title_file))):
                return
            result_list.append(tab * n + flag + "[" + basename + "](" + title_file + ")")
            # result_str += tab * n + flag + "[" + path + "](" + dir + "/README.md"  + ")\n"
            n = n + 1
        else:
            n = 0
        # 按文件名称排序
        dirs = sorted(os.listdir(path))
        for file in dirs:
            find_files(os.path.join(rel_path,file), n, dir)
    else:
        # path是文件
        if basename.endswith(".md") and basename != "SUMMARY.md" and basename != "README.md":
            title_name = basename[:-3]
            result_list.append(tab * n + flag + "[" + title_name + "](" + rel_path + ")")
            # result_str += tab * n + flag + "[" + path + "](" + dir + path + ")\n"

if __name__ == "__main__":
    dir = "."
    result_list = []
    if(len(sys.argv)<2):
        print("Usage: {} [source File Path]".format(os.path.basename(sys.argv[0])))
        exit(1)
    dir = sys.argv[1]
    find_files("", 0, dir)
    with open(os.path.join(dir,'SUMMARY.md'), 'w') as f:
        for file in result_list:
            print(file)
            f.write(file)
            f.write('\n')

