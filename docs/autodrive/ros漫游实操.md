# ros漫游实操

#### rosnode

```shell
rosnode cleanup # 如果使用ctrl+c 杀掉结点的话，则还会在rosnode list中显示
rosnode kill [node]
rosnode list
```

#### 编译rosMsg 并引用头文件

##### cmakeLists.txt

```cmake
# 1.首先要找到生成模块
find_package(catkin REQUIRED COMPONENTS
	message_generation
)
# 2. 添加要编译的msg
add_message_files(
  DIRECTORY msg # msg是文件夹
)
# 或
add_message_files(
  DIRECTORY msg
  FILE ${msg_list}
)
# 3. 生成
generate_messages(
  DEPENDENCIES
  std_msgs # 要添加基础依赖的ros系统标准msg
)
# 4. 还不清楚具体能干啥，但是必须要
catkin_package(CATKIN_DEPENDS message_runtime)

```

执行cmake后就生成了头文件

##### c++文件中

```c++
//5. c++ 文件中包含头文件
#include "{projectName}/{msgName}.h"
```

