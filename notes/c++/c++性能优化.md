### 性能优化笔记

```c++
工厂类型
enum class shape_type{
    circle;
    triangle;
};
shape* create_shape(shape_type type) {
  switch (type) {
	case shape_type::circle:
	  return new circle(...);
  }
}

使用unique_ptr
unique_ptr<shape> create_shape(shape_type type) {
  switch (type) {
	case shape_type::circle:
	  return make_unique<circle>(...);
  }
}

vector<unique_ptr<shape>>;
auto ptr = create_shape(...);
container.push_back(move(ptr));
```

 ```c++
RAII 帮助类
class shape_wrapper {
public:
    explicit shape_wrapper(shape* ptr=nullptr): ptr_(ptr) {}
    ~shape_wrapper() {
        delete ptr_;
    }
    shape* get() const {return ptr_;}
private:
    shape* ptr_;
};
 ```

使用

```c++
void foo() {
	shape_wrapper ptr_wrapper(create_shape(...))
}
```

存在问题：一旦进行拷贝构造，就有可能出现重复释放



使用RAII：

`std::mutex mtx;`

`std::lock_guard<std::mutex> guard{mtx}`



#### 进行性能测试时，如何防止编译器优化：

1. 全局变量（只保证在下一个同步点到来之前写入内存，所以需要使用同步原语）
2. 使用同步原语：互斥锁、内存屏障、原子操作（防止重排序）
3. 谨慎使用volatile（禁止编译器优化，但可能会有负面影响，导致没达到想要的效果，一般只用于测试和内存映射到文件）
4. 可以使用`__attribute__((noinline))`来防止意外内联（可能两种算法，一种被编译器inline了，另一种不会被inline，需要让它们一致）



#### 编译器重排序

1. 顺序较严格的x86处理器一般只会把较晚的LOAD指令移到较早的STORE之前
2. 对同一个内存地址的修改，不同的CPU会看到相同的修改顺序
3. 对不同的内存地址的修改，不同的CPU可能看到不同的修改顺序
4. volatile声明对处理器的乱序执行没有影响
5. 同步指令包括LOCK前缀、MFENCE指令



#### 时钟函数

```c++
最好的：rdtsc
其次的：
std::chrono::system_clock
std::chrono::high_resolution_clock

使用：
    
#include<chrono>
uint64_t get_time() {
	auto now = std::chrono::high_resolution_clock::now();
	return std::chrono::duration_cast<std::chrono::nanoseconds>(now.time_since_epoch()).count();
}

#include <x86intrin.h>   
uint64_t rdtsc() {
    return __rdtsc();
}
```



### 测试工具

##### gperftools（推荐，友好）

安装

sudo apt install google-pperftools

使用

LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libprofiler.so.0 CPUPROFILE=test.prof ./可执行文件名

google-pprof --svg 可执行文件名 test.prof > gprof.svg

#### perf

sudo perf record -F 1000 --call-graph dwarf ./可执行程序

perf report -n

#### 火焰图

安装

git clone https://github.com/brendangregg/FlameGraph.git

使用

perf script | /path/to/FlameGraph/stackcollapse-perf.pl > out.perf

/path/to/FlameGraph/stackcollapse-perf.pl out.perf > perf.svg

 



### C++基本构建

#### 虚函数

虚函数多一重间接，相当于通过函数指针调用函数

虚函数通常会防止内联，这是主要的性能问题



#### 函数对象

* 行为像函数的对象
  * 函数
  * 函数指针
  * 有成员operator() (...)的类对象（狭义函数对象）
* 类函数对象具有强类型，类型决定行为
  * 函数（指针）的类型只包含了参数类型和返回值类型，不包含函数本身
  * 因此需要类似`map<int, string, bool(*)(int, int) mp2(less_func);`比较麻烦

例：

```c++
template<class T>
struct less {
	bool operator(const T& x, const T& y) const {
		return x < y;
	}
};
const T& x： 为了可以接受常数or右值
后面的const一般都需要加上，不然传入不可修改对象的时候容易出现奇怪的报错，存在潜在风险
```



#### lambda表达式

```c++
auto add_2 = [](int x) {
	return x + 2;
}
auto adder = [](int n) {
	return [n](int x) {
		return x + n;
	}
}
```

* 一般不用说明返回值，可以用后置 -> 指定返回类型

* 全局唯一类型

* 中括号内放置需要捕获的数据

使用示例：

`sort(v.begin(), v.end(), [](int x, int y) {return x < y;});`



#### std::function

* 不同类型的函数对象可以抹去差异，原型相同就可以放在function对象中
* function对象创建和销毁可能使用堆上内存，不要频繁创建销毁
* 可以用来放置lambda函数，抹去lambda函数的全局唯一类型，管理起来



#### 移动和noexcept

下列成员函数一般不允许抛异常

* 析构函数
* 移动构造函数（如果自己实现，最好手动写上noexcpet）
* 移动赋值运算符
* 交换函数swap



#### 通透比较器

```c++
c++14的时候
template<class T = void>
struct less {
	bool operator(const T& x, const T& y) const {
		return x < y;
	}
};
比前面的函数对象多了个默认T=void
    
在模板的显式特化里面放了一个成员函数模板
只要T和U的类型支持小于比较即可
template <>
struct less<void> {
    template <class T, class U>
    auto operator(T&& x, U&& y) const {
        return std::forward<T>(x) < std::forward<U>(y);
    }
    typedef void is_transparent; # 明确给容器看的，告诉容器支持通透比较
};
```

使用场景

`std::map<std::string, valueType, std::less<>> mp;` 第三项就是通透比较器

##### 使用场景1

mp.find("one");

mp.find("one"sv);

如果无法通透比较，此时需要临时构造出一个string进行比较，影响性能

##### 使用场景2

```c++
template <typename IdType>
struct id_compare {
	template<typename T, typename U>
	bool operator()(const T&lhs, const U& rhs) const { return lhs.id < rhs.id; }
	template<typename T, typename U>
	bool operator()(const T&lhs, IdType rhs_id) const { return lhs.id < rhs_id; }
	template<typename T, typename U>
	bool operator()(IdType lhs_id, const T& rhs) const { return lhs_id < rhs.id; }
	typedef void is_transparent;
};
struct Obj {
	int id;
};
set<Obj, id_compare<int>> s{...};
```



#### 泛型lambda表达式

```c++
auto less_obj = [] (auto&& x, auto&& y)
{
	return forward<decltype(x)>(x) < forward<decltype(y)>(y);
}
使用：
less_obj(1,5)
```

函数模板

* sort

`sort(v.begin(), v.end(), less<int>());`

* partition 分区

`auto it = partition(v.begin(), v.end(), [](int x) { return x % 2 == 0 })`

把符合条件的移到前面，不符合的移动到后面，返回的迭代器指向后面不满足条件的第一个位置

* copy_if

`vector v{2,3,4,5,6,7,8,9};`

`vector<int> r;`

`copy_if(v.begin(), v.end(), back_inserter(r), [](int x) { return x % 2 = 0 })`

会把符合条件的放到新的地方去

* remove_if

`vector v{2,3,4,5,6,7,8,9};`

`auto it = remove_if(v.begin(), v.end(), [](int x) { return x % 2 = 0 });`

修改容器里面的元素，迭代器it后面的没有变，it前面的是需要的，通常需要跟`erase(it, v.end())`一起使用



#### 视图类型

##### string_view

能修改视图自身，支持string的常见操作

std::function的性能优化版本

```c++
static map<string_view, int(*)(int, int), less<>> oper_dict {
	{"+"sv, +[](int x, int y) {return x + y;}},
	{"-"sv, +[](int x, int y) {return x - y;}},
	{"*"sv, +[](int x, int y) {return x * y;}},
	{"/"sv, +[](int x, int y) {return x / y;}},
}
```

1. 第一个参数用string_view
2. 第二个参数用函数指针取代`std::function`，占用空间更少，较大概率性能会更好
3. 第三个参数用通透比较符
4. lambda表达式前面使用“+”的原因：列表初始化需要类型统一，而lambda表达式是完全不同类型的对象，为了自动推导可以成立，可以用加号，把不同的lambda表达式转换为有效表达式（函数指针）



##### span （C++20 或 c++14以上的GSL）

返回子span

可以通过数组或者连续内存范围来生成

不可修改视图本身，可修改指向的数据，除非用 `span<const T>`

```c++
#include <span>
 
void analyse_sequence(span<int> sp);
int a[] = {1,2,3,4,5}; //vector<int> 和 array<int, N>也可以
analyse_sequence(a);
```

一个失败的span使用案例

```c++
span<Data> sp;
if (...) {
	vector<Data> v = ...;
	sp = v;
}
DoSomething(sp);
```

问题在于sp指向的底层数据v，在花括号结束后就消失了，导致span悬挂

这种内存问题，可以用-fsanitize=address编译，或者用valgrind检查

 

##### ranges::view (c++20)

* 抽象的视图概念，要求对象支持遍历，可在常数时间拷贝、移动和赋值
* 使用者需要保证在view存续期间其指向的数据一直存在
* string_view和span豆瓣组view
* ranges库里提供了很多其他的view

```c++
int a[] = {1,7,3,6,5,2,4,8};
auto r = a
	| views::filter([](int i) {return i % 2 == 0;})
	| views::reverse;
//得到内容为 {8，4，2，6}的视图
```

**elements_view示例**

浪费性能的写法

```c++
void clear_data(const set<int>& ids) {
	for (int id: ids) {...}
}

map<int, size_t> mp;
set<int> ids;
for (const auto& item: mp) {
	ids.insert(item.first);
}
clear_data(ids);
```

 好的写法

```c++
void clear_data(range auto&& ids) {
	for (int id: ids) {...}
}

map<int, size_t> mp;
clear_data(views::keys(mp));

//range 是一个concept，要求满足是一个range
//auto&& 自动推导，其实是个函数模板，用的是转发引用
```

 