# PyLMKit

[简体中文版 README](https://github.com/52phm/pylmkit/blob/main/README_zh.md)

**pylmkit** is a project aimed at building or integrating Large Model (LM) applications with practical value. It is designed to assist users in quickly constructing applications tailored to their own business needs.

## Quick Install
```bash
pip install -U pylmkit
```

## Document

- <a href="http://app.pylmkit.cn" target="_blank">PyLMKit应用（online application）</a>
- <a href="http://en.pylmkit.cn" target="_blank">English document</a>
- <a href="http://zh.pylmkit.cn" target="_blank">中文文档</a>


## Functionality

- RolePlay：By setting up role templates and combining online search, memory, and knowledge base functionalities, we achieve typical conversational applications.Role-playing is a fundamental and essential feature in various major model enterprise apps. Nowadays, many underlying logics of functions such as `short video copywriting`, `Little Red Book copywriting`, and `emotionally intelligent circle of friends` are based on setting different role templates in role-playing.

**Case Tutorial**

[PyLMKit RolePlay: Using Tutorials(English version)](https://github.com/52phm/pylmkit/blob/main/examples/01-RolePlay-APP.md)

[PyLMKit 角色扮演案例教程(简体中文版)](https://github.com/52phm/pylmkit/blob/main/examples/01-角色扮演应用案例.ipynb)


![PyLMKit RolePlay](https://github.com/52phm/pylmkit/blob/main/docs/images/RolePlay.png)

- RAG：RAG (Retrieval-Augmented Generation) is a method that utilizes knowledge base retrieval to provide content relevant to user queries, thereby enhancing the accuracy and specificity of the model's answers. RAG encompasses local knowledge bases, web-based knowledge bases, and database knowledge bases. Currently, pylmkit supports the rapid construction of local and web-based knowledge bases.

  **PyLMKit has designed four RAG functionalities**

  - DocRAG: Knowledge base based on local documents.
  - WebRAG: Knowledge base based on web pages.
  - DBRAG: Knowledge base based on databases.
  - MemoryRAG: Knowledge base based on memory.

**Case Tutorial**

[PyLMKit RAG: Using Tutorials(English version)](https://github.com/52phm/pylmkit/blob/main/examples/02-RAG-Retrieval-Augmented-Generation.md)

[PyLMKit基于知识库检索增强生成RAG案例教程(简体中文版)](https://github.com/52phm/pylmkit/blob/main/examples/02-基于知识库检索增强生成RAG案例.ipynb)


![PyLMKit RAG](https://github.com/52phm/pylmkit/blob/main/docs/images/RAG.png)

- Other features are constantly being updated...

  

## QuickStart

[PyLMKit QuickStart(English version)](https://github.com/52phm/pylmkit/blob/main/examples/00-QuickStart.md)

[PyLMKit 快速开始教程 (简体中文版)](https://github.com/52phm/pylmkit/blob/main/examples/00-快速开始.md)

## LICENSE

Apache License Version 2.0





