# C++ 数据类型

### map,unordered_map

```c++
iterator find (const key_type& k); // 未找到时，iterator返回map::end即map.end()
const_iterator find (const key_type& k) const;
//example
it = map.find('b');
if (it != map.end())
    mymap.erase (it);
```

#### std::make_pair , std::pair 值对

```c++
#include <utility> //需包含的头文件

	Map<int, string> mapStudent;
	mapStudent.insert(std::pair<int, string>(1, “student_one”));//pair插入
    mapStudent.insert(std::make_pair(1, “student_one”));//make_pair无需指定类型
    mapStudent.insert(map<int, string>::value_type (2, “student_two”));//value_type
    mapStudent[3] =  “student_three”;//数组方式插入
    
```

#### std::make_shared , std::move

```c++
//循环1000次，时间为0.3ms -- 时间都差不多，可能是对象还不够大，改天找较大的对象再试一下
std::vector<std::shared_ptr<const Eigen::Vector4d>> vectors;
vectors.emplace_back(std::make_shared<Eigen::Vector4d>(v));
vectors.emplace_back(std::make_shared<Eigen::Vector4d>(std::move(v)));
```

#### c++智能指针

可以使用智能指针的场景（个人经验）

1. 全程使用智能指针管理
2. 局部变量，然后后make_shared
3. 三种用途
   - shared_ptr
   - unique_ptr
   - weak_ptr
     - 解决循环引用计数问题
     - 使用时需使用weak_ptr.lock()来获得shared_ptr，保证在这个shared_ptr存活时，对象不被释放（这个类似于Java引用的Get)

##### 初始化方式

```C++
// 构造函数初始化
std::shared_ptr<int> pointer(new int(1));
std::shared_ptr<int> pointer1 = pointer;
std::shared_ptr<std::string> ss(new std::string("AAA"));
std::shared_ptr<std::string> = std::shared_ptr<std::string>(new std::string("AAA"));

// std::make_shard初始化(推荐)
std::shared_ptr<string> p3 = std::make_shared<string>();
std::shared_ptr<string> p2 = std::make_shared<string>("hello");
//auto关键字代替std::shared_ptr，p5指向一个动态分配的空vector<string>
auto p5 = make_shared<vector<string>>();

// reset 初始化
std::shared_ptr<int> pointer = nullptr;
pointer.reset(new int(1));
```

##### 类型转换

```c++
template <class T, class U>
  shared_ptr<T> static_pointer_cast (const shared_ptr<U>& sp) noexcept;
  // struct A {} ;
  // struct B : A {};
  foo = std::make_shared<A>();
  // cast of potentially incomplete object, but ok as a static cast:
  bar = std::static_pointer_cast<B>(foo);

  std::cout << "foo's static  type: " << foo->static_type << '\n'; // A
  std::cout << "foo's dynamic type: " << foo->dynamic_type << '\n'; // A
  std::cout << "bar's static  type: " << bar->static_type << '\n'; // B
  std::cout << "bar's dynamic type: " << bar->dynamic_type << '\n'; // A
```

- unique_ptr作为参数时，应该使用值传递还是右值引用(&&)？
  - 应当使用值传递，可以确保原对象已经交出了控制权。
  - 若传递右值引用，那么调用方则不确定是否还能使用原有的指针

#### C++常用容器

deque：双向队列

queue：单向队列（内部实现其实是deque）

priority_queue：优先队列（在头文件queue中）

map/unordered_map：字典

set/unordered_set：集合

stack：栈

vector/array: Array静态，vector动态

list: 双向链表

forward_list: 单向链表

#### priority_queue 优先队列

pop() 弹出

top() 查看最前面的值

push()/emplace() 插入元素

默认是优先输出最大的值

```c++
std::priority_queue<int> a;
// 等同于 std::priority_queue<int,vector<int>,less<int> > a;

// 小元素优先
std::priority_queue<int,vector<int>,greater<int> > a;

// 定义
template <class T, class Container = vector<T>,
  class Compare = less<typename Container::value_type> > class priority_queue;

// 构造方式
std::priority_queue<int> first;
  std::priority_queue<int> second (myints,myints+4);
  std::priority_queue<int, std::vector<int>, std::greater<int> >
                            third (myints,myints+4);
  

// using mycomparison:
class mycomparison
{
  bool reverse;
public:
  mycomparison(const bool& revparam=false)
    {reverse=revparam;}
  bool operator() (const int& lhs, const int&rhs) const
  {
    if (reverse) return (lhs>rhs);
    else return (lhs<rhs);
  }
};

typedef std::priority_queue<int,std::vector<int>,mycomparison> mypq_type;
```

