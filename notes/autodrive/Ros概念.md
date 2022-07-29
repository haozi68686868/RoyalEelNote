# Ros笔记

- [Nodes](http://wiki.ros.org/Nodes): Node是使用ROS与其他节点通信的可执行文件
- [Messages](http://wiki.ros.org/Messages): ROS data type used when subscribing or publishing to a topic.
- [Topics](http://wiki.ros.org/Topics): Nodes can *publish* messages to a topic as well as *subscribe* to a topic to receive messages.
- [Master](http://wiki.ros.org/Master): Name service for ROS (i.e. helps nodes find each other)
- [rosout](http://wiki.ros.org/rosout): 相当于stdout 或者stderr
- [roscore](http://wiki.ros.org/roscore): Master + rosout + parameter server (parameter server will be introduced later)

###### ros::spin() 和 ros::spinOnce()

- spin()会反复回调；spinOnce()只调用一次，建议配合循环使用

### ros::AsyncSpinner 多线程订阅消息

只订阅1个话题时，使用ros::spin()进入接受循环



### ros::nodelet

可以实现多个nodelet在一个node中（一个进程中运行），相互通信可以没有copy损耗，而相互间认为是在同一个node



### ros::NodeHandle

1. advertise

2. advertiseService

3. createTimer

   - createTimer

   - createSteadyTimer

   - createWallTimer

4. getParam(const std::string &key, T &[s](http://docs.ros.org/en/melodic/api/xmlrpcpp/html/Validator_8cpp.html#aae737581b3c3d8d8c583c191c2f35fe9))
5. getParamCached
6. getParamNames (std::vector< std::string > &keys) s
7. hasParam(const std::string &key)
8. ok()
9. serviceClient
10. setParam
11. setCallbackQueue
12. shutdown
13. subscribe
14. 

### senseAuto Ros

NodeWrapper:

- 目前包含onExit/onInit/onReady/onRunning/onFailed五个状态，通过NodeStatus的多态调用
  - 目前派生出对应的ExitStatus/InitStatus/ReadyStatus/RunningStatus/FailedStatus，通过传入NodeWrapper的指针调用不同的回调：
    - e.g. FailedStatus::Execute(NodeWrapper *node_wrapper) → node_wrapper->onFailed()
    - （参考状态机设计模式）
  - 不同的wrapper可以重载以上五个函数，进行不同的操作：
    - **默认每个函数都是返回true（不做任何操作）**
  - Spin的函数持续不断的唤醒strategy进行操作
  - Heartbeat - Monitor:
    - 目前默认开启heartbeat，并期望由monitor控制ready到running的切换
      - 节点在Init的过程中，会通过服务查询monitor是否有效（总计尝试5次，每次1秒间隔）：
        - 是否有查询到monitor：
          - 是：询问monitor是否本节点需要同步状态切换：
            - 是：strategy使用wait-trigger模式：
              - init → ready后等待monitor指示
              - 同时初始化on monitor request的回调函数
            - 否：strategy使用classic模式：
              - init → ready → running，自动进入工作状态
          - 否：strategy进入classic模式：
            - init → ready → running，自动进入工作状态
    - onHeartbeatTimer和onMonitorRequest可以被具体的Wrapper重载
  - API：
    - AddEvent(senseAD::NodeState )：事件加入队列
    - Spin(): 持续回调，直到ros::ok()为false
- NodeStatus:
  - 用于改变NodeWrapper的状态以及执行不同的动作
  - 可以派生出不同Status类用作扩展
  - 所有的Status都与节点状态进行对应，并预先注册到一个全局的map中(map<NodeState, NodeStatus *>)
    - 目前沿用senseAD::NodeState作为节点状态：
      - e.g. { senseAD::NodeState::STARTING, new InitStatus() }
- NodeStrategy：
  - 维护有一张节点状态和Status的map，默认是全局注册表（依上述）
  - 内部维护有status的队列，每次都从队头取出一个事件
    - 在non-blocking模式下，如果队列为空，取出的事件为senseAD::NodeState::UNKNOWN，节点不做任务处理

#### 回放数据使用仿真时间

```shell
# 启动一个roscore
roscore
# 设置为使用仿真时间
rosparam set use_sim_time true
# 回放数据
rosbag play --clock xxx.bag
```

#### rosbag filter

```shell
rosbag filter input.bag output.bag "topic == '/odometry/gps' and t.to_sec() <= 1284703931.86"
```

