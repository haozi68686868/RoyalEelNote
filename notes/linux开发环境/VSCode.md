## VSCode学习笔记

### 好用的插件

- ssh-remote
- bracket Pair Colorizer

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

