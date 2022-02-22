### Lidar

获取点云信息

```c++
LidarParserBase::GetAllPoints(
    uint64_t *target_time_ptr,
    uint64_t *end_point_time_ptr,
    pcl::PointCloud<senseAD::LidarPointXYZIR> *output,
    bool is_center,
    bool use_dist,
    std::map<uint64_t, senseAD::OdometryExt> *pose_map);
```

- is_center ： 是否输出到car_center坐标系，否则输出到target_frame坐标系，通常是lidar本身
- use_dist：是否运行点云运动补偿



##### 输出topic

- /sensor/lidar/<lidar_id>/point_cloud
  - lidar自身的点云，默认是lidar坐标系
- /sensor/lidar/fusion/point_cloud
  - 所有lidar的点云，默认是car_center坐标系
  - 对每个lidar可以配置是否加入fusion的点云