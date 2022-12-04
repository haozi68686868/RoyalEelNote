#### 输出端口（5Hz更新）

##### rostopic

- 节点状态

  - /monitor/node_status

  - ad_monitor_msgs::MonitorSummary

    - ```
      #ad_monitor_msgs::MonitorSummary.msg
      # Header include seq, timestamp(last node pub time), and frame_id(sensor model)
      std_msgs/Header header
      
      # type of the summary
      string type
      
      uint8 level
      # summary level enum:
      uint8 INFO = 0
      uint8 WARNING = 1
      uint8 ERROR = 2
      uint8 FATAL = 3
      
      # output data in json format
      string summary_data
      
      # suggestion for driver
      string suggestion
      ```

    - 

- 节点信息

  - /monitor/monitor_info

  - ad_monitor_msgs::MonitorSummary

  - ```
    struct MonitorInfo {
        bool is_auto_drive{false};
        int seq{0};
        std::string type{"monitor_info"};
        std::string topic{"monitor_info"};
        int64_t stamp;  // ms
        MonitorDetail monitor_detail;
        MonitorDiagnoseInfo diagnose_info;
    };
    
    struct MonitorDetail {
        IPCResource ipc_resource;
        RosTopicStatusSummary topic_detail_status_list;
        SystemCostTime system_cost_time;
        LidarStatisticSummary lidar_eval_list;
        CameraStatisticSummary camera_eval_list;
        InsStatisticSummary ins_summary;
        RadarStatisticSummary radar_eval_list;
        FusionStatusSummary fusion_status;
        NtpSummary ntp_summary;
        InterfaceSummary interface_summary;
        FrpcSummary frpc_summary;
    };
    
    struct MonitorDiagnoseInfo {
        MonitorDiagnoseInfo() { status = MONITOR_STATUS_NORMAL; }
        uint8_t status;
        std::vector<MonitorObjectDiagnoseInfo> info;
    };
    
    struct MonitorObjectAttributeInfo {
        uint8_t status;
        std::string name;
        std::string detail;
    };
    ```

- monitorDiagnoseInfo

  - 诊断信息

- monitorSummary

- plugin_data

  - 插件plugin的指针

##### proto

```protobuf
syntax = "proto3";

option java_multiple_files = true;
option java_package = "io.grpc.senseauto.monitor";
option java_outer_classname = "MonitorProto";
option objc_class_prefix = "HLW";

package monitor;

service Monitor {
  rpc GetSummary (SummaryRequest) returns (SummaryReply) {}
  rpc GetSummaryType (SummaryTypeRequest) returns (SummaryTypeReply) {}
}

enum Level {
  INTO = 0;
  WARNING = 1;
  ERROR = 2;
  FATAL = 3;
  UNSET = -1;
}

message SummaryRequest {
  string type = 1;
  Level min_level = 2;
  uint64 after_time_ns = 3;
}

message Summary {
  string type = 1;
  uint64 timestamp_ns = 2;
  Level level = 3;
  string summary_data = 4;
  string suggestion = 5;
}

message SummaryReply {
  repeated Summary data = 1;
}

message SummaryTypeRequest {
}

message SummaryTypeReply {
  repeated string types = 1;
}
```

- 定期更新：5Hz

----



- [1. monitor总体概述](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-1.monitor总体概述)
  - [1.1 状态描述](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-1.1状态描述)
  - [1.2 目前涵盖的监控内容](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-1.2目前涵盖的监控内容)
  - [1.3 平台支持](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-1.3平台支持)
  - [1.4 总体视觉效果图](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-1.4总体视觉效果图)
- [2. system资源监控](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-2.system资源监控)
  - [2.1 功能描述](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-2.1功能描述)
  - [2.2 关于数据获取](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-2.2关于数据获取)
  - [2.3 阈值设定与调整](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-2.3阈值设定与调整)
  - [2.4 多模式支持](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-2.4多模式支持)
  - [2.5 视觉效果图](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-2.5视觉效果图)
- [3. 节点监控](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-3.节点监控)
  - [3.1 功能描述](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-3.1功能描述)
  - [3.2 节点运行状态监控](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-3.2节点运行状态监控)
  - [3.3 关键函数耗时](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-3.3关键函数耗时)
  - [3.4 ros消息帧率及延迟](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-3.4ros消息帧率及延迟)
  - [3.5 节点的系统占用监控](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-3.5节点的系统占用监控)
- [4. 系统整体延迟](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-4.系统整体延迟)
  - [4.1 数据获取](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-4.1数据获取)
  - [4.2 每个节点的耗时参考计算方式](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-4.2每个节点的耗时参考计算方式)
  - [4.3整体延迟的参考计算方式](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-4.3整体延迟的参考计算方式)
  - [4.5 视觉效果图](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-4.5视觉效果图)
- [5. frpc服务监控](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-5.frpc服务监控)
- [6. 定位融合状态监控](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-6.定位融合状态监控)
- [7. NTP监控](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-7.NTP监控)
  - [7.1 数据获取](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-7.1数据获取)
  - [7.2 视觉效果图](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-7.2视觉效果图)
  - [7.3 多模式行为](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-7.3多模式行为)
- [8. Lidar监控](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-8.Lidar监控)
  - [8.1 数据获取](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-8.1数据获取)
  - [8.2 视觉效果图](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-8.2视觉效果图)
  - [8.3 多模式行为](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-8.3多模式行为)
- [9. Camera监控](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-9.Camera监控)
  - [9.1 数据获取](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-9.1数据获取)
  - [9.2 视觉效果图](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-9.2视觉效果图)
  - [9.3 多模式行为](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-9.3多模式行为)
- [10. Radar监控](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-10.Radar监控)
  - [10.1 数据获取](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-10.1数据获取)
  - [10.2 视觉效果图](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-10.2视觉效果图)
  - [10.3 多模式行为](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-10.3多模式行为)
- [11. Ins监控](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-11.Ins监控)
  - [11.1 数据获取](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-11.1数据获取)
  - [11.2 视觉效果图](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-11.2视觉效果图)
  - [11.3 多模式行为](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-11.3多模式行为)
- [12. 接口状态监控](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-12.接口状态监控)
  - [12.1 数据获取](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-12.1数据获取)
  - [12.2 视觉效果图](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-12.2视觉效果图)
  - [12.3 多模式行为](https://confluence.senseauto.com/pages/viewpage.action?pageId=39157160#monitor使用手册（更新至monitorv2.0版本）-12.3多模式行为)

monitor肩负着系统中的一个重要使命，需要通过它来实现监控运行的系统，并可以直观的看出各个系统组件的状态，从而快速且准确的定位系统软硬件问题。



 本文档主要介绍monitor的功能及具体实现原理，用户如何与hmi界面交互，获取监控信息。

### 1. monitor总体概述

#### 1.1 状态描述

​     Monitor会对监控对象的状态进行诊断分析，诊断结果分为三个状态，状态量和颜色表征分别为：

- **NORMAL**
- **WARN**
- **ERROR**

​    如何对待报警信息？

- 持续爆红的情况，需要引起注意，尤其是处于自动驾驶过程中，视情况可能需要停止自动驾驶进行问题排查
- 瞬间爆红而后恢复后有复现，视情况可能需要停止自动驾驶进行问题排查
- 瞬间爆红而后恢复不再复现，可以继续自动驾驶，记录后续排查
- 持续爆黄或者爆黄而后恢复后有复现，可以继续自动驾驶，可以记录后续排查
- 瞬间爆黄而后不再复现，可以继续自动驾驶，可以记录后续排查，优先级较低

#### **1.2 目前涵盖的监控内容**

- system资源监控
  - cpu、gpu、内存、显存、缓存、cpu iowait等的总体占用率
  - cpu、gpu、内存、显存的总体占用均值及最值统计
  - 磁盘实时读写速度、磁盘读写最大速率、磁盘剩余空间
- 节点监控
  - 资源监控
    - 重要节点的系统占用（cpu使用率、gpu使用率、内存、显存）
    - 每个节点线程数量监控
    - 各个节点系统占用的均值，最值统计
  - 状态
    - 节点运行状态（是否崩溃、是否卡死）
    - 各个节点关键ros消息帧率、关键ros消息延迟
    - 各个节点关键函数的耗时，及关键函数的均值最值统计
- 硬件监控
  - 传感器监控（camera、lidar、radar、ntp、imu）
    - 传感器通信是否正常
    - 传感器数据延迟、丢帧等
  - ntp、定位融合状态
    - 定位融合状态
    - ntp时间同步状态，和具体的offset
      - 工控机、sensehub、lidar、imu时间同步状态
  - 外设接口检查
    - 接口配置是否正常（接口名、ip等），需要要硬件镜像中保持一致
    - 接口状态是否正常（up），包括can口、网口、gmsl口
- frpc远程连接服务功能监控
- 系统延迟（传感器到最终决策控制的延时），即各个中间过程的延迟总和
- 融合状态监控

#### 1.3 平台支持

- L4实车，仿真，离线回放模式及其他模式
- L2实车，仿真，离线回放模式及其他模式

#### 1.4 总体视觉效果图

monitor的HMI界面分为两层，第一层是主界面，主要展示节点信息及少量监控信息；

第二层是详细页面，包含所有的监控项具体数据及对应图形展示。

![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-17%2015-41-01.png?version=1&modificationDate=1645084514000&api=v2)

​                     **首页视觉图**

![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-18%2014-53-49.png?version=1&modificationDate=1645167285000&api=v2)![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-18%2014-45-15.png?version=2&modificationDate=1645167299000&api=v2)![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-18%2014-44-23.png?version=2&modificationDate=1645167299000&api=v2)![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-18%2014-45-01.png?version=2&modificationDate=1645167299000&api=v2)![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-18%2014-44-09.png?version=2&modificationDate=1645167299000&api=v2)![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-18%2014-45-27.png?version=2&modificationDate=1645167299000&api=v2)

**详细页面**

### 2. system资源监控

#### 2.1 功能描述

  系统资源监控，每隔3秒获取一次当前系统的以下数据：

- cpu
  - 总体 iowait
  - 总体使用率
- 内存
  - 内存整体占用情况
  - 缓存整体使用情况
- GPU（若多于一块，则每块的具体数据都展示）
  - 显存占用
  - GPU使用率
- 磁盘（仅监控系统盘）
  - 剩余空间
  - 实时读取速度
  - 实时写入速度
  - 磁盘满负荷下的写入性能（仅启动时性能测试一次，后续不再更新）
  - 磁盘满负荷下的读取性能（仅启动时性能测试一次，后续不再更新）

  然后，将这些值与预先设置好的阈值进行对比，其中GPU信息获取方式是异步的，其他都是同步的。这里的阈值分为两种，警告阈值与错误阈值，结果有三种，

- **NORMAL，未达到警告阈值
  **
- **WARN， 达到警告阈值但未达到错误阈值，前端会爆黄
  **
- **ERROR，达到错误阈值，前端爆红**

不管诊断结果如何，前端都会显示这些数据，如果出现**WARN**和**ERROR**的情况，前端还会给出具体

错误信息。

另外，monitor还对cpu使用率、gpu使用率、内存、显存的总体占用的均值及最值进行了统计，并在前端进行展示。目前均值统计支持以下两种模式，

可以通过设置/opt/ros/kinetic/share/ros_monitor/launch 文件的 statistics_for_auto_mode变量来实现切换，因为自动模式下的数据更有参考意义，默认设置为自动模式。

- 自动模式(默认)，仅对自动驾驶模式下数据进行统计， statistics_for_auto_mode设置为true
- 默认模式，系统启动后所有采集的数据均加入统计，statistics_for_auto_mode设置为false

#### 2.2 关于数据获取

  主要通过下面方式获取，

- proc文件系统
  - cpu， 通过读取/proc/stat， 解析文件，计算得到**cpu及iowait**使用率
  - 内存，通过读取/proc/meminfo， 解析文件，计算得到**内存及缓存**整体使用情况
  - 磁盘实时读取写入情况，通过读取/proc/diskstats，解析文件，计算得到当前磁盘**写入与读取**速度
- nvidia-smi工具
  - gpu使用率
  - gpu显存信息及使用情况
- 其他
  - 磁盘剩余空间，通过读取 /etc/mtab， 解析文件，计算得到当前磁盘剩余空间
  - 磁盘读写性能，通过dd命令工具，读写一定量大小的数据，得到对应的磁盘读写性能数据

#### 2.3 阈值设定与调整

警告阈值：警告阈值的设定，经过一些实车测试实验后，以实际驾驶过程中比最大值较大一些的值作为参考警告值。

错误阈值：设定为一般情况下达不到的一个值。

阈值调整：软件或者硬件版本有更新的情况下，可能会导致正常行驶的数据值发现变化，这种情况下需要进行阈值调整，目前由 [陈坚](https://confluence.senseauto.com/display/~chenjian5) [欧明阳](https://confluence.senseauto.com/display/~oumingyang) 负责。

#### 2.4 多模式支持

系统资源检测功能，支持目前L2和L4的所有的模式下获取系统资源信息，需要注意的是，

我们只在L2/L4实车模式下进行阈值诊断与上报，其余模式下都只是获取系统资源占用及前端显示，不会进行诊断。

#### 2.5 视觉效果图

 

#### ![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-17%2015-30-13.png?version=1&modificationDate=1645083043000&api=v2)

​      cpu及gpu占用(HMI主页面右上角)

![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-17%2015-01-58.png?version=1&modificationDate=1645082717000&api=v2)

​                                 系统监控详细页面

![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-17%2015-33-17.png?version=1&modificationDate=1645083398000&api=v2)

​                                        统计值列表

### 3. 节点监控

#### 3.1 功能描述

- 节点的运行状态，基本上覆盖了除了visualizer节点之外的绝大部分节点
- 节点关键函数的耗时，及关键函数的均值最值统计
- 节点ros消息帧率及延迟
- 节点的系统占用(cpu使用率、gpu使用率、内存、显存、线程数量)
- 节点cpu使用率、gpu使用率、内存、显存,关键函数耗时均值，最值统计

#### 3.2 节点运行状态监控

- **实现方式**：每个被监控的节点都需要发出一个名为 “/node_state” 的 ros 消息，消息类型参考 senseauto-msgs/ad_monitor_msgs/msg/NodeStateInfo.msg，

里边包含节点名字、pid、节点状态等信息, monitor会接收这个消息并进行监控，如果节点超过3秒没有发出这个 ros 消息，就判定该节点为异常。

- **监控节点的获取**：daemon 启动时会指定一个模式(对应一个xml文件)，里面包含了所有启动的节点，monitor会从这里获取节点信息。

​      另外，monitor为维护一个需要监控节点的进程及阈值配置列表（L2和L4各一份，不同分支)，我们取这二者的交集作为最终实际会监控的进程集合。

- **多模式行为：**支持目前L2及L4的所有模式，离线与实车情况行为均相同。
- **视觉效果图**

**![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-17%2017-00-50.png?version=1&modificationDate=1645088492000&api=v2)**



#### 3.3 关键函数耗时

将各个模块的关键函数耗时收集并显示到前端，但还不支持关键函数耗时的诊断。

- 实现方式：由各个节点内部统计，并将统计结果通过“/node_state” 的 ros 消息发出，monitor收集并汇总到前端。
- 多模式行为：支持目前L2及L4的所有模式，离线与实车情况行为均相同。
- 目前已统计的各个模块关键函数汇总               

| L4                    | 模块                                                         | 关键函数              | L2                                                           | 模块 | 关键函数 |
| --------------------- | ------------------------------------------------------------ | --------------------- | ------------------------------------------------------------ | ---- | -------- |
| monitor               | onTimer()                                                    | monitor               | onTimer()                                                    |      |          |
| lidar                 | threadWorker()                                               | lidar                 | threadWorker()                                               |      |          |
| perception_lidar      | onPointCloud()                                               | perception_lidar      | onPointCloud()                                               |      |          |
| camera                | GetImage()                                                   | camera                | GetImage()                                                   |      |          |
| perception_camera     | onIPCImage()                                                 | perception_camera     | onIPCImage()                                                 |      |          |
| radar                 | publishContiX08Radar()                                       | radar                 | publishContiX08Radar()                                       |      |          |
| perception_radar      | onContiArs408Radar()                                         | perception_radar      | onContiArs408Radar()onContiArs308Radar()                     |      |          |
| ins                   | GnssCallback()ImuCallback()InsCallback()DualAntennaHeadingCallback() | ins                   | GnssCallback()ImuCallback()InsCallback()DualAntennaHeadingCallback() |      |          |
| perception_aggregator | ProcessAggregator()                                          | perception_aggregator | ProcessAggregatorWithDataBuffer()                            |      |          |
| decision_planning     | MakePlanning()MakeDecision()                                 | pilot_decision        | DMPPonTimer()                                                |      |          |
| localization          | manager_FrontendProcess()                                    | localization          | manager_FrontendProcess()                                    |      |          |
| prediction            | onFusionObject()                                             | pilot_prediction      | onFusionObject()                                             |      |          |
| hdmap                 | publishSubmapData()                                          | hdmap                 | publishSubmapData()                                          |      |          |
| control               | onTimer()                                                    | pilot_control         | onTimer()                                                    |      |          |



如果有模块有新增关键函数耗时监控需求，请联系 [陈坚](https://confluence.senseauto.com/display/~chenjian5) [欧明阳](https://confluence.senseauto.com/display/~oumingyang)。

- 视觉效果图

![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-17%2017-05-08.png?version=1&modificationDate=1645088850000&api=v2)

![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-17%2017-08-55.png?version=1&modificationDate=1645089468000&api=v2)![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-17%2017-14-55.png?version=1&modificationDate=1645089468000&api=v2)

#### 3.4 ros消息帧率及延迟

- 实现方式

  ： 会监控ros topic的三个维度,

  - 两帧之间的时间差
  - 一段时间（目前设置为1秒）的平均帧率，计算方式为一秒内收到的消息数目
  - 消息延迟，计算方式是当前时间减去ros 消息的header时间戳

​    获取这部分数据后，会对这三维的数据进行数值诊断，有异常的，上报给前端显示。诊断状态同样为normal,warn,error三种。

​    每个ros消息都会和一个节点绑定，如果一个节点同时绑定了多个消息，那么会设置其中一个作为关键消息帧率，前端主界面会展示这个关键消息帧率。

- **配置相关**

​    目前L2与L4的平台分别维护一份ros消息监控列表。    

​    阈值配置，由于不同的消息发出频率有差别，因此不同的消息其两帧时间差及平均帧率阈值会不同，消息延迟与帧率无关，目前设置为一个统一的值。

​    除了阈值，每个消息绑定的节点名及改消息是否为关键消息的配置。目前配置中只覆盖了部分关键消息， 如果有需要新增ros消息，可以联系 [陈坚](https://confluence.senseauto.com/display/~chenjian5) [欧明阳](https://confluence.senseauto.com/display/~oumingyang) 。

​    目前支持的ros消息：

```
L4：``/perception/camera/traffic_light_sign``/perception/fusion/object``/perception/lidar/dangerous_zone``/perception/lidar/object``/decision_planning/decision_debug``/decision_planning/planning_debug``/decision_planning/decision_target``/decision_planning/trajectory``/decision_planning/trajectory_for_prediction``/sensor/dual_antenna_heading``/sensor/gnss``/sensor/imu``/prediction/objects``/prediction/collected_objects``/canbus/vehicle_command``/canbus/vehicle_report``/hdmap/sub_map``/localization/navstate_info``/control/control_debug` `L2：``/perception/fusion/object``/decision_planning/decision_debug``/decision_planning/planning_debug``/decision_planning/decision_target``/decision_planning/trajectory``/sensor/dual_antenna_heading``/sensor/gnss``/sensor/imu``/sensor/ins``/prediction/objects``/prediction/collected_objects``/canbus/vehicle_command``/canbus/vehicle_report``/hdmap/sub_map``/localization/navstate_info``/control/control_debug``/sensor/radar/front``/sensor/radar/front_left``/sensor/radar/front_right``/sensor/radar/rear_right``/sensor/radar/rear_left``/ved/ved_info
```



- **多模式行为**

​    目前只在L2/L4实车模式下进行ros消息帧率的数据获取与诊断上报，其余模式下不进行数据获取，也不进行数据诊断。

- 视觉效果图(**todo 显示关键消息的名字**)

![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-18%2011-57-02.png?version=1&modificationDate=1645157135000&api=v2)![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-18%2011-58-49.png?version=1&modificationDate=1645157135000&api=v2)

![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-18%2014-11-27.png?version=1&modificationDate=1645164713000&api=v2)![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-18%2014-15-51.png?version=1&modificationDate=1645164985000&api=v2)

#### 3.5 节点的系统占用监控

  三秒获取一次进程的cpu使用率，gpu使用率，内存使用，显存使用，线程数，并与阈值对比诊断，当出现warn和error的情况，结果汇总给前端。

  gpu数据采用的是异步获取，其余均采用同步获取的方式。

  **阈值设定**：与系统资源监控类似，可以参考2.4

  **数据获取：**

- 通过proc 文件系统获取，
  - 进程cpu使用率，/proc/pid/stat
  - 进程内存使用，/proc/pid/statm
  - 进程线程数，/proc/pid/status
- nvidia-smi工具
  - 进程显存占用
- nvtop 开源工具
  - 进程gpu使用率

原始的nvtop是一个死循环的界面，主要是用来实时通过界面观察的，无法直接使用，目前是在开源工具基础上，加上了获取一次数据，按照一定格式输出文件并自动退出的功能。

**多模式行为：与系统资源监控类似，可以参考2.5**

**视觉效果图**

![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-18%2014-27-06.png?version=1&modificationDate=1645165735000&api=v2)![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-18%2014-27-29.png?version=1&modificationDate=1645165735000&api=v2)

**3.6 数据统计**

对进程的cpu使用率，gpu使用率，内存使用，显存使用，及关键函数耗时进行最值及平均值的统计，

与系统资源的统计类似，支持默认与自动模式两种方式。实车与离线模式行为相同。

**视觉效果图**

**![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-18%2014-29-44.png?version=2&modificationDate=1645165883000&api=v2)**

### 4. 系统整体延迟

#### **4.1 数据获取**

 每个节点自己统计节点耗时，并通过/node_state 消息发出，再由monitor统一计算，给到前端展示，但不会进行阈值诊断

#### **4.2 每个节点的耗时参考计算方式**

[系统整体耗时需求信息确认](https://confluence.senseauto.com/pages/viewpage.action?pageId=34950267)

#### **4.3整体延迟的参考计算方式**

由于很多模块的数据处理是并行的，下面的计算方式并不能严格反应从传感器到决策控制的耗时，但是可以作为重要的参考指标

```
L4：``system_cost_time = perception_aggregator + prediction + decision_planning + control +``  ``max(radar + perception_radar, lidar + perception_lidar, camera + max(perception_camera_od, perception_camera_tl))``L2：``system_cost_time = perception_aggregator + pilot_prediction + pilot_decision + pilot_control +``  ``max(radar + perception_radar, lidar, camera + max(center_camera_perception, left_camera_perception, right_camera_perception, rear_camera_perception))
```

**4.4 多模式行为：**仅支持L2/L4实车模式

#### 4.5 视觉效果图

![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-18%2014-33-20.png?version=1&modificationDate=1645166072000&api=v2)

### 5. frpc服务监控

  frpc服务是用于支持远程ssh连接实车的服务。

**实现方式**

- 检测进程是否处于运行状态，通过pgrep实现
- 检测当前使用的端口号是否与laelap远程数据库一致

 **多模式行为**

   仅在l2/l4实车模式下开启

**视觉效果图**

**![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-18%2014-38-03.png?version=1&modificationDate=1645166334000&api=v2)**

### 6. 定位融合状态监控

**实现方式**：ins和localization模块会通过ros消息发出状态信息，monitor会进行状态信息收集与诊断，并将结果反馈到前端。

这里只有两种状态，融合状态匹配为normal，不匹配为error。

**多模式行为：** 只支持L4/L2实车模式，其他模式默认关闭

**视觉效果图**

**![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-18%2014-39-51.png?version=1&modificationDate=1645166542000&api=v2)![img](https://confluence.senseauto.com/download/attachments/39157160/Screenshot%20from%202022-02-18%2014-41-26.png?version=1&modificationDate=1645166542000&api=v2)**



### 7. NTP监控

#### **7.1 数据获取**

- ntp监控的对象包括：同步状态、卫星连接、层级、时间是否更新、时间差，如果设备是sensehub的话，还会增加sensehub的软硬件版本检查。
- ntp同步状态的获取是通过执行"ntpstat"和"ntpq -p"来获取的。通过解析终端命令结果，得到上述监控对象的信息。
- 如果设备是sensehub，会通过shell命令进入sensehub，解析/mnt下的md5sum-SW-V2.3-HW-DCU2.1.txt文件来获取软硬件版本信息，如下图所示

![img](https://confluence.senseauto.com/download/attachments/39157160/WXWorkCapture_16425797208763.png?version=1&modificationDate=1645185937000&api=v2)

#### **7.2 视觉效果图 **

在【其他】栏中，包含有ntp的监控信息，包括ntp服务设备、同步状态和时间差。如果是sensehub，还会显示出其软硬件版本号。如果有error爆出，会在当前页面下方显示具体的错误原因，比如层级错误、offset超阈值等。

**![img](https://confluence.senseauto.com/download/attachments/39157160/ntp_miaoan.png?version=1&modificationDate=1645249178000&api=v2)![img](https://confluence.senseauto.com/download/attachments/39157160/sensehub.png?version=1&modificationDate=1645257251000&api=v2)**

#### **7.3 多模式行为**

只支持L4/L2实车模式，其他模式默认关闭。

### 8. Lidar监控

Lidar的监控项包括：lidar通信、lidar网页配置（仅支持Pandar系列），lidar硬件状态（如授时状态，仅支持Pandar系列），点云帧率和延时。

#### **8.1 数据获取**

- Pandar系列的配置和状态均可以从网页中直接获取，包括GPS连接状态、NEMA状态、Lidar目标端口、转速、GPS目标端口、时钟源、FOV设置等。在monitor中通过curl的方式访问lidar ip对应的网页、并解析出对应的字段。
- Lidar点云的帧率和延时统计数据来自sensor，sensor会发出/sensor/lidar/eval_data的topic，monitor在接收该topic后，会对其中的帧率和延时做判断，同时将数据发送给前端，绘出lidar的帧率和延时图。

#### **8.2 视觉效果图**

在【sensor】栏，点击Lidar，即可查看点云帧率和延时的实时统计图。如果有error爆出（包括lidar配置错误、lidar硬件状态错误、帧率和延时超阈值的错误），会在当前页面直接显示。

**![img](https://confluence.senseauto.com/download/attachments/39157160/lidar.png?version=1&modificationDate=1645250306000&api=v2)**

#### **8.3 多模式行为**

只支持L4/L2实车模式，其他模式默认关闭。

### 9. Camera监控

Camera的监控项包括：camera通信、帧率、延时、相机间的时间同步，如果使用zmq相机的话，还会包括sensehub_fps检查、camera_profile检查、dcu相机连接检查。

#### **9.1 数据获取**

- camera_profile的检查，是通过shell命令进入sensehub、并执行其内部的脚本来实现的，包括

  - `sshpass -p 'zynq' ssh -o StrictHostKeyChecking=no root@${sensehub_ip} 'cat .autostart/common/profile.sh |grep HAS_NOVATEL'`
  - `sshpass -p 'zynq' ssh -o StrictHostKeyChecking=no root@${sensehub_ip} 'cat .autostart/common/profile.sh |grep CAMERA_TYPE='`
  - `sshpass -p 'zynq' ssh -o StrictHostKeyChecking=no root@${sensehub_ip} 'cat .autostart/common/profile.sh |grep CAMERA_ARRAY'`

- sensehub_fps的检查，是通过shell命令进入sensehub、查看interupts来实现的

  - `sshpass -p 'zynq' ssh -o StrictHostKeyChecking=no root@${sensehub_ip} 'cat /proc/interrupts |grep csi2r'`

- ```
  dcu相机连接的检查，是通过shell命令进入sensehub、并执行其内部的脚本来实现的，具体方式为
  ```

  - `sshpass -p 'zynq' ssh -o StrictHostKeyChecking=no root@${ip_address} 'cd .autostart && ./check_scripts/check_dcu2_link_status.sh'`

- camera帧率、延时和时间同步的信息来自于sensor，sensor会发出/sensor/camera/eval_data的topic，monitor在收到该topic之后，会对其中的帧率、延时和时间同步做判断，同时将数据发送给前端，绘出camera的帧率和延时图。

#### **9.2 视觉效果图**

在【sensor】栏，点击Camera，即可查看相机帧率和延时的实时统计图。如果有error爆出，会在当前页面直接显示。

**![img](https://confluence.senseauto.com/download/attachments/39157160/ccamera.png?version=1&modificationDate=1645251393000&api=v2)**

#### **9.3 多模式行为**

只支持L4/L2实车模式，其他模式默认关闭。

### 10. Radar监控

Radar监控项主要包括各个radar的实时状态（跟踪目标扩展信息、目标质量信息、检测模式、运动状态等），同时会对radar的软件版本做检查。

#### **10.1 数据获取**

Radar的实时状态信息和软件版本信息都来自sensor模块。在sensor模块中，解析出0x201的CAN报文，即可获得radar state；解析出0x700的CAN报文，即可获得software version。在获取radar state和software version之后，sensor模块会发出/sensor/radar/eval_data的topic，monitor在收到该topic后，与配置文件作对比，检查radar的状态和软件版本。

#### **10.2 视觉效果图**

在【sensor】栏，点击Radar，即可查看对应的监控信息，每个radar的state报文信息都会在该页面显示，同时如果有error爆出，也会直接显示在该页面内，如下图检测到软件版本错误。

**![img](https://confluence.senseauto.com/download/attachments/39157160/radar.png?version=1&modificationDate=1645252010000&api=v2)**

#### **10.3 多模式行为**

只支持L4/L2实车模式，其他模式默认关闭。

### 11. Ins监控

monitor对ins的监控，目前可以适配Bynav和Novatel两种设备。监控项均包含通信检查、配置检查和RTK检查，同时包含ins数据解析的延时监控。

#### **11.1 数据获取**

- Novatel：利用串口通信，对设备发出对应的log指令，对结果进行字符串解析，查看配置及信号接收是否正常
  - log comconfig \n指令，可以查看COM配置
  - log loglista once \n指令，可以查看GPRMC和GPGGA的配置
  - log ppscontrol once \n指令，可以查看PPS配置
  - log bestposa once \n、log rtkvela \n、log passcom1a \n指令，可以完成RTK的检查
- Bynav：利用TCP通信，对设备发出对应的log指令，对结果进行字符串解析，查看配置及信号接收是否正常
  - log insconfig\r\n指令，可以获取臂杆参数
  - log comconfig once\r\n指令，可以获取COM配置
  - log loglista once\r\n指令，可以查看GPRMC和GPGGA的配置
  - FREQUENCYOUT\r\n指令，可以查看PPS配置
  - log bestposa once\r\n、TRANS ON COM2 ICOM1\r\n指令，可以完成RTK的检查
- sensor模块会发出/sensor/ins/eval_data的topic，包含ins数据解析的延时统计，monitor在收到该数据后，发送给前端绘图。

#### **11.2 视觉效果图**

在【sensor】栏，点击INS，即可查看对应的监控信息和延时统计图。对应的error也会在该页面显示。

在地库，ins设备由于卫星信号的限制，RTK的检查会报错。且由于ins的检查较为耗时，monitor启动后可能会在前端观察到所有的监控项均为error，这是因为monitor还没获取到第一次的检查结果，且监控项的初始值均为false。在启动大约50s之后，monitor会拿到ins的第一次检查结果，并更新到前端。

**![img](https://confluence.senseauto.com/download/attachments/39157160/ins.png?version=1&modificationDate=1645253085000&api=v2)![img](https://confluence.senseauto.com/download/attachments/39157160/ins2.png?version=1&modificationDate=1645253154000&api=v2)**

#### **11.3 多模式行为**

只支持L4/L2实车模式，其他模式默认关闭。

### 12. 接口状态监控

接口状态监控，主要包括CAN口和网口的检查。

#### **12.1 数据获取**

- CAN口：通过candump获取CAN口的输出，并判断是否有对应的can_id
- 网口：执行ping，获取网口的连接状态、延时和丢包率

#### **12.2 视觉效果图**

在【其他】栏，可以看到CAN口和网口实时状态，如果为绿色，则表示接口正常，如果是红色，说明接口状态异常。

www.baidu.com是为了检查访问外网的情况，若该状态为红色，可能是因为访问受限（由于访问频率的限制由于访问频率的限制），可以本地测试一下是否可以正常访问外网。

若CAN口报错，可以先联系@欧明阳查看。

**![img](https://confluence.senseauto.com/download/attachments/39157160/can.png?version=1&modificationDate=1645254349000&api=v2)**

#### **12.3 多模式行为**

只支持L4/L2实车模式，其他模式默认关闭。