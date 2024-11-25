---
title:  Git 的底层工作原理
tags: Archive git configuration 
# date: 2024-05-15 10:41:17
# sidebar:
#  nav: llm
# published: false
# aside:
#  toc: true
---
基本的存储对象、commit的工作原理、分支/标签的工作原理、不同类型的merge(rebase)
# Git

## 存储库 Repositories
Git 存储库底层是一个 KV 数据存储，在其中存储以下内容：
- Blob：Git中最基本的数据类型，通常是文件的二进制表示
- Tree 对象：有点类似于目录，可以包含指向 Blob/其他 Tree 的指针
- Commit 对象：指向一个 Tree 对象的指针 + 一些元数据（作者信息、任何父commit）
- Tag 对象：指向一个 Commit 对象的指针 + 一些元数据
- Reference：指向一个对象的指针（通常是commit/tag objects）

# 参考

https://wildlyinaccurate.com/a-hackers-guide-to-git/