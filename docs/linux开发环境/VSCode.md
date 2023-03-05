## VSCode学习笔记

### 好用的插件

- ssh-remote
- bracket Pair Colorizer
- VS Code Counter
- GitLens : 分锅神器
- Git Graph

### 踩坑日记

g++ -g -o [output file] [cpps] -I [include path]

eg: g++ -g -o ./bin/main main.cpp src/*.cpp -I ./include/

```
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "build",
            "type": "shell",
            "command": "g++",
            "args": [
                "-g",
                "-o",
                "./bin/main",
                "main.cpp",
                "src/*.cpp",
                "-I",
                "./include/"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "problemMatcher": []
        }
    ]
}


```

得到所需的include path 配置到c_cpp_properties
gcc -v -E -x c++ -

自动格式化 ctrl + shift + I

#### 避免vscode 对c++11新特性报警

```json
"setting.json"
"C_Cpp.default.compilerArgs": [
"-g",
"${file}",
"-std=c++11",
"-o",
"${fileDirname}/${fileBasenameNoExtension}"
]
,"clang.cxxflags": ["-std=c++14"] //有效
```

##### VSCode自动换行

Word Wrap

##### VSCode Ubantu18 添加右键菜单

1. 进入~/.local/share/nautilus/scripts文件夹

```text
cd ~/.local/share/nautilus/scripts
```

2. 创建右键菜单文件

```text
vim Vscode_it
```

3. Vscode_it的内容为

```text
#!/bin/bash
code $NAUTILUS_SCRIPT_SELECTED_FILE_PATHS
```

4. 给Vscode_it加权限

```text
sudo chmod u+x Vscode_it
```