---
title: vscode 如何配置粘贴图片的保存路径
tags: Archive vscode configuration 
# date: 2024-05-15 10:41:17
# sidebar:
#  nav: llm
# published: false
# aside:
#  toc: true
---

现在用的博客网站的图片默认是渲染后的位置加载的，为了简单起见，放在根目录下的 `/images/` 中，但由于vscode启动了安全策略，只允许相对路径，因此无法粘贴到根目录。
> 举个例子，一篇2024-11-11的文章会渲染到 muclover.github.io/2024/11/11 下，如果将粘贴目录设置到和 .md 文件相同子目录 images 下，那么最终渲染出来的文章，会去 muclover.github.io/2024/11/11 下寻找图片

**启用下列设置**: 可以在vscode的设置中搜素 copyfile
```json
“markdown.copyFiles.destination”：{
    "**/*.md" : "${documentWorkspaceFolder}/images/${documentBaseName}/"
}
```
- `documentWorkspaceFolder`: 工作区
- `documentBaseName`: .md 文档的文件名

这样可以产生 `../images/documentbaseName/image-1.png` 这种样式，由于 `_posts` 是二级目录，每次粘贴后再删除 `..` 保留 `/` 就可以了
> 或者也可以在写完文章后，写个脚本在提交前执行