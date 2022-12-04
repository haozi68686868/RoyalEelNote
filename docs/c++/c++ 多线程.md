# Multi Thread

### std::mutex

- std::lock_guard
  - 基础锁
- std::unique_lock
  - lock_guard的升级版，使用更加灵活，例如可以灵活控制锁的范围，功能更加强大，但更耗时一些
- std::condition_variable
  - 高效地配合线程同步

### std::thread

```c++
void threadFun2()
{
	for (int i = 0; i < 10000; i++)
		count2++;
}
// 启动多个线程
	std::vector<std::thread> threads;
	for (int i = 0; i < 10; i++)
		threads.push_back(std::thread(threadFun2));
	for (auto&thad : threads)
		thad.join();
```

### std::atomic

- 原子操作，提供原子一些基本的原子操作，例如递增，赋值，逻辑与或等等
- std::atomic\<T>
  - 模板类型要求T是一个trivially copyable type（拷贝不变的类型）
  - 所以std::atomic<shared_ptr>并不合法（可能会加入c++20的标准）

### 线程同步实现方式小结

1. 互斥锁
   - mutex、lock_guard、unique_lock
2. 条件变量：condition_variable
3. 信号量（C语言）：semaphore
4. 异步操作
   - std::async
   - futrue
   - promise
5. 原子操作

### pthread和thread的区别

C++的thread是经过良好设计并且跨平台的线程表示方式，然而pthread是“粗犷、直接、暴力”的类UNIX平台线程表示方式，如你在C++11的thread你可以使用lock_guard等来实现RAII方式的lock管理，而pthread则很难。p for POSIX

如果只在 Linux 下编程，那么 C++11 的 thread 的附加值几乎为零（我认为它过度设计了，同时损失了一些功能），你自己把 Pthreads 封装成一个简单好用的线程库只需要两三百行代码，用十几个 pthreads 函数实现 4 个 class：thread、mutex、lock_guard、condvar，而且 RAII 的好处也享受到了。

std::thread内部其实使用pthread实现的（Linux平台），winthread（Windows平台）

- std::thread：
  - 优点：跨平台支持好
  - 缺点：过度封装，功能不全，比如没有shared_mutex(C++17支持)
- pthread：
  - 优点：效率更高
  - 缺点：只支持Unix类系统