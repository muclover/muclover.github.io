---
title: 生成openssl证书链和公钥pinnings
tags: Archive Configuration Openssl
---


# 关于证书的问题: 为什么客户端需要内置 Root 证书？证书链
参考：https://www.kawabangga.com/posts/5330

# HTTP Public Key Pinning

HTTP公钥固定是一种防止利用CA机构错发证书，而进行中间人攻击的安全机制，用于预防CA遭受入侵或其他会造成CA签发未授权证书的情况。

工作原理：服务器通过Public-Key-Pins（或Public-Key-Pins-Report-Only用于监测）HTTP头向浏览器传递HTTP公钥固定信息。HTTP公钥固定将网站X.509证书链中的一个SPKI（和至少一个备用密钥）以pin-sha256方式进行哈希，由参数max-age（单位秒）所指定一段时间，可选参数includeSubDomains决定是否包含所有子域名，另一个可选参数report-uri决定是否回报违反HTTP公钥固定策略的事例。在max-age所指定的时间内，证书链中证书的至少一个公钥须和固定公钥相符，这样客户端才认为该证书链是有效的。

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

#### 1.Root证书
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

#### 2.Intermediate 证书
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

#### 3.Server 证书
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

#### 4.验证、生成证书链
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

### 参考
- 如何产生证书: https://www.cnblogs.com/dirigent/p/15246731.html
- ssl工具: https://www.ssleye.com/ssltool/cer_check.html
[wikipedia-HTTP公钥固定](https://zh.wikipedia.org/wiki/HTTP%E5%85%AC%E9%92%A5%E5%9B%BA%E5%AE%9A)


# 证书透明度
证书透明度：保证证书签发流程的安全。

