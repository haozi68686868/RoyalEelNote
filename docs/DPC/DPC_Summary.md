#### DPC算法

##### 路径规划算法

- 全局路径（也可以用于局部路径）

A* 算法

Djikstra算法

PRM（Probabilistic Road Map）概率地图

RRT（Rapidly-Exploring Random Trees）快速随机扩展树

- 局部路径

TEB（Time Elastic Band）时间弹性带

DWA（Dynamic Window Approach）动态窗口逼近

- 覆盖路径

TSP、ATSP（Traveling Salesman Problem）旅行商问题

Boustrophedon牛耕法、

BSA（Backtracking Spiral Algorithm）回溯螺旋算法

##### 控制算法

MPC算法

purepirsuit算法

LQR算法

PID

##### 路径规划和控制常用的代价函数

如果希望能尽快完成
$$
J_1=t_f
$$
车速变化小
$$
J_2=\int_0^{t_f}a^2(t)dt
$$
转动较小
$$
J_3=\int_0^{t_f}\omega^2(t)dt
$$
远离障碍物
$$
J_4=\sum_{j=1}^n\int_0^{t_f}e^{-d_j(t)^2}dt
$$


##### 决策算法



