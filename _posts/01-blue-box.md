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

