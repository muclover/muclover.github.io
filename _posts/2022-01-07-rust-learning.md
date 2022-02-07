---
tags: number-theory group-theory
title: Basic Group Theory
#published: false
sidebar:
    nav: cryptomat
---

<!-- TODO: totient; gcd's -->

## Multiplicative inverses modulo $m$

The multiplicative group of integers modulo $m$ is defined as:
\begin{align}
    \Z_m^* = \\{a\ |\ \gcd(a,m) = 1\\}
\end{align}
But why?
This is because Euler's theorem says that:
\begin{align}
\gcd(a,m) = 1\Rightarrow a^{\phi(m)} = 1
\end{align}
This in turn, implies that every element in $\Z_m^\*$ has an inverse, since:
\begin{align}
a\cdot a^{\phi(m) - 1} &= 1
\end{align}
Thus, for a prime $p$, all elements in $\Z_p^\* = \\{1,2,\dots, p-1\\}$ have inverses.
Specifically, the inverse of $a \in \Z_p^*$ is $a^{p-2}$.