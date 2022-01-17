#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, sys

path = "."
result_list = []
result_str = ""
flag = "* "
tab = "  "
# 定义递归方法
def find_files(path, n = 0, dir = ""):
    global result_str
    if os.path.isdir(path):
        if path <> "node_modules" and path <> "_book" and path <> ".DS_Store":
            if path <> ".":
                dir += path + "/"
            # path是文件夹
            if path <> ".":
                result_list.append(tab * n + flag + "[" + path + "](" + dir + "/README.md" + ")")
                result_str += tab * n + flag + "[" + path + "](" + dir + "/README.md"  + ")\n"
                n = n + 1
            else:
                n = 0
            # 按文件名称排序
            dirs = sorted(os.listdir(path))
            for file in dirs:
                find_files(file, n, dir)
    else:
        # path是文件
        if path.endswith(".md") and path <> "SUMMARY.md" and path <> "README.md":
            result_list.append(tab * n + flag + "[" + path + "](" + dir + path + ")")
            result_str += tab * n + flag + "[" + path + "](" + dir + path + ")\n"
find_files(".", 0, "")
for file in result_list:
    print file
try:
    f = open('./SUMMARY.md', 'w')
    f.write(result_str)
finally:
    if f:
        f.close()
