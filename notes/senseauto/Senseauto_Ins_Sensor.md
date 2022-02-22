## Ins Sensor

#### Imu（Inertial Measurement Unit）

惯性测量单元

```c++
typedef struct {
    ImuStatus status = ImuStatus::NOT_GOOD;

    float64_t measurement_time;

    /**
     * Linear acceleration of the IMU in the Vehicle reference frame
     * x for Forward, y for Left, z for Up, in meters per power second
     * 线加速度 单位: m/s2
     */
    Point3D_t linear_acceleration;

    /**
     * Angular velocity of the IMU in the Vehicle reference frame
     * x across Forward axes, y across Left axes,
     * z across Up axes, in radians per second
     * 角速度 单位: rad/s
     */
    Point3D_t angular_velocity;
} Imu;
```

#### Ins（Inertial Navigation System）

惯性导航系统

```c++
typedef struct {
    InsStatus status = InsStatus::INVALID;
    float64_t measurement_time;

    /**
     * Position of the INS(the IMU most of the time) in the Map reference frame.
     * Longitude and Latitude are in degrees, Height in meters.
     * 经纬高位置
     */
    PointLLH_t position;

    /**
     * Attitude of the IMU in the Map reference frame in radians.
     * Approximate to the Vehicle Reference Point(VRP) most of the time.
     * The VRP is the center of rear axle.
     * 欧拉角，相对于地图
     */
    EulerAngles_t euler_angle;

    /**
     * Linear velocity of the IMU in the Vehicle reference frame
     * x for Forward, y for Left, z for Up, in meters per second
     × 线速度 相对于自身，m/s
     */
    Point3D_t linear_velocity;
} Ins;
```

#### GNSS（Global Navigation Satellite System）

全球导航卫星系统

- 仅基于卫星，精度能达到米级

RTK

- （Real - time kinematic，实时动态）载波相位差分技术，厘米级精度
- 需要基站，单基站只能覆盖50km左右

```c++
typedef struct {
    GnssStatus status = GnssStatus::INVALID;
    float64_t measurement_time;

    /**
     * Position of the GNSS antenna phase center. in the Map reference frame.
     * Longitude and Latitude are in degrees, Height in meters.
     */
    PointLLH_t position;
    // East/north/up in meters.
    PointENU_t position_std_dev;

    // East/north/up in meters per second.
    PointENU_t linear_velocity;
    // East/north/up in meters per second.
    PointENU_t linear_velocity_std_dev;

    // Number of satellites in position solution.
    uint32_t num_sats;
} Gnss;
```

- 天线信息

```c++
typedef struct {
    GnssStatus status = GnssStatus::INVALID;
    float64_t measurement_time;

    /**
     * The heading is the angle from True North of the primary antenna to
     * secondary antenna vector in clockwise direction, in radians
     */
    float32_t heading;
    // heading standard deviation in degrees
    float32_t heading_std;

    // pitch angle in degrees
    float32_t pitch;
    // pitch standard deviation in degrees
    float32_t pitch_std;

    // Number of satellites in position solution.
    uint32_t num_sats;
} DualAntennaHeading;
```

#### Senseauto使用的数据

```shell
"log bestposb ontime 1", # not used
"log inspvab ontime 0.01", # INS position(LLH) velocity(ENU) atitude(Euler) 100Hz
"log rawimuxb ontime 0.01", # rawimux -- IMU Data Extended 
"saveconfig"
```

- Senseauto仅使用这两条消息即可计算
  - INSPVA
    - 位置(LLH)
    - 速度(ENU)，注意，Senseauto定义的ins消息似乎是自车的速度（仅注释这么写，需要确认注释的内容）。
    - 姿态(ENU)
  - RAWIMUX
    - 线加速度(自车)
    - 角速度(自车)



- Horizon处理方式
  - 当成一种ins来用
  - 录制的为rec的时候，专门标注为livox_imu.dump.rec，（在ros_node里做区别处理）