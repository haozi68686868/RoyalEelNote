# git 开发笔记

- https://git-scm.com/book/en/v2
- 如果遇到合并冲突怎么办
  1. 先尝试rebase
  2. 如果无法自动rebase
     1. 则先拉到最新代码
     2. cherry-pick对应的commit
     3. 解决冲突(文件中修改)
     4. git add (文件) -- 标示解决完冲突的文件
     5. git cherry-pick continue
     6. 完成cherry-pick
     7. 重新上传代码

#### 撤销操作

```shell
## 删除操作
# 系统的删除操作，未被git跟踪的文件也会生效
rm -f {file}
# 删除git已跟踪的文件和文件的索引
git rm -f {file}
# 仅在git跟踪中删除，在本地目录保留；若该文件在上个提交中有，则本次提交中删除该文件
git rm --cached {file}

## 取消暂存区的状态
# 重置暂存区，相当于git add的反向操作，取消文件的暂存状态
git reset HEAD {file}
# 重置整个工作区，需注意，这个命令只能重置到某个提交状态，无法对指定路径或文件单独执行
git reset --hard HEAD

## 回退未保存的更改
# 将工作区的某个文件回退到上次提交的状态，需注意，这个命令对已经加入暂存区的文件是无效的。也就是回退到已经暂存的状态。
git checkout -- {file}
```

#### 合并分支

**Step 1.** Fetch and check out the branch for this merge request

```
git fetch origin
git checkout -b "rec_parser_for_HigecBus" "origin/rec_parser_for_HigecBus"
```

**Step 2.** Review the changes locally

**Step 3.** Merge the branch and fix any conflicts that come up

```
git fetch origin
git checkout "origin/master"
git merge --no-ff "rec_parser_for_HigecBus"
```

**Step 4.** Push the result of the merge to GitLab

```
git push origin "master"
```

**Tip:** You can also checkout merge requests locally by [following these guidelines](https://gitlab.senseauto.com/help/user/project/merge_requests/index.md#checkout-merge-requests-locally).

#### 删除远端的提交（危险慎用）

```shell
git reset --hard HEAD~1 #到某一个提交的状态
git push --force # 注意需要解除protect，并且需要清楚自己在做什么)
```

#### 强制移动分支HEAD

```
git branch -f <branch_name> <target_commit>
```

#### 修改作者

```
git commit --amend --author="liuxinhao <liuxinhao@senseauto.com>"
```

#### cherry-pick一个merge提交

```
git cherry-pick <commit-id> -m 1
```

#### 修改远程仓库地址

```shell
git clone xxx_a.git
cd xxx_a
git remote set-url origin xxx_b.git
git push origin
# 推送所有分支
git push origin '*:*'
```

