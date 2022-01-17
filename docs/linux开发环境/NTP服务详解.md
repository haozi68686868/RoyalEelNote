# NTP服务详解

## 时间服务器作用：

大数据产生与处理系统是各种计算设备集群的，计算设备将统一、同步的标准时间用于记录各种事件发生时序，

如E-MAIL信息、文件创建和访问时间、数据库处理时间等。

大数据系统内不同计算设备之间控制、计算、处理、应用等数据或操作都具有时序性，

若计算机时间不同步，这些应用或操作或将无法正常进行。

大数据系统是对时间敏感的计算处理系统，时间同步是大数据能够得到正确处理的基础保障，是大数据得以发挥作用的技术支撑。

大数据时代，整个处理计算系统内的大数据通信都是通过网络进行。

时间同步也是如此，利用大数据的互联网络传送标准时间信息，实现大数据系统内时间同步。

网络时间同步协议(NTP)是时间同步的技术基础。

 

## （一）确认ntp的安装

### 1）确认是否已安装ntp

【命令】rpm –qa | grep ntp

若只有ntpdate而未见ntp，则需删除原有ntpdate。如：

ntpdate-4.2.6p5-22.el7_0.x86_64

fontpackages-filesystem-1.44-8.el7.noarch

python-ntplib-0.3.2-1.el7.noarch

 

### 2）删除已安装ntp

【命令】yum –y remove ntpdate-4.2.6p5-22.el7.x86_64

 

### 3）重新安装ntp

【命令】yum –y install ntp

 

## （二）配置ntp服务

### 1）修改所有节点的/etc/ntp.conf

【命令】vi /etc/ntp.conf

【内容】

restrict 192.168.6.3 nomodify notrap nopeer noquery      //当前节点IP地址

restrict 192.168.6.2 mask 255.255.255.0 nomodify notrap  //集群所在网段的网关（Gateway），子网掩码（Genmask）

 

### 2）选择一个主节点，修改其/etc/ntp.conf

【命令】vi /etc/ntp.conf

【内容】在server部分添加一下部分，并注释掉server 0 ~ n

server 127.127.1.0

Fudge 127.127.1.0 stratum 10

 

### 3）主节点以外，继续修改/etc/ntp.conf

【命令】vi /etc/ntp.conf

【内容】在server部分添加如下语句，将server指向主节点。

server 192.168.6.3

Fudge 192.168.6.3 stratum 10

 

===修改前===

![img](https://images2017.cnblogs.com/blog/915691/201710/915691-20171012224824762-194290384.png)

 

===修改后===

节点1（192.168.6.3）：

![img](https://images2017.cnblogs.com/blog/915691/201710/915691-20171013130739105-562427169.png)

 

节点2（192.168.6.4）：

![img](https://images2017.cnblogs.com/blog/915691/201710/915691-20171013130835090-2027496738.png)

 

节点3（192.168.6.5）：

![img](https://images2017.cnblogs.com/blog/915691/201710/915691-20171013130912324-1592177452.png)

 

##  （三）启动ntp服务、查看状态

### 1）启动ntp服务

【命令】service ntpd start

 

### 2）查看ntp服务器有无和上层ntp连通

【命令】ntpstat

![img](https://images2017.cnblogs.com/blog/915691/201710/915691-20171013002936340-1631273268.png)

查看ntp状态时，可能会出现如下所示情况

① unsynchronised time server re-starting polling server every 8 s

![img](https://images2017.cnblogs.com/blog/915691/201710/915691-20171013131031496-1095710777.png)

② unsynchronised polling server every 8 s

![img](https://images2017.cnblogs.com/blog/915691/201710/915691-20171013131052840-421840461.png)

这种情况属于正常，ntp服务器配置完毕后，需要等待5-10分钟才能与/etc/ntp.conf中配置的标准时间进行同步。

等一段时间之后，再次使用ntpstat命令查看状态，就会变成如下正常结果：

![img](https://images2017.cnblogs.com/blog/915691/201710/915691-20171013131330184-1857767541.png)

 

### 3）查看ntp服务器与上层ntp的状态

【命令】ntpq -p

![img](https://images2017.cnblogs.com/blog/915691/201710/915691-20171013010729637-1391262052.png)

remote：本机和上层ntp的ip或主机名，“+”表示优先，“*”表示次优先

refid：参考上一层ntp主机地址

st：stratum阶层

when：多少秒前曾经同步过时间

poll：下次更新在多少秒后

reach：已经向上层ntp服务器要求更新的次数

delay：网络延迟

offset：时间补偿

jitter：系统时间与bios时间差

 

4）查看ntpd进程的状态

【命令】watch "ntpq -p"

【终止】按 Ctrl+C 停止查看进程。

![img](https://images2017.cnblogs.com/blog/915691/201710/915691-20171013011156934-1599095450.png)

第一列中的字符指示源的质量。星号 ( * ) 表示该源是当前引用。

remote：列出源的 IP 地址或主机名。

when：指出从轮询源开始已过去的时间（秒）。

poll：指出轮询间隔时间。该值会根据本地时钟的精度相应增加。

reach：是一个八进制数字，指出源的可存取性。值 377 表示源已应答了前八个连续轮询。

offset：是源时钟与本地时钟的时间差（毫秒）。

 

## （四）设置开机启动

【命令】chkconfig ntpd on

 

## （五）从其他博客的一些参考摘录

===/etc/ntp.conf 配置内容===

![复制代码](http://common.cnblogs.com/images/copycode.gif)

```
# 1. 先处理权限方面的问题，包括放行上层服务器以及开放局域网用户来源：
restrict default kod nomodify notrap nopeer noquery     <==拒绝 IPv4 的用户
restrict -6 default kod nomodify notrap nopeer noquery  <==拒绝 IPv6 的用户
restrict 220.130.158.71   <==放行 tock.stdtime.gov.tw 进入本 NTP 的服务器
restrict 59.124.196.83    <==放行 tick.stdtime.gov.tw 进入本 NTP 的服务器
restrict 59.124.196.84    <==放行 time.stdtime.gov.tw 进入本 NTP 的服务器
restrict 127.0.0.1        <==底下两个是默认值，放行本机来源
restrict -6 ::1
restrict 192.168.100.0 mask 255.255.255.0 nomodify <==放行局域网用户来源，或者列出单独IP

# 2. 设定主机来源，请先将原本的 [0|1|2].centos.pool.ntp.org 的设定批注掉：
server 220.130.158.71 prefer  <==以这部主机为最优先的server
server 59.124.196.83
server 59.124.196.84

# 3.默认的一个内部时钟数据，用在没有外部 NTP 服务器时，使用它为局域网用户提供服务：
# server    127.127.1.0     # local clock
# fudge     127.127.1.0 stratum 10

# 4.预设时间差异分析档案与暂不用到的 keys 等，不需要更动它：
driftfile /var/lib/ntp/drift
keys      /etc/ntp/keys
 
```

![复制代码](http://common.cnblogs.com/images/copycode.gif)

 

### ===restrict选项格式===

restrict [ 客户端IP ]  mask  [ IP掩码 ]  [参数]

“客户端IP” 和 “IP掩码” 指定了对网络中哪些范围的计算机进行控制，如果使用default关键字，则表示对所有的计算机进行控制，参数指定了具体的限制内容，常见的参数如下：

◆ ignore：拒绝连接到NTP服务器

◆ nomodiy： 客户端不能更改服务端的时间参数，但是客户端可以通过服务端进行网络校时。

◆ noquery： 不提供客户端的时间查询

◆ notrap： 不提供trap远程登录功能，trap服务是一种远程时间日志服务。

◆ notrust： 客户端除非通过认证，否则该客户端来源将被视为不信任子网 。

◆ nopeer： 提供时间服务，但不作为对等体。

◆ kod： 向不安全的访问者发送Kiss-Of-Death报文。

 

### ===server选项格式===

server host  [ key n ] [ version n ] [ prefer ] [ mode n ] [ minpoll n ] [ maxpoll n ] [ iburst ]

其中host是上层NTP服务器的IP地址或域名，随后所跟的参数解释如下所示：

◆ key： 表示所有发往服务器的报文包含有秘钥加密的认证信息，n是32位的整数，表示秘钥号。

◆ version： 表示发往上层服务器的报文使用的版本号，n默认是3，可以是1或者2。

◆ prefer： 如果有多个server选项，具有该参数的服务器有限使用。

◆ mode： 指定数据报文mode字段的值。

◆ minpoll： 指定与查询该服务器的最小时间间隔为2的n次方秒，n默认为6，范围为4-14。

◆ maxpoll： 指定与查询该服务器的最大时间间隔为2的n次方秒，n默认为10，范围为4-14。

◆ iburst： 当初始同步请求时，采用突发方式接连发送8个报文，时间间隔为2秒。

 

### ===查看网关方法===

【命令1】route -n 

【命令2】ip route show 

【命令3】netstat -r

 

### ===层次（stratum）===

stratum根据上层server的层次而设定（+1）。

对于提供network time service provider的主机来说，stratum的设定要尽可能准确。

而作为局域网的time service provider，通常将stratum设置为10

![img](https://images2017.cnblogs.com/blog/915691/201710/915691-20171013005125324-1966406641.png)

 

0层的服务器采用的是原子钟、GPS钟等物理设备，stratum 1与stratum 0 是直接相连的，

往后的stratum与上一层stratum通过网络相连，同一层的server也可以交互。

ntpd对下层client来说是service server，对于上层server来说它是client。

ntpd根据配置文件的参数决定是要为其他服务器提供时钟服务或者是从其他服务器同步时钟。所有的配置都在/etc/ntp.conf文件中。

![这里写图片描述](https://img-blog.csdn.net/20160917151428497)

 

### ===注意防火墙屏蔽ntp端口===

ntp服务器默认端口是123，如果防火墙是开启状态，在一些操作可能会出现错误，所以要记住关闭防火墙。

 

### ===同步硬件时钟===

ntp服务，默认只会同步系统时间。

如果想要让ntp同时同步硬件时间，可以设置/etc/sysconfig/ntpd文件，

在/etc/sysconfig/ntpd文件中，添加【SYNC_HWCLOCK=yes】这样，就可以让硬件时间与系统时间一起同步。

允许BIOS与系统时间同步，也可以通过hwclock -w 命令。

 

### ===ntpd、ntpdate的区别===

下面是网上关于ntpd与ntpdate区别的相关资料。如下所示所示：

使用之前得弄清楚一个问题，ntpd与ntpdate在更新时间时有什么区别。

ntpd不仅仅是时间同步服务器，它还可以做客户端与标准时间服务器进行同步时间，而且是平滑同步，

并非ntpdate立即同步，在生产环境中慎用ntpdate，也正如此两者不可同时运行。

时钟的跃变，对于某些程序会导致很严重的问题。

 

许多应用程序依赖连续的时钟——毕竟，这是一项常见的假定，即，取得的时间是线性的，

一些操作，例如数据库事务，通常会地依赖这样的事实：时间不会往回跳跃。

不幸的是，ntpdate调整时间的方式就是我们所说的”跃变“：在获得一个时间之后，ntpdate使用settimeofday(2)设置系统时间，

这有几个非常明显的问题：

【一】这样做不安全。

ntpdate的设置依赖于ntp服务器的安全性，攻击者可以利用一些软件设计上的缺陷，拿下ntp服务器并令与其同步的服务器执行某些消耗性的任务。

由于ntpdate采用的方式是跳变，跟随它的服务器无法知道是否发生了异常（时间不一样的时候，唯一的办法是以服务器为准）。

【二】这样做不精确。

一旦ntp服务器宕机，跟随它的服务器也就会无法同步时间。

与此不同，ntpd不仅能够校准计算机的时间，而且能够校准计算机的时钟。

【三】这样做不够优雅。

由于是跳变，而不是使时间变快或变慢，依赖时序的程序会出错

（例如，如果ntpdate发现你的时间快了，则可能会经历两个相同的时刻，对某些应用而言，这是致命的）。

因而，唯一一个可以令时间发生跳变的点，是计算机刚刚启动，但还没有启动很多服务的那个时候。

其余的时候，理想的做法是使用ntpd来校准时钟，而不是调整计算机时钟上的时间。

NTPD在和时间服务器的同步过程中，会把BIOS计时器的振荡频率偏差——或者说Local Clock的自然漂移(drift)——记录下来。

这样即使网络有问题，本机仍然能维持一个相当精确的走时。

 

### ===国内常用NTP服务器地址及IP===

```shell
210.72.145.44 (国家授时中心服务器IP地址)  
133.100.11.8 日本 福冈大学  
time-a.nist.gov 129.6.15.28 NIST, Gaithersburg, Maryland   
time-b.nist.gov 129.6.15.29 NIST, Gaithersburg, Maryland   
time-a.timefreq.bldrdoc.gov 132.163.4.101 NIST, Boulder, Colorado   
time-b.timefreq.bldrdoc.gov 132.163.4.102 NIST, Boulder, Colorado   
time-c.timefreq.bldrdoc.gov 132.163.4.103 NIST, Boulder, Colorado   
utcnist.colorado.edu 128.138.140.44 University of Colorado, Boulder   
time.nist.gov 192.43.244.18 NCAR, Boulder, Colorado   
time-nw.nist.gov 131.107.1.10 Microsoft, Redmond, Washington   
nist1.symmetricom.com 69.25.96.13 Symmetricom, San Jose, California   
nist1-dc.glassey.com 216.200.93.8 Abovenet, Virginia   
nist1-ny.glassey.com 208.184.49.9 Abovenet, New York City   
nist1-sj.glassey.com 207.126.98.204 Abovenet, San Jose, California   
nist1.aol-ca.truetime.com 207.200.81.113 TrueTime, AOL facility, Sunnyvale, California   
nist1.aol-va.truetime.com 64.236.96.53 TrueTime, AOL facility, Virginia  
————————————————————————————————————  
ntp.sjtu.edu.cn 202.120.2.101 (上海交通大学网络中心NTP服务器地址）  
s1a.time.edu.cn 北京邮电大学  
s1b.time.edu.cn 清华大学  
s1c.time.edu.cn 北京大学  
s1d.time.edu.cn 东南大学  
s1e.time.edu.cn 清华大学  
s2a.time.edu.cn 清华大学  
s2b.time.edu.cn 清华大学  
s2c.time.edu.cn 北京邮电大学  
s2d.time.edu.cn 西南地区网络中心  
s2e.time.edu.cn 西北地区网络中心  
s2f.time.edu.cn 东北地区网络中心  
s2g.time.edu.cn 华东南地区网络中心  
s2h.time.edu.cn 四川大学网络管理中心  
s2j.time.edu.cn 大连理工大学网络中心  
s2k.time.edu.cn CERNET桂林主节点  
s2m.time.edu.cn 北京大学
```