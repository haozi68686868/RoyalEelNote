官方文档：https://zguide.zeromq.org/

一、ZeroMQ简述

ZeroMQ是一种基于消息队列的多线程网络库，其对套接字类型、连接处理、帧、甚至路由的底层细节进行抽象，提供跨越多种传输协议的套接字。引用云风的话来说:ZeroMQ 并不是一个对 socket 的封装，不能用它去实现已有的网络协议。它有自己的模式，不同于更底层的点对点通讯模式。它有比 tcp 协议更高一级的协议。（当然 ZeroMQ 不一定基于 TCP 协议，它也可以用于进程间和进程内通讯）它改变了通讯都基于一对一的连接这个假设。ZeroMQ 把通讯的需求看成四类。其中一类是一对一结对通讯，用来支持传统的 TCP socket 模型，但并不推荐使用。常用的通讯模式只有三类：

> 请求回应模型。由请求端发起请求，并等待回应端回应请求。从请求端来看，一定是一对对收发配对的；反之，在回应端一定是发收对。请求端和回应端都可以是 1:N 的模型。通常把 1 认为是 server ，N 认为是 Client 。ZeroMQ 可以很好的支持路由功能（实现路由功能的组件叫作 Device），把 1:N 扩展为 N:M （只需要加入若干路由节点）。从这个模型看，更底层的端点地址是对上层隐藏的。每个请求都隐含有回应地址，而应用则不关心它。
>
> 发布订阅模型。这个模型里，发布端是单向只发送数据的，且不关心是否把全部的信息都发送给订阅端。如果发布端开始发布信息的时候，订阅端尚未连接上来，这些信息直接丢弃。不过一旦订阅端连接上来，中间会保证没有信息丢失。同样，订阅端则只负责接收，而不能反馈。如果发布端和订阅端需要交互（比如要确认订阅者是否已经连接上），则使用额外的 socket 采用请求回应模型满足这个需求。
>
> 管道模型。这个模型里，管道是单向的，从 PUSH 端单向的向 PULL 端单向的推送数据流。

------

二、案例

请求回应模型

###### cli.cpp

```text
#include <zmq.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>

int main(void)
{
    printf("Connecting to server...\n");

    void * context = zmq_ctx_new();
    void * socket = zmq_socket(context, ZMQ_REQ);
    zmq_connect(socket, "tcp://localhost:6666");

    while(1)
    {
        char buffer[10];
        const char * requestMsg = "Hello";
        int bytes = zmq_send(socket, requestMsg, strlen(requestMsg), 0);
        printf("[Client][%d] Sended Request Message: %d bytes, content == \"%s\"\n", i, bytes, requestMsg);

        bytes = zmq_recv(socket, buffer, 10, 0);
        buffer[bytes] = '\0';
        printf("[Client][%d] Received Reply Message: %d bytes, content == \"%s\"\n", i, bytes, buffer);

    }

    zmq_close(socket);
    zmq_ctx_destroy(context);

    return 0;
}
```

###### ser.cpp

```text
#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>

int main(void)
{
    void * context = zmq_ctx_new();
    void * socket = zmq_socket(context, ZMQ_REP);
    zmq_bind(socket, "tcp://*:6666");

    while(1)
    {
        char buffer[10];
        int bytes = zmq_recv(socket, buffer, 10, 0);
        buffer[bytes] = '\0';
        printf("[Server] Recevied Request Message: %d bytes, content == \"%s\"\n", bytes, buffer);

        sleep(1);

        const char * replyMsg = "World";
        bytes = zmq_send(socket, replyMsg, strlen(replyMsg), 0);
        printf("[Server] Sended Reply Message: %d bytes, content == \"%s\"\n", bytes, replyMsg);
    }

    zmq_close(socket);
    zmq_ctx_destroy(context);

    return 0;
}
```

makefile

```
all: cli ser

cli:cli.cpp
g++ -std=c++11 cli.cpp -o cli -lzmq -lpthread -g

ser:ser.cpp
g++ -std=c++11 ser.cpp -o ser -lzmq -lpthread -g

clean:
rm -f ser cli
```



三、流程步骤

请求回应模型

服务端：

```
zmq_ctx_new()
zmq_socket()
zmq_bind()
zmq_recv()
zmq_send()
```

客户端：

```
zmq_ctx_new()
zmq_socket()
zmq_bind()
zmq_send()
zmq_recv()
```

源码走读

1.zmq_ctx_new()

```
//返回ctx_t对象
void *zmq_ctx_new (void)
{
// We do this before the ctx constructor since its embedded mailbox_t
// object needs the network to be up and running (at least on Windows).
if (!zmq::initialize_network ()) {
return NULL;
}

// Create 0MQ context.
zmq::ctx_t *ctx = new (std::nothrow) zmq::ctx_t;
if (ctx) {
if (!ctx->valid ()) {
delete ctx;
return NULL;
}
}
return ctx;
}
```



------

函数返回context（上下文），其实调用的是ctx_t对象（实例化）

```
zmq::ctx_t::ctx_t () :
_tag (ZMQ_CTX_TAG_VALUE_GOOD),
_starting (true),
_terminating (false),
_reaper (NULL),
_max_sockets (clipped_maxsocket (ZMQ_MAX_SOCKETS_DFLT)),
_max_msgsz (INT_MAX),
_io_thread_count (ZMQ_IO_THREADS_DFLT),
_blocky (true),
_ipv6 (false),
_zero_copy (true)
{
\#ifdef HAVE_FORK
_pid = getpid ();
\#endif
\#ifdef ZMQ_HAVE_VMCI
_vmci_fd = -1;
_vmci_family = -1;
\#endif

// Initialise crypto library, if needed.
zmq::random_open ();

\#ifdef ZMQ_USE_NSS
NSS_NoDB_Init (NULL);
\#endif

\#ifdef ZMQ_USE_GNUTLS
gnutls_global_init ();
\#endif
}
```

主要就是设置初始化的参数；如;_max_sockets = 1024;_io_thread_count = 1;当然还有一些状态设置等等；

------

2.zmq_socket()

```
void *zmq_socket (void *ctx_, int type_)
{
//对象为NULL，则返回
if (!ctx_ || !(static_cast<zmq::ctx_t *> (ctx_))->check_tag ()) {
errno = EFAULT;
return NULL;
}
//强转
zmq::ctx_t *ctx = static_cast<zmq::ctx_t *> (ctx_);
zmq::socket_base_t *s = ctx->create_socket (type_);
return (void *) s;
}
```

参数：

```
void *ctx_；zmq_ctx_new返回的上下文参数；

int type_:Socket types.

Socket types：

ZMQ_PAIR 0
ZMQ_PUB 1
ZMQ_SUB 2
ZMQ_REQ 3
ZMQ_REP 4
ZMQ_DEALER 5
ZMQ_ROUTER 6
ZMQ_PULL 7
ZMQ_PUSH 8
ZMQ_XPUB 9
ZMQ_XSUB 10
ZMQ_STREAM 11
```



返回值：创建生成的socket

------

调用create_socket()

```
zmq::socket_base_t *zmq::ctx_t::create_socket (int type_)
{
scoped_lock_t locker (_slot_sync);
//初始化邮箱数组,增加两个插槽(slots),
//zmq_ctx_term thread 和 reaper thread
if (unlikely (_starting)) {
if (!start ())
return NULL;
}

// Once zmq_ctx_term() was called, we can't create new sockets.
if (_terminating) {
errno = ETERM;
return NULL;
}

// If max_sockets limit was reached, return error.
if (_empty_slots.empty ()) {
errno = EMFILE;
return NULL;
}

// Choose a slot for the socket.
uint32_t slot = _empty_slots.back ();
_empty_slots.pop_back ();

// Generate new unique socket ID.
//生成新的唯一的套接字ID。
int sid = (static_cast<int> (max_socket_id.add (1))) + 1;

// Create the socket and register its mailbox.
//创建socket并且注册邮箱
socket_base_t *s = socket_base_t::create (type_, this, slot, sid);
if (!s) {
_empty_slots.push_back (slot);
return NULL;
}
_sockets.push_back (s);
_slots[slot] = s->get_mailbox ();

return s;
}
```



------

调用start ()函数:



```
bool zmq::ctx_t::start ()
{
// Initialise the array of mailboxes. Additional two slots are for
// zmq_ctx_term thread and reaper thread.
_opt_sync.lock ();
const int term_and_reaper_threads_count = 2;
const int mazmq = _max_sockets; //1023
const int ios = _io_thread_count;//1
_opt_sync.unlock ();
int slot_count = mazmq + ios + term_and_reaper_threads_count;//1026
try {
//增加容量,不创建对象
_slots.reserve (slot_count);
_empty_slots.reserve (slot_count - term_and_reaper_threads_count);
}
catch (const std::bad_alloc &) {
errno = ENOMEM;
return false;
}
//改变了容器的大小，且创建了容器中的对象
_slots.resize (term_and_reaper_threads_count);

// Initialise the infrastructure for zmq_ctx_term thread.
_slots[term_tid] = &_term_mailbox;

//创建线程
_reaper = new (std::nothrow) reaper_t (this, reaper_tid);
if (!_reaper) {
errno = ENOMEM;
goto fail_cleanup_slots;
}
if (!_reaper->get_mailbox ()->valid ())
goto fail_cleanup_reaper;
_slots[reaper_tid] = _reaper->get_mailbox ();
_reaper->start ();

// Create I/O thread objects and launch them.
_slots.resize (slot_count, NULL);
//创建IO线程并启动
for (int i = term_and_reaper_threads_count;
i != ios + term_and_reaper_threads_count; i++) {
io_thread_t *io_thread = new (std::nothrow) io_thread_t (this, i);
if (!io_thread) {
errno = ENOMEM;
goto fail_cleanup_reaper;
}
if (!io_thread->get_mailbox ()->valid ()) {
delete io_thread;
goto fail_cleanup_reaper;
}
_io_threads.push_back (io_thread);
_slots[i] = io_thread->get_mailbox ();
io_thread->start ();
}

// In the unused part of the slot array, create a list of empty slots.
for (int32_t i = static_cast<int32_t> (_slots.size ()) - 1;
i >= static_cast<int32_t> (ios) + term_and_reaper_threads_count; i--) {
_empty_slots.push_back (i);
}

_starting = false;
return true;

fail_cleanup_reaper:
_reaper->stop ();
delete _reaper;
_reaper = NULL;

fail_cleanup_slots:
_slots.clear ();
return false;
}
```

ZMQ从入门到掌握<三>

------

订阅-发布模式

ZeroMQ的订阅发布模式是一种单向的数据发布，当客户端向服务端订阅消息之后，服务端便会将产生的消息源源不断的推送给订阅者



特点：



> 1.一个发布者，多个订阅者的关系，1：n；
> 2.当发布者数据变化时发布数据，所有订阅者均能够接收到数据并处理。
> 这就是发布/订阅模式。
>
> 注：使用SUB设置一个订阅时，必须使用zmq_setsockopt()对消息进行过滤，例如：



说明：发布者使用PUB套接字将消息发送到队列中，订阅者使用SUB套接字从队列中源源不断的接收消息。新的订阅者可以随时加入，但之前的消息是无法接收到的；已有的订阅者可以随时退出；订阅者还可以添加“过滤器”用来有选择性的接收消息。

------

图例：

![img](https://pic1.zhimg.com/80/v2-d8e39c2d13e3c68767778979323cda28_720w.jpg)

![img](https://pic1.zhimg.com/80/v2-dc828f8b16f329fb0aa6d105461d5e90_720w.jpg)

------

案例代码：

###### pub.cpp

```
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <assert.h>
#include <string.h>
#include "zmq.h"

int main()
{
void* context = zmq_ctx_new();
assert(context != NULL);

void* socket = zmq_socket(context, ZMQ_PUB);
assert(socket != NULL);

int ret = zmq_bind(socket, "tcp://*:5555");
assert(ret == 0);

int i = 0;
while(1)
{
char szBuf[1024] = {0};
snprintf(szBuf, sizeof(szBuf), "server i=%d", i);
ret = zmq_send(socket, szBuf, strlen(szBuf) + 1, 0);
i++;

//sleep(1);
}

zmq_close (socket);
zmq_ctx_destroy (context);

return 0;
}
```



###### sub.cpp

```
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <assert.h>
#include "zmq.h"
#include <thread>

using namespace std;

#define TRUE 1

void Recv(void* arg)
{
while(TRUE)
{
void* socket = arg;
printf("into while\n");
char szBuf[1024] = {0};
int ret = zmq_recv(socket, szBuf, sizeof(szBuf) - 1, 0);
if (ret > 0)
{
printf("Recv:%s\n", szBuf);
}
}
}


void Recv2(void* arg)
{
while(TRUE)
{
void* socket = arg;
printf("into while\n");
char szBuf[1024] = {0};
int ret = zmq_recv(socket, szBuf, sizeof(szBuf) - 1, 0);
if (ret > 0)
{
printf("Recv2:%s\n", szBuf);
}
}
}

int main()
{
printf("Hello world!\n");

void* context = zmq_ctx_new();
assert(context != NULL);

void* socket = zmq_socket(context, ZMQ_SUB);
assert(socket != NULL);

int ret = zmq_connect(socket, "tcp://localhost:5555");
assert(ret == 0);

ret = zmq_setsockopt(socket, ZMQ_SUBSCRIBE, "", 0);
assert(ret == 0);
thread t1(Recv,socket);
thread t2(Recv2,socket);
/*
while(1)
{
printf("into while\n");
char szBuf[1024] = {0};
ret = zmq_recv(socket, szBuf, sizeof(szBuf) - 1, 0);
if (ret > 0)
{
printf("%s\n", szBuf);
}
}
*/
t1.join();
t2.join();
zmq_close(socket);
zmq_ctx_destroy(context);

return 0;
}
```

makefile

```
all:pub sub

CXX=g++
CXXFLAGS=-fPIC -std=c++11 -o
LDFLAGS=-lzmq -lpthread

pub:pub.cpp
$(CXX) pub.cpp $(CXXFLAGS) pub $(LDFLAGS)

sub:sub.cpp
$(CXX) sub.cpp $(CXXFLAGS) sub $(LDFLAGS)
clean:
rm -f sub pub
```

推拉模式

> 推拉模式，PUSH发送，send。PULL方接收，recv。PUSH可以和多个PULL建立连接，PUSH发送的数据被顺序发送给PULL方。比如你PUSH和三个PULL建立连接，分别是A,B,C。PUSH发送的第一数据会给A,第二数据会给B，第三个数据给C，第四个数据给A。一直这么循环。

------

看一下图：

![img](https://pic1.zhimg.com/80/v2-d8e39c2d13e3c68767778979323cda28_720w.jpg)

------



> 最上面是产生任务的 分发者 ventilator
> 中间是执行者 worker
> 下面是收集结果的接收者 sink

代码：



Ventilator.cpp



```text
#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
 
int main(void)
{
    void * context = zmq_ctx_new();
    void * sender = zmq_socket(context, ZMQ_PUSH);
    zmq_bind(sender, "tcp://*:6666");
	printf ("Press Enter when the workers are ready: ");
    getchar ();
	printf ("Sending tasks to workers...\n");
    while(1)
    { 
        const char * replyMsg = "World";
        zmq_send(sender, replyMsg, strlen(replyMsg), 0);
        printf("[Server] Sended Reply Message content == \"%s\"\n", replyMsg);
    }
 
    zmq_close(sender);
    zmq_ctx_destroy(context);
 
    return 0;
}
```

------

work.cpp



```
#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>

int main(void)
{
void * context = zmq_ctx_new();
void * recviver = zmq_socket(context, ZMQ_PULL);
zmq_connect(recviver, "tcp://localhost:6666");

void * sender = zmq_socket(context, ZMQ_PUSH);
zmq_connect(sender, "tcp://localhost:5555");

while(1)
{ 
char buffer [256];
int size = zmq_recv (recviver, buffer, 255, 0);
if(size < 0)
{
return -1;
}
printf("buffer:%s\n",buffer);
const char * replyMsg = "World";
zmq_send(sender, replyMsg, strlen(replyMsg), 0);
printf("[Server] Sended Reply Message content == \"%s\"\n", replyMsg);
}

zmq_close(recviver);
zmq_close(sender);
zmq_ctx_destroy(context);

return 0;
}
```



------



sink.cpp



```text
#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>
 
int main(void)
{
    void * context = zmq_ctx_new();
    void * socket = zmq_socket(context, ZMQ_PULL);
    zmq_bind(socket, "tcp://*:5555");
 
    while(1)
    { 
       	char buffer [256];
		int size = zmq_recv (socket, buffer, 255, 0);
		if(size < 0)
		{
			return -1;
		}
        printf("buffer:%s\n",buffer);
    }
 
    zmq_close(socket);
    zmq_ctx_destroy(context);
 
    return 0;
}
```

