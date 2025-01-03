# 阻塞、非阻塞、同步、异步
典型的一次 IO 包含两个阶段：
1. 数据准备
2. 数据读写

阻塞和非阻塞：根据系统 IO 的就绪状态判断，也就是数据准备阶段

同步和异步：根据应用程序和内核的交互方式判断，也就是数据读写阶段

> 在Linux 中，阻塞和非阻塞都是同步 IO，异步 IO 需要特殊的 API
> - 包括 select/poll/epoll 都是同步 IO
> - Linux 上的 AIO 才是异步 IO，类似于 Windows 上的 IOCP


```c
ssize_t recv(int sockfd, void *buf, size_t len, int flags);

int size = recv(sockfd, buf, 1024, 0);
// size == -1 发生了内部错误
// size == -1 && errno = EAGAIN (或者 EWOULDBLOCK) 非阻塞返回
// size == 0  网络对端关闭了连接
// size > 0 有数据可读
```
- `sockfd` 默认工作在阻塞模式，若 `sockfd` 没有数据可读，则会使得当前线程阻塞，直到 `sockfd` 有数据到来
- 若函数返回，则有数据读写
- 若设置为非阻塞，则会直接返回，不会造成当前线程阻塞
    - 通过返回值可以返判断是否是非阻塞返回，比如 `EAGAIN`

IO 的同步和异步
- 在操作系统和应用程序之间，当 TCP 接收缓冲区有数据时，然后`recv` 返回后，需要开始读数据，
- 同步：应用程序准备 buf 去持续读数据，线程一直在读数据
    - 需要消耗应用程序的时间
- 异步：对远端发过来的数据，应用程序告诉操作系统有一个buf，让操作系统将远程数据放到buf中，然后在完成后通知应用程序
  - 不需要等待 buf 读取，在操作系统通知应用程序后，buf 已经存储了对端发过来的数据
  - 通知方式：信号、回调函数
  - 读数据不需要消耗应用程序的时间
  - 需要依赖操作系统提供的接口（看OS是否支持）
  - 异步的编程方式更复杂，但效率更高

同步表示 A 向 B 请求调用一个网络 IO 接口时（或业务API），数据的读写都是由请求方 A 自己来完成的（不管是阻塞还是非阻塞）；异步表示 A 向 B 请求调用一个网络 IO 接口时（或业务API），向 B 传入请求的事件以及事件发生时通知的方式后，A 可以去处理其他逻辑，当 B 监听到事件处理完成后，使用约定好的通知方式来通知 A 处理结果
- 同步阻塞
- 同步非阻塞
- 异步阻塞：没有意义
- 异步非阻塞

```c
// 异步接口: aio_read 和 aio_write
int aio_read(struct aiocb *aiocbp);

struct aiocb {
    int aio_fildes;
    off_t aio_offset;
    volatile void *aio_buf;
    size_t aio_nbytes;
    int aio_reqprio;
    struct sigevent aio_sigevent;
    int aio_lio_opcode;
}
```

应用层上的业务指的是并发的同步和异步
- 同步：调用 API 时，需要自己完成数据的读取
  - A 等待 B 做完事情后，得到返回值，继续处理
- 异步：不需要自己完成读取，在完成读取完成后会收到通知
  - A 告诉 B 它感兴趣的事件以及通知方式，A继续执行自己的业务逻辑。等到 B 监听到相应的事件发生后，B 会通知 A，A开始进行相应的数据处理逻辑

Node.js 基于**异步非阻塞**模式下的高性能服务器
- 任何操作都需要传入操作的数据和回调

# Linux 上的 5 种 IO 模型
阻塞 Blocking IO
![BIO](/images/01-hp-box/image.png)

非阻塞 Non-Blocking IO
![NIO](/images/01-hp-box/image-1.png)

IO多路复用
![multiplex](/images/01-hp-box/image-2.png)

信号驱动 IO
![signal](/images/01-hp-box/image-3.png)
- 内核在第一个阶段是异步的过程，第二个阶段是同步的过程
- 提供了消息通知机制，不需要用户进程不断轮询检查数据是否准备好，减少系统调用次数，提升了效率

异步 IO
![AIO](../images/01-hp-box/image-4.png)
# 如何设计网络服务器
多核时代，如何选择线程模型：
- one loop per thread is usually a good model - libev 作者的观点，将多线程服务器编程转换为如何设计一个高效且易于使用的 event loop，然后每个线程运行一个 event loop 即可

event loop 是非阻塞编程的核心，总是和 IO 多路复用一起使用
- 非阻塞，不可能一直轮询
- IO 多路复用，一般不和阻塞 IO 使用，因为阻塞 IO 中的 `read()/write()/accept()/connect()` 都可能阻塞当前线程，线程就没有办法处理其他 socket 上的 IO 事件了。

> epoll + fork 和 epoll + pthread
> - nginx 服务器使用了 epoll + fork 多进程的方式来实现简单好用的负载算法，并且通过引入一把乐观锁解决了该模型下的 **服务器惊群** 问题

# Reactor 模式
> https://en.wikipedia.org/wiki/Reactor_pattern

**重要组件：Event 事件、Reactor 反应堆、Demultiplex 事件分发器、Eventhandler 事件处理器**
![reactor](/images/01-hp-box/image-5.png)

![](/images/01-hp-box/image-6.png)

> https://mirbozorgi.com/understanding-the-reactor-pattern-thread-based-and-event-driven/
> https://dzone.com/articles/understanding-reactor-pattern-thread-based-and-eve
> https://stackoverflow.com/questions/26828181/reactor-design-pattern-in-a-single-thread-vs-multiple-threads
# epoll
select/poll/epoll

## 两种模式
**LT 模式**

**ET 模式**