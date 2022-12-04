LQR+Kalman = LQG

LQR + constraints = MPC



LQR和MPC我分别都在车辆在30km/h的条件下实现过。

首先我说一下本质区别

LQR的控制律是根据(Riccati)方程来求解的。

MPC的控制律是根据二次规划来求解的。

都是最优化问题，但MPC的解是可以增加限制的，就好比LQR多增加了一个限制条件的方程，而在MPC里面本身就有这个内容。

这就是两个求最优解本质的不同



LQR = linear quadratic regulator （线性二次型调节器）

MPC = Model Predictive Control （模型预测控制）

PID

Pure Pirsuit

LQG = linear guadratic Gaussian (线性二次高斯控制)



LQR : https://zhuanlan.zhihu.com/p/139145957