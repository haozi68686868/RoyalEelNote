### Grep

**1.作用**

Linux系统中grep命令是一种强大的文本搜索工具，它能使用正则表达式搜索文本，并把匹 配的行打印出来。grep全称是Global Regular Expression Print，表示全局正则表达式版本，它的使用权限是所有用户。

**2.格式** grep [options]

**3.主要参数** [options]主要参数：

```text
-a或--text   不要忽略二进制的数据。
  -A<显示列数>或--after-context=<显示列数>   除了显示符合范本样式的那一列之外，并显示该列之后的内容。
  -b或--byte-offset   在显示符合范本样式的那一列之前，标示出该列第一个字符的位编号。
  -B<显示列数>或--before-context=<显示列数>   除了显示符合范本样式的那一列之外，并显示该列之前的内容。
  -c或--count   计算符合范本样式的列数。
  -C<显示列数>或--context=<显示列数>或-<显示列数>   除了显示符合范本样式的那一列之外，并显示该列之前后的内容。
  -d<进行动作>或--directories=<进行动作>   当指定要查找的是目录而非文件时，必须使用这项参数，否则grep指令将回报信息并停止动作。
  -e<范本样式>或--regexp=<范本样式>   指定字符串做为查找文件内容的范本样式。
  -E或--extended-regexp   将范本样式为延伸的普通表示法来使用。
  -f<范本文件>或--file=<范本文件>   指定范本文件，其内容含有一个或多个范本样式，让grep查找符合范本条件的文件内容，格式为每列一个范本样式。
  -F或--fixed-regexp   将范本样式视为固定字符串的列表。
  -G或--basic-regexp   将范本样式视为普通的表示法来使用。
  -h或--no-filename   在显示符合范本样式的那一列之前，不标示该列所属的文件名称。
  -H或--with-filename   在显示符合范本样式的那一列之前，表示该列所属的文件名称。
  -i或--ignore-case   忽略字符大小写的差别。
  -l或--file-with-matches   列出文件内容符合指定的范本样式的文件名称。
  -L或--files-without-match   列出文件内容不符合指定的范本样式的文件名称。
  -n或--line-number   在显示符合范本样式的那一列之前，标示出该列的列数编号。
  -q或--quiet或--silent   不显示任何信息。
  -r或--recursive   此参数的效果和指定“-d recurse”参数相同。
  -s或--no-messages   不显示错误信息。
  -v或--revert-match   反转查找。
  -V或--version   显示版本信息。
  -w或--word-regexp   只显示全字符合的列。
  -x或--line-regexp   只显示全列符合的列。
  -y   此参数的效果和指定“-i”参数相同。
  --help   在线帮助。
```

**pattern正则表达式主要参数：**

```text
\： 忽略正则表达式中特殊字符的原有含义。
^：匹配正则表达式的开始行。
$: 匹配正则表达式的结束行。
\<：从匹配正则表达 式的行开始。
\>：到匹配正则表达式的行结束。
[ ]：单个字符，如[A]即A符合要求 。
[ - ]：范围，如[A-Z]，即A、B、C一直到Z都符合要求 。
. ：所有的单个字符。
* ：有字符，长度可以为0
```

**4.grep命令使用简单实例**

```text
$ grep ‘test’ d*
显示所有以d开头的文件中包含 test的行。
$ grep ‘test’ aa bb cc
显示在aa，bb，cc文件中匹配test的行。
$ grep ‘[a-z]\{5\}’ aa
显示所有包含每个字符串至少有5个连续小写字符的字符串的行。
$ grep ‘w\(es\)t.*\1′ aa
如果west被匹配，则es就被存储到内存中，并标记为1，然后搜索任意个字符(.*)，这些字符后面紧跟着 另外一个es(\1)，找到就显示该行。如果用egrep或grep -E，就不用”\”号进行转义，直接写成’w(es)t.*\1′就可以了。
```

**5.grep命令使用复杂实例**

```text
假设您正在’/usr/src/Linux/Doc’目录下搜索带字符 串’magic’的文件：
$ grep magic /usr/src/Linux/Doc/*
sysrq.txt:* How do I enable the magic SysRQ key?
sysrq.txt:* How do I use the magic SysRQ key?
其中文件’sysrp.txt’包含该字符串，讨论的是 SysRQ 的功能。
默认情况下，’grep’只搜索当前目录。如果 此目录下有许多子目录，’grep’会以如下形式列出：
grep: sound: Is a directory
这可能会使’grep’ 的输出难于阅读。这里有两种解决的办法：
明确要求搜索子目录：grep -r
或忽略子目录：grep -d skip
如果有很多 输出时，您可以通过管道将其转到’less’上阅读：
$ grep magic /usr/src/Linux/Documentation/* | less
这样，您就可以更方便地阅读。
 
```

**下面还有一些有意思的命令行参数：**

```text
grep -i pattern files ：不区分大小写地搜索。默认情况区分大小写，
grep -l pattern files ：只列出匹配的文件名，
grep -L pattern files ：列出不匹配的文件名，
grep -w pattern files ：只匹配整个单词，而不是字符串的一部分(如匹配’magic’，而不是’magical’)，
grep -C number pattern files ：匹配的上下文分别显示[number]行，
grep pattern1 | pattern2 files ：显示匹配 pattern1 或 pattern2 的行，
grep pattern1 files | grep pattern2 ：显示既匹配 pattern1 又匹配 pattern2 的行。

grep -n pattern files  即可显示行号信息

grep -c pattern files  即可查找总行数

这里还有些用于搜索的特殊符号：
\< 和 \> 分别标注单词的开始与结尾。
例如：
grep man * 会匹配 ‘Batman’、’manic’、’man’等，
grep ‘\<man’ * 匹配’manic’和’man’，但不是’Batman’，
grep ‘\<man\>’ 只匹配’man’，而不是’Batman’或’manic’等其他的字符串。
‘^’：指匹配的字符串在行首，
‘$’：指匹配的字符串在行尾，
```

### awk

## **一、awk简介**

awk 是一种编程语言，用于在linux/unix下对文本和数据进行处理。数据可以来自标准输入、一个或多个文件，或其它命令的输出。可以在命令行中使用，但更多是作为脚本来使用。

awk的处理文本和数据的方式是这样的，它逐行扫描文件，从第一行到最后一行，寻找匹配的特定模式的行，并在这些行上进行操作。如果没有指定处理动作，则把匹配的行显示到标准输出(屏幕)，如果没有指定模式，则所有被操作所指定的行都被处理。

awk分别代表其作者姓氏的第一个字母。因为它的作者是三个人，分别是Alfred Aho、Brian Kernighan、Peter Weinberger。

```text
 awk是行处理器: 优势在于处理庞大文件时不会出现内存溢出或是处理缓慢的问题。
 awk处理过程: 依次对每一行进行处理，然后输出,默认分隔符是空格或者tab键 
```

### **二、awk的形式语法格式**

```
awk [options] 'commands' filenames
options：
```

`-F` 对于每次处理的内容，可以指定一个自定义的分隔符，默认的分隔符是空白字符（空格或 tab 键 ）

### **三、awk工作原理**

```
awk -F":" '{print $1,$3}' /etc/passwd
 (1)awk使用一行作为输入，并将这一行赋给变量$0,每一行可称作为一个记录，以换行符结束 
 (2)然后，行被空格分解成字段，每个字段存储在已编号的变量中，从$1开始 
 (3)awk如何知道空格来分隔字段的呢?因为有一个内部变量FS来确定字段分隔符，初始时，FS赋为空格或者是tab 
 (4)awk打印字段时，将以设置的方法，使用print函数打印，awk在打印的字段间加上空格，因为$1,$2间有一个,逗号。逗号比较特殊，映射为另一个变量，成为输出字段分隔符OFS，OFS默认为空格 
 (5)awk打印字段时，将从文件中获取另一行，并将其存储在$0中，覆盖原来的内容，然后将新的字符串分隔成字段并进行处理。该过程持续到处理文件结束。
command：
 BEGIN{}                   {}               END{}         filename
 
 行处理前的动作          行内容处理的动作     行处理之后的动作    文件名
 
 BEGIN{}和END{} 是可选项。
 函数-BEGIN{}：读入文本之前要操作的命令。（也可以设置变量.取值可以不加$）
 {}:主输入循环：用的最多。读入文件之后擦操作的命令。如果不读入文件都可以不用写。
 END{}:文本全部读入完成之后执行的命令。
```

### **示例**

```bash
 [root@awk ~]# awk 'BEGIN{ print 1/2} {print "ok"} END{print "----"}' /etc/hosts
 或者：
 [root@awk ~]# cat /etc/hosts | awk 'BEGIN{print 1/2} {print "ok"} END{print "----"}'
 0.5
 ok
 ok
 ----
 
```

### **四、记录与字段相关内部变量：**

```bash
 1.记录和字段
 awk 按记录处理：一行是一条记录，因为awk默认以换行符分开的字符串是一条记录。（默认\n换行符：记录分隔符）
 字段：以字段分割符分割的字符串   默认是单个或多个“ ” tab键。
 
 2.awk中的变量
 $0:表示整行；
 NF : 统计字段的个数
 $NF:是number finally,表示最后一列的信息
 RS：输入记录分隔符；
 ORS：输出记录分隔符。
 NR:打印记录号，（行号）
 FNR：可以分开,按不同的文件打印行号。
 FS : 输入字段分隔符,默认为一个空格。  
 OFS 输出的字段分隔符，默认为一个空格。 
 FILENAME 文件名  被处理的文件名称
 $1  第一个字段，$2第二个字段，依次类推...
```