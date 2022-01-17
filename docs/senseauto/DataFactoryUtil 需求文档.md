# DataFactoryUtil 需求文档

### 背景简介

​	提出DataFactoryUtil的原始需求来源于通用评测工具，没有提供一个友好的评测配置工具。对于DataFactoryUtil，期望他能完成两个功能：

1. 多种数据格式的浏览器，可以方便查看数据的结构
2. 提供友好的人机交互接口，编辑并添加评测任务的Evaluator，可以通过该工具直接生成EvaluatorTask.json（通用评测工具的配置文件）

### 详细需求

#### 功能1

1. 支持多种数据格式：
   - 优先支持：jsonFile / jsonLine
     - jsonFile: 一份数据为一个文件夹，每个文件1个json
     - jsonLine: 一份数据为单个文件，每行数据为1个json
   - 需要支持：yaml / rosbag
2. 可以智能识别可支持的数据格式：用户选择一个数据路径，自动识别出数据类型
3. 可以支持仅浏览一个数据，也可支持同时查看两个数据，数据的类型和结构可以完全不同。
4. 数据结构以树状展示，可以折叠和展开
5. 选中数据时，可以显示其类型(可以设计为触发式)
   - 基本类型：
     - 数值类型：double / int / bool / string / vector(可以区分float vector和int vector)
     - 结构类型：object / array
6. 对于每一个元素，可以有一个函数得到它的key值，详见"通用评测工具使用文档"中定义的key
7. 程序架构要求易于拓展支持新的数据格式，即只需要写数据格式解析部分的新代码

#### 功能2

1. 本质上也是一个evaluatorTask的浏览器和编辑器，可以完成交互式修改任务
2. 可以完成打开(读取解析)、保存、另存为等操作
3. evaluatorTask目前包含两种内容：dataLoader和evaluators
   - 对于dataloader
     1. 可以修改dataloader的数据路径及识别数据类型
     2. 修改时间格式
     3. 指定时间戳的数据元素（key值）
   - 对于evaluators
     - 可以浏览当前task的所有evaluators的所有属性
     - 可以增加、删除、编辑evaluator
     - 注意：evaluators中会包含多种不同类型的evaluator
     - 可以调用功能1中的模块，直接获取evaluator所需要匹配的数据元素的key值。
4. 程序架构要求可以易于拓展支持更多类型的evaluators