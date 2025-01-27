---
title: 在存在Opensssl3.x版本的ubuntu上安装openssl1.1.1
tags: Archive Configuration Openssl
aside:
  toc: true
---

# 在存在Opensssl3.x版本的ubuntu上安装openssl1.1.1

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

使用的时候需要添加到运行时动态链接库
```bash
# 添加到运行时动态链接库地址
export LD_LIBRARY_PATH=~/my-package/ssl/lib lib:$LD_LIBRARY_PATH # 临时使用

# 编译时
OPENSSL_LIB_DIR=/home/muxi/package-my/openssl-1.1.1-lib/ssl/lib OPENSSL_INCLUDE_DIR=/home/muxi/package-my/openssl-1.1.1-lib/ssl/include cargo build
```
然后就可以运行了