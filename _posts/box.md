---
title: Rust 异步原理
tags: Archive Rust Async
published: false
---

2024-11-07 14:47:45
# Box
## TCP协议
TCP 是有序传输的，每个数据段都需要一个序号，才能保证在收到乱序的包时，能够重新按顺序组装起来。通过 `Seq` 字段来表示，其增加方式如下：
- 若数据段 1 的起始 Seq 号为 1，长度为 1448，那么数据段 2 的起始 Seq 号为 1+1448=1449，如果数据段 2 的长度也是 1448，那么数据段 3 的起始 Seq 号为 1+1448+1448=2897
- 一个Seq号的大小是根据上一个数据段的Seq号和长度相加而来的
- Seq 号是由发送方来维护的，由于 TCP 是双向连接，所有双方各自维护了一个 Seq 号

![alt text](./attachments/image.png)


Ack：确认号，接受方向发送方确认已经收到了哪些字节
- 比如甲发送了“Seq:x Len:y”的数据段给乙，那乙回复的确认号就是x+y，这意味着它收到了x+y之前的所有字节
- 理论上，接收方回复的Ack号恰好就等于发送方的下一个Seq号
> 累计确认机制：可能发送了多个包，但只回了一个ACK，或者中间的ACK丢失了，只发送了收到了前面所有包的ACK，就可以确保中间的包也被收到了

TCP 的特性：
- 有序性：当包乱序时，接收方只要根据Seq号从小到大重新排列
- 可靠性：有包丢失时，接收方通过前一个Seq+Len的值与下一个Seq的差，就能判断缺了哪些包


例子：from 《Wireshark网络分析就这么简单》

![alt text](./attachments/tcp-example.png)

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

![alt text](./attachments/tcp-three-handshark.png)
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
