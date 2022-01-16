## dbc文件解析

**DBC文件**

DBC文件是用来描述CAN网络通信信号的一种格式文件。它可以用来监测与分析CAN网络上的报文数据，也可以用来模拟某个CAN节点。



**关键字对应对象：**

BU_ 网络节点

BO_ 报文

SG_ 信号

EV_ 环境变量



**本文出现的符号：**

' | ' ——可选择

' ; '——结束定义

[...]——内容可选（0或1次）

{...}——内容重复（0或多次）

(*...*)——注释

unsigned_integer：无符号整型

signed_integer：有符号整型

double：双精度小数

char_string：字符串

C_identifier：C语言变量命名


**1、DBC文件结构**

![img](https://pic4.zhimg.com/80/v2-41ed3ee54b0e982c78528b3a7eb5abdb_720w.png)

**非必须部分：**

♦ signal_types

♦ sigtype_attr_list

♦ category_definitions

♦ categories

♦ filter

♦ signal_type_refs

♦ signal_extended_value_type_list

**必须部分：**



♣ bit_timing

此部分为必须的，但是通常为空。

♣ nodes

定义网络节点。

♣ message

定义消息帧与信号。

**2、版本与新符号**

DBC文件头部包含着‘version’与‘new symbol’的信息，‘version’或为空，或由用户自行定义。

![img](https://pic3.zhimg.com/80/v2-b1273f0fd5855e8996c8f15d24204c86_720w.png)

**3、波特率定义**

![img](https://pic4.zhimg.com/80/v2-3ba37338111d59c18bd5f79098185a9b_720w.png)

bit timing 定义了CAN网络的波特率，[ ]内容表示为可选部分，可以被省略，但关键词 'BS_' 必须出现。

**4、节点定义**

![img](https://pic4.zhimg.com/80/v2-5547ff9ec686ae3db60dc9cd348f88db_720w.png)

节点定义名必须独一无二，命名规则与C语言变量相同。

**5、报文帧定义**

![img](https://pic2.zhimg.com/80/v2-d3c8e303911b02b87abd88121d93ce6d_720w.png)

报文的CAN-ID必须是独一无二的，message_name命名规则与C语言变量相同。message_size为无符号整型，规定了报文数据域的字节数。

![img](https://pic2.zhimg.com/80/v2-1494f402d8fb027c5a140e9ec1ed1a51_720w.png)

transmitter name表示报文发送节点，如果一个报文没有指定发送节点，则必须设置为‘Vector__XXX’。

**6、信号定义**

![img](https://pic3.zhimg.com/80/v2-7fe01c33a82f7bb2c05ff8d3505d5702_720w.png)

其中规定了信号名、起始位置、信号长度、字节顺序、数值类型、因子、偏移等关键信息。

![img](https://pic2.zhimg.com/80/v2-f925ccf168012f8f1804498c51800fd1_720w.png)

multiplexer_indicator定义了该信号是否为一个正常信号，或一个复用信号，此项可以被省略。

![img](https://pic1.zhimg.com/80/v2-5862e1c370ffd71932df6c2a070b4338_720w.png)

byte_order为字节顺序，0为intel格式，1为motorola。

![img](https://pic1.zhimg.com/80/v2-b6ecf48d7c806ae385ee3c10551056e4_720w.png)

value_type， + 无符号数， - 有符号数。

![img](https://pic3.zhimg.com/80/v2-c4fde92a2d48b27aa83a21b2f7318156_720w.png)

facator与offset用来将原始值与物理值之间进行转化。minumum与maximum为double类型，表示信号的最值范围。

![img](https://pic2.zhimg.com/80/v2-0ecf7763f6e02a8f0f71204b9b1ff0e9_720w.png)

unit为字符串，用来表示信号单位，receiver为接收者。如果一个信号没有指定接收者，则必须设置为‘Vector__XXX’。

**7、范例模板**

![img](https://pic3.zhimg.com/80/v2-78dc0bcff1252d46dce56dce34928436_720w.png)



![img](https://pic4.zhimg.com/80/v2-87651730775effac9b5f320220cd6333_720w.jpg)

**信号列表：**

![img](https://pic1.zhimg.com/80/v2-cf0c2ce53ffbbf8b87bd2b341e64f9dc_720w.png)

---

dbc对于汽车工程师来说，应该说是很熟了，它是用于描述整车CAN通信矩阵的文件，包括CAN消息的ID定义、收发周期、交互节点、数据场定义等，通常我们是用candb++来编辑dbc文件，很少有人去抠dbc文件的格式，下面就来捋一捋dbc的格式。

Dbc中主要的格式有以下几条：下面就分别捋一捋每条指令的意思。

```
BO_420 VCU_15: 8 VCU

SG_VCU_DCU_TorqSet : 24|12@0+ (1,-1000) [-1000|1022] "Nm" DCU
CM_BO_420"Transmitted by VCU,including TorqSet,TorqAct,ModeReq,";
CM_ SG_ 420 VCU_DCU_TorqSet "The DCU torque set ";
BA_ "GenMsgCycleTime" BO_ 420 1000;
BA_ "GenSigStartValue" SG_ 420 VCU_DCU_TorqSet 1000;
VAL_ 420 VCU_DCU_TorqSet 2000 "Invalid"
```

**1.BO_** **420** **VCU_15:** **8** **VCU**

BO_：代表一条消息的起始标识；

420：消息ID的十进制形式，=0x1A4；

VCU_15：消息名；

“:”：分割符号；

8：报文长度，帧字节数；

VCU：发出该消息的网络节点，标识也可以为为Vector__XXX，表示未指明具体节点；

**2.SG_** **VCU_DCU_TorqSet** **:24|12@0+** **(1,-1000)** **[-1000|1022]** **"Nm"** **DCU**

SG_：代表一个信号信息的起始标识;

VCU_DCU_TorqSet：信号名，分长名与短名，此处是短名，长为名非必须;

“:”：分割符号;

24：信号起始bit;

|：分割符号;

12：信号长度;

@0+ ：@0表示是Motorola格式（Intel格式是1），+表示是无符号数据

(1,-1000)：(精度值，偏移值);

[-1000|1022] ：[最小值|最大值]， 物理意义的最小与最大，现实世界的有物理意义的值，比如此处设定扭矩最大为1022Nm;

"Nm"：信号的单位;

DCU：接收处理此信号的节点，同样可以不指明，写为Vector__XXX;

**3.CM_** **BO_** **420"Transmitted** **by** **VCU,** **including** **TorqSet,TorqAct,ModeReq,"**

CM_ SG_ 420 VCU_DCU_TorqSet "The DCU torqueset "

CM_：起始标识，以上两条分别对CAN信息和信号的功能进行详细的描述，用于注释;

**4.BA_"GenMsgCycleTime"** **BO_** **420** **1000**

BA_：起始标识，用于描述BO_420的周期属性单位为ms，也就是说BO_420的周期为1000ms

**5.BA_"GenSigStartValue"** **SG_** **420** **VCU_DCU_TorqSet** **1000**

BA_：起始标识，用于描述信号VCU_DCU_TorqSet的初始值为1000



**6.VAL_** **420** **VCU_DCU_TorqSet2000** **"Invalid"**

VAL_：起始标识符，用于对信号值的描述，如上将信号VCU_DCU_TorqSet信号的无效值设置为2000。