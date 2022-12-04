```
// full coverage 
bool MissionPlannerLanelet2::planFullCoveragePath(
  const geometry_msgs::PoseStamped & start_checkpoint,
  const geometry_msgs::PoseStamped & goal_checkpoint,
  lanelet::ConstLanelets * path_lanelets_ptr)
```



lanelet_map_ptr_: 加载的地图

getClosestLanelet（）：根据位置获取最近的Lanelet



getAjacentMatrix(); 获取routing_graph的邻接矩阵

LKHTSPSolver tsp_solver; 
LKH-3 Solver http://akira.ruc.dk/~keld/research/LKH-3/