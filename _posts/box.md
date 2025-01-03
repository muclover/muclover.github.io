---
title: Rust 异步原理
tags: Archive Rust Async
published: false
---

2024-11-07 14:47:45
# Capature
阅读 packt 购买的 [《Asynchronous Programming in Rust: Learn asynchronous programming by building working examples of futures, green threads, and runtimes》](https://subscription.packtpub.com/book/programming/9781805128137/pref/preflvl1sec03/what-this-book-covers)

目录：
- Part I: 异步编程基础
- Part II: 事件队列和绿色线程
- Part III: Rust 中的 Futures 和 async/await

阅读: Rust 生命周期
- lifetime-kaka: https://thinkgos.github.io/lifetimekata/index.html

## Box
**一些异步相关的文章存档：**
https://huangjj27.github.io/async-book/01_getting_started/02_why_async.html | 为什么使用异步？ - Rust 中的异步编程

https://course.rs/advance/async/future-excuting.html | 底层探秘: Future 执行与任务调度 - Rust语言圣经(Rust Course)

https://zhuanlan.zhihu.com/p/611587154 | 16 Rust学习笔记-异步编程(async/await/Future) - 知乎

https://mincodes.com/posts/understanding-async-rust/ | 理解 Rust 异步编程 | MinCodes

https://rustcc.cn/article?id=e6d50145-4bc2-4f1e-84da-c39c8217640b | Rust异步浅谈 - Rust语言中文社区

https://rustmagazine.github.io/rust_magazine_2022/Q1/contribute/async-cancel.html | Rust 异步与取消 - Rust Magazine 2022

https://funkill.github.io/async-book-i18n/zh-cn/async-in-rust/chapter.html | Rust异步编程: 你需要知道的事 - Asynchronous Programming in Rust

https://rustmagazine.github.io/rust_magazine_2021/chapter_10/async-trait.html | Rust Async trait 更新与多线程 - Rust精选

https://nickymeuleman.netlify.app/blog/multithreading-rust | Rust 中的多线程 | Nicky 博客

https://rustcc.cn/article?id=7f326442-401e-4514-ac13-2279a54afc8e | gm-quic - 一款纯rust编写的高效异步 IETF quic传输协议实现 - Rust语言中文社区

https://rust-book.junmajinlong.com/ch100/00.html | Rust异步编程和tokio框架 - Rust入门秘籍

https://www.tisonkun.org/2023/11/05/async-rust/ | Async Rust 的实现 | 夜天之书

https://github.com/wyfcyx/osnotes/blob/master/pl/Rust/future-in-200-lines.md | osnotes/pl/Rust/future-in-200-lines.md at master · wyfcyx/osnotes

https://www.linuxzen.com/understanding-rust-futures-by-going-way-too-deep.html | 【译】深入理解 Rust future

https://fasterthanli.me/articles/understanding-rust-futures-by-going-way-too-deep | 深入理解 Rust Futures

https://os.phil-opp.com/async-await/ | Async/Await | 用Rust编写操作系统

https://medium.com/@tzutoo/rust-async-io-a-beginners-guide-to-asynchronous-programming-in-rust-600219226c82 | Rust Async IO：Rust 异步编程初学者指南 | 作者：tzutoo | Medium



## TCP协议
TCP 是有序传输的，每个数据段都需要一个序号，才能保证在收到乱序的包时，能够重新按顺序组装起来。通过 `Seq` 字段来表示，其增加方式如下：
- 若数据段 1 的起始 Seq 号为 1，长度为 1448，那么数据段 2 的起始 Seq 号为 1+1448=1449，如果数据段 2 的长度也是 1448，那么数据段 3 的起始 Seq 号为 1+1448+1448=2897
- 一个Seq号的大小是根据上一个数据段的Seq号和长度相加而来的
- Seq 号是由发送方来维护的，由于 TCP 是双向连接，所有双方各自维护了一个 Seq 号


Ack：确认号，接受方向发送方确认已经收到了哪些字节
- 比如甲发送了“Seq:x Len:y”的数据段给乙，那乙回复的确认号就是x+y，这意味着它收到了x+y之前的所有字节
- 理论上，接收方回复的Ack号恰好就等于发送方的下一个Seq号
> 累计确认机制：可能发送了多个包，但只回了一个ACK，或者中间的ACK丢失了，只发送了收到了前面所有包的ACK，就可以确保中间的包也被收到了

TCP 的特性：
- 有序性：当包乱序时，接收方只要根据Seq号从小到大重新排列
- 可靠性：有包丢失时，接收方通过前一个Seq+Len的值与下一个Seq的差，就能判断缺了哪些包


例子：from 《Wireshark网络分析就这么简单》

![alt text](/images/box/image-3.png)

1. 收到了乱序的包，重新排序：`Seq:101 Len:100` -> `Seq:301 Len:100` -> `Seq:401 Len:100`
2. 由于第一个包的 `Seq+Len=201`，表示第二个包的 Seq 应该是 201，而实际上收到了 301，因此 201 这个包丢失，回复 `Ack:201` 给发送方让其重传
> 可以回复3个`Ack:201`让发送方快速重传，不需要等超时重传，发送端会重新发送2、3、4号数据包。可以通过SACK来告诉发送端只需要传输201包。并且ACK可以在传送数据时一起发送。

TCP 头的一些 Flag 标志位：
- SYN：表示正在发起连接请求。因为连接是双向的，所以建立连接时，双方都要发一个SYN
- FIN：表示正在请求终止连接。因为连接是双向的，所以彻底关闭一个连接时，双方都要发一个FIN
- RST：用于重置一个混乱的连接，或者拒绝一个无效的请求

TCP如何管理连接：三次握手和四次挥手

三次握手，最开始的3个TCP包
1. 客户端发送请求建立连接，告诉服务器客户端的初始 Seq 是 X
2. 服务器发送 ACK = X+1 表示确定建立连接，并发送初始 Seq Y
3. 客户端发送 ACK = Y+1

![alt text](/images/box/image.png)
> 握手时，Seq 并不是从0开始，需要关闭Wireshark里的Relative Sequence Number(protocols-->TCP里面进行设置)

为什么两个包不行？
- 两个包不够可靠
- 例子：客户端发送第一个请求建立连接，但在网络中阻塞掉，没有到达服务器，然后又发送了第二个请求建立连接。则服务器首先对第二个请求建立了连接。但后续客户端的第一个请求又到达了服务器，服务器不知道这是一个旧的请求，就重新回复建立了连接（这是无效的连接）
- 在三次握手下，客户端收到服务器的回复后，能知道这个连接是否是它想要的连接。如果是，则回复ACK，如果不是，则发送拒绝包，服务器收到ACK表示连接正常建立，收到拒绝包，则放弃连接


四次挥手，4个TCP包
1. 客户端希望断开连接，FIN 标志
2. 服务器表示知道了，断开连接
3. 服务器表示希望断开自己这边的连接，FIN标志
4. 客户端表示知道了，断开连接

### 窗口

### 重传

### 延迟确认和Nagle算法

## UDP协议
UDP无需连接，所以非常适合DNS查询


## git 相关

新增上游地址:
```bash
git remote add upstream git@xxx.com
git remote update upstream # 更新
git rebase upstream/master
```
> 参考: [git fork开发流程](https://blog.junezhu.top/2018/07/06/git-fork-process.html)
> [git rebase 用法详解与工作原理](https://waynerv.com/posts/git-rebase-intro/)


新增分支，并切换到分支，并推送到远程:
```bash
git checkout -b mybranch
git push --set-upstream origin mybranch
git push origin mybranch:mybranch
```

更改刚刚的commit message:
```bash
git commit --amend # 然后可以修改message

```
- 如果已经提交到远程了，那就需要 `git push --force` 来强制远程和本地保持一致

更改之前的commit message:
```bash
git rebase -i HEAD~3 # 可以对 commit 进行合并，或者选择想要的部分进行修改
```

> 在 gitee 中需要设置全局变量的 user.name 和 user.email，local变量没有用


更换vim作为默认编辑器
```bash
git config --global core.editor /usr/bin/vim
```


## QUIC 协议
QUIC（Quick UDP Internet Connections）协议。
![EMQX 的两种stream操作模式](/images/box/image-1.png)

### bilibili
https://space.bilibili.com/3546759305366493/video



## HTTP2 协议

HTTP2 的特点：
- 二进制
- 首部压缩（HPACK算法）
- 流 stream 的多路复用
    - 解决 HTTP1 中的队头阻塞问题
- 流量控制: 由于多路复用带来的复杂性
- 请求优先级、请求依赖
- 服务器主动推送


### 帧 frame 格式
所有帧都有一个 8 字节的首部，具体格式如下：
![frame](/images/box/image-2.png)




参考资料：
- [HTTP介绍-Daniel](https://doc.yonyoucloud.com/doc/wiki/project/http-2-explained/background.html)


## HTTPS 协议

## DNS 协议

### DoH
[深入理解DNS加密协议：全面对比DNS、DoH、DoT和DoQ](https://some.fylsen.com/posts/comprehensive-comparison-dns-encryption-protocols-doh-dot-doq/)

![对比](/images/box/image-6.png)

- 传统 DNS：使用明文UDP包发送查询
  - `dig example.com A`
- DoH：通过 HTTPS POST/GET 请求查询
  - `https://dns.example.com/dns-query?dns=ABC...`
- DoT：在 TLS 层上传输 DNS 查询
  - `openssl s_client -connect dns.example.com:853`
- DoQ：使用 QUIC 协议传输 DNS 查询
  - `quic-client dns.example.com:784`

**安全特性对比**
![安全特性对比](/images/box/image-7.png)

**基础性能指标**
![性能指标](/images/box/image-8.png)

**不同网络条件下的性能表现**
![不同网络条件下的性能表现](/images/box/image-9.png)

**资源消耗对比**
![资源消耗对比](/images/box/image-10.png)

**场景适用性分析**
![场景适用性分析](/images/box/image-11.png)

**性能要求场景适用性**
![性能要求场景适用性](/images/box/image-12.png)


# 网络是怎么运行的
当你输入一个网址是如何返回一个网页给你的？


IP --> subnet --> NAT --> Ethernet --> broadcast --> ARP --> switch --> router --> AS(Autonomous System)/ISP --> DHCP --> DNS --> TCP/UDP --> HTTPS(TLS/SSL --> HTTP)


在局域网下是如何分配IP地址的，当一个新的设备请求加入局域网时，会发送一个DHCP请求
- 首先为了通过网线获取数据，首先需要知道网址对应 url 的 ip 地址, 通过 DNS 来解析域名为 IP 地址, 假设工作在 IPV4 上

IPV4由32位组成，可以分为4组 A.B.C.D, 每组的取值范围是 0-255。
发送请求需要自己电脑的 ip, 在日常使用的 IP 地址都是处于局域网下, 本机的 IP 通过 DHCP 协议来决定, 每当设备连接到一个新的网络，都发送一个 DHCP 广播请求来寻找可用的DHCP服务器, 然后 DHCP 服务器会给设备提供一个 IP 地址及子网掩码(subnet mask), 在同一个局域网(LAN)下的所有设备的 IP 的网络部分都相同。
> 子网掩码将IP地址分为两部分: 网络 + 主机

通过 DHCP 提供的 IP 是私有 IP(10.0.0.0 - 10.255.255.255, 172.16.0.0 - 172.31.255.255, 192.168.0.0 - 192.168.255.255), 所有具有私有 IP 的设备通过 router 离开局域网时, NAT 会将所有的私有 IP 转换为同一个 public IP 地址来进行网络通信。

![DHCP](/images/box/image-4.png)


在知道通信双方的 IP 地址后，可以开始进行传输了 
应用层:     | Application Data|
传输层:     | TCP Header| Application Data|
网络层:     | IP Header | TCP Header| Application Data|
数据链路层: | Eth Header || IP Header | TCP Header| Application Data| CRC |

在经过数据链路层来通过网线传输数据时，会经过许多个物理设备，每个设备都有自己的 MAC 地址，每个路由器都会拆开以太网帧来查看 IP 包的目标IP地址，确保目标IP不是它自己，然后路由器查看自己的路由表，若目标IP匹配到表中的某个子网，然后路由器就会重新封装IP包，然后将MAC源地址改成自己的地址，MAC目标地址改成下一个路由器的地址，然后发送。

交换机是数据链路层设备，路由器是网络层设备。交换机不会接触IP地址，交换机通常只连接一个局域网内的多台设备，
- 当局域网下的设备要通过ip地址进行通信时，有两种类型(根据子网掩码来判断)：
  - 目的ip地址在局域网内：交换机使用 switch 表，将 MAC 地址映射到端口上，在一个局域网上的设备A想给B发送消息，A通过网线只能发送给交换机，但A不知道B的MAC地址，A会发送一个ARP广播消息来查找B的MAC地址，源地址为A的MAC，目标地址是广播地址，通常是FF::FF::FF::FF::FF::FF，交换机收到含有广播地址的消息后会发送消息到所有端口，保证发送给了局域网的每个设备，每个设备会拆开报文查看ip目标地址是否是自己。然后B返回一个ARP消息给A，交换机会更新自己的switch表，将对应的端口和MAC地址的对应关系保证，A在收到B的ARP回应消息后，再发送消息给B，交换机会直接把消息传出到设备B上。
  - 目的ip地址不在局域网内：直接发送给网关（局域网的出口设备，一般是路由器，在企业里可能是防火墙等含路由功能的设备），然后通过路由来进行传输

![交换机和路由器的区别](/images/box/image-5.png)

> 一个城市的网络由多个路由器集群组成，这些路由器集群构成了一个自治系统 AS，由 ISP 管理和运营。不同的 AS 之间通过边界网关协议来交换路由信息，确保数据包能在成千上万的数据包之间选择最佳路径传输

# Actor/Reactor及多线程

在构造网络服务器时，一种最简单的方法是直接为每个请求分发一个线程来进行响应，但是线程的资源有限，并且线程切换的上下文成本很高，而网络 IO 中主要是为了等待 IO 的到达，而不是处理数据，导致大量线程处于空闲状态，因此多线程模型下服务器无法处理 C10K 问题。

> 为了避免频繁的线程创建，可以利用线程池来避免线程创建/销毁开销，通常的一种模型是单个调度程序在套接字上阻塞以接收新请求，然后将请求转入到有界阻塞队列中，超出队列限制的连接被丢弃。然后线程池轮询有界阻塞队列来分配线程处理其中的请求，但仍然解决不了 C10K 问题

> 在线程模型上，也可以使用多进程模型达成和多线程模型一样的效果，但是线程的资源开销更大，上下文切换成本更大。


## Event-Driven 架构
事件驱动架构将线程和连接分离，事件驱动架构由事件创建者和事件消费者组成。创建者是事件的来源，只知道事件已经发生。消费者是需要知道事件已经发生的实体。

**Reactor 模式是事件驱动架构的一种实现技术**，简单来说是使用一个单线程事件循环阻塞资源发出的事件，并将它们分派给相应的处理程序和回调。

只要注册了事件的处理程序和回调来处理它们，就无需阻塞 I/O。事件指的是新传入连接、准备读取、准备写入等实例。这些处理程序/回调可以在多核环境中使用线程池。

包括两个组成部分
- Reactor: 运行在单独的线程中, 响应 IO 事件, 并分发给实际的处理程序
- 处理程序: 处理程序执行非阻塞操作, 完成具体的任务

Reactor 允许使用单个线程高效地处理多个阻塞任务。Reactor 还管理一组事件处理程序。当调用它执行任务时，它会与可用的处理程序连接并使其处于活动状态。

### 单 Reactor、单线程
抽象出来两个组件
- Reactor: 负责响应IO事件，当检测到一个新的事件，将其发送给相应的Handler去处理；新的事件包含连接建立就绪、读就绪、写就绪等。
- Handler: 将自身（handler）与事件绑定，负责事件的处理，完成channel的读入，完成处理业务逻辑后，负责将结果写出channel。


缺点: 当其中某个 handler 阻塞时，会导致其他所有的client 的 handler 都得不到执行，并且更严重的是，handler 的阻塞也会导致整个服务不能接收新的 client 请求(因为 acceptor 也被阻塞了)。 因为有这么多的缺陷， 因此单线程Reactor 模型用的比较少。这种单线程模型不能充分利用多核资源，所以实际使用的不多。因此，单线程模型仅仅适用于handler 中业务处理组件能快速完成的场景。


### 单 Reactor、多线程

### 多 Reactor、多线程


### Preactor
Preactor 是将 Reactor 中的 IO 换成异步 IO，在 reactor 中等待 IO 事件发生后，需要自己调用回调函数读取数据，而在异步 IO 中读取数据由 OS 完成，只需要负责数据处理

## 同步/异步、阻塞/非阻塞 IO
以一个网络 IO 为例，IO 事件包含两个部分：
1. 数据从网络到内核空间
2. 数据从内核空间拷贝到用户空间
> 同步 IO 和异步 IO 的主要区别在于第 2 点，同步 IO 需要自己去读取数据，而异步 IO 这两个部分的操作都是立刻返回，无需等待
> 阻塞 IO 和非阻塞 IO 的主要区别在于第 1 点，是否需要等待数据到内核空间的这个过程

阻塞IO：需要等待 IO 事件返回后才继续进行处理

非阻塞IO：执行 IO 操作后，立马返回，不需要等待，需要隔一段时间来轮询 IO 事件是否发生

IO 多路复用：是一种特殊的阻塞 IO，但不是阻塞在单个事件上，而是阻塞在 select/poll/epoll 这样的系统调用上，阻塞多个事件上，多个事件中存在 IO 事件发生，则会唤醒线程来处理

> 同步 IO 包括上面 3 种类型

同步IO ：线程发起read操作，调用操作系统,这是会有一次用户态切换到内核态，内核开始等待数据到达，数据完成后，从内核拷贝到用户态空间，这个过程线程是一直等待状态的。

阻塞IO：线程发起read操作，然后线程一直处于等待状态，直到IO操作完成，其实和上面的同步IO一样。

非阻塞IO：线程发起read操作，用户态切换到内核态，如果内核数据没有准备好，立刻返回一个错误，线程根据错误决定每隔一会轮询依次，当内核数据准备好后，会将数据从内核拷贝到用户态空间这个时候线程是一只处于等待状态的，也就是说第一阶段是非阻塞，第二阶段还是阻塞的。

异步IO：线程发起read操作后，便可以做其他事了，操作系统数据准备好后（已经拷贝到用户态）会告诉线程。

## Actor
reactor，proactor这两种模型都是通过共享内存来进行通信，而actor强调的是通过通信来共享内存，actor强调的是没有共享，所有的线程之间都是消息传递来实现通信，数据交互，每一个actor就是一个线程