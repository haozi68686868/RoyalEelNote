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