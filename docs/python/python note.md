# python note

- python的浮点数有17位有效数字，默认print函数会显示12位有效数字，如果需完整显示需要format

### 

### Python关键字

#### \__all__

执行"from xxx import *“语句时，只有\__all__中的成员可以被导入

```
__all__ = ["Nodelist","function2"]
```

#### \__slot__

槽位，用于节省空间；类成员只能定义"\__slot__"所包含的变量

#### \__version__

库版本

#### \__file__

库文件路径

#### \__getitem__(self, key)

obj[key] 调用该函数 

#### \__setitem__(self, key, value)

obj[key] = value 调用该函数 

#### \__delitem__(self, key)

del obj[key] 调用该函数 

#### \__debug__

调试标志 Python -O xxx.py时，该值为false，默认情况为True

- \__debug__ 为false时，断言assert不生效