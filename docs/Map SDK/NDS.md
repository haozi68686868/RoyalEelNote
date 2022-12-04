

#### NavigationData Standard

- 分离导航软件和地图数据
- 基于SQLite
- Product Database
  - 一个NDS数据库由多个产品组成
- Update Region
- Building Blocks：每个block能提供NDS的一个具体功能
  - 路径规划（Routing）
  - 命名
  - overview
  - 地图显示
  - POI
  - 语音
- Level：
  - 大尺度数据存在High Level：用于路径规划
  - 细节数据存在Low Level
  - 每个Level划分为tiles，（网格划分 Tiling Scheme）
- Content
  - Feature：现实世界的物体
  - attribute：属性
  - metadata：元数据

------

nds 数据结构

1. nds按功能将数据划分成building block，其中routing building block和name building block是强制的，其他的都是可选的

2. nds数据的分层和划分：

WGS84 和 EGM96

nds使用的是WGS84坐标系统（the World Geodetic System dating from 1984），就是平常我们说的经纬度。当我们说一个具体的位置的时候，就说这个问题位置的经度是多少，纬度是多少，这样就可以唯一的定位到一个精确的点。

nds使用EGM96（the Earth Gravitational Model from 1996）来表示高度信息。EGM96描述的高度信息很好的近似海拔高度，它比WGS84中的高度信息更准确。

Coding of Coordinate（坐标编码）

为了对坐标进行编码，我们把360°的范围完全映射到32位的int表示范围。对于经度（X坐标）从-180°到+180°，完全覆盖32位的int数，也就是覆盖了-2^31 到+2^31。对于纬度（Y坐标）-90°到+90°，覆盖了-2^30 到+2^30，只是用到了31位，比经度而已，最高一位不使用。这里需要注意的，y坐标只用到了31位，为了保证正负号的意义，在用32位int表示纬度的时候，我们总是保证y31和y30的值是一样的（其实int本身就可以保证正负号一致性，只是特别提醒下大家）。

对x坐标，我们用有符号的32bit的int表示： x = x31 x30…x1 x0

对于y坐标，我们用有符号的31bit的int表示：y = y30…y1 y0

下面这个表，表示了一个坐标点在 wgs84，NDS的十进制表示，NDS的16进制表示。

NOTE:

* 由于精度的原因，在计算机里，浮点运算的结果与整数运算的结果是不一样的。不过，在NDS中，int型表示的坐标比地图供应商提供的浮点坐标的表示精确度高的多，所有在NDS使用整型编码坐标，运算过程中不会有精度缺失的问题。（供应商提供的浮点坐标，一般是小数点后6位，精确度大概是0.1米这个样子，而NDS的精度大概是0.009米）

* 在把floating的坐标转换成int的坐标时，我们采用floor操作，而不是truncate，或者round。之所以必须用floor，这要关联到tile的划分规则，因为坐标向下取整，不改变坐标点所在的tile，同时也不会改变上下层tile间的父子关系。

floor：向下取整，就是取一个比自己小中最大的整数。其实就是在坐标轴上向左取。

round：就是四舍五入。

truncate：对于正数，和floor一样，对于负数，就是取一个比自己大中最小的整数。其实就是在坐标轴上向0方向取。

* 纬度范围为180°，只用到31bit就可以满足纬度的范围，但是在实际的使用过程中，我们还是用32bit来存储纬度，读取的时候把最高位掩盖掉。比如：值-272788154，如果用31bit来表示，其值为0x6fae5306，用32bit来表示就是0xefae5306，其实就是最高2bit的值必须相同。

Morton Codes

一个经纬度坐标是个2维值，包括经度（X）和纬度（Y）。morton code是个表示1维的值。所以，我们需要把个2维的值映射到个1维的值。方法如下，

x = x31 x30…x1 x0 和 y = y30…y1 y0

Morton code c 为一个63bit的int值

c = x31y30 x30…y1 x1 y0 x0

就是由x和y的各个bit位交错组合而成，c的值范围为0 ≤ c < 2^63。如果我们用一个64bit的int来存，我们使最高bit总是为0，这样这个int总是为一个正数。

如果记录是按照他们的morton code来排序，我们就说，这是Morton order。

上面那个表格的坐标对应的morton code为：

在NDS，有多个应用就是按morton order排序的，比如 poi building block， tile也是按morton order来排序。

Tiling Scheme（网格划分）

我们知道，每个feature都有自己的唯一的坐标点，我们可以通过地理位置来查找feature，定位feature和分组feature。这要求我们必须支持高性能的数据管理，比如。。。。

NDS使用tiling scheme来完成这个功能。就是把整个地球表面按网格切分成一个一个格子，这个格子我们称为tile（tile本意就是瓷砖的意思）。每个tile近似为一个正方形的区域（实际上，每个tile的4条边长度都不一样，因为tile是按经纬度大小一样宽来切割的，但是纬度越高，相同经度表示的距离就越短）。

NDS中，database是以tile为单位来进行存储的。也就是说，一个tile包含了在这个tile边界的地理范围的内的所有feature，这些feature将按datascript所定义的格式进行编码，存储为database的一个BLOBs。

Tiles具有很多优点：

* 应用程序通过一次访问数据库，就可以把在同一个地理范围内的所有相关数据都加载进来。这能够提高地图显示和路径规划的性能。

* tiles可以作为数据更新的单位。我们只需要对每一个tile记录一个版本信息，而不是每个独立的feature记录版本信息。这也可以节省大量的数据空间。

* tiles可以实现了对feature的分层引用。比如如果我们要引用到多个feature，这些feature属于同一个tile，这时候，这些feature的tileId只需要指定一次就可以。

Tiles and Building Blocks

导航数据在存储的时候，按照存储方式不同，分为BLOBs（二进制流存储）和relational（关系表存储）。

tiling scheme应用于BLOBs的存储方式，比如basic map display building block，routing building block等等，都是按照tiles的方式来分隔数据，按tiles划分数据后，就可以通过一个点快速查找这个点周边的数据。

而关系表存储的数据是没有tile的概念，比如POI building block。不过，我们也是需要支持周边查询POI的功能，这时候通过virtual tiles来支持那些特殊的查询功能。

1） Tile and Levels

tiling scheme同时定义了level的概念，在一个level上对应的所有的tile刚好覆盖了整个地球表面。在同一个level的每个tile的边界宽度都是固定的经纬度宽，所以同一level的tile在wgs84的坐标系统中大小是一致的。

*tile的边界长和宽，在wgs84的坐标系统中是相同的，但是如果转换成米为单位的坐标系统，他们的长宽就是不同的，纬度越高，相同经度所表示的距离（以米为单位）就越短。

最高level只包含2个tiles，到下一级level的时候，每个当前level的tile分割成下一级level的4个大小一样的tiles。这个过程反复进行，知道最低级level。上下级tiles就组成了类似于父子包含关系。

最高level被定义为level 0，最低level定义为level 15。一共16级，其中有些level是强制需要的，有些level是可选择是否生成这个level的数据。NDS使用level 13来定义最详细的路网数据，也就是说在routing data里面没有比level 13更低的level数据。对于那些低于level 13的level是留给 map display使用了。比如，我们可以存储详细的city map在levle 14中。

下图显示了level 0的tile情况，只有2个tile，这个tile的tile number 分别是tile 0和tile 1。在这个level中，一个坐标点属于哪个tile，由经度坐标的最高bit位来决定，即经度范围为（0° ≤ x < 180°）的属于tile 0，经度范围为（–180° ≤ x < 0°）的属于tile 1。上面我们定义了坐标的morton code,morton code很容易确定一个坐标属于哪个tile number。即，在level 0中，坐标点的morton code的最高bit位决定了这个坐标点的tile number（morton code共有63bit，别搞错成64bit），最高bit为0，就属于tile 0，最高bit为1就属于tile 1.

下图显示了level 1的tile划分情况。同样的按照morton code规则，这层level的tile number由morton code最高3bit来定义。下图中显示了tile number的二进制表示法，其中最高1位用破折号分开，从中可以看出，这个最高位就是当前tile所从属的上一级level的tile number。即当前tile number总是以上一级level的tile number为前缀的。

下图显示了level 2的情况，还是根据morton code来定义tile number。规则简单，实用，真是划分tile居家便利之良策。图上我们也画出morton order（也就tile number从小到大的排序）。

level k所包含的tile数为2^(2k+1),其每个tile的边长为2^(31-k)。level k所在的tile的tile number由坐标点的morton code的最高2^(k+1)位来标示（morton code是64bit）。

tile还有个概念就是anchor point，我们知道，就是tile内部的坐标点在存储的时候，为了压缩空间，我们并不是把完整的x，y值存起来，而是存储一个相对某个坐标的offset。这个相对坐标就是anchor point。一般而言，anchor point有2种取法，一种是取最左下角的点，这样好处是所有的offset都是正数，还有一种是取中心点，好处是offset是对称的，（中心点坐标anchor point还有个好处是可用应用Tolerance Range来划分网格来减少link被打断的概率，不过NDS的link总是不被打断，也就没这个好处） 。

NDS使用中心点作为其tile的anchor point。tile中的点坐标在存储的时候，只是存储相对于anchor point的offset。在存储link的shapepoint时候，第一个点为相对anchor point的offset，其后的点就是相对前一个点的offset。

tile在NDS中都有一个标示自己的tile ID，tile id由level number和tile number这2部分组成的一个32bit的整数。生成的规则由下图说明。

2） Tile and Clipping

一个feature可以完全属于一个tile，或者横跨多个tile，其的位置将按照明确的规则来归属到某个tile或者多个tile。

feature完全包含在一个tile中：这种情况简单，feature将划归到其所在的tile。这里需要说明的是一个点在tile边界上，其归属到那个tile。

上图是一个tile的边界，对于4个顶点，只有左下角的点（那个黑点）属于当前的tile，对于4条边，只有左边和下边属于当前的tile。其他都不属于当前的tile。（这种定义规则，加上坐标点在取整的时候采用截尾法，这样在处理坐标点时候，一个坐标点在不同level所属于的tile将会保持父子一致关系。）

feature横跨多个tile：这时候我们需要把一个完整的feature在tile的边界上切分多个子feature。每个子feature划归到对应的tile。

feature的geometry横跨多个tile，我们会在tile的边界上进行clip（切分），每个切分出来的部分都归属到对应的tile。（route link虽然也是横跨多个tile，但是route link不会被切分，route link从属于其start node所在的tile。route link是一个逻辑feature，本身没有geometry信息，其geometry信息被提取出来单独做成另一个feature：geo line，所以route link对应的geo line将会被切分。具体细节以后讨论。）

一个feature横跨相邻的tiles，我们会在边界上把feature切分成2个新的feature，在边界上的点坐标，或者线条将会重复存储（2个新的feature都会存储自己对应的geometry信息，这样边界上的geometry就会重复存储），这2个新的fearture就是完全包含在一个tile中了，其很容易确定归属到那个tile。

feature被切分后，原来feature所对应的关联信息（比如name object）会都保留到切分后的feature上。

