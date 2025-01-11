# Todo Blog
high: https://www.firezone.dev/blog/sans-io
high: https://predr.ag/blog/breakage-in-the-cargo-toml-how-rust-package-features-work/
high: https://rustmagazine.github.io/rust_magazine_2021/chapter_7/how-we-improved-the-performance-of-our-rust-app.html
high: https://rustmagazine.github.io/rust_magazine_2021/chapter_5/rust-memory-troubleshootting.html
high: https://rustmagazine.github.io/rust_magazine_2021/chapter_9/rethink-async.html
high: https://rustmagazine.github.io/rust_magazine_2021/chapter_1/rust_async.html
https://rustmagazine.github.io/rust_magazine_2021/chapter_12/tokio_part1.html
https://rustmagazine.github.io/rust_magazine_2021/chapter_12/lock-free.html
https://rustmagazine.github.io/rust_magazine_2021/chapter_11/play-async.html
https://rustmagazine.github.io/rust_magazine_2021/chapter_8/reqwest-middleware.html
https://rustmagazine.github.io/rust_magazine_2021/chapter_4/hw_bin_opt.html
https://rustmagazine.github.io/rust_magazine_2021/chapter_4/ant_async_os_opt.html
https://rustmagazine.github.io/rust_magazine_2021/chapter_2/rust_error_handle_and_log.html
https://tony612.github.io/tokio-internals/01.html
https://fractalfir.github.io/generated_html/refl_priv.html

rust 的内存布局视频：https://www.youtube.com/watch?v=7_o-YRxf_cc

Rust组合器选择的网址：https://rustcombinators.com/
- 当你有一个 `Option<T>` 或者 `Result<T,E>`，需要获取 `T` 或者 `E` 时，你应该怎么做

# wsl 上安装 perf
参考使用 bcc：https://massoudasadiblog.blogspot.com/2024/07/ebpf-on-wsl2-kernel-version-6x-ubuntu.html?m=1
参考：https://gist.github.com/abel0b/b1881e41b9e1c4b16d84e5e083c38a13
- https://gist.github.com/MarioHewardt/5759641727aae880b29c8f715ba4d30f
参考bcc的安装文档：https://github.com/iovisor/bcc/blob/master/INSTALL.md#wslwindows-subsystem-for-linux---binary

**bcc的安装**可以参考这个：http://www.aisoftcloud.cn/blog/article/1684117709501802?session=

下面是我本地的 wsl2 版本，安装的是 Ubuntu 22.04
```bash
PS C:\Users\muclo> wsl --version
WSL 版本： 2.3.26.0
内核版本： 5.15.167.4-1
WSLg 版本： 1.0.65
MSRDC 版本： 1.2.5620
Direct3D 版本： 1.611.1-81528511
DXCore 版本： 10.0.26100.1-240331-1435.ge-release
Windows 版本： 10.0.26100.2605
```

通过以下命令来安装 perf
```bash
wsl --update  # 查看自己的内核是否需要更新
sudo apt update
sudo apt install flex bison 
git clone https://github.com/microsoft/WSL2-Linux-Kernel --depth 1
cd WSL2-Linux-Kernel/tools/perf
make -j8 # parallel build
sudo cp perf /usr/local/bin
```
- 在执行 `make -j8` 的时候，会发现本地缺少的包是什么，根据提示来依次安装后，再重新执行 `make`，如下所示：
```bash
Makefile.config:471: No libdw DWARF unwind found, Please install elfutils-devel/libdw-dev >= 0.158 and/or set LIBDW_DIR
Makefile.config:476: No libdw.h found or old libdw.h found or elfutils is older than 0.138, disables dwarf support. Please install new elfutils-devel/libdw-dev
Makefile.config:597: No sys/sdt.h found, no SDT events are defined, please install systemtap-sdt-devel or systemtap-sdt-dev
Makefile.config:645: No libunwind found. Please install libunwind-dev[el] >= 1.1 and/or set LIBUNWIND_DIR
Makefile.config:688: Disabling post unwind, no support found.
Makefile.config:768: slang not found, disables TUI support. Please install slang-devel, libslang-dev or libslang2-dev
Makefile.config:815: Missing perl devel files. Disabling perl scripting support, please install perl-ExtUtils-Embed/libperl-dev
Makefile.config:965: No liblzma found, disables xz kernel module decompression, please install xz-devel/liblzma-dev
Makefile.config:978: No libzstd found, disables trace compression, please install libzstd-dev[el] and/or set LIBZSTD_DIR
Makefile.config:989: No libcap found, disables capability support, please install libcap-devel/libcap-dev
Makefile.config:1002: No numa.h found, disables 'perf bench numa mem' benchmark, please install numactl-devel/libnuma-devel/libnuma-dev
Makefile.config:1061: No libbabeltrace found, disables 'perf data' CTF format support, please install libbabeltrace-dev[el]/libbabeltrace-ctf-dev
Makefile.config:1095: No alternatives command found, you need to set JDIR= to point to the root of your Java directory

Auto-detecting system features:
...                                   dwarf: [ OFF ]
...                      dwarf_getlocations: [ OFF ]
...                                   glibc: [ on  ]
...                                  libbfd: [ OFF ]
...                          libbfd-buildid: [ OFF ]
...                                  libcap: [ OFF ]
...                                  libelf: [ on  ]
...                                 libnuma: [ OFF ]
...                  numa_num_possible_cpus: [ OFF ]
...                                 libperl: [ OFF ]
...                               libpython: [ on  ]
...                               libcrypto: [ on  ]
...                               libunwind: [ OFF ]
...                      libdw-dwarf-unwind: [ OFF ]
...                                    zlib: [ on  ]
...                                    lzma: [ OFF ]
...                               get_cpuid: [ on  ]
...                                     bpf: [ on  ]
...                                  libaio: [ on  ]
...                                 libzstd: [ OFF ]
```
一个不完全的清单可能如下，具体的根据上述提示来安装：
```bash
sudo apt install python-dev-is-python3 libtraceevent-dev libcap-dev \
binutils-dev libnuma-dev libunwind-dev libdw-dev libslang2-dev systemtap-sdt-dev liblzma-dev libzstd-dev libbabeltrace-dev
```

注意事项：
- 在使用 `make -j8` 编译的时候，需要注意你现在的环境，如果处于 conda 环境下，那么使用的 python 版本也会是 conda 下的，因此可能会找不到对应的 libpythonxx.so 文件。
- 需要使用 `conda deactivate` 退出虚拟环境后才能使用本地下的环境进行安装
```bash
# conda 常用命令
conda-env list # 查看已有虚拟环境
which python # 看使用的 python 是哪里的
conda create -n test_env python=3.10 # 使用 python3.10 创建 test_enc 环境
conda remove -n test_env --all # 删除虚拟环境
conda activate test_env # 激活环境，进不去的话可以尝试 source activate test_env
```

# Rust 性能分析
因为常见的性能瓶颈一般都是两类，CPU 和 I/O 。所以工具也基本面向这两类。
## on-cpu 分析
- cargo-flamegraph
- perf

可以通过 Frame Pointer 和 DWARF 两种方式拿到函数的调用栈，默认是不启用的，通过下列方式启用 Frame Pointer
```bash
RUSTFLAGS="-C force-frame-pointers=yes" cargo build --release
```
> 因为Frame Pointer的保存和恢复需要引入额外的指令从而带来性能开销，所以Rust编译器，gcc编译器默认都是不会加入Frame Pointer的信息，需要通过编译选项来开启。

### Frame Pointer
Frame Pointer是基于标记栈基址 EBP 的方式来获取函数调用栈的信息，通过 EBP 我们就可以拿到函数栈帧的信息，包括局部变量地址，函数参数的地址等。
在做 CPU profiling 的过程中，Frame Pointer 帮助进行函数调用栈的展开，具体原理是编译器会在每个函数入口加入如下的指令以记录调用函数的 EBP 的值
```
push ebp
mov	ebp, esp
sub	esp, N
```
并在函数结尾的时候加入如下指令以恢复调用函数的EBP
```
mov	esp, ebp
pop	ebp
ret
```

通过这种方式整个函数调用栈像一个被 EBP 串起来的链表，如下图所示:
![alt text](/images/01-hp-box/image-7.png)

通过 EBP 调试程序就可以拿到完整的调用栈信息，进而进行调用栈展开。

### perf
最简单的使用方式：
```bash
# 在 Cargo.toml 加入
[profile.release]
debug = true

# 执行
cargo build --release
perf record -g target/release/perf-test
perf report
```


### 火焰图
利用 perf 生成火焰图：
```bash
git clone https://github.com/brendangregg/FlameGraph
cd FlameGraph
sudo perf record --call-graph=dwarf mytest
sudo perf script | ./stackcollapse-perf.pl > out.perf-folded
./flamegraph.pl out.perf-folded > perf.svg
```

火焰图的纵轴代表了函数调用栈，横轴代表了占用CPU资源的比例，跨度越大代表占用的CPU资源越多，从火焰图中我们可以更直观的看到程序中CPU资源的占用情况以及函数的调用关系。


> 还可以使用 [cargo-flamegraph](https://crates.io/crates/flamegraph) 生成火焰图，但是对于异步 Async 代码来说，火焰图的效果不好，因为异步调度器和执行器几乎会出现在火焰图中每一块地方，看不出瓶颈所在。这个时候使用 perf 工具会更加清晰。

## off-cpu 分析
Off-CPU 是指在 I/O、锁、计时器、分页/交换等被阻塞的同时等待的时间。

Off-CPU 的性能剖析通常可以在程序运行过程中进行采用链路跟踪来进行分析。还有就是使用 offcpu 火焰图进行可视化观察。

这里推荐的工具是 eBPF 的前端工具包 bcc 中的 offcputime-bpfcc 工具。
这个工具的原理是在每一次内核调用finish_task_switch()函数完成任务切换的时候记录上一个进程被调度离开CPU的时间戳和当前进程被调度到CPU的时间戳，那么一个进程离开CPU到下一次进入CPU的时间差即为Off-CPU的时间。

需要使用debug编译，因为offcputime-bpfcc依赖于frame pointer来进行栈展开，所以我们需要开启RUSTFLAGS="-C force-frame-pointers=yes"的编译选项以便打印出用户态的函数栈。我们使用如下的命令获取Off-CPU的分析数据。
```bash
./target/debug/mytest & sudo offcputime-bpfcc -p `pgrep -nx mytest` 5
```

然后使用 火焰图工具将其生成 off-cpu 火焰图：
```bash
git clone https://github.com/brendangregg/FlameGraph
cd FlameGraph
sudo offcputime-bpfcc -df -p `pgrep -nx mytest` 3 > out.stacks
./flamegraph.pl --color=io --title="Off-CPU Time Flame Graph" --countname=us < out.stacks > out.svg
```
与On-CPU的火焰图相同，纵轴代表了函数调用栈，横轴代表了Off-CPU时间的比例，跨度越大代表Off-CPU的时间越长。



## 检查内存泄漏和不必要的内存分配
可以使用 [Valgrind](https://www.valgrind.org/) 工具来检查程序是否存在内存泄露，或者在关键的调用路径上存在不必要的内存分配。

有一个非常有用的 Rust 编译标志（仅在 Rust nightly 中可用）来验证数据结构有多大及其缓存对齐。
```bash
RUSTFLAGS=-Zprint-type-sizes cargo build --release
```
除了通常的 Cargo 输出之外，包括异步 Future 在内的每个数据结构都以相应的大小和缓存对齐方式打印出来。比如：
```rust
print-type-size type: `net::protocol::proto::msg::Data`: 304 bytes, alignment: 8 bytes
print-type-size     field `.key`: 40 bytes
print-type-size     field `.data_info`: 168 bytes
print-type-size     field `.payload`: 96 bytes
```
Rust 异步编程非常依赖栈空间，异步运行时和库需要把所有东西放到栈上来保证执行的正确性。
如果你的异步程序占用了过多的栈空间，可以考虑将其进行优化为**平衡的同步和异步代码组合**，把特定的异步代码隔离出来也是一种优化手段。


## 其他适合 Rust 性能剖析的工具介绍
除了 perf 和 火焰图 工具，下面还有一些 Rust 程序适用的工具。

Hotspot和Firefox Profiler是查看perf记录的数据的好工具。
Cachegrind和Callgrind给出了全局的、每个函数的、每个源线的指令数以及模拟的缓存和分支预测数据。
DHAT可以很好的找到代码中哪些部分会造成大量的分配，并对峰值内存使用情况进行深入了解。
heaptrack是另一个堆分析工具。
counts支持即席（Ad Hoc）剖析，它将eprintln！语句的使用与基于频率的后处理结合起来，这对于了解代码中特定领域的部分内容很有帮助。
Coz执行因果分析以衡量优化潜力。它通过coz-rs支持Rust。因果分析技术可以找到程序的瓶颈并显示对其进行优化的效果。

参考：
- https://rustmagazine.github.io/rust_magazine_2021/chapter_11/rust-profiling.html
- https://github.com/iovisor/bcc
- https://rustmagazine.github.io/rust_magazine_2021/chapter_12/rust-perf.html


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