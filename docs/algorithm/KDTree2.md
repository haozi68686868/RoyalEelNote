kd-tree是在进行激光点云编程中经常使用的一个工具，我们平时使用的时候可能就是使用其中的一小部分的内容，并未对其进行很深的思考。那么kd-tree的原理到底是什么呢？我们又经常使用哪些常用函数呢？

本片文章将对kd-tree进行细致的整理，方便以后的使用和阅读。

## 1、简介

kd-tree简称k维树，是一种空间划分的数据结构。常被用于高维空间中的搜索，比如范围搜索和最近邻搜索。kd-tree是二进制空间划分树的一种特殊情况 ![[公式]](https://www.zhihu.com/equation?tex=%5E%7B%5B1%5D%7D) 。

在激光雷达SLAM中，一般使用的是三维点云。所以，kd-tree的维度是3。

由于三维点云的数目一般都比较大，所以，使用kd-tree来进行检索，可以减少很多的时间消耗，可以确保点云的关联点寻找和配准处于实时的状态。

本篇文章将从原理层面讲解kd-tree，以便大家在使用中，可以有着更深刻的理解。

## 2、原理

### 2.1、数据结构

kd-tree，是k维的二叉树。其中的每一个节点都是k维的数据，数据结构如下所示 ![[公式]](https://www.zhihu.com/equation?tex=%5E%7B%5B2%5D%7D) ：

```cpp
struct kdtree{
    Node-data - 数据矢量   数据集中某个数据点，是n维矢量（这里也就是k维）
    Range     - 空间矢量   该节点所代表的空间范围
    split     - 整数       垂直于分割超平面的方向轴序号
    Left      - kd树       由位于该节点分割超平面左子空间内所有数据点所构成的k-d树
    Right     - kd树       由位于该节点分割超平面右子空间内所有数据点所构成的k-d树
    parent    - kd树       父节点  
}
```

上面的数据在进行算法解析中，并不是全部都会用到。一般情况下，会用到的数据是{数据矢量，切割轴号，左支节点，右支节点}。这些数据就已经满足kd-tree的构建和检索了。

### 2.2、构建kd-tree

kd-tree的构建就是按照某种顺序将无序化的点云进行有序化排列，方便进行快捷高效的检索。

构建算法：

```cpp
Input:  无序化的点云，维度k
Output：点云对应的kd-tree
Algorithm：
1、初始化分割轴：对每个维度的数据进行方差的计算，取最大方差的维度作为分割轴，标记为r；
2、确定节点：对当前数据按分割轴维度进行检索，找到中位数数据，并将其放入到当前节点上；
3、划分双支：
    划分左支：在当前分割轴维度，所有小于中位数的值划分到左支中；
    划分右支：在当前分割轴维度，所有大于等于中位数的值划分到右支中。
4、更新分割轴：r = (r + 1) % k;
5、确定子节点：
    确定左节点：在左支的数据中进行步骤2；
    确定右节点：在右支的数据中进行步骤2；
```

这样的化，就可以构建出一颗完整的kd-tree了。

拿个例子说明为：

二维样例：{（2,3），（5,4），（9,6），（4,7），（8,1），（7,2）}

构建步骤：

1、初始化分割轴：

发现x轴的方差较大，所以，最开始的分割轴为x轴。

2、确定当前节点：

对{2，5，9，4，8，7}找中位数，发现{5,7}都可以，这里我们选择7，也就是**(7,2)**;

3、划分双支数据：

在x轴维度上，比较和7的大小，进行划分：

左支：{(2,3)，(5,4)，(4,7)}

右支：{(9,6)，(8,1)}

4、更新分割轴：

一共就两个维度，所以，下一个维度是y轴。

5、确定子节点：

左节点：在左支中找到y轴的中位数**(5,4)**，左支数据更新为{(2,3)}，右支数据更新为{(4,7)}

右节点：在右支中找到y轴的中位数**(9,6)**，左支数据更新为{(8,1)}，右支数据为null。

6、更新分割轴：

下一个维度为x轴。

7、确定(5,4)的子节点：

左节点：由于只有一个数据，所以，左节点为**(2,3)**

右节点：由于只有一个数据，所以，右节点为**(4,7)**

8、确定(9,6)的子节点：

左节点：由于只有一个数据，所以，左节点为**(8,1)**

右节点：右节点为空。

最终，就可以构建整个的kd-tree了。

示意图如下所示 ![[公式]](https://www.zhihu.com/equation?tex=%5E%7B%5B1%5D%7D) ：

二维空间表示：

![img](https://pic2.zhimg.com/80/v2-1d1889536e44341ba8c2baa899baa90d_720w.jpg)二维坐标系下的分割示意图

kd-tree表示：

![img](https://pic3.zhimg.com/80/v2-7676335c0617c02a9e012e6ecf2620fa_720w.jpg)构建kd-tree

### 2.3、最近邻检索

在构建了完整的kd-tree之后，我们想要使用他来进行高维空间的检索。所以，这里讲解一下比较常用的最近邻检索，其中范围检索也是同样的道理。

最近邻搜索，其实和之前我们曾经学习过的KNN很像。不过，在激光点云章，如果使用常规的KNN算法的话，时间复杂度会空前高涨。因此，为了减少时间消耗，在工程上，一般使用kd-tree进行最近邻检索。

由于kd-tree已经按照维度进行划分了，所以，我们在进行比较的时候，也可以通过维度进行比较，来快速定位到与其最接近的点。由于可能会进行多个最近邻点的检索，所以，算法也可能会发生变化。因此，我将从最简单的一个最近邻开始说起。

- **一个最近邻**

一个最近邻其实很简单，我们只需要定位到对应的分支上，找到最接近的点就可以了。

举个例子：查找(2.1,3.1)的最近邻。

1. 计算当前节点(7,2)的距离，为6.23，并且暂定为(7,2)，根据当前分割轴的维度（2.1 < 7），选取左支。
2. 计算当前节点(5,4)的距离，为3.03，由于3.03 < 6.23，暂定为(5,4)，根据当前分割轴维度（3.1 < 4），选取左支。
3. 计算当前节点(2,3)的距离，为0.14，由于0.14 < 3.03，暂定为(2,3)，根据当前分割轴维度（2.1 > 2），选取右支，而右支为空，回溯上一个节点。
4. 计算(2.1,3.1)与(5,4)的分割轴{y = 4}的距离，如果0.14小于距离值，说明就是最近值。如果大于距离值，说明，还有可能存在值与(2.1,3.1)最近，需要往右支检索。

由于0.14 < 0.9，我们找到了最近邻的值为(2,3)，最近距离为0.14。

- **多个最近邻**

多个近邻其实和一个最近邻类似，不过是存储区间变为了多个，判定方法还是完全一样。

由于篇幅的原因，这里就不在赘述。这篇博客讲的很详细，有兴趣的同学可以去学习一下：

[加载中www.joinquant.com](https://link.zhihu.com/?target=https%3A//www.joinquant.com/view/community/detail/c2c41c79657cebf8cd871b44ce4f5d97)

## 3、常用函数

kd-tree在日常使用中，一般会在两个方面使用：

- 最近邻搜索
- 距离范围搜索

距离范围搜索的原理和最近邻搜索的差不多，把满足距离的全部放进去就可以了。

最近邻搜索的函数在激光点云匹配中找最近点的时候用的比较多：

```cpp
//头文件
#include <pcl/kdtree/kdtree_flann.h>
//设定kd-tree的智能指针
pcl::KdTreeFLANN<pcl::PointXYZI>::Ptr kdtreeCornerLast(new pcl::KdTreeFLANN<pcl::PointXYZI>());
//输入三维点云，构建kd-tree
kdtreeCornerLast->setInputCloud(laserCloudCornerLast);
//在点云中寻找点searchPoint的k近邻的值，返回下标pointSearchInd和距离pointSearchSqDis
kdtreeCornerLast->nearestKSearch (searchPoint, K, pointIdxNKNSearch, pointNKNSquaredDistance);
```

其中，当k为1的时候，就是最近邻搜索。当k大于1的时候，就是多个最近邻搜索。

距离范围搜索：

```cpp
//在点云中寻找和点searchPoint满足radius距离的点和距离，返回下标pointIdxRadiusSearch和距离pointRadiusSquaredDistance
kdtreeCornerLast->radiusSearch (searchPoint, radius, pointIdxRadiusSearch, pointRadiusSquaredDistance)
```

其完整的使用代码可以参考PCL的官方文件 ![[公式]](https://www.zhihu.com/equation?tex=%5E%7B%5B3%5D%7D) :

```cpp
#include <pcl/point_cloud.h>
#include <pcl/kdtree/kdtree_flann.h>

#include <iostream>
#include <vector>
#include <ctime>

int
main (int argc, char** argv)
{
  srand (time (NULL));

  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);

  // Generate pointcloud data
  cloud->width = 1000;
  cloud->height = 1;
  cloud->points.resize (cloud->width * cloud->height);

  for (std::size_t i = 0; i < cloud->points.size (); ++i)
  {
    cloud->points[i].x = 1024.0f * rand () / (RAND_MAX + 1.0f);
    cloud->points[i].y = 1024.0f * rand () / (RAND_MAX + 1.0f);
    cloud->points[i].z = 1024.0f * rand () / (RAND_MAX + 1.0f);
  }

  pcl::KdTreeFLANN<pcl::PointXYZ> kdtree;

  kdtree.setInputCloud (cloud);

  pcl::PointXYZ searchPoint;

  searchPoint.x = 1024.0f * rand () / (RAND_MAX + 1.0f);
  searchPoint.y = 1024.0f * rand () / (RAND_MAX + 1.0f);
  searchPoint.z = 1024.0f * rand () / (RAND_MAX + 1.0f);

  // K nearest neighbor search

  int K = 10;

  std::vector<int> pointIdxNKNSearch(K);
  std::vector<float> pointNKNSquaredDistance(K);

  std::cout << "K nearest neighbor search at (" << searchPoint.x 
            << " " << searchPoint.y 
            << " " << searchPoint.z
            << ") with K=" << K << std::endl;

  if ( kdtree.nearestKSearch (searchPoint, K, pointIdxNKNSearch, pointNKNSquaredDistance) > 0 )
  {
    for (std::size_t i = 0; i < pointIdxNKNSearch.size (); ++i)
      std::cout << "    "  <<   cloud->points[ pointIdxNKNSearch[i] ].x 
                << " " << cloud->points[ pointIdxNKNSearch[i] ].y 
                << " " << cloud->points[ pointIdxNKNSearch[i] ].z 
                << " (squared distance: " << pointNKNSquaredDistance[i] << ")" << std::endl;
  }

  // Neighbors within radius search

  std::vector<int> pointIdxRadiusSearch;
  std::vector<float> pointRadiusSquaredDistance;

  float radius = 256.0f * rand () / (RAND_MAX + 1.0f);

  std::cout << "Neighbors within radius search at (" << searchPoint.x 
            << " " << searchPoint.y 
            << " " << searchPoint.z
            << ") with radius=" << radius << std::endl;


  if ( kdtree.radiusSearch (searchPoint, radius, pointIdxRadiusSearch, pointRadiusSquaredDistance) > 0 )
  {
    for (std::size_t i = 0; i < pointIdxRadiusSearch.size (); ++i)
      std::cout << "    "  <<   cloud->points[ pointIdxRadiusSearch[i] ].x 
                << " " << cloud->points[ pointIdxRadiusSearch[i] ].y 
                << " " << cloud->points[ pointIdxRadiusSearch[i] ].z 
                << " (squared distance: " << pointRadiusSquaredDistance[i] << ")" << std::endl;
  }


  return 0;
}
```

#### **kd 树上的 kNN 算法**

给定一个构建于一个样本集的 kd 树，下面的算法可以寻找距离某个点 *p* 最近的 *k* 个样本。

零、设 L 为一个有 *k* 个空位的列表，用于保存已搜寻到的最近点。
一、根据*p* 的坐标值和每个节点的切分向下搜索（也就是说，如果树的节点是按照 *x**r*=*a**x**r*=*a*xr=a 进行切分，并且 *p**p*p 的 *r**r*r坐标小于 *a**a*a，则向左枝         进行搜索；反之则走右枝）。
二、当达到一个底部节点时，将其标记为访问过。如果 *L**L*L 里不足 *k**k*k 个点，则将当前节点的特征坐标加入 *L**L*L ；如果 *L**L*L 不为空并且当前节点         的特征与 *p**p*p 的距离小于 *L**L*L 里最长的距离，则用当前特征替换掉 *L**L*L 中离 *p**p*p 最远的点。
三、如果当前节点不是整棵树最顶端节点，执行 (a)；反之，输出 *L**L*L，算法完成。
*a*.*a*.a. 向上爬一个节点。如果当前（向上爬之后的）节点未曾被访问过，将其标记为被访问过，然后执行 (1) 和 (2)；如果当前节点被访      问过，再次执行 (a)。
1.1.1. 如果此时 *L**L*L 里不足 *k**k*k 个点，则将节点特征加入 *L**L*L；如果 *L**L*L 中已满 *k**k*k 个点，且当前节点与 *p**p*p 的距离小于 *L**L*L 里最长的距离，      则用节点特征替换掉 *L**L*L 中离最远的点。
2.2.2. 计算 *p**p*p 和当前节点切分线的距离。如果该距离大于等于 *L**L*L 中距离 *p**p*p 最远的距离**并且** *L**L*L 中已有 *k**k*k 个点，则在切分线另一边不会有更近的点，执行       (三)；如果该距离小于 *L**L*L 中最远的距离**或者** *L**L*L 中不足 *k**k*k 个点，则切分线另一边可能有更近的点，因此在当前节点的另一个枝从 (一) 开始执行。

#### **啊呃… 被这算法噎住了，赶紧喝一口下面的例子**

设我们想查询的点为 *p*=(−1,−5)*p*=(−1,−5)p=(−1,−5)，设距离函数是普通的 *L*2*L*2L2 距离，我们想找距离问题点最近的 *k*=3*k*=3k=3 个点。如下：
![6.png](https://image.joinquant.com/880ee4b91acd0d801bd8cbecddbd5b39)

首先执行 (一)，我们按照切分找到最底部节点。首先，我们在顶部开始
![树5.png](https://image.joinquant.com/6258242090a8b86310b2dd1d465bba3f)

和这个节点的 *x**x*x 轴比较一下，
![findleaf1.png](https://image.joinquant.com/e84a7e1ba8e4a33730558c09d635a1aa)

*p**p*p 的 *x**x*x 轴更小。因此我们向左枝进行搜索：
![树7.png](https://image.joinquant.com/0d128b8d1efab58726ffdabdb858a2ae)

这次对比 *y**y*y 轴，
![findleaf2.png](https://image.joinquant.com/995d91276f4351ead1f4b644735228aa)

*p**p*p 的 *y**y*y 值更小，因此向左枝进行搜索：
![树8.png](https://image.joinquant.com/50f6eaaa6e2dcd7bf3ebe1e22139f9be)

这个节点只有一个子枝，就不需要对比了。由此找到了最底部的节点 (−4.6,−10.55)(−4.6,−10.55)(−4.6,−10.55)。
![树9.png](https://image.joinquant.com/1c69996ad65ee3284fa43ae89793e88d)

在二维图上是
![7.png](https://image.joinquant.com/1848ac29db08416ef7baed2a008eb017)

此时我们执行 (二)。将当前结点标记为访问过，并记录下 *L*=[(−4.6,−10.55)]*L*=[(−4.6,−10.55)]L=[(−4.6,−10.55)]。啊，访问过的节点就在二叉树上显示为被划掉的好了。

然后执行 (三)，嗯，不是最顶端节点。好，执行 (a)，我爬。上面的是 (−6.88,−5.4)(−6.88,−5.4)(−6.88,−5.4)。
![树10.png](https://image.joinquant.com/0002c2968f4a97ba5e68930b5d7b533d)
![8.png](https://image.joinquant.com/f1a504b1f679bd9748bf4018ea1c71d9)

执行 (1)，因为我们记录下的点只有一个，小于 *k*=3*k*=3k=3，所以也将当前节点记录下，有 *L*=[(−4.6,−10.55),(−6.88,−5.4)]*L*=[(−4.6,−10.55),(−6.88,−5.4)]L=[(−4.6,−10.55),(−6.88,−5.4)]。再执行 (2)，因为当前节点的左枝是空的，所以直接跳过，回到步骤 (三)。(三) 看了一眼，好，不是顶部，交给你了，(a)。于是乎 (a) 又往上爬了一节。
![树11.png](https://image.joinquant.com/2bbf3758124830de7e11e4456900a951)
![9.png](https://image.joinquant.com/f39d547deeafbdc29c58bfdd65da6ea3)

(1) 说，由于还是不够三个点，于是将当前点也记录下，有 *L*=[(−4.6,−10.55),(−6.88,−5.4),(1.24,−2.86)]*L*=[(−4.6,−10.55),(−6.88,−5.4),(1.24,−2.86)]L=[(−4.6,−10.55),(−6.88,−5.4),(1.24,−2.86)]。当然，当前结点变为被访问过的。

(2) 又发现，当前节点有其他的分枝，并且经计算得出 *p**p*p 点和 *L**L*L 中的三个点的距离分别是 6.62,5.89,3.106.62,5.89,3.106.62,5.89,3.10，但是 *p**p*p 和当前节点的分割线的距离只有 2.142.142.14，小于与 *L**L*L 的最大距离：
![10.png](https://image.joinquant.com/2a755c9cca7b2697d49b267166f14553)

因此，在分割线的另一端可能有更近的点。于是我们在当前结点的另一个分枝从头执行 (一)。好，我们在红线这里：
![树12.png](https://image.joinquant.com/b8d5fb100d4608b79a41201c2f73410e)

要用 *p**p*p 和这个节点比较 *x**x*x 坐标:
![findleaf3.png](https://image.joinquant.com/dc00ae0dcb5212d814b8c7910bb277e4)

*p**p*p 的 *x**x*x 坐标更大，因此探索右枝 (1.75,12.26)(1.75,12.26)(1.75,12.26)，并且发现右枝已经是最底部节点，因此启动 (二)。
![树13.png](https://image.joinquant.com/357e68430d1a80927ab96cd284860196)

经计算，(1.75,12.26)(1.75,12.26)(1.75,12.26) 与 *p**p*p 的距离是 17.4817.4817.48，要大于 *p**p*p 与 *L**L*L 的距离，因此我们不将其放入记录中。
![11.png](https://image.joinquant.com/ca6cc29e28640d76c60d384e204bda0e)

然后 (三) 判断出不是顶端节点，呼出 (a)，爬。
![树14.png](https://image.joinquant.com/b990e692fd701da85f24f7e5a3638708)

(1) 出来一算，这个节点与 *p**p*p 的距离是 4.914.914.91，要小于 *p**p*p 与 *L**L*L 的最大距离 6.626.626.62。
![12.png](https://image.joinquant.com/ab27a1147c11c3fda33be82d84562ea8)

因此，我们用这个新的节点替代 *L**L*L 中离 *p**p*p 最远的 (−4.6,−10.55)(−4.6,−10.55)(−4.6,−10.55)。
![13.png](https://image.joinquant.com/3b637a26fb0af76b0ce2f027a1b4606e)

然后 (2) 又来了，我们比对 *p**p*p 和当前节点的分割线的距离
![14.png](https://image.joinquant.com/3b03de2b0c240c69a55c5ff1f3bd2277)

这个距离小于 *L**L*L 与 *p**p*p 的最小距离，因此我们要到当前节点的另一个枝执行 (一)。当然，那个枝只有一个点，直接到 (二)。
![树15.png](https://image.joinquant.com/c3aa4fe8215cbf59d9518955056b88ff)

计算距离发现这个点离 *p**p*p 比 *L**L*L 更远，因此不进行替代。
![15.png](https://image.joinquant.com/3e88b7d5ae4bbc0fca2d32ad28f103ce)

(三) 发现不是顶点，所以呼出 (a)。我们向上爬，
![图16.png](https://image.joinquant.com/2715846daf0cf26655b391e8d1dc569a)

这个是已经访问过的了，所以再来（a），
![图17.png](https://image.joinquant.com/cc51536c66b8f7492df3782c24aff8f2)

好，（a）再爬，
![图18.png](https://image.joinquant.com/ecc53901c03d25bedf5febe9e496b7ca)

啊！到顶点了。所以完了吗？当然不，还没轮到 (三) 呢。现在是 (1) 的回合。

我们进行计算比对发现顶端节点与p的距离比L还要更远，因此不进行更新。
![16.png](https://image.joinquant.com/24a59cf9391c80cd818ed9942b63fb44)

然后是 (2)，计算 *p**p*p 和分割线的距离发现也是更远。
![17.png](https://image.joinquant.com/5b8ea4b5aba82d4a6c17f74b6b8f0d6b)

因此也不需要检查另一个分枝。

然后执行 (三)，判断当前节点是顶点，因此计算完成！输出距离 *p**p*p 最近的三个样本是 *L*=[(−6.88,−5.4),(1.24,−2.86),(−2.96,−2.5)]*L*=[(−6.88,−5.4),(1.24,−2.86),(−2.96,−2.5)]L=[(−6.88,−5.4),(1.24,−2.86),(−2.96,−2.5)]。