#### 将二进制文件读入std::string

```c++
std::ifstream fin;
fin.open(file,std::ios::binary);
std::stringstream ss;
ss << fin.rdbuf();
std::string res = ss.str();
```

