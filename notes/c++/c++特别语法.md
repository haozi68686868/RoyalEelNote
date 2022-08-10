C++对于左值和右值没有标准定义，但是有一个被广泛认同的说法：

- 可以取地址的，有名字的，非临时的就是左值；
- 不能取地址的，没有名字的，临时的就是右值；

### lambda表达式

```
[捕捉列表](参数列表)mutable->返回值类型{函数体}
捕捉列表：该列表出现在lambda函数的开始位置，编译器根据[]来判断接下来的代码是否为lambda函数，捕捉列表可以捕捉所有”当前位置能访问到的变量“供lambda函数使用
参数列表：与普通函数的参数列表一致。则可以连同()一起省略
mutable:默认情况下，lambda函数总是一个const函数，mutable可以取消其常量性。使用该修饰符，参数列表不可以省略(即使参数列表为空)
->返回值类型。用于追踪返回值类型。没有返回值时可以省略。返回值类型明确的情况下，也可以省略
{函数体}：在该函数体，除了可以使用参数外，也可以使用捕捉到的所有变量

[函数对象参数] (操作符重载函数参数) mutable 或 exception 声明 -> 返回值类型 {函数体}
a [var]:表示“值传递方式”捕获变量var
b [=]:表示“值传递方式”捕获所有父作用域中的变量(包括this)
c [&var]:表示”引用传递“变量var
d [&]:表示“引用传递”捕获所有父作用域中的变量(this)
e [this]：表示值传递方式捕获当前的this指针
f [=,&a,&b]:引用传递a和b，其他变量值传递
```

```c++
// 最简单的lambda表达式
[]{};
// 省略参数列表和返回值类型,返回值类型有编译器推演为int
int a=3,b=4;
[=]{return a+3;};
// 省略返回值类型
auto fun1 = [&](int c){b = a + c;};
// 各部分完整的lambda函数
auto fun2 = [=,&b](int c)->int(return += a + c;);
// 值传递x
int x = 10;
auto add_x = [x](int a)mutable{x *= 2; return a + x;};
return 0;

//Usage Example 1
std::vector<int> some_list;
int total = 0;
int value = 5;
std::for_each(begin(some_list), end(some_list), [&, value, this](int x)
{
    total += x * value * this->some_func();
});
//Usage Example 2
int main() {
    vector<int> data;
    for (int i = 0; i < 10; ++i)
        data.push_back(i);
    sort(data.begin(), data.end(), [](int &a, int &b)->bool {
         return a > b;
         });
    for (int i = 0; i < data.size(); ++i)
        cout << data[i] << endl;
    return 0;
}
```

### std::bind 和 std::function

“可调用对象” std::function，可以取代函数指针，因为它同样可以延迟函数的执行。

```c++
// 普通函数
int add(int a, int b){return a+b;} 

// lambda表达式
auto mod = [](int a, int b){ return a % b;}

// 函数对象类
struct divide{
    int operator()(int denominator, int divisor){
        return denominator/divisor;}};
//可调用对象
std::function<int(int ,int)>  a = add; 
std::function<int(int ,int)>  b = mod ; 
std::function<int(int ,int)>  c = divide(); 
```

可将std::bind函数看作一个通用的函数适配器，它接受一个可调用对象，生成一个新的可调用对象来“适应”原对象的参数列表。并且，绑定部分参数后，可减少调用对象传入的参数。

```c++
//绑定一个普通函数
double my_divide (double x, double y) {return x/y;}
auto fn_half = std::bind (my_divide,_1,2); // 
std::cout << fn_half(10) << '\n';// 5

// 绑定成员函数:
  auto bound_member_fn = std::bind (&MyPair::multiply,_1); // returns x.multiply()
  std::cout << bound_member_fn(ten_two) << '\n';           // 20

  auto bound_member_data = std::bind (&MyPair::a,ten_two); // returns ten_two.a
  std::cout << bound_member_data() << '\n';                // 10
```

- _1表示占位符，位于<functional>中，std::placeholders::_1

```c++
struct Foo {
    void print_sum(int n1, int n2){std::cout << n1+n2 << '\n';}
};
ostream & print(ostream &os, const string& s, char c)
{
    os << s << c;
    return os;
}
int main() 
{
    Foo foo;
    ostringstream os1;
    auto f = std::bind(&Foo::print_sum, &foo, 95, std::placeholders::_1);
    f(5); // 100
    
    for_each(words.begin(), words.end(), 
                   [&os, c](const string & s){os << s << c;} );//lambda函数
    for_each(words.begin(), words.end(),bind(print, ref(os1), _1, c));//std::ref表示引用
}
```

- bind绑定类成员函数时，第一个参数表示对象的成员函数的指针，第二个参数表示对象的地址(相当于this指针)。

#### 虚函数

- 为什么要把基类的析构函数定义为虚函数

```
如果不这样做，则在析构基类指针时，不会调用派生类的析构函数，造成不必要的问题。
```

#### dynamic_cast和static_cast有什么区别？

dynamic_cast在运行时确定，static_cast在编译时确定

假设有基类Base和子类A，上行转换为A->Base，下行转换为Base->A。

在下行转换时只能只用dynamic_cast

```c++
// 对于上行转换，A*转换为Base* static_cast和dynamic_cast是相同的
// c++98 风格
A* a;
Base* base_ptr = (Base*) a;
base_ptr = static_cast<Base*>(a);

// 对于下行转换，static_cast是不安全的，必须使用dynamic_cast
Base* base_ptr = new A();
A* a= (A*) base_ptr;
a = dynamic_cast<A*>(base_ptr);
```

对于下行转换，说到下行转换，有一点需要了解的是在C++中，一般是可以用父类指针指向一个子类对象，如parent* P1 = new Children(); 但这个指针只能访问父类定义的数据成员和函数，这是C++中的静态联翩，但一般不定义指向父类对象的子类类型指针，如Children* P1 = new parent；这种定义方法不符合生活习惯，在程序设计上也很麻烦。**这就解释了也说明了，在上行转换中，static_cast和dynamic_cast效果是一样的，而且都比较安全，因为向上转换的对象一般是指向子类对象的子类类型指针；而在下行转换中，由于可以定义就不同了指向子类对象的父类类型指针，同时static_cast只在编译时进行类型检查，而dynamic_cast是运行时类型检查，则需要视情况而定。**

dynamic_cast主要用于类层次结构中父类和子类之间指针和引用的转换，由于具有运行时类型检查，因此可以保证下行转换的安全性，何为安全性？即转换成功就返回转换后的正确类型指针，如果转换失败，则返回NULL，之所以说static_cast在下行转换时不安全，是因为即使转换失败，它也不返回NULL。

**但是，尽量避免使用dynamic_cast，因为效率很低，在注重效率的场景，应该尽可能安全得使用static_cast**

#### C++的const类成员函数

- 我们定义的类的成员函数中，常常有一些成员函数不改变类的数据成员，也就是说，这些函数是"只读"函数，而有一些函数要修改类数据成员的值。如果把不改变数据成员的函数都加上const关键字进行标识，显然，可提高程序的可读性。其实，它还能提高程序的可靠性，**已定义成const的成员函数，一旦企图修改数据成员的值，则编译器按错误处理**。 const成员函数和const对象 实际上，const成员函数还有另外一项作用，即常量对象相关。对于内置的数据类型，我们可以定义它们的常量，用户自定义的类也一样，可以定义它们的常量对象。

```c++
class Screen {
public:
    int ok() const {return _cursor; }
    int error(intival) const { _cursor = ival; }
};
```

- 在C++中，只有被声明为const的成员函数才能被一个const类对象调用。

#### 友元 Friend

- 在定义一个类的时候，可以把一些函数（包括全局函数和其他类的成员函数）声明为“友元”，这样那些函数就成为该类的友元函数，在友元函数内部就可以访问该类对象的私有成员了。
- 一个类 A 可以将另一个类 B 声明为自己的友元，类 B 的所有成员函数就都可以访问类 A 对象的私有成员。

```c++
friend  返回值类型  函数名(参数表);
friend  返回值类型  其他类的类名::成员函数名(参数表);
friend  class  类名;
```

```c++
class CCar
{
private:
    int price;
    friend class CDriver;  //声明 CDriver 为友元类
};
class CDriver
{
public:
    CCar myCar;
    void ModifyCar()  //改装汽车
    {
        myCar.price += 1000;  //因CDriver是CCar的友元类，故此处可以访问其私有成员
    }
};
int main()
{
    return 0;
}
```

#### c++11 for循环

```c++
for(auto& x:arr)
{
    std::cout << x << std::endl;
}
//两种写法是等价的

for(auto it = arr.begin(); it != arr.end(); ++it)
{
std::cout << *it << std::endl;
}
```

如果要让一个自定义类能完成 for(auto item :array)的for循环迭代操作，需要实现begin,end,++,!=,*，这5个操作运算

#### c++模版及相关关键字

##### decltype

decltype关键字与auto关键字相似，但又有不同之处；auto关键字是在编译时通过已经初始化的变量来确定auto所代表的类型。换句话说，auto修饰的表达式必须是已经初始化的变量；那么如果我们只是想得到此变量的类型，那又该如何做呢？这个时候就轮到decltype出场了，decltype关键字也是用来在编译时推导出一个表达式的类型，但此表达式初始化与否，在编译器都没有多大的影响。

```c++
const decltype(z) *p = &z;  //*p -> const int
decltype(z) *pi = &z;       //*pi -> int, pi->int*
decltype(pi) *pp = π     //*pp -> int*, pp->int**

cout << pp << endl;         //打印结果：0x61fe80
cout << *pp << endl;        //打印结果：0x61fe84
cout << **pp << endl;       //打印结果：2

template <class U, class V>
void Somefunction(U u, V v)
{
	result = u*v;//now what type would be the result???
	decltype(u*v) result = u*v;//Hmm .... we got what we want
}
```

##### std::enable_if 和 SFINAE

SFINAE是英文Substitution failure is not an error的缩写，意思是匹配失败不是错误。

```c++
//std::enable_if Definition
//默认实现是空
template <bool, typename T=void>
struct enable_if {
};

//如果bool是true的话，特化为定义一个type T,特化版本优先
template <typename T>
struct enable_if<true, T> {
  using type = T;
};

// 1. 返回类型（布尔）仅在T为整数类型时有效：
template <class T>
typename std::enable_if<std::is_integral<T>::value,bool>::type
is_odd (T i) {
    return bool(i%2);
}

// 2. 第二个模板参数仅在T为整数类型时有效：
template < class T,
           class = typename std::enable_if<std::is_integral<T>::value>::type>
bool is_even (T i) {
    return !bool(i%2);
}
```

```c++
std::enable_if_t<T> 等价于 typename std::enable_if<T>::type
```

#### 结构体 - 内存填充规则

```c++
class A
{
    int a;
    short b;
    int c;
    char d;
};// size(A) = 16 （32位编译）/ size(A) = 16 (64位编译)
class B
{
    double a;
    short b;
    int c;
    char d;
};// size(B) = 20 (32位编译) / size(B) = 24 （64位编译）
//这里主要的区别是，在32位系统中，double是由2个4字节构成的
class C
{
	char a; 
    char b; 
    char c;
};// size(C) = 3 这里最大的数据类型是1个字节，所以只需要填充对齐到1的整数倍即可

class D
{
	char a; 
    short b;
};// size(D) = 4 这里最大的数据类型short是2个字节，所以需要填充到2的整数倍
```

- 编译指令

```shell
gcc -o helloworld main.cpp # 默认编译方式
gcc -m32 -o helloworld main.cpp # -m32 32位编译方式
```

- gcc会将结构体的大小填充为结构体**最大成员**的整数倍
- 64位编译和32位编译的最大区别在于：
  - 64位的最大对齐字节是8，32位的最大对齐字节是4。
  - 32位中double类型是用2个4字节表示的

#### delete和delete[]

- delete 用于析构单个对象 MyClass* a = new MyClass();
- delete[] 用于析构多个对象 MyClass* a = new MyClass[10];

#### new和malloc的区别

| 特征               | new/delete                            | malloc/free                          |
| ------------------ | ------------------------------------- | ------------------------------------ |
| 分配内存的位置     | 自由存储区                            | 堆                                   |
| 内存分配成功返回值 | 完整类型指针                          | void*                                |
| 内存分配失败返回值 | 默认抛出异常                          | 返回NULL                             |
| 分配内存的大小     | 由编译器根据类型计算得出              | 必须显式指定字节数                   |
| 处理数组           | 有处理数组的new版本new[]              | 需要用户计算数组的大小后进行内存分配 |
| 已分配内存的扩充   | 无法直观地处理                        | 使用realloc简单完成                  |
| 是否相互调用       | 可以，看具体的operator new/delete实现 | 不可调用new                          |
| 分配内存时内存不足 | 客户能够指定处理函数或重新制定分配器  | 无法通过用户代码进行处理             |
| 函数重载           | 允许                                  | 不允许                               |
| 构造函数与析构函数 | 调用                                  | 不调用                               |

