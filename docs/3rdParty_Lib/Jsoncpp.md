# Jsoncpp

JSON全称为JavaScript ObjectNotation，它是一种轻量级的数据交换格式，易于阅读、编写、解析。jsoncpp是c++解析JSON串常用的解析库之一。

jsoncpp中主要的类：

Json::Value：可以表示所有支持的类型，如：int , double ,string , object, array等。其包含节点的类型判断(isNull,isBool,isInt,isArray,isMember,isValidIndex等),类型获取(type),类型转换(asInt,asString等),节点获取(get,[]),节点比较(重载<,<=,>,>=,==,!=),节点操作(compare,swap,removeMember,removeindex,append等)等函数。
Json::Reader：将文件流或字符串创解析到Json::Value中，主要使用parse函数。Json::Reader的构造函数还允许用户使用特性Features来自定义Json的严格等级。
Json::Writer：与JsonReader相反，将Json::Value转换成字符串流等，Writer类是一个纯虚类，并不能直接使用。在此我们使用 Json::Writer 的子类：Json::FastWriter(将数据写入一行,没有格式),Json::StyledWriter(按json格式化输出,易于阅读)

 

JsonCpp使用注意点:

1.对不存在的键获取值会返回此类型的默认值。
2.通过key获取value时,要先判断value的类型,使用错误的类型获取value会导致程序中断。
3.获取json数组中某一项key的value应该使用value[arraykey][index][subkey]获取或循环遍历数组获取。
4.append函数功能是将Json::Value添加到数组末尾。

5.由于Jsoncpp解析非法json时，会自动容错成字符类型。对字符类型取下标时，会触发assert终止进程。
解决方法：启用严格模式，让非法的json解析时直接返回false，不自动容错。这样，在调用parse的时候就会返回false。

```
Json::Reader *pJsonParser = new Json::Reader(Json::Features::strictMode());
```

 

判断json字符串中是否存在某键值的几种方法:

```
1.value.isMember("key");    //存在返回true,否则为false
2.value["sex"].isNull();    //为NULL返回1,否则为0
```

 

JsonCpp读写示例代码:

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```c++
#include <iostream>
#include <sstream>
#include <fstream>
#include <json/json.h>

void readJsonFromFile()
{
    std::ifstream ifs;
    ifs.open("a.json");
    std::stringstream buffer;
    buffer << ifs.rdbuf();
    ifs.close();

    auto str = buffer.str();

    Json::Reader reader;
    Json::Value value;
    if (reader.parse(str, value)) {
        //节点判断
        std::cout << "value's empty:" << value.empty() << std::endl;
        std::cout << "name is string:" << value["name"].isString() << std::endl;
        std::cout << "age is string:" << value["age"].isString() << std::endl;

        //类型获取
        std::cout << "name's type:" << value["name"].type() << std::endl;
        std::cout << "like's type:" << value["like"].type() << std::endl;

        //类型转换
        //根据Key获取值时最好判断类型,否则解析会中断
        std::cout << "name:" << value["name"].asString() << std::endl;
        std::cout << "age:" << value["age"].asInt() << std::endl;

        //节点获取
        std::cout << value["job"] << std::endl;                        //[]方式获取
        std::cout << value.get("name", "dxx") << std::endl;            //get方式获取
        std::cout << value.isMember("job") << std::endl;
        std::cout << "value's obj:" << value.isObject() << std::endl;
        std::cout << "like's obj:" << value["like"].isObject() << std::endl;
        std::cout << "like.size:" << value["like"].size() << std::endl;
        std::cout << "like[0][food]:" << value["like"][0]["food"].asString() << std::endl;

        //节点操作
        std::cout << "name compare age:" << value["name"].compare("age") << std::endl;
        value["name"] = "swduan";            //修改
        value["address"] = "hz";             //增加
        value["phone"] = "10086";        
        value.removeMember("age");           //删除
        value["like"][0]["sport"] = "game";  //往value["like"]中添加一项元素

        Json::Value item;
        item["hate"] = "game";
        value["like"].append(item);            //value["like"]中再添加一维数组
        std::cout << "value[\"like\"]'s size:" << value["like"].size() << std::endl;
        
        std::cout << "--------------------" << std::endl;
        std::cout << value.toStyledString() << std::endl;

        std::cout << "--------------------" << std::endl;
        auto all_member = value.getMemberNames();
        for (auto member : all_member) {
            std::cout << member << std::endl;
        }

        std::cout << "--------------------" << std::endl;
        value.clear();        //清空元素
        std::cout << value.toStyledString() << std::endl;
    }
}

void jsonWriteToFile()
{
    Json::FastWriter write;
    Json::Value root;

    Json::Value item;
    Json::Value arrayObj;
    item["book"] = "c++";
    item["food"] = "apple";
    item["music"] = "ddx";
    arrayObj.append(item);

    root["name"] = "dsw";
    root["age"]  = 18;
    root["like"] = arrayObj;    //注意:这里不能用append,append功能是将Json::Value添加到数组末尾

    auto str = root.toStyledString();
    std::cout << str << std::endl;

    std::ofstream ofss;
    ofss.open("a.json");
    ofss << str;
    ofss.close();
}

int main()
{
    jsonWriteToFile();
    readJsonFromFile();

    getchar();
    return 0;
}
```