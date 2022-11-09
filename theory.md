---
layout: article
# title: Blockchain
  # @start locale config
  # @end locale config
key: page-theory
sidebar:
    nav: theory
aside:
    toc: true
---

This is a work-in-progress document, meant to summarize various concepts in cryptography and other theory topic.

You can navigate to various topics by using the sidebar on the left.

这是我记录密码学学习相关的笔记。

2022-11-09 20:22:19：记录一下写作计划，这是一个很长的故事，等到毕业后也要继续进行。
- 准备首先从 zkp 相关的背景知识和方案开始，首先介绍基本的群、环、域和椭圆曲线相关知识，然后介绍多项式承诺方案，紧接着介绍 Groth16 的详细方案。
- 之后会开始介绍 IP-based 的协议
  - 首先是 sum-check 协议，GKR 协议
  - Thaler13 的优化
  - vsql17 引入的优化
  - Libra19 方案
- MIP-based 的协议
  - Spartan20
- IOP-based 的协议
  - PLONK19：这是现今使用最广泛的协议之一，有着许多的工程优化与实践。
  - Marlin19：这也是一个经典的 IOP 协议，引入了 holographic 的方法
  - STARK18：RAM-based 的 ZKP 方案
- DLOG-based 的协议
  - Bullerproof18
  - halo2
- 介绍一些不一样的 ZKP 方案，如 commit-and-prove 的方案
- 介绍 MPC-in-the-head 方案
- 介绍几类相关的应用
  - zerocash
  - hawk
  - zexe
  - verifiable computation
- 总结一下多项式承诺方案以及其基本的性质和效率平衡

## 学习资源
### 密码学以及相关的数学

#### 书籍

#### 项目
crypto3: [C++17实现的现代密码学库](https://github.com/NilFoundation/crypto3)

ZKP
ZKEVM
### 零知识证明
#### 资源
[很全的ZKP资源](https://github.com/ingonyama-zk/ingopedia)
我的推荐：
thaler's book：[Proofs, Arguments, and Zero-knowledge](https://people.cs.georgetown.edu/jthaler/ProofsArgsAndZK.html)
- 很全面的书，涉及到了 ZKP 的方方面面
the moon-math:[moonmath](https://github.com/LeastAuthority/moonmath-manual)
- 椭圆曲线部分很好

#### 项目
[thaler's book 实现](https://github.com/thor314/pazk)：很久没更新了，有机会看看能不能参与一下。
[STARK 的 rust 实现](https://github.com/0xProject/OpenZKP)
#### Paper


### 安全多方计算
#### 资源
#### 项目
[Yao-GC](https://github.com/cronokirby/yao-gc)

#### Paper

### 同态加密
#### 资源
[资源集合](https://github.com/jonaschn/awesome-he)

#### 项目
[FHE](https://github.com/openfheorg/openfhe-development)
[BFV加密方案](https://github.com/Sunscreen-tech/Sunscreen)

#### Paper