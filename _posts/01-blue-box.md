# Box 记录
2025-01-24 14:46:00:
- [Foundations of Large Language Models](https://arxiv.org/pdf/2501.09223)

2025-01-14 10:32:43
- `pub(crate) something` 表示在当前包可见，也就是可以直接在其他模块里使用 `use crate::something` 来导入对应 item(结构体、enum、模块)
- 也可以使用完整的绝对路径进行引用

Burn Book：https://burn.dev/burn-book/basic-workflow/index.html
- Rust 写的深度学习框架
# **http 自动解压缩**
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

# Rust 的 println! 格式化
在 Rust 中，格式化参数是通过一系列占位符和相应的参数值来实现的。比如：
```rust
let hello = "hello"
let world = "world"
println!("{},{}", hello, world);
```

一个格式参数的完整形式是 {which:how}，其中的 which 和 how 都是可选的。
- which 用于指定要格式化的特定参数，可以通过索引下标或者名称来选择。如果没有指定which，则默认按照参数列表的顺序，从 0 到 n 自动选择参数。例如：
```rust
// 使用索引
println!("{0} {1} {} {}", 66, 77);// 等同于println!("{0} {1} {2} {3}", 66, 77, 66, 77);
// 命名参数来个性化参数列表，但是如果同时使用索引和命名参数，那么命名参数必须放在最后。
println!("{days}天有{hours}小时", days=1, hours=24);
```
- how，它定义了参数的格式化方式，例如对齐方式、浮点数的精度、数值基数等

文本类型的格式化
- fill: 填充字符，用于当内容的宽度小于所需的最小宽度时进行填充，默认是空格。
- align: 对齐方式，其中 < 代表左对齐，> 代表右对齐，^ 代表居中对齐，默认是左对齐。
- width: 指定最小宽度，如果内容的长度小于此宽度，将根据设置的对齐方式用填充字符补充。
- precision: 对于字符串，它指定了最大输出宽度。如果字符串的长度超出这个值，会根据最大宽度截断字符串。

```rust
// 格式 {:[fill][align][width][.precision]}
println!("{:>8}", "foo"); // 输出 "     foo"，默认使用空格填充以及右对齐
println!("{:*>8}", "foo"); // 输出 "*****foo"，使用 '*' 填充并右对齐
println!("{:*<8}", "foo"); // 输出 "foo*****"，使用 '*' 填充并左对齐
println!("{:*^8}", "foo"); // 输出 "**foo***"，使用 '*' 填充并居中对齐
```

数值类型
```rust
// {:[fill][align][sign][#][0][width][.precision][type]}

    // 格式化整数
    println!("{:04}", 42); // 输出：0042
    println!("{:+}", 42); // 输出：+42
    println!("{:#x}", 255); // 输出：0xff
    println!("{:#b}", 5); // 输出：0b101
    println!("{:0>5}", 14); // 输出：00014

    // 格式化浮点数
    println!("{:.*}", 2, 1.234567); // 输出：1.23
    println!("{:+.2}", 3.141592); // 输出：+3.14
    println!("{:.2}", 3.141592); // 输出：3.14
    println!("{:10.4}", 1234.56); // 输出："   1234.5600"，宽度为10，小数点后4位
    println!("{:0>10.4}", 1234.56); // 输出："0001234.5600"，填充0，宽度为10，小数点后4位

    // 格式化时使用特定的填充字符
    println!("{:*>10}", 42); // 输出：********42
    println!("{:.*}", 2, 1.234567); // 输出：1.23
```

参考：
https://www.cnblogs.com/RioTian/p/18145045

