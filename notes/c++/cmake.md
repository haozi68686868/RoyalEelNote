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

##### Target_link_libraries

```
target_include_directories(<Target>
	PUBLIC <dirs>…
	PRIVATE <dirs>…
	INTERFACE <dirs>…
)
```

当创建动态库时，

- 如果源文件(例如CPP)中包含第三方头文件，但是头文件（例如hpp）中不包含该第三方文件头，采用PRIVATE。
- 如果源文件和头文件中都包含该第三方文件头，采用PUBLIC。
- 如果头文件中包含该第三方文件头，但是源文件(例如CPP)中不包含，采用 **INTERFACE**。

**原文：CMake target_link_libraries Interface Dependencies**

http://stackoverflow.com/questions/26037954/cmake-target-link-libraries-interface-dependencies

其他属性可以参考http://www.cmake.org/cmake/help/v3.0/manual/cmake-buildsystem.7.html#transitive-usage-requirements

**关键字用法说明：**

**PRIVATE**：私有的。生成 libhello-world.so时，只在 hello_world.c 中包含了 hello.h，libhello-world.so **对外**的头文件——hello_world.h 中不包含 hello.h。而且 main.c 不会调用 hello.c 中的函数，或者说 main.c 不知道 hello.c 的存在，那么在 hello-world/CMakeLists.txt 中应该写入：

```vbnet
target_link_libraries(hello-world PRIVATE hello)
target_include_directories(hello-world PRIVATE hello)
```

**INTERFACE**：接口。生成 libhello-world.so 时，只在libhello-world.so **对外**的头文件——hello_world.h 中包含 了 hello.h， hello_world.c 中不包含 hello.h，即 libhello-world.so 不使用 libhello.so 提供的功能，只使用 hello.h 中的某些信息，比如结构体。但是 main.c 需要使用 libhello.so 中的功能。那么在 hello-world/CMakeLists.txt 中应该写入：

```vbnet
target_link_libraries(hello-world INTERFACE hello)
target_include_directories(hello-world INTERFACE hello)
```

**PUBLIC**：公开的。**PUBLIC = PRIVATE + INTERFACE**。生成 libhello-world.so 时，在 hello_world.c 和 hello_world.h 中都包含了 hello.h。并且 main.c 中也需要使用 libhello.so 提供的功能。那么在 hello-world/CMakeLists.txt 中应该写入：

```vbnet
target_link_libraries(hello-world PUBLIC hello)
target_include_directories(hello-world PUBLIC hello)
```

实际上，这三个关键字指定的是目标文件依赖项的使用**范围（scope）**或者一种**传递（propagate）**。[官方说明](https://link.zhihu.com/?target=https%3A//cmake.org/cmake/help/v3.15/manual/cmake-buildsystem.7.html%23transitive-usage-requirements)

可执行文件依赖 libhello-world.so， libhello-world.so 依赖 libhello.so 和 libworld.so。

1. main.c 不使用 libhello.so 的任何功能，因此 libhello-world.so 不需要将其依赖—— libhello.so 传递给 main.c，hello-world/CMakeLists.txt 中使用 PRIVATE 关键字；
2. main.c 使用 libhello.so 的功能，但是libhello-world.so 不使用，hello-world/CMakeLists.txt 中使用 INTERFACE 关键字；
3. main.c 和 libhello-world.so 都使用 libhello.so 的功能，hello-world/CMakeLists.txt 中使用 PUBLIC 关键字；