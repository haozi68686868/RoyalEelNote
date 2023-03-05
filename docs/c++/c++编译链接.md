

### 符号可见性

- gcc控制符号可见性

- -fvisibility=hidden
- 配合 __attribute__((visibility("default")))使用，加了这行的函数才可以对外看见符号

##### 静态库不能隐藏符号？

- 待实验验证

