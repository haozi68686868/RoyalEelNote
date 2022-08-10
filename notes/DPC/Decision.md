#### 输入

红绿灯

车辆信息（底盘信息、用户按键信息）

全局路径信息

障碍物信息（预测结果）

地图信息

## L4

#### 

1. Distillation（蒸馏）：根据输入提取关键信息，便于后续逻辑决策
   - 红绿灯关联
   - 动态障碍物
   - 换道可行性分析
   - 换道参考线
2. 

#### 场景（Scenario）

- 提问，如何判断当前的场景？
  - 场景到另一个场景有切换逻辑
- Scenario+内部stage
- 横向场景
  - implicit_routing_lane_change
  - lane_keep
  - lane_keep_nudge
  - manual_lane_change
  - obstacle_lane_change
  - open_space_lanekeep
  - routing_lane_change
  - reroute
- 纵向场景
  - cruise
  - danger_space
  - junction
  - junction_slowdown
  - lateral_request_stop
  - openspace_cruise
  - pullover（靠边）
  - vru_cross_scenario

#### 任务（Task）

- 纵向
  - CruiseTask
  - StopTask
  - Slowdown
- 横向
  - LaneKeep
    - lane_keep_implicit
    - lane_keep_openspace
    - lane_keep_nudge
  - LaneChange