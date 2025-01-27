---
title: gcc 多个版本优先级配置，Python3设置为默认版本
tags: Archive OpenHarmony Configuration
aside:
 toc: true
---

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

Other Solutions: https://stackoverflow.com/questions/38780057/how-to-insert-current-date-time-in-vscode

