执行的脚本：

```shell
./tools/rec_parser/scripts/offline_data_process.sh -i /home/SENSETIME/huangsiyuan/03-dataset/2020_11_06_11_02_21_AutoCollect \
 --output /home/SENSETIME/huangsiyuan/03-dataset/2020_11_06_11_02_21_AutoCollect/sensors_record_parsed \
 -c  /home/SENSETIME/huangsiyuan/03-dataset/2020_11_06_11_02_21_AutoCollect/config/vehicle/CN-009 \
 -e  /home/SENSETIME/huangsiyuan/03-dataset/2020_11_06_11_02_21_AutoCollect/config/vehicle/CN-009/gnss/gnss-to-top_center_lidar-extrinsic.json

```



困惑点：

1. 我们做sparse，或者说最后的数据中有哪些是有用的？LiDAR + Novatel?

```
你需要什么数据就解析什么数据，目前需要的是top_center_lidar的PCD
```

2. novatel解析中，需要提供enu_origin_file，这个是指gnss2car还是gnss2lidar?

```
enu坐标系是个相对坐标系，也是直角坐标系，需要指出原点的经纬高
-e rec_parser/config/sh_enu_origin.txt(我印象是这个名字)
```

3. 执行脚本中，有warning: 我们暂时没有用到timestam？

```shell
[WARN] Message sync bytes not found, ignored
        line: 106;file: /home/SENSETIME/huangsiyuan/02-workspace/0-SenseAuto/senseauto_init_script/repo_pro/senseauto/tools/rec_parser/src/parser/novatel_parser.cpp
-------这个我也不知道，WARN很多不用管
```

4. 提示我们enu无效：

```shell
extract NovAtel pose of CN-009 in enu
invalid origin
extract NovAtel pose of CN-009 in utm
output coord type is: utm
```

5. 解析过程中，提示：因而最后完全没有输出camera相关

```shell
jq: error: Could not open file /home/SENSETIME/huangsiyuan/03-dataset/2020_11_06_11_02_21_AutoCollect/sensors_record_parsed/config/vehicle/CN-009/hardware/camera_pylon_10.0.json: No such file or directory
```

6. 其他文件load失败：

```
Load /home/SENSETIME/huangsiyuan/03-dataset/2020_11_06_11_02_21_AutoCollect/sensors_record_parsed/top_center_lidar.timestamps failed
open /home/SENSETIME/huangsiyuan/03-dataset/2020_11_06_11_02_21_AutoCollect/sensors_record_parsed/top_center_lidar-enu.txt failed.
open /home/SENSETIME/huangsiyuan/03-dataset/2020_11_06_11_02_21_AutoCollect/sensors_record_parsed/-enu.txt failed.

```

7. 最后sparse的结果，和你当初给我的链接下载下来的有点不同，

```shell
├── config
│   └── vehicle
├── gps.txt
├── novatel_bestgnsspos.csv
├── novatel_bestpos.csv
├── novatel_dualantennaheading.csv
├── novatel-enu.txt
├── novatel_inspva.csv
├── novatel.LOG
├── novatel-pose.txt
├── novatel_rawimu.csv
├── novatel-utm.txt
├── top_center_lidar
└── vehicle_info.csv
```

