# Box 记录
将 python3 设置为默认版本 https://www.cnblogs.com/slyu/p/13362005.html

gzip 命令
```bash
# 压缩生成 .gz 文件
gzip file
# 压缩文件夹
gzip -r directory
# 解压缩 .gz 文件
gzip -d
# gzip递归解压缩给定目录中的所有文件
gzip -l directory
# 显示有关给定压缩文件的统计信息
# 输出将包括未压缩的文件名、压缩和未压缩的大小以及压缩率
gzip -l filename

```
# 如何对待事务性的、琐碎的工作
1. 摆正心态：工作就是工作，完成分配的任务，就是你的目的，不要产生对抗性情绪。工作不是学习，不能期待所有工作内容都能得到成长。
2. 不出错 + 高效率：不出错（多问多看） --> 提高效率（寻找改进点、改进建议）
3. 建立系统性思维：寻找琐碎的工作处于业务的位置，定位是什么？加深自己的理解
4. 不要忘记主线任务：始终要保证对核心产出投入足够的时间和精力，做出自己有亮点的地方
5. 适当拒绝：学会沟通

# http 自动解压缩
libcurl: 客户端可以通过 `Accept-Encoding` 来告诉服务器，它支持的压缩算法
- deflate（zlib 算法）
- gzip
- br
- zstd (reqwest支持)

服务器根据 `Accept-Encoding` 来选择一种压缩算法来进行数据的压缩，然后在响应头 `Content-Encoding` 里指示使用了什么压缩算法。

libcurl 接口支持：
```c
curl_easy_setopt(curl, CURLOPT_ACCEPT_ENCODING, string);
```
- 只能支持 deflate, gzip, zstd，br 这些 Content-Encoding
- 若 string 是 NULL，则不会产生 `Accept-Encoding`
- 若 string 长度为 0, 则 `Accept-Encoding` 会包含所有支持的压缩算法

支持通用和 **chunked** 传输，deflate 和 gzip 需要 zlib 库，br 需要 brotli 解码库，zstd 需要 libzstd库

curl 需要使用 `--compressed` 来支持自动解压缩
## Std 中的宏
测试宏:
- `assert`
- `assert_eq`
- `assert_ne`

编译期 falg 布尔值计算、features:
- `cfg`

调试、打印
- `print`
- `println`
- `dbg`
- `debug_assert`
- `debug_assert_eq`
- `debug_assert_ne`
- `eprint`
- `eprintln`
- `line`
- `column`
- `file`

字符串
- `format`
- `format_args`
- `stringify`
- `concat`

标记
- `todo`
- `unimplemented`
- `unreachable`
- `panic`
- `compile_error`

判断
- `matches`

向量
- `vec`

输入输出 IO
- `write`
- `writeln`
## std 中的时间模块
结构体：
- Duration：表示一段时间，包括整数部分和小数部分，分别表示秒和纳秒
- Instant: 在不同平台中使用不同的系统调用来获取当前时间，单调非递减的绝对时间值
- SystemTime: 系统时钟
- SystemTimeError
- TryFromFloatSecsError 

```rust
use std::time::{Duration, Instant}

fn main() {
    let five_seconds = Duration::new(5, 0);
    let ten_millis = Duration::from_millis(10);

    let now = Instant::now();
    std::thread::sleep(Duration::new(2, 0)); // sleep 2 seconds
    println!("{}", now.elapsed().as_secs()); // print 2
}
```

常量：UNIX_EPOCH，绝对时间锚定值，此常量在所有系统上均定义为 “1970-01-01 00:00:00 UTC”。
```rust
use std::time::{SystemTime, UNIX_EPOCH};

fn main() {
    match SystemTime::now().duration_since(UNIX_EPOCH) {
        Ok(n) => println!("1970-01-01 00:00:00 UTC was {} seconds ago!", n.as_secs()),
        Err(_) => panic!("SystemTime before UNIX EPOCH!"),
    }
}
```
## Std 中的 IO 模块
定义核心 io 功能的 trait、工具函数、类型。最核心的部分是 `Read` 和 `Write` trait，提供通用接口来读取/写入 IO。
- 一些实现了 `Read` 和 `Write` 的类型：`File`、`TcpStream`、可能有 `Vec<T>`
- `Read`：添加了 `read` 方法
- `Write`：添加了 `write` 方法

> 实现了 `Read` trait 的类型称为 reader，实现了 `Write` trait 的类型称为 `writer`。

`Seek` 和 `BufRead` 是 reader 来控制如何去读取 IO 而使用的 trait。
- `Seek`：控制下一个字节来自哪里
- `BufRead`：使用内部缓冲区来提供其他一系列的读取方式

基于字节的接口通常是不高效且不实用，因为每次使用都需要进行系统调用。`std::io` 提供了两个结构体 `BufReader` 和 `BufWriter` 来进行更高效的操作，封装了 reader 和 write，使用 buffer 来减少调用的次数，并提供更好的方法来访问IO
- 使用 `BufReader` 和 `BufRead` trait 来提供额外的方法
- 而 `BufWriter` 不添加额外的方法，只提供缓冲功能（buffer 会 flushed 刷新，从缓冲到真正的IO处）

```rust
use std::io; use std::io::prelude::*; use std::io::BufReader; use std::fs::File;
fn main() -> io::Result<()> {
    let f = File::open("foo.txt")?;
    let mut reader = BufReader::new(f);
    let mut buffer = String::new();
    reader.read_line(&mut buffer)?;     // read a line into buffer
    println!("{}", buffer);
    Ok(());
}
```

有迭代器类型，如 `Lines`，还有很多其他的功能函数，如 `io::copy`

`io::Result` IO 中的错误类型。

**结构体**
- `BufReader<R>`：`R` 是一个泛型，表示一个 reader，为 reader 提供带有 buffer 的结构
    - 直接使用 `Read` trait效率很低（每次使用调用都会导致系统调用）
    - `BufReader` 能提高对同一文件/网络socket进行小规模和重复读取的速度，在一次性读取大量数据或只读取几次时，将没有优势
    - 默认的缓冲区容量为 8KB，可以使用 `BufReader::with_capacity(size, R)` 来指定缓冲区大小
    - 对从内存中已有的源数据（比如 `Vec<u8>`）中读取时，也没有优势
> 主要的优势点，如在网络IO下，由于网络数据并不是一次性到达的，因此每次调用 read 只能读取一部分数据（这是耗时的系统调用），而使用 BufReader 来读取的话，则有一个缓冲区来读取数据

- `BufWriter`
- `Bytes`
- `Chain`
- `Cursor`
- `IoSlice`
- `Lines`
- `Sink`
- `Split`
- `Stdin`
- `Stdout`
- `Stderr`
- `Take`


## 网络
### Std 中的网络模块


### Rust 相关的网络模块

#### mio
mio：基于事件驱动的网络I/O库，提供了高效的非阻塞IO操作，是一个底层库，核心功能：
- 提供基于事件驱动的网络编程模型
- 支持非阻塞I/O操作
- 提供可扩展的事件处理器接口
- 高性能的事件通知机制
- 跨平台支持，由 epoll、kqueue 和 IOCP 支持的 I/O 事件队列

省略了的部分，让用户来自定义：
- 文件操作
- 线程池/多线程事件循环
- 计时器

使用场景：mio适用于需要处理大规模并发连接的网络应用程序，如网络服务器、代理、实时通信系统等。

#### quiche
Quiche 是一个 HTTP/3 和 QUIC 协议库，提供了对这两种新一代网络通信协议的支持。它是 Cloudflare 开发的开源项目，旨在为开发者提供简单易用、高效可靠的方式来使用 HTTP/3 和 QUIC 协议。
- 提供了完整的 HTTP/3 客户端和服务端支持
- 提供了 QUIC 协议实现

#### Actix-web
基于 Rust 语言和 Actix 框架的高性能 Web 服务库，提供了异步、并发和可伸缩的特性。它可以用于构建各种类型的 Web 应用程序，包括 RESTful API 服务、实时通讯应用和传统的网页应用等。
- 提供异步处理请求的能力
- 高性能的HTTP/1.x和HTTP/2服务器
- 中间件支持
- WebSocket 支持
- SSL 安全连接支持

#### WebSocket
[WebSocket](https://github.com/websockets-rs/rust-websocket)库为Rust语言提供了便捷的方式来实现WebSocket通信，并且支持双向通信、消息广播等核心功能。



#### hyper
hyper是一个偏底层的http库，支持HTTP/1和HTTP/2，支持异步Rust，并且同时提供了服务端和客户端的API支持。rocket、iron和reqwest底层都是基于hyper的

#### Rust web 框架的比较
https://github.com/flosse/rust-web-framework-comparison

参考:
[透过 Rust 探索系统的本原：网络篇](https://mp.weixin.qq.com/s/bOxEEK7Hh_tsua8HBahsjg)