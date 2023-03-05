##### 车辆动力学建模

$$
a = \frac{dV_x}{dt}=\frac{F_{xr}-R_{xf}-R_{xr}}{m}
$$

清扫车风阻很小，远小于摩擦力，故忽略掉

- 轮胎力

$$
F_{xr}=C_{\sigma f}\sigma_{xf}
$$

$$
\sigma_f=\frac{r_{eff}\omega_w-V_x}{V_x}\  (r_{eff}\omega_w<V_x)
$$

$$
\sigma_f=\frac{r_{eff}\omega_w-V_x}{r_{eff}\omega_w}\  (r_{eff}\omega_w>V_x)
$$

- 滚阻

$$
R_{xf}+R_{xr}=f(F_{zf}+F_{zr})
$$

- 对于轮胎来说

$$
T_r=r_{eff}\cdot(F_{xr}+R_{xr})
$$

- 对于电机，负载力矩=轮胎的转矩加损耗转矩

$$
T_L=T_r+T_\Delta
$$

