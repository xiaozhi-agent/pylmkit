# PyLMKit

**pylmkit** 是一个旨在构建或集成具有实际价值的大模型（LM）应用程序的项目，旨在帮助用户快速构建符合其业务需求的应用程序。


## 快速安装
```bash
pip install -U pylmkit
```

## 文档

- [English document](http://en.pylmkit.cn)
- [中文文档](http://zh.pylmkit.cn)


## 功能

- 角色扮演：通过设置角色模板并结合在线搜索、记忆和知识库功能，实现了典型的对话类的功能应用。
- 其他功能也在不断更新……

## 快速开始

**设置 API KEY**

- 一个方便的方法是创建一个新的.env文件，并在其中配置所有的API密钥信息，从而方便地使用不同的模型。.env文件的格式如下：

```text
# OpenAI
openai_api_key = ""

# 百度-千帆
QIANFAN_AK = ""
QIANFAN_SK = ""

# 阿里-通义
DASHSCOPE_API_KEY = ""

# 科大讯飞-星火
spark_appid = ""
spark_apikey = ""
spark_apisecret = ""
spark_domain = "generalv3"

# 清华-智谱AI
zhipu_apikey = ""

# 百川
baichuan_api_key = ""
baichuan_secret_key = ""

# 腾讯-混元
hunyuan_app_id = ""
hunyuan_secret_id = ""
hunyuan_secret_key = ""
```
加载.env文件的方法如下（建议将.env文件放置在与您运行的.py文件相同的路径下）。
```python
from dotenv import load_dotenv

# load .env
load_dotenv()
```
- 另一种方法是通过os.environ进行配置，下面是一个例子：
```python
import os


# openai
os.environ['openai_api_key'] = ""

# 百度
os.environ['qianfan_ak'] = ""
os.environ['qianfan_sk'] = ""
```

**在Python中运行Demo**
```python
from dotenv import load_dotenv
from pylmkit.app import RolePlay
from pylmkit.llms import ChatOpenAI
from pylmkit.memory import MemoryHistoryLength
from pylmkit.llms import ChatQianfan


# load .env
load_dotenv()

# load llm model
model = ChatOpenAI()
# model = ChatQianfan(model="ERNIE-Bot-turbo")

# memory type
memory = MemoryHistoryLength(memory_length=500)

# roleplay: Enable memory and search functions.
# rp = RolePlay(
#     role_template="{memory}\n {search}\n User question :{query}", 
#     llm_model=model,
#     memory=memory,
#     online_search_kwargs={'topk': 2},
# )

# roleplay: Only activate memory function.
rp = RolePlay(
    role_template="{memory}\n User question :{query}", 
    llm_model=model,
    memory=memory,
    online_search_kwargs={},
)

while True:
    query = input("input...")
    response, refer = rp.invoke(query)
    print(response)
    

```
- llm模型

LLM模型可以使用`PyLMKit`导入，也支持使用`LangChain`导入模型。导入其他模型例子:

```python
from pylmkit.llms import ChatQianfan  # 百度-千帆
from pylmkit.llms import ChatSpark  # 讯飞-星火
from pylmkit.llms import ChatZhipu  # 清华-智谱
from pylmkit.llms import ChatHunyuan  # 腾讯-混元
from pylmkit.llms import ChatBaichuan  # 百川
from pylmkit.llms import ChatTongyi  # 阿里-通义

```

- 角色模板

用户可根据自身情况调整角色模板。在模板中，`{memory}` 表示上下文记忆的位置，`{search}` 表示搜索引擎的内容，`{query}` 表示用户输入的问题。

- 返回值

该算法返回两个值:“response”和“reference”。“response”表示返回的内容，“reference”表示引用信息，例如使用搜索引擎时对网页的引用。

**在Streamlit web中运行Demo**

- 步骤1: 创建一个新的.py文件，例如main.py。
```python
from pylmkit import BaseWebUI
from dotenv import load_dotenv
from pylmkit.app import RolePlay
from pylmkit.llms import ChatOpenAI
from pylmkit.memory import MemoryHistoryLength
from pylmkit.llms import ChatQianfan


# load .env
load_dotenv()

# load llm model
model = ChatOpenAI()
# model = ChatQianfan(model="ERNIE-Bot-turbo")

# memory type
memory = MemoryHistoryLength(memory_length=500, streamlit_web=True)  # set streamlit_web=True

# roleplay: Only activate memory function.
rp = RolePlay(
    role_template="{memory}\n User question :{query}", 
    llm_model=model,
    memory=memory,
    online_search_kwargs={},
)

# init web
web = BaseWebUI()
web.run(
    obj=rp.invoke,  # Designated main function.
    input_param=[{"label": "User input", "name": "query", "type": "chat"},  # type: chat text string bool float ...
                 ],
    output_param=[{'label': 'response content', 'name': 'ai', 'type': 'chat'},
                  {'label': 'refer info', 'name': 'refer', 'type': 'refer'}  # type: chat refer text string bool float ...
                  ]
)

```
- 步骤2: 运行web程序

在与main.py相同目录的终端命令行中，输入

```text
streamlit run main.py
```

## 开源协议

Apache License Version 2.0





