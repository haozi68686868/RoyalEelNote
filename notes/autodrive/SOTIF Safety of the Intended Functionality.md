# SOTIF Safety of the Intended Functionality

试图结合自己最近在工作上的所见所闻所感，避开深层次的技术细节不谈，围绕SOTIF的概念和方法论解释以下三个关键问题。如果理解有更新，会持续纠正完善这个答案。因系个人浅见，如有错误之处烦请指正。

1. 为什么要SOTIF?
2. SOTIF的方法论
3. SOTIF面临的挑战

/******************** 分割线 ******************** /

## 1. 为什么要SOTIF?

我想先从今年刚发生的一起沃尔沃召回事件来引入对这个问题的回答。

2020年3月19日，由于自动紧急制动系统（Autonomous Emergency Braking, AEB）存在故障，沃尔沃汽车宣布在全球范围内召回汽车近74万辆，共涉及9款在售车型。

涉及召回的车型均出自沃尔沃与吉利斥巨资联合打造的CMA平台。CMA平台开发由位于瑞典的吉利欧洲研发中心CEVT主导。CEVT有很多来自沃尔沃的资深专家，开发流程和开发工具都沿袭沃尔沃，属于业内领先水平。同时，CEVT也继承了沃尔沃始终把汽车安全放在首位的开发文化，功能安全是自然也是满足的。

那么，既然满足功能安全要求，那么电子电器系统的开发是完全可靠的，为什么还会出现这么大规模的因为电子电器系统问题而导致的召回事件呢？

分析这次召回的原因，是因为一些场景下无法有效识别物体，导致AEB在该工作的时候不工作。而一般AEB探测物体依赖传感器毫米波雷达和摄像头两个关键传感器的信息融合。因为多普勒效应，毫米波雷达不擅长识别静态物体；而摄像头在雾天或者光线不足等情况下探测度都会降低，这些因素都会导致在一些场景下无法正确识别物体从而激活AEB。

因此，这次召回不是因为传感器故障导致的，而是传感器本身的功能局限导致的。

我们知道，ISO 26262功能安全旨在避免电子电气系统故障导致功能异常而引起的不合理的危害。而如果传感器不是故障仅仅是功能受限，不属于ISO 26262的范畴。可以想象，参与这个项目的功能安全设计的工程师们在提心吊胆地了解情况后长舒了一口气：这个锅功能安全可以不背。

此次召回事件说明 ：即使系统没有发生故障，仍然会因为当前技术的局限性而导致不能被接受的危害。

同时这次召回事件也暴露出，ISO 26262是有局限性的。而且如果这个局限不能得到弥补，别说无人驾驶，就是辅助驾驶功能都无法很好地落地。于是，为弥补这种局限，预期功能安全SOTIF (Safety of the Intended Functionality)诞生了。

## 2. SOTIF的方法论

简单来说，SOTIF强调的是避免因为预期的功能表现局限而导致不合理的风险。

因为SOTIF诞生的背景是智能驾驶的发展，所以如果按照智能驾驶的功能链：感知——决策——执行来归类，“功能表现局限”体现在3个方面：

- 传感器感知局限导致场景识别错误（包括对驾驶员误操作的漏识别）
- 深度学习不够导致决策算法判断场景错误（包括对驾驶员误操作的误响应）
- 执行器功能局限导致与理想目标偏差

而从另一个维度，“功能表现”可以概括为4类：

1. 在危险场景介入    （正常工作）
2. 在非危险场景介入 （误触发）
3. 在危险场景不介入 （漏触发）
4. 在非危险场景不介入（正常关闭）

可以预见，第1/4种情况没有风险，第2/3种情况有风险，因此这误触发和漏触发是SOTIF需要考虑的范畴。

要有效避免误触发和漏触发，第一步是识别场景并进行分类，确定哪些场景下功能触发安全，哪些场景下功能不触发安全。

在SOTIF的方法论中，将所有的场景划分成以下四个部分：

![img](https://pic1.zhimg.com/50/v2-e0b2442998221a0f68afe31d00b8c6e5_hd.jpg?source=1940ef5c)![img](https://pic1.zhimg.com/80/v2-e0b2442998221a0f68afe31d00b8c6e5_720w.jpg?source=1940ef5c)

且SOTIF的目标为：最大可能减小Area2(known unsafe scenarios)和Area3(unknown unsafe scenarios)。

![img](https://pic2.zhimg.com/50/v2-7c1c8de9364a13606349e43925e1f796_hd.jpg?source=1940ef5c)![img](https://pic2.zhimg.com/80/v2-7c1c8de9364a13606349e43925e1f796_720w.jpg?source=1940ef5c)

对于Area2(known unsafe scenarios)，SOTIF的基本思想是：通过安全分析识别出风险场景，针对风险场景开发应对的策略，再对已知场景搭建实时仿真环境或者设计实车测试，根据实验结果来优化设计。这个和传统的V模型开发理念一致，比较好理解。

其中，ISO 26262中推荐的安全分析方法（FMEA/FTA）仍然可以用到SOTIF帮助识别风险。只是需要注意的是，此时FTA也仅用来做定性分析，而非定量分析。

而对于Area3(unknown unsafe scenarios)，处理起来则相对棘手很多。举个例子，这就好比我们在开发一辆将来投放在中国市场的车，需要在开发初期事先识别出一辆车在中国路况下可能会碰到的各种场景。我想即使让全世界顶尖的安全专家坐一起搜肠刮肚，产出也很难令人满意。

为了让朋友们更直观地感受这个问题有多难，请看下面让马斯克看了会流泪的例子：特斯拉智能驾驶功能错把具有中国特色的幸运红绸识别成了路障。

![img](https://pic1.zhimg.com/50/v2-9d68cb7552efa61f192aab48b4836e86_hd.jpg?source=1940ef5c)![img](https://pic1.zhimg.com/80/v2-9d68cb7552efa61f192aab48b4836e86_720w.jpg?source=1940ef5c)

而SOTIF对降低Area3，相比Area3暂时没有细节的方法，宽泛地提到两点：

（1）提高系统和零部件功能的可信度。

> Validation: set of activities ensuring and gaining confidence that a system is able to accomplish its intended use, goals, and objectives
> Note to entry: ......Validation activities address mainly "area 3" of figure 7 including the validation of SOTIF in unknown use cases."

（2）endurance run。概括来说就是通过实车路试和仿真测试积累大数据。当数据积累越多，越能够将unknown scenarios变成known scenarios。

## 3. SOTIF面临的挑战

（1）SOTIF在完全无人驾驶开发中如何应用？

对于辅助驾驶功能，驾驶员在loop里，功能对有把握的场景系统做出合理辅助，没有把握的场景交给驾驶员接管兜底。那么理论上只要我们的测试数据足够多，对有把握的场景判断足够准确，加上驾驶员的反馈把握设计方向，最终总能可以较清晰得界定一条balance line，使得功能设计可以在“不触发”和“触发”中找到平衡点。

但是如果是无人驾驶，驾驶员不在loop，所有的场景都需要系统自己来做判断，这对系统要求就非常高。对于某个特定的场景功能触发更合理？还是不触发更合理？谁来评判？怎么保证评判结果市场能接受？

这是SOTIF面对无人驾驶需要回答的问题。

（2）SOTIF如何进行定量分析？

ISO 26262中推荐使用FTA对随机硬件失效进行定量分析，用数据说话，有理有据；但是从上面的介绍可以看到，SOTIF所有的安全分析仅停留在定性分析，那么不可避免会有主观判定的差异导致分析结果偏差。这样一来，没有数据支撑，OEM没有底气对供应商提要求，供应商没有底气反驳OEM，那么工程师们就要浪费时间扯皮了。

所以，SOTIF要想更好地落地，定义定量分析方法必不可少。