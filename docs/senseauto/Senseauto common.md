## Senseauto common

ros消息的订阅和发布

1. 在NodeWrapper基类中的init方法，会调用topicManager初始化，读取yaml文件，从文件配置subscribe和publish的topic
2. 手动代码订阅



##### ros 结点有一个状态机

spin过后会在状态机之间跳转

1. onFailed
2. onInit
3. onReady
4. onRunning
5. onExit
6. onReset

[TODO] Init -> onRunning ->