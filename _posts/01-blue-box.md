# Box 记录
2025-01-24 14:46:00:
- [Foundations of Large Language Models](https://arxiv.org/pdf/2501.09223)

2025-01-14 10:32:43
- `pub(crate) something` 表示在当前包可见，也就是可以直接在其他模块里使用 `use crate::something` 来导入对应 item(结构体、enum、模块)
- 也可以使用完整的绝对路径进行引用

Burn Book：https://burn.dev/burn-book/basic-workflow/index.html
- Rust 写的深度学习框架
## std::mem::forget 函数
为什么在转换为迭代器后，不会调用 drop 函数
- 因为在 into_iter 中使用了 `std::mem::forget` 函数

`into_iter` 函数将一个集合转换为一个迭代器，它会获取集合的所有权。
- 创建一个迭代器对象。
- 将集合的所有权转移到迭代器中。
- 防止集合的析构函数被自动调用（因为集合的所有权已经被转移）。

`std::mem::forget` 是 Rust 标准库中的一个函数，它的作用是防止 Rust 自动调用析构函数。具体来说：
- 当你调用 `forget(self)` 时，self 的所有权被“遗忘”，Rust 不会自动调用其析构函数。
- 这通常用于手动管理资源的生命周期，例如在实现自定义迭代器时。

函数原型
```rust
pub fn forget<T>(t: T)
```

使用场景：
- 手动管理资源

```rust
use std::mem::forget;
use std::ptr;

struct MyResource {
    data: *mut u8,
}

impl Drop for MyResource {
    fn drop(&mut self) {
        println!("Dropping MyResource");
        unsafe { ptr::drop_in_place(self.data); }
    }
}

fn main() {
    let resource = MyResource { data: Box::into_raw(Box::new(42)) };
    // 遗忘 resource，防止自动调用 Drop
    forget(resource);
    // 手动释放资源
    unsafe {
        println!("Manually dropping resource");
        Box::from_raw(resource.data);  // 调用 Box 的析构函数
    }
}
```
- 与 FFI 交互：将资源传递给C代码时，防止 Rust 在外部的C代码仍然使用这些资源时自动释放它们。
```rust
use std::mem::forget;

struct MyResource {
    data: *mut u8,
}
impl Drop for MyResource {
    fn drop(&mut self) {
        println!("Dropping MyResource");
        // 释放资源
    }
}
fn pass_to_c(resource: MyResource) {
    // 将资源传递给 C 代码
    unsafe {
        // 假设有一个 C 函数接收资源
        // c_function(resource.data);
    }
    // 遗忘资源，防止自动调用 Drop
    forget(resource);
}
fn main() {
    let resource = MyResource { data: Box::into_raw(Box::new(42)) };
    pass_to_c(resource);
}
```

- 自定义迭代器
```rust
use std::mem::forget;

struct MyCollection {
    data: Vec<i32>,
}
impl Drop for MyCollection {
    fn drop(&mut self) {
        println!("Dropping MyCollection");
    }
}
struct MyIterator {
    data: Vec<i32>,
    index: usize,
}
impl MyCollection {
    fn into_iter(self) -> MyIterator {
        let iter = MyIterator {
            data: self.data,
            index: 0,
        };
        // 遗忘原始集合，防止自动调用 Drop
        forget(self);
        iter
    }
}
fn main() {
    let collection = MyCollection { data: vec![1, 2, 3] };
    let iter = collection.into_iter();

    for item in iter {
        println!("{}", item);
    }
}
```

forget 的主要作用是防止 Drop 函数被自动调用，用于需要手动管理资源的生命周期场景。

## 在存在Opensssl3.x版本的ubuntu上安装openssl1.1.1
编译安装
```bash
wget https://www.openssl.org/source/openssl-1.1.1.tar.gz
tar -xzvf openssl-1.1.1.tar.gz
cd openssl-1.1.1
# 配置
./config --prefix=~/my-package/ssl --openssldir=~/my-package/ssl shared no-apps
# 如果出现 no-apps 选项的错误，那么直接忽略这个选项
./config --prefix=~/my-package/ssl --openssldir=~/my-package/ssl shared
# 编译安装
make -j12
sudo make install
```

使用
```bash
# 添加到运行时动态链接库地址
export LD_LIBRARY_PATH=~/my-package/ssl/lib lib:$LD_LIBRARY_PATH # 临时使用

# 编译时
OPENSSL_LIB_DIR=/home/muxi/package-my/openssl-1.1.1-lib/ssl/lib OPENSSL_INCLUDE_DIR=/home/muxi/package-my/openssl-1.1.1-lib/ssl/include cargo build
```
然后就可以运行了

## TLS/SSL 证书
https://blog.laisky.com/p/https-in-action/#gsc.tab=0
https://www.kawabangga.com/posts/5330


证书透明度： https://certificate.transparency.dev/howctworks/
## TCP
2025-01-21 11:44:46

> TCP 四次挥手，在实际中可能只能抓到 3 个包

TCP flag：
- SYN：建立连接
- FIN：断开连接
- ACK：响应
- PSH：有 DATA数据传输
- RST：连接重置
- URG：紧急

PSH 和 ACK 是通用的组合
ACK是可能与SYN，FIN等同时使用的，比如SYN和ACK可能同时为1，它表示的就是建立连接之后的响应，
RST一般是在FIN之后才会出现为1的情况，表示的是连接重置。

PSH为1的情况，一般只出现在 DATA内容不为0的包中，也就是说PSH为1表示的是有真正的TCP数据包内容被传递。

https://zh.wikipedia.org/wiki/TCP%E5%BB%B6%E8%BF%9F%E7%A1%AE%E8%AE%A4
https://www.cnblogs.com/Xinenhui/p/17982452
https://zyy.rs/post/tcp-flags-psh-and-urg/
https://www.cnblogs.com/diegodu/p/4213799.html
high: https://writings.sh/post/network-tcp
http://timd.cn/tcp-window/

TCP 的接收方在收到数据后，需要回复 ACK 数据包，表示已经确认接收到 ACK 确认号前面的所有数据。

ACK 机制：接收方在接收到数据后，不会立即发送ACK的原因：
- 收到数据包的序号签名还有需要接收的数据包。
- 为了降低网络流量，ACK 有延迟确认机制
- ACK 的值到达最大值，从0开始

### Nagle 算法（发送角度）
综合 累计发送 + 延迟发送 这两个策略

避免小数据传输（发送角度）
- 没有已发送未确认的报文时，马上发送数据
- 存在未确认数报文时，直接没有已发送未确认报文或数据长度达到MSS大小时再发送数据
- 不满足上面的条件，那么发送方会囤积数据直到条件满足


### Delay ACK（接收角度）
TCP有两种确认方式：
- 快速 ACK：本端收到数据包后，立即发送ACK给对端
- 延迟 ACK：本端收到数据包后，等待一段时间再发送ACK
    - 如果需要发送数据，那么ACK在发送数据包中携带
    - 否则，发送一个累计确认的ACK给对端(收到的最大seq+1)
> 在实现中，使用 pingpong 来区分
> 延迟确认：控制累计确认的时机


TCP 传输的数据流：
- TCP 交互数据流：一般情况下数据总是以小于 MSS 的分组发送，做的是小流量的数据交互，如 SSH、Telnet
- TCP 成块数据流：TCP 尽最大能力传输数据，数据按照 MSS 发送，如 FTP

Delay Ack：延迟发送ACK
- 延迟一段时间后再发送ACK，系统有一个固定的定时器每隔200ms来检查是否需要发送ACK包
- ACK可以合并，如果连续收到两个TCP包，只需要回复最终的ACK（累计确认机制）
- 接收方有数据要发送，那么可以在发送数据的TCP包里面带上ACK信息，避免单独发送ACK包

参考：
- https://www.kawabangga.com/posts/5845
- https://blog.csdn.net/wdscq1234/article/details/52430382
- https://blog.csdn.net/2303_77208351/article/details/137938001

> 有延迟确认，那么接收方会累计ACK，而发送方在延迟的时间内收不到AK，就不会发送小的数据包，而是留在缓冲中。
- 两个一起使用的时候会影响性能


### TCP 对 HTTP 性能的影响
1. 建立连接，三次握手
2. TCP 慢启动：TCP拥塞控制手段，在TCP刚建立好之后的最初传输阶段会限制连接的最大传输速度，后续逐步提高
3. TCP 延迟确认
4. Nagle 算法
5. TIME_WAIT积累与端口耗尽
6. 服务端端口耗尽
7. 服务端HTTP进程打开文件数量达到最大
> HTTPS，还需要加上 TLS 的影响

https://www.cnblogs.com/rexcheny/p/10777906.html

## OH 编译问题
> 需要版本 python3.9(待验证，看更高版本是不是可以)、gcc-11、clang 使用 gcc-11
![alt text](/images/01-blue-box/image.png)

![alt text](/images/01-blue-box/image-1.png)
![alt text](/images/01-blue-box/image-2.png)

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

> `sudo chown -R muxi /root`
> 不小心将 OpenHarmony 安装到了 /root 下，需要 执行上面的命令后才能使用 `code .` 打开

### 如何直接跑 tdd 和 xdc 在 Windows 上
首先要保证存在 hdc 工具，下载 [OH开发者工具](https://repo.huaweicloud.com/openharmony/os/4.1-Release/ohos-sdk-windows_linux-public.tar.gz)，解压后，压缩包中有linux，windows两个文件夹，找到 windows 下的 `toolchains-windows-x64-5.0.2.57-Canary1.zip` 文件，解压到对应目录，然后添加路径到环境变量中，比如 `D:\OH\toolchains-windows-x64-5.0.2.57-Canary1\toolchains`
- 打开终端，执行 `hdc version` 查看版本信息


注意使用 `pip list` 查看安装的版本，其中 setuptools 的版本号不能大于 50，如果大于，可以使用：
```bash
python -m pip uninstall setuptools
python -m pip install setuptools==46.1.3
```
环境上需要下载：
```bash
git clone https://gitee.com/openharmony/testfwk_developer_test
git clone https://gitee.com/openharmony/testfwk_xdevice
```
在 `testfwk_xdevice` 上需要直接 `python setup.py install` 和 在 `plugins\ohos` 目录下执行 `python setup.py install`(不执行也没啥)
- **需要将两个文件放到同一个目录下，比如 /TDD**

对于协议栈，TDD 就是本地的 UT，没有 XTS；由于 request 模块依赖协议栈，因此协议栈的修改需要跑 request 模块的 UT 和 XTS，可以使用一个已完成的 PR 来验证本地 windows 环境是否正确：
- 比如对已合并的 PR： `https://gitee.com/openharmony/request_request/pulls/1171` 来进行测试
0. 镜像烧写
- 首先需要进行镜像烧写，在 PR 下面找到最新的 build 成功的记录，然后查看门禁报告 `https://ci.openharmony.cn/workbench/cicd/detail/67807ce064650f998b35725f/runlist`
- 下载 dayu200 里面的文件
![alt text](/images/01-blue-box/image-3.png)

1. TDD
如上所示，下载 `dayu200_tdd` 里的文件
将下载文件解压，将解压文件里面的 `/tests` 目录，拷贝到上面的 `/TDD` 目录下的 `testfwk_developer_test`中。

修改 `testfwk_developer_test/config/user_config.xml` 配置文件：
- 修改 sn 信息为 `hdc list targets` 的输出值
```xml
<!-- sn 信息 -->
<sn>xxx</sn> 
<!-- 增加测试文件目录 -->
<test_cases>
<dir>../tests</dir>
</test_cases>
```

最后在目录 `D:\rk3568\TDD\testfwk_developer_test` 启动终端，然后运行 `./start.bat`，然后执行
```bash
run -t UT -tp request
```

2. XTS
如上所示，下载 `dayu200_xts` 里的文件，直接解压后进入下面的文件夹
```bash
\Artifacts-dayu200_xts-20250110-1-00135-version-dayu200_xts\suites\acts\acts
```
然后运行：`run.bat` 文件，执行 `run acts`

注意，在跑 xts 的时候需要保证 rk **屏幕常亮** 和 **连接网络**，测试需要通过网络来下载数据
- 屏幕常亮：`hdc shell power-shell setmode 602`
```bash
  600  :  normal mode
  601  :  power save mode
  602  :  performance mode
  603  :  extreme power save mode
```

**对于协议栈的测试来说，TDD 就是项目下的 UT 测试，也就是通过执行 `cargo test` 来完成**
- 需要执行的 XTS 和 TDD 都是上传下载的，因此上传下载依赖协议栈，因此：
- 刷上对应 PR 的镜像到 rk 中
    - 使用上传下载的其他最近 PR 上的 XTS 和 TDD 测试
> 协议栈 images + 上传下载的 XTS 和 TDD


如果安装了 xdevice，那么就直接使用 `python -m xdevice` 然后运行 `run acts` 即可。
> run.bat 中包含了卸载和安装命令，如果版本没有变化就可以直接运行上述命令来执行哟管理
```bash
python -m pip uninstall -y hypium
python -m pip uninstall -y xdevice-aw
python -m pip uninstall -y xdevice-aosp
python -m pip uninstall -y xdevice-oh-apptest
python -m pip uninstall -y xdevice-ohos
python -m pip uninstall -y xdevice-extension
python -m pip uninstall -y xdevice-devicetest
python -m pip uninstall -y xdevice-devicetest-extension
python -m pip uninstall -y xdevice-devicetest-common-aw
python -m pip uninstall -y xdevice-app-dfx-test
python -m pip uninstall -y xdevice-common-aw
python -m pip uninstall -y xdevice
```

测试报告的问题：
- 测试报告现在用的两套逻辑，要么下载到新报告，要么使用旧报告
- 新报告下载不了的时候，直接使用了旧报告，但旧报告也要下载资源，如果下载不了，就会出现 {{}} 这种错误，因此需要下载下面网站的资源，然后解压后替换到报告目录下
- https://gitee.com/openharmony-sig/compatibility/blob/master/test_suite/resource/xdevice/template.zip
## 理解 Atomic 和 Meory Ordering 
标记为 memory_order_relaxed 的原子操作不是同步操作；它们不会在并发内存访问中强加顺序。它们只保证原子性和修改顺序的一致性。
- 通常用于 counter 的 +/-，只要求原子性，不要求顺序/同步

## 关于证书的问题
为什么客户端需要内置 Root 证书？证书链


参考：https://www.kawabangga.com/posts/5330

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

### 通过 openssl 生成公钥哈希值 pinnings
[OH-network-http-文档](https://gitee.com/openharmony/docs/blob/master/zh-cn/application-dev/network/http-request.md#%E9%A2%84%E7%BD%AE%E8%AF%81%E4%B9%A6%E5%85%AC%E9%92%A5%E5%93%88%E5%B8%8C%E5%80%BC)

```bash
# 从证书中提取出公钥
openssl x509 -in rootCA.crt.pem -pubkey -noout > root.pubkey.pem
# 将pem格式的公钥转换成der格式
openssl asn1parse -noout -inform pem -in root.pubkey.pem -out root.pubkey.der
# 计算公钥的SHA256并转换成base64编码
openssl dgst -sha256 -binary root.pubkey.der | openssl base64
```

例子
```
root: sha256//9bk2UWmCEN3+zE2FcN0tLASEooDlvTjWXWlRM5ZRH/Q=
server: sha256//5YxAVCGlRCZFMPYImcUznsT7UGG77XoWwjwRGE3YZTc=
```

### 通过 openssl 生成证书链
如何产生证书：https://www.cnblogs.com/dirigent/p/15246731.html

服务器需要加入 key.pem, 与服务器证书对应, 用于产生签名，然后客户端可以使用服务器返回的证书来进行验证看签名是否正确
- 服务器返回：
    - 服务器的证书（也可以说包含在证书链里）
    - 证书链
    - 签名
- 客户端需要验证三个都正确后才信任服务器
    - 验证证书链
    - 验证签名，确保证书和私钥匹配。
    - 检查证书的有效性


证书链的验证需要客户端需要导入 root-ca.pem, 信任手动创建的根证书文件用于测试

结合 kimi 产生如何生成 openssl 证书链的命令如下，都生成 pem 格式：

1. Root证书
```bash
# 1. 生成根密钥
# openssl genpkey -algorithm RSA -out rootCA.key.pem -aes256
# 然后输入 pem 密码: 1234
# 以下命令生成没有密码的pem
openssl genpkey -algorithm RSA -out rootCA.key.pem -pkeyopt rsa_keygen_bits:2048 
# 等价于: openssl genrsa -out rootCA.key.pem 2048

# 2. 创建根证书，10年有效期
openssl req -x509 -new -nodes -key rootCA.key.pem -sha256 -days 3650 -out rootCA.crt.pem -subj "/C=CN/ST=Beijing/L=Beijing/O=RootCA/OU=RootCA/CN=RootCA"
```
> 根证书不需要创建签名请求（CSR）。根证书是自签名的，生成过程直接从私钥开始，而不是从 CSR 开始。

如何移除现有私钥的密码
```bash
openssl rsa -in encrypted_private_key.pem -out decrypted_private_key.pem
```

2. Intermediate 证书
创建文件 `extensions.cnf`，然后复制以下内容
```ini
[v3_ca]
basicConstraints = CA:TRUE
subjectAltName = @alt_names

[alt_names]
IP.1 = 127.0.0.1
```

```bash
# 1. 生成中间密钥
#openssl genpkey -algorithm RSA -out intermediateCA.key.pem -aes256
# 生成没有密码
openssl genpkey -algorithm RSA -out intermediateCA.key.pem -pkeyopt rsa_keygen_bits:2048

# 2. 创建中间证书签名请求（CSR）
openssl req -new -key intermediateCA.key.pem -out intermediateCA.csr.pem -subj "/C=CN/ST=Beijing/L=Beijing/O=IntermediateCA/OU=IntermediateCA/CN=IntermediateCA"

# 3. 使用根证书签署中间证书
openssl x509 -req -in intermediateCA.csr.pem -CA rootCA.crt.pem -CAkey rootCA.key.pem -CAcreateserial -out intermediateCA.crt.pem -days 3650 -sha256 -extfile extensions.cnf -extensions v3_ca
```

3. Server 证书
创建文件 `server_extensions.cnf`，拷贝以下内容：
```ini
[server_ext]
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage=digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName=@alt_names

[alt_names]
IP.1 = 127.0.0.1
```
```bash
# 1. 生成服务器密钥
# openssl genpkey -algorithm RSA -out server.key.pem -aes256
openssl genpkey -algorithm RSA -out server.key.pem -pkeyopt rsa_keygen_bits:2048

# 2. 创建服务器证书签名请求（CSR）
openssl req -new -key server.key.pem -out server.csr.pem -subj "/C=CN/ST=Beijing/L=Beijing/O=Server/OU=Server/CN=127.0.0.1"

# 3. 使用中间证书签署服务器证书
openssl x509 -req -in server.csr.pem -CA intermediateCA.crt.pem -CAkey intermediateCA.key.pem -CAcreateserial -out server.crt.pem -days 365 -sha256 -extfile server_extensions.cnf -extensions server_ext
```

验证：
```bash
# 打印
openssl x509 -in rootCA.crt.pem -text -noout

# 验证中间证书
openssl verify -CAfile rootCA.crt.pem intermediateCA.crt.pem

# 验证证书链
openssl verify -CAfile rootCA.crt.pem -untrusted intermediateCA.crt.pem server.crt.pem 
```

最后的文件:
```bash
certs
├── extensions.cnf
├── intermediateCA.crt.pem
├── intermediateCA.csr.pem
├── intermediateCA.key.pem
├── rootCA.crt.pem
├── rootCA.key.pem
├── server.crt.pem
├── server.csr.pem
├── server.key.pem
└── server_extensions.cnf

0 directories, 10 files
```
创建证书链
```bash
cat rootCA.crt.pem intermediateCA.crt.pem server.crt.pem > chain.crt.pem
# 验证
openssl verify -CAfile rootCA.crt.pem chain.crt.pem
```

**但是在 OpenSSL 的函数 `SSL_CTX_use_certificate_chain_file` 中使用的使用，需要反过来**:
```bash
cat server.crt.pem intermediateCA.crt.pem rootCA.crt.pem > chain.crt.pem
```
然后在函数里面通过才能成功，不然会报以下错误
```c
// 加载证书链文件
if (SSL_CTX_use_certificate_chain_file(ctx, "path/to/chain.pem") != 1) {
    ERR_print_errors_fp(stderr);
    return -1;
}
//Error
called `Result::unwrap()` on an `Err` value: Error { code: ErrorCode(1), cause: Some(Ssl(ErrorStack([Error { code: 167772353, library: "SSL routines", function: "tls_post_process_client_hello", reason: "no shared cipher", file: "../ssl/statem/statem_srvr.c", line: 2220 }]))) }
Request send failed: HttpClientError { ErrorKind: Connect, Cause: Custom { kind: Other, error: SslError { code: SslErrorCode(1), internal: Some(Ssl(ErrorStack([StackError { code: 167773200, file: "../ssl/record/rec_layer_s3.c", line: 1593, func: Some("ssl3_read_bytes"), data: Some("SSL alert number 40") }]))) } } }
```

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
- 创建软连接：`sudo ln -s /usr/bin/python3 /usr/bin/python`
- 使用 update-alternatives 来为使用 python2 和 python3 
    - `sudo update-alternatives --install /usr/bin/python python /usr/bin/python2 100`
    - `sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 150`
    - 设置优先级来切换 python2 和 python3，也可以用于不同 python3 版本的切换，如 python3.10 和 python3.11 之间进行切换
- 使用 `sudo apt install python-is-python3`
    - 自动完成所有链接创建
- 使用别名：`alias python='python3'` 在需要 `/use/bin/python` 时，无效
> 如果安装了 mini-conda，那么可以使用 conda 来管理 python 环境，唯一需要注意的事情是：注意有些软件，尤其是内核相关，需要在原始环境下安装，在 conda 中使用的 python 和原始环境是不一样的，这样就会报错，因此应该先 `conda deactive` 然后再进行安装

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


除了使用 update-alternatives 来管理，还可以手动设置软连接来进行管理：
```bash
# 切换到 Python3.9
sudo ln /usr/local/python3/bin/python3.9 /usr/bin/python3
sudo ln /usr/local/python3/bin/pip3 /usr/bin/pip3
# 切换到 Python3.9
sudo ln /usr/bin/python3.10 /usr/bin/python3
sudo ln /usr/local/python3/bin/pip3.10 /usr/bin/pip3
```
sudo apt install python-is-python3

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

# Git 常用命令记录
删除本地分支和远程分支
```bash
git branch -r # 检查远程分支状态

# 1. 删除本地分支
git branch -d <branch-name>
# 如果分支尚未合并，则需要强制删除
git branch -D <branch-name>

# 2. 删除远程分支
git push origin --delete <branch-name>

# 3. 清理本地远程分支引用
git remote prune origin

# 完全同步本地和远程的状态
git fetch --all --prune
```

# tcpdump 使用
```bash
tcpdump [option] proto dir type
```
- option 可选参数
- proto 类过滤器: 根据协议过滤
    - tcp, udp, icmp, ip, ip6, arp, rarp, ether, wlan, fddi, tr, decent
- type 类过滤器: 后面需要接参数
    - host, net, prot, protrange
- direction 类过滤器: 根据数据流向进行过滤, 可以使用逻辑运算符来组合
    - src, dst
    - 如: src or dst

**tcpdump 输出内容**
```bash
# 时分秒毫秒 网络协议 发送方的ip地址+端口 箭头表示数据流向 接收方的ip地址和端口 冒号 数据包内容
21:26:49.013621 IP 172.20.20.1.15605 > 172.20.20.2.5920: Flags [P.], seq 49:97, ack 106048, win 4723, length 48
```
- 数据包内容中, 会包括 TCP 报文 Flags
    - `[S]`: SYN (开始连接)
    - `[P]`: PSH (推送数据)
    - `[F]`: FIN (结束连接)
    - `[R]`: RST (重置连接)
    - `[.]`: 没有 Flag, 可能是 ACK/URG

常用过滤规则
- 基于host过滤
- 基于网段过滤
- 基于端口过滤
- 基于协议过滤
- 基于 ip 协议版本过滤

可选参数解析

过滤规则的组合


https://www.cnblogs.com/wongbingming/p/13212306.html

# HTTP 协议

https://byvoid.com/zhs/blog/http-keep-alive-header/


