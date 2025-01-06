# Box 记录
## OH 编译问题
> 需要版本 python3.9(待验证，看更高版本是不是可以)、gcc-11、clang 使用 gcc-11

我安装了 gcc-11 和 gcc-13，则默认通过 `sudo apt install clang` 会使用 `gcc-13`，因此需要先卸载 gcc-13 后再重新安装。
```bash
sudo apt remove gcc-13
sudo apt remove clang
sudo apt install clang
```
然后检查：
```bash
clang -v
# 出现
Found candidate GCC installation: /usr/bin/../lib/gcc/x86_64-linux-gnu/11
Selected GCC installation: /usr/bin/../lib/gcc/x86_64-linux-gnu/11
```
- 如果有多个版本的话，会显示多个 Found candidate GCC installation
## 理解 Atomic 和 Meory Ordering 
标记为 memory_order_relaxed 的原子操作不是同步操作；它们不会在并发内存访问中强加顺序。它们只保证原子性和修改顺序的一致性。
- 通常用于 counter 的 +/-，只要求原子性，不要求顺序/同步


## 增加 pinning 根证书
HTTP客户端提供了一种额外的机制来保证HTTPS通信的安全，SSL Pinning。SSL Pinning又可以细分为Certificate Pinning和Public Key Pinning。

HTTP Public Key Pinning (HPKP), 是HTTPS网站防止攻击者利用数字证书认证机构（CA）错误签发的证书进行中间人攻击的一种安全机制，用于预防CA遭受入侵或其他会造成CA签发未授权证书的情况。

采用公钥固定时，网站会提供**已授权公钥的哈希列表**，指示客户端在后续通讯中只接受列表上的公钥。

客户端预先设置一组公钥的固定值，然后在 TLS 握手时判断服务器提供的证书是否在固定的公钥值里面，如果是，则表明是合法的服务器，则建立连接。
- 在 Android 中，可以利用 Network Security Configuration（网络安全配置）。通过在 XML 配置文件中定义信任的公钥或者证书等信息。

在 ylong_http_client 通过下面的方法来在客户端中设置public key pinning
```rust
// 其中 pinned_key
let pinned_key = PubKeyPins::builder()
    .add(
        "https://7.249.243.101:6789",
        "sha256//VHQAbNl67nmkZJNESeTKvTxb5bQmd1maWnMKG/tjcAY=")
    .build()
    .unwrap();
let builder = ClientBuilder::new().add_public_key_pins(pinned_key);
```

新增接口：
```rust
let pinned_key = PubKeyPins::builder()
    .add_with_root_strategy(
        "https://7.249.243.101:6789",
        "sha256//VHQAbNl67nmkZJNESeTKvTxb5bQmd1maWnMKG/tjcAY=")
    .build()
    .unwrap();
```

SSL中的几个的函数：
```c
// c_openssl_1_1
#include <openssl/ssl.h>
SSL *ssl; // 假设已经初始化的SSL连接

// 获取对等方（peer）的证书

// 它会增加证书引用计数，调用者在使用完证书后需要负责减少引用计数（通常使用X509_free函数）以避免内存泄漏
X509 *peer_cert = SSL_get1_peer_certificate(ssl);
// 不会增加证书的引用计数，返回的X509结构体指针的生命周期由 SSL 连接本身的生命周期决定。
// 当 SSL 连接关闭或者被释放时，这个指针所指向的资源也会被释放。
// 用这个函数想要保存证书信息的话，需要手动增加引用计数
X509 *peer_cert = SSL_get1_peer_certificate(ssl);
// c_openssl_3_0
```

证书链的函数
```c
STACK_OF(X509) *cert_chain = SSL_get_peer_cert_chain(ssl);
if (cert_chain!= NULL) {
    int num_certs = sk_X509_num(cert_chain);
    for (int i = 0; i < num_certs; i++) {
        X509 *cert = sk_X509_value(cert_chain, i);
        // 在这里可以对证书链中的每个证书进行操作，例如验证等
    }
    // 当操作完成后，需要释放证书链栈结构（如果需要）
    sk_X509_free(cert_chain);
}
```
`SSL_get_peer_cert_chain` 是 OpenSSL 库中的函数。它主要用于获取对等方（peer）的证书链。在 SSL/TLS 连接中，证书链是一系列证书，从服务器（或客户端，取决于连接场景）提供的终端实体证书开始，一直向上追溯到根证书颁发机构（CA）的证书。这个函数返回一个指向 `STACK_OF(X509)` 类型的指针，其中 `STACK_OF` 是 OpenSSL 中用于表示栈结构的类型，而X509是表示证书的结构体类型。

`SSL_get0_verified_chain ` 它的作用是获取经过验证的对等方证书链。这里强调 “经过验证”，意味着这个证书链已经经过了 SSL/TLS 连接中的验证过程（例如，在 SSL 握手过程中，会对证书链进行一系列的验证，包括证书的有效期、签名是否正确、证书链是否完整等），与 SSL_get_peer_cert_chain 不同的是，它返回的是经过验证的结果，在某些情况下，可以直接使用这个结果进行后续操作，例如在应用层进一步确认证书链的相关信息，而不需要再次从头开始进行完整的验证流程。


## 多个版本的gcc，改变 gcc 的优先级
```bash
sudo update-alternatives --display gcc # 查看gcc的优先级
ls /usr/bin/gcc* # 查看有几个版本的 gcc

sudo update-alternatives --config gcc # 手动配置想要的gcc版本

# 配置不同版本的 gcc 的优先级，然后在自动选择的时候，会选择优先级高的
# 如果想要自动替换的话，更改优先级即可
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 11
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-13 13

# 类似的 g++ 也可以
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 11
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-13 13

# 删除某个版本
sudo update-alternatives --remove gcc /usr/bin/gcc-11

# 检查版本信息
gcc -v
g++ -v
```

安装方法：https://www.cnblogs.com/DHJ151250/p/17990879
- 通过添加 ppa 源来进行安装

## 将 Python3 设置为默认版本
将 python3 设置为默认版本 https://www.cnblogs.com/slyu/p/13362005.html

https://blog.wssh.trade/posts/ubuntu-python/

Ubuntu默认安装的是 Python3.10，但OH需要安装 Python3.9，以下是一种方法：
注意默认是有 Python3.10

先安装 Python3.9
```bash
# 添加 ppa 源
sudo add-apt-repository ppa:deadsnakes/ppa
# 安装 python3.9
sudo apt install python3.9
# 检查版本
python3.9 --version
# 使用 update-alternatives
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.9 9
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.9 10
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 9
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 10

# 然后手动切换到 3.9
sudo update-alternatives --config python
sudo update-alternatives --config python3
# 安装 python3.9 的开发工具
sudo apt install python3.9-dev
```

参考：https://blog.wssh.trade/posts/ubuntu-python/

## gzip 命令
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
## 如何在 vscode 中插入时间
2025-01-02 14:45:39
```json
[
    {
        "key": "alt+shift+t",
        "command": "editor.action.insertSnippet",
        "when": "editorTextFocus",
        "args": {
            "snippet": "$CURRENT_YEAR-$CURRENT_MONTH-$CURRENT_DATE $CURRENT_HOUR:$CURRENT_MINUTE:$CURRENT_SECOND"
        }
    }
]
```

Other Solutions: https://stackoverflow.com/questions/38780057/how-to-insert-current-date-time-in-vscode

## 如何对待事务性的、琐碎的工作
1. 摆正心态：工作就是工作，完成分配的任务，就是你的目的，不要产生对抗性情绪。工作不是学习，不能期待所有工作内容都能得到成长。
2. 不出错 + 高效率：不出错（多问多看） --> 提高效率（寻找改进点、改进建议）
3. 建立系统性思维：寻找琐碎的工作处于业务的位置，定位是什么？加深自己的理解
4. 不要忘记主线任务：始终要保证对核心产出投入足够的时间和精力，做出自己有亮点的地方
5. 适当拒绝：学会沟通

## **http 自动解压缩**
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