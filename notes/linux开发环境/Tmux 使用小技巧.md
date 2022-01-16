# Tmux 使用小技巧

##### 使用鼠标

```text
set -g mouse on
```

##### 使用命令行模式

```
ctrl+B : 
```

##### 查找字符串

```shell
# 进入copy mode
ctrl+B [
# 退出copy mode
q/Esc
# 查找字符串
ctrl+s
# 再次搜索
n
# 反向再次搜索
shift+n
```

##### 会话管理

```
tmux new　　创建默认名称的会话（在tmux命令模式使用new命令可实现同样的功能，其他命令同理，后文不再列出tmux终端命令）
tmux new -s mysession　　创建名为mysession的会话
tmux ls　　显示会话列表
tmux a　　连接上一个会话
tmux a -t mysession　　连接指定会话
tmux rename -t s1 s2　　重命名会话s1为s2
tmux kill-session　　关闭上次打开的会话
tmux kill-session -t s1　　关闭会话s1
tmux kill-session -a -t s1　　关闭除s1外的所有会话
tmux kill-server　　关闭所有会话
```

##### 命令行命令

```shell
# 设置键盘模式
set-window-option -g mode-keys emacs/vi/
```

