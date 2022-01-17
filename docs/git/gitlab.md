\#检出仓库：

git clone git://github.com/jquery/jquery.git

\#查看远程仓库：

git remote -v

\#添加远程仓库：

git remote add [name] [url]

\#删除远程仓库：

git remote rm [name]

\#修改远程仓库：

git remote set-url --push [name] [newUrl]

\#拉取远程仓库：

git pull [remoteName] [localBranchName]

\#推送远程仓库：

git push [remoteName] [localBranchName]



\#提交本地test分支作为远程的master分支

git push origin test:master

\#提交本地test分支作为远程的test分支

git push origin test:test



\#查看本地分支：

git branch

\#查看远程分支：

git branch -r

\#创建本地分支：

git branch [name] ----注意新分支创建后不会自动切换为当前分支

\#切换分支：

git checkout [name]

\#创建新分支并立即切换到新分支：

git checkout -b [name]

\#删除分支：

git branch -d [name] ---- -d选项只能删除已经参与了合并的分支，对于未有合并的分支是无法删除的。如果想强制删除一个分支，可以使用-D选项

\#合并分支：

git merge [name] ----将名称为[name]的分支与当前分支合并

\#创建远程分支(本地分支push到远程)：

git push origin [name]

\#删除远程分支：

git push origin :heads/[name] or gitpush origin :[name]



\#查看版本：

git tag

\#创建版本：

git tag [name]

\#删除版本：

git tag -d [name]

\#查看远程版本：

git tag -r

\#创建远程版本(本地版本push到远程)：

git push origin [name]

\#删除远程版本：

git push origin :refs/tags/[name]

\#合并远程仓库的tag到本地：

git pull origin --tags

\#上传本地tag到远程仓库：

git push origin --tags

\#创建带注释的tag：

git tag -a [name] -m 'yourMessage'





git branch 查看本地所有分支

git status 查看当前状态 

git commit 提交 

git branch -a 查看所有的分支

git branch -r 查看本地所有分支

git commit -am "init" 提交并且加注释

git remote add origin git@192.168.1.119:ndshow

git push origin master 将文件给推到服务器上

git remote show origin 显示远程库origin里的资源

git push origin master:develop

git push origin master:hb-dev 将本地库与服务器上的库进行关联

git checkout --track origin/dev 切换到远程dev分支

git branch -D master develop 删除本地库develop

git checkout -b dev 建立一个新的本地分支dev

git merge origin/dev 将分支dev与当前分支进行合并

git checkout dev 切换到本地dev分支

git remote show 查看远程库

git add .

git rm 文件名(包括路径) 从git中删除指定文件

git clone git://github.com/schacon/grit.git 从服务器上将代码给拉下来

git config --list 看所有用户

git ls-files 看已经被提交的

git rm [file name] 删除一个文件

git commit -a 提交当前repos的所有的改变

git add [file name] 添加一个文件到git index

git commit -v 当你用－v参数的时候可以看commit的差异

git commit -m "This is the message describing the commit" 添加commit信息

git commit -a -a是代表add，把所有的change加到git index里然后再commit

git commit -a -v 一般提交命令

git log 看你commit的日志

git diff 查看尚未暂存的更新

git rm a.a 移除文件(从暂存区和工作区中删除)

git rm --cached a.a 移除文件(只从暂存区中删除)

git commit -m "remove" 移除文件(从Git中删除)

git rm -f a.a 强行移除修改后文件(从暂存区和工作区中删除)

git diff --cached 或 $ git diff --staged 查看尚未提交的更新

git stash push 将文件给push到一个临时空间中

git stash pop 将文件从临时空间pop下来

git remote add origin git@github.com:username/Hello-World.git

git push origin master 将本地项目给提交到服务器中

git pull 本地与服务器端同步

git push (远程仓库名) (分支名) 将本地分支推送到服务器上去。

git push origin serverfix:awesomebranch

git fetch 相当于是从远程获取最新版本到本地，不会自动merge

git commit -a -m "log_message" (-a是提交所有改动，-m是加入log信息) 本地修改同步至服务器端 ：

git branch branch_0.1 master 从主分支master创建branch_0.1分支

git branch -m branch_0.1 branch_1.0 将branch_0.1重命名为branch_1.0

git checkout branch_1.0/master 切换到branch_1.0/master分支

du -hs

> 查看版本

```
cat /opt/gitlab/embedded/service/gitlab-rails/VERSION
```

> 实时查看日志

```
 gitlab-ctl tail
```

> 数据库关系升级

```
 gitlab-rake db:migrate
```

> 清理redis缓存

```
gitlab-rake cache:clear
```

> 升级GitLab-ce 版本

```
yum update gitlab-ce
```

> 升级PostgreSQL最新版本

```
 gitlab-ctl pg-upgrade
```