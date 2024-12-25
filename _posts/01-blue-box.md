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