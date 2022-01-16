\1. 假设你目前的git log状态如下: 

6558fe1 AUTODRIVE-4270 xxx 

54110d4 AUTODRIVE-5289 yyy 

0caddfc AUTODRIVE-5193 zzz 

其中 yyy zzz已经合并到master，而xxx已提交commit但未合并，其topic为AUTODRIVE-4270_xxx 

现在经过代码review，xxx已经需要进行一些修改。 

假设你现在已经完成了这些修改，那么应该如何将修改合并到xxx中并更新gerrit上的commit？ 

```
git commit --amend
git push origin HEAD:refs/for/master%topic=AUTODRIVE-4270_xxx
```



\2. 从gerrit上拉项目，本地提交commit后发现没有change-id，原因是？ 

```
在clone时没有包含commit-msg hook，应使用”Clone with commit-msg hook“的指令
```



\3. 在gerrit中，可以支持对一个commit进行多次修改，也支持不同git项目中的commit一起运行CI 

a) gerrit中是用什么来保证多次提交属于同一个commit？ 

```
change-id
```

b) CI中是以什么为单位来一次运行不同git项目中的commit？ 

```
topic
```

\4. commit准备好后，应该找哪些人+1 +V？ 

```
路测完成后+V
模块相关、代码review、代码合并的人员+1
CI测试+1
```



\5. 哪些文件应该使用lfs追踪？ 

```
占用空间较大的文件(>100kB)，例如图片、视频、动态库、静态库、模型等
```

