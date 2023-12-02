# PyLMKit

**pylmkit** 是一个旨在构建或集成具有实际价值的大模型（LM）应用程序的项目，旨在帮助用户快速构建符合其业务需求的应用程序。


## 快速安装
```bash
pip install -U pylmkit
```

## 文档

- <a href="http://app.pylmkit.cn" target="_blank">PyLMKit应用（online application）</a>
- <a href="http://en.pylmkit.cn" target="_blank">English document</a>
- <a href="http://zh.pylmkit.cn" target="_blank">中文文档</a>


## 功能

- 角色扮演：通过设置角色模板并结合在线搜索、记忆和知识库功能，实现了典型的对话类的功能应用。RolePlay角色扮演是一种基础功能，也是重要的功能。现在在各大大模型企业的APP中可以看到很多关于`短视频文案、小红书文案、高情商朋友圈`等这些功能的底层逻辑是基于角色扮演中设置不同的角色模板实现的。
  
**案例教程**

[PyLMKit RolePlay: Using Tutorials(English version)](https://github.com/52phm/pylmkit/blob/main/examples/01-RolePlay-APP.md)

[PyLMKit 角色扮演案例教程(简体中文版)](https://github.com/52phm/pylmkit/blob/main/examples/01-角色扮演应用案例.ipynb)


![PyLMKit RolePlay](https://github.com/52phm/pylmkit/blob/main/docs/images/RolePlay.png)

- RAG（Retrieval-Augmented Generation，检索增强生成）是一种利用知识库检索的方法，提供与用户查询相关的内容，从而增强模型答案的准确性和特异性。RAG包括本地知识库、基于网络的知识库、记忆知识库和数据库知识库。

  **PyLMKit设计了四种RAG功能**

  - 基于本地文档的知识库DocRAG
  - 基于网页的知识库WebRAG
  - 基于数据库的知识库DBRAG
  - 基于记忆的知识库MemoryRAG


**Case Tutorial**

[PyLMKit RAG: Using Tutorials(English version)](https://github.com/52phm/pylmkit/blob/main/examples/02-RAG-Retrieval-Augmented-Generation.md)

[PyLMKit基于知识库检索增强生成RAG案例教程(简体中文版)](https://github.com/52phm/pylmkit/blob/main/examples/02-基于知识库检索增强生成RAG案例.ipynb)


![PyLMKit RAG](https://github.com/52phm/pylmkit/blob/main/docs/images/RAG.png)

- 其他功能正在更新中……


## 快速开始

[PyLMKit QuickStart(English version)](https://github.com/52phm/pylmkit/blob/main/examples/00-QuickStart.md)

[PyLMKit 快速开始教程 (简体中文版)](https://github.com/52phm/pylmkit/blob/main/examples/00-快速开始.md)

## 开源协议

Apache License Version 2.0





