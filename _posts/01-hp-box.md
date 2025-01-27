# Todo Blog
2025-01-19 23:40:04:
- https://kobzol.github.io/rust/2025/01/15/async-rust-is-about-concurrency.html
  - 推荐：Rust 异步的优势不是性能，而是其他方面
- https://shikaan.github.io/assembly/x86/guide/2024/09/08/x86-64-introduction-hello.html
  - 对汇编语言的 Friendly introduction

2025-01-13 00:44:07 
- https://conradludgate.com/posts/async
- https://www.youtube.com/watch?v=7pU3gOVAeVQ
- https://www.reddit.com/r/rust/comments/1djkz6t/i_dont_understand_how_the_stdthreadscope/
- https://stackoverflow.com/questions/77661629/why-do-we-need-stdthreadscope-if-we-can-just-use-thread-join-to-drop-refer

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


# sysinfo 库
[深入浅出：Rust sysinfo 库实战指南](https://mp.weixin.qq.com/s?__biz=MjM5OTc0NTUxMg==&mid=2452977070&idx=1&sn=aae88895e21d43f9a714d0cedd812e52&chksm=b0f7172987809e3fbae25fe908c86981c13727748a0431852bcaf2e9482c04392a1545a354cc&cur_album_id=3824647361294991361&scene=190#rd)

[sysinfo](https://crates.io/crates/sysinfo)

sysinfo库则为 Rust 开发者提供了一个跨平台(Linux, Windows, IOS, Android, FreeBSD, MacOS等)的解决方案，用于获取系统信息，如：
- 进程信息
- CPU 使用情况
- 磁盘信息
- 系统组件信息
- 网络信息

使用
```toml
[dependencies]
sysinfo = "0.33.1"
```


