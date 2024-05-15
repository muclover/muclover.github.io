---
title: Decentralized Thoughts - Decentralized thoughts about decentralization Note
tags: Archive Theory Cryptography
# date: 2024-05-15 09:42:24
# sidebar:
#  nav: llm
# published: false
# aside:
#  toc: true
---
以前的记录，同步过来。

[Decentralized Thoughts - Decentralized thoughts about decentralization](https://decentralizedthoughts.github.io/)
- 区块链 密码学相关的知识

# 密码学
## What is a cryptographic hash function?
2020-8-28 Alin Tomescu
讨论了 ROM 和 哈希函数的应用

类比：哈希函数是 "guy in the sky"
- 输入任意长度的 $x$
- 输出固定长度、看起来是随机的 $y$
- 对同样的输入有同样的值

哈希函数是 random oracle
- 输入任意长度的 $x$
- 检查是否已经为 $x$ 产生了 256 随机比特
	- 若已经存在，则返回
	- 否则，随机选择 256 比特，返回，并存储下这个对应关系 $(x,y)$ 
ROM 的限制
- 理论上不能构建 ROM 这样的算法
- 实际上可以绕过

定义哈希函数为数学函数 $H:\{0,1\}^*\rightarrow \{0,1\}^{256}$ 
- collision-resistance 和鸽笼原理
- 由于输入无限，输出有限，那么必然存在两个不同的输入对应于同一个输出，这就是 collision
- ROM 下可以证明发生 collision 是不可能的
	- $2^{256}$ 需要调用函数 $2^{128}$ 次

应用：
- 文件完整性校验
- PoW
- Commitment
## What is a Merkle Tree
[What is a Merkle Tree?](https://decentralizedthoughts.github.io/2020-12-22-what-is-a-merkle-tree/#fn:consideredtobe)
2020-12-22 Alin Tomescu
问题：
- 文件外包
- set membership
- anti-entropy：在不可靠信道上传递文件
	- 将文件划分为块 -> 然后

Merkle Tree 是 collision-resistant hash function
- Merkle proof
## Polynomials over a field
**定理**：度为 $d$ 的多项式最多 $d$ 个根（field 中）
> ring 上可能有超过 d 个根
> - 如：环$\mathbb{Z}_{12}$
> 	- $2X= 4\pmod{12}$ 有 2 个根 $2,8$ 

**Proof**
- **Claim**：若 $deg(P)\ge 1$ 并且 $P(a)=0$ 则存在多项式 $Q$ 使得 $P=(X-a)Q,deg(Q)<deg(P)$ 
> 证明这个 claim
> - 当 $d=1$ 时：
> 	- 由于在 field 中，则 $a=(p_0)(p_1)^{-1}$，并且 $Q=p_1$ 是一个 non-trivial degree zero 多项式，使得 $P=(X-a)Q$ 成立
> - 当 $d>1$ 时：
> 	- 定义一个新多项式 $P'=P-p_dX^{d-1}(X-a)$, $p_d$ 是 $P$ 的最大系数

## Range proofs from Polynomial commitments
[Range Proofs from Polynomial Commitments, Re-explained](https://decentralizedthoughts.github.io/2020-03-03-range-proofs-from-polynomial-commitments-reexplained/#fn:KZG10a)
2020-3-3 Alin Tomescu

从多项式承诺中构造 ZK range proof
Statement：prover 有 $z\in\mathbb{Z}_p$ ，verifier 有 $z$ 的承诺，prover 要证明 $0\le z\le 2^n$ 
- 使用 KZG 来实例化

prover 做的事情
1. 承诺两个度为 $n+1$ 的多项式
2. 证明 3 个 evaluation

首先选择一个多项式 $f$ 使得 $f(1)=z$ 然后计算对应的承诺 $PC(f)$
$z$ 的二进制分解：$z=\sum_{i=0}^{n-1} 2^i\cdot z_i$ 为 $z_0,\dots,z_{n-1}$ 
- P 将 $z$ 编码为度为 $n-1$ 的多项式 $g$ 
	- $g(\omega^{n-1})=z_{n-1}$ 
	- $g(\omega^{i})=2g_{\omega^{i+1}}+z_i,\forall i=n-2,\dots,0$ 
	 - $g(1)=z$ 
- $g$ 可以使用 FFT 计算
- 然后使用多项式承诺产生对 $g$ 的承诺 $PC(g)$

为了证明 $z$ 在 range 内，prover 需要证明 3 个条件
1. $g(1)=f(1)$
2. $g(\omega^{n-1})\in\{0,1\}$ 
3. $g(X)-2g(X\omega)\in \{0,1\},\forall X\in H / \{\omega^{n-1}\}$ 
> 等价于
> - $g(1)=z$
> - $z_{n-1}$ 是二进制值
> - $z_i$ 是二进制值 $i\in[0,n-1)$ 和 $z=\sum_{i=0}^{n-1}z_i$ 

然后证明 3 个多项式 evaluation
1. $\omega_1(X)=(g-f)\cdot (\frac{X^n-1}{X-1})$
2. $\omega_2(X)=g(1-g)\cdot (\frac{X^n-1}{X-\omega^{n-1}})$
3. $\omega_3(X)=[g(X)-2g(X\omega)]\cdot[1-g(X)+2g(X\omega)]\cdot (X-\omega^{n-1})$ 

> 证明
> 1. $g(1)=f(1)$ 等价于 $\omega_1(X)=(g-f)\cdot (\frac{X^n-1}{X-1})$
	2. $g(\omega^{n-1})\in\{0,1\}$ 等价于 $\omega_2(X)=g(1-g)\cdot (\frac{X^n-1}{X-\omega^{n-1}})$
	3. $g(X)-2g(X\omega)\in \{0,1\},\forall X\in H / \{\omega^{n-1}\}$ 等价于 $\omega_3(X)=[g(X)-2g(X\omega)]\cdot[1-g(X)+2g(X\omega)]\cdot (X-\omega^{n-1})$ 


> [!info] 证明
> 1. 证明
> 	1. => $\omega_1(X)$ 在 $H/w^0$ 都为 $0$，在 $\omega^0$ 上时，因为 $g(1)=f(1)$ 使得 $\omega^0$ ，因此 $H$ 上的 $\omega_1(X)=0$ 
> 	2. <= 因为 $H$ 上 $\omega_1(X)=0$ ，因为在 $H/\omega^0$ 上已经为 0 ，所以只有当 $g(1)=f(1)$

然后使用 random linear combination：$\tau\in\mathbb{F}_p$
$$
R(X)=\omega_1(X)+\tau\omega_2(X)+\tau^2\omega_3(X)=0,\forall X\in H
$$

然后 Prover 将 $R(X)$ 除以 $X^n-1$ 产生商多项式 $q(X)$
Prover 证明 $\omega(X)=R(X)-q(X)\cdot (X^n-1)=0$ 
- 等价于 $R(X)=0,\forall X\in H$ 

# 共识


# 区块链