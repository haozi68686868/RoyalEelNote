### CLion

#### CLion启动 ROS配置（以及所有需要source的编译环境）

- 关键问题：从开始菜单打开不会执行source ~/.bashrc
- 解决方案：
  1. 编辑 <clion_path>/bin/clion.sh，在最后启动之前，执行source ~/.bashrc
  2. 开始菜单的命令必须用bash，如果是sh则没有source指令