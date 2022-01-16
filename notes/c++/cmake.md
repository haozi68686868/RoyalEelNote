# CMake 笔记

### option , add_definations

```cmake
option(<option_variable> "help string describing option" [initial value=OFF])
#example
option(ARG_HAHAHA "HAHAHA" ON)
if (ARG_HAHAHA)
    add_definitions(-DARG_HAHAHA)
    add_definitions(-DARG_VALUE=“123”)
endif()
#cmake command
cmake .. -ARG_HAHAHA=OFF
```

**option的值与缓存的值(cmakeCache.txt)有关，如果改变option的值，建议清理build文件夹，重新加载**

### 常用路径

一、变量的引用方式是使用`“${}”`，在IF中，不需要使用这种方式，直接使用变量名即可
 二、自定义变量使用`SET(OBJ_NAME xxxx)`，使用时`${OBJ_NAME}`
 三、cmake的常用变量：
 `CMAKE_BINARY_DIR`, `PROJECT_BINARY_DIR` ：这两个变量内容一致，如果是内部编译，就指的是工程的顶级目录，如果是外部编译，指的就是工程编译发生的目录。
 `CMAKE_SOURCE_DIR`, `PROJECT_SOURCE_DIR`：这两个变量内容一致，都指的是工程的顶级目录。
 `CMAKE_CURRENT_BINARY_DIR`：外部编译时，指的是target目录，内部编译时，指的是顶级目录
 `CMAKE_CURRENT_SOURCE_DIR`：CMakeList.txt所在的目录
 `CMAKE_CURRENT_LIST_DIR`：CMakeList.txt的完整路径
 `CMAKE_CURRENT_LIST_LINE`：当前所在的行
 `CMAKE_MODULE_PATH`：如果工程复杂，可能需要编写一些cmake模块，这里通过SET指定这个变量
 `LIBRARY_OUTPUT_DIR`, `BINARY_OUTPUT_DIR`：库和可执行的最终存放目录
 `PROJECT_NAME`, `CMAKE_PROJECT_NAME`：前者是当前CMakeList.txt里设置的project_name，后者是整个项目配置的project_nam