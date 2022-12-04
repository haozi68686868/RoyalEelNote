### GTest

通常有两种：

- 致命断言 - ASSERT_XXX
- 非致命断言 - EXPECT_XXX

### 1、真假判断

```cpp
EXPECT_TRUE(ret)：ret == true
EXPECT_FALSE(ret)：ret == false
```

### 2、等于不等于

```cpp
EXPECT_EQ(expected, actual)：expected == actual
EXPECT_NE(expected, actual)：expected != actual
EXPECT_FLOAT_EQ(expected, actual)：(float)expected == actual
EXPECT_DOUBLE_EQ(expected, actual)：(double)expected == actual
EXPECT_NEAR(var1, var2, tol)：abs(var1 - var2) <= tol
```

当判断浮点数时，推荐使用后三个。

### 3、大于小于

```cpp
EXPECT_LT(var1, var2)：var1 < var2
EXPECT_GT(var1, var2)：var1 > var2
EXPECT_LE(var1, var2)：var1 <= var2
EXPECT_GE(var1, var2)：var1 >= var2
```

### 4、字符串判断

```cpp
EXPECT_STREQ(s1, s2)：s1 == s2
EXPECT_STRNE(s1, s2)：s1 != s2
EXPECT_STRCASEEQ(s1, s2)：s1 == s2
EXPECT_STRCASENE(s1, s2)：s1 != s2
```

### 5、类型断言

```c++
::testing::StaticAssertTypeEq<T1, T2>();
```

