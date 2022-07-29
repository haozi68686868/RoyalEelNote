# linux

#### 控制台快捷操作

```shell
#光标到末尾 
ctrl+e
#光标到开头 
ctrl+A
#开启新terminal 
ctrl+alt+T
#新的标签栏 terminal 
ctrl+shift+T
#复制/粘贴
ctrl+shift+C/V
#取消
ctrl+C
```

#### 远程文件操作

```
scp test1/outputData.txt [sensetime@10.11.248.8](mailto:sensetime@10.11.248.8):~
ssh liuxinhao@10.11.232.140
Good3ense@
```

#### 输出文本

```shell
echo "" (） 
-n 不换行输出
-e 使能转义字符
特殊转义字符：
	“\c” 不换行
	\a 发出警告声；
    \b 删除前一个字符；
    \c 最后不加上换行符号；
    \f 换行但光标仍旧停留在原来的位置；
    \n 换行且光标移至行首；
    \r 光标移至行首，但不换行；
    \t 插入tab；
    \v 与\f相同；
    \\ 插入\字符；
        可以选择的编码如下所示(这些颜色是ANSI标准颜色)：
          编码          颜色/动作
          0      　     重新设置属性到缺省设置
          1     　      设置粗体
          2     　      设置一半亮度(模拟彩色显示器的颜色)
          4     　      设置下划线(模拟彩色显示器的颜色)
          5     　      设置闪烁
          7     　      设置反向图象
          22    　      设置一般密度
          24    　      关闭下划线
          25     　     关闭闪烁
          27     　     关闭反向图象
          30      　    设置黑色前景
          31   　       设置红色前景
          32   　       设置绿色前景
          33   　       设置黄色前景
          34   　       设置蓝色前景
          35    　      设置紫色前景
          36     　     设置青色前景
          37    　      设置白色(灰色)前景
          38      　    在缺省的前景颜色上设置下划线
          39      　    在缺省的前景颜色上关闭下划线
          40      　    设置黑色背景
          41      　    设置红色背景
          42     　     设置绿色背景
          43     　     设置黄色背景
          44     　     设置蓝色背景
          45     　     设置紫色背景
          46     　     设置青色背景
          47      　    设置白色(灰色)背景
          49      　    设置缺省黑色背景
    其他有趣的代码还有：
           \033[2J  　     清除屏幕
          \033[0q  　    关闭所有的键盘指示灯
          \033[1q 　     设置"滚动锁定"指示灯(Scroll Lock)
          \033[2q 　     设置"数值锁定"指示灯(Num Lock)
          \033[3q 　     设置"大写锁定"指示灯(Caps Lock)
          \033[15:40H  把关闭移动到第15行，40列
          \007  　　      发蜂鸣生beep
```

##### systemctl

```
systemctl list-units [--all] --type=service  列出所有运行的服务
systemctl list-unit-files --type=service 列出所有启动服务
```

#### 系统工具

```shell
#打开文件管理器
xdg-open .
nautilus .
```

#### 快速查看硬盘和文件夹的空间

```
sudo du -h --max-depth=0 *
```

#### ssh无法免密登录

```bash
ssh -v liuxinhao@10.157.48.178
```

```
# sudo vim /etc/ssh/sshd_config
# Authentication:
StrictModes no # 设置为no
```

#### grep指令

```shell
grep -E "421|221" # 正则匹配，匹配421或221
```

#### 卸载软件及其配置文件

```shell
sudo apt --purge remove deepin.com.weixin.work # --purse 卸载配置文件
```

#### apt无法正常安装 (sudo apt update 都不正常)

1. 源可能有问题，如下

```shell
错误:34 https://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial-security Release               
  server certificate verification failed. CAfile: /etc/ssl/certs/ca-certificates.crt CRLfile: none
  
E: 仓库 “https://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial Release” 没有 Release 文件。
N: 无法安全地用该源进行更新，所以默认禁用该源。
N: 参见 apt-secure(8) 手册以了解仓库创建和用户配置方面的细节。
E: 仓库 “https://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial-updates Release” 没有 Release 文件。
```

- 基础解决方案：换源！
- 其他可能有帮助的操作

```shell
sudo update-ca-certificates -f
apt-get install --reinstall ca-certificates
```

2. public Key 过期，报错如下：

```shell
错误:18 http://packages.ros.org/ros/ubuntu xenial InRelease                    
  由于没有公钥，无法验证下列签名： NO_PUBKEY F42ED6FBAB17C654
```

- 解决方案：获取公钥，即可

```shell
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F42ED6FBAB17C654
```

#### 查看硬盘型号

```
sudo smartctl -a /dev/sda
```

#### 内存泄露

##### 结合free、top等命令进行资源监控

free命令：

![img](https://img-blog.csdnimg.cn/20210426171723786.png)



top命令：第四行展示的是内存总量、内存使用量、空闲内存以及块设备缓冲。

![img](https://img-blog.csdnimg.cn/20210426171741974.png)

也可以看到待监控进程的内存占用百分比。如果这里的内存占用百分比增速过快，则需要考虑是否存在内存泄露的问题。

![img](https://img-blog.csdnimg.cn/20210426171756723.png)

#### CPU性能

```
time echo "scale=3000; 4*a(1)" | bc -l
cat /proc/cpuinfo
```

