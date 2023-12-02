# PyLMKit

[简体中文版 README](https://github.com/52phm/pylmkit/blob/main/README_zh.md)

**pylmkit** is a project aimed at building or integrating Large Model (LM) applications with practical value. It is designed to assist users in quickly constructing applications tailored to their own business needs.

## Quick Install
```bash
pip install -U pylmkit
```

## Document

[链接文本](http://app.pylmkit.cn){:target="_blank" rel="noopener"}

- <a href="http://app.pylmkit.cn" target="_blank">PyLMKit应用（online application）</a>
- <a href="http://en.pylmkit.cn" target="_blank">English document</a>
- <a href="http://zh.pylmkit.cn" target="_blank">中文文档</a>


## Functionality

- RolePlay：By setting up role templates and combining online search, memory, and knowledge base functionalities, we achieve typical conversational applications.Role-playing is a fundamental and essential feature in various major model enterprise apps. Nowadays, many underlying logics of functions such as `short video copywriting`, `Little Red Book copywriting`, and `emotionally intelligent circle of friends` are based on setting different role templates in role-playing.

    - [Example PyLMKit RolePlay: Using Tutorials](https://github.com/52phm/pylmkit/blob/main/examples/00-How-to-use-RolePlay.ipynb)

![PyLMKit RolePlay](https://github.com/52phm/pylmkit/blob/main/docs/images/RolePlay.png)

- RAG：RAG (Retrieval-Augmented Generation) is a method that utilizes knowledge base retrieval to provide content relevant to user queries, thereby enhancing the accuracy and specificity of the model's answers. RAG encompasses local knowledge bases, web-based knowledge bases, and database knowledge bases. Currently, pylmkit supports the rapid construction of local and web-based knowledge bases.

  **PyLMKit has designed four RAG functionalities**

  - DocRAG: Knowledge base based on local documents.
  - WebRAG: Knowledge base based on web pages.
  - DBRAG: Knowledge base based on databases.
  - MemoryRAG: Knowledge base based on memory.

[Example PyLMKit RAG: Using Tutorials](https://github.com/52phm/pylmkit/blob/main/examples/01-How-to-use-RAG.ipynb)

![PyLMKit RAG](https://github.com/52phm/pylmkit/blob/main/docs/images/RAG.png)

- Other features are constantly being updated...

  

## QuickStart

**Set API KEY**

- A convenient method is to create a new .env file and configure all API key information within it, enabling easy utilization of different models. The format of the .env file is as follows:

```python
openai_api_key = ""  # OpenAI

QIANFAN_AK = ""  # 百度-千帆
QIANFAN_SK = ""

DASHSCOPE_API_KEY = ""  # 阿里-通义

spark_appid = ""  # 科大讯飞-星火
spark_apikey = ""
spark_apisecret = ""
spark_domain = "generalv3"

zhipu_apikey = ""  # 清华-智谱AI

baichuan_api_key = ""  # 百川
baichuan_secret_key = ""

hunyuan_app_id = ""  # 腾讯-混元
hunyuan_secret_id = ""
hunyuan_secret_key = ""
```

The method to load the .env file is as follows (it is recommended to place the .env file in the same path as your running .py file).

```python
from dotenv import load_dotenv

# load .env
load_dotenv()
```

- Another method is to configure it through os.environ. Here's an example.

```python
import os


os.environ['openai_api_key'] = ""  # openai

os.environ['qianfan_ak'] = ""  # 百度
os.environ['qianfan_sk'] = ""
```

**A demo running in Python.**


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
    return_language='English'
)

while True:
    query = input("input...")
    response, refer = rp.invoke(query)
    print(response)
    

```

- llm model

The LLM model can be imported using `PyLMKit` and also supports importing models with `LangChain`. Importing other models:

```python
from pylmkit.llms import ChatQianfan  # 百度-千帆
from pylmkit.llms import ChatSpark  # 讯飞-星火
from pylmkit.llms import ChatZhipu  # 清华-智谱
from pylmkit.llms import ChatHunyuan  # 腾讯-混元
from pylmkit.llms import ChatBaichuan  # 百川
from pylmkit.llms import ChatTongyi  # 阿里-通义

```

- role template

Users can adjust the role template according to their own circumstances. In the template, `{memory}` represents the location where context memories are placed, `{search}` represents the content of the search engine, and `{query}` represents the user's input question.

- return

The algorithm returns two values: "response" and "refer." The "response" represents the content returned, while "refer" refers to the citation information, such as the webpage citation when using a search engine.


**Running in the Streamlit web**


- step1: Create a new .py file, such as main.py.


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
    return_language='English'
)

# init web
web = BaseWebUI()
web.run(
    obj=rp.invoke,  # Designated main function.
    input_param=[{"label": "User input", "name": "query", "type": "chat"},  # type, chat text string bool float ...
                 ],
    output_param=[{'label': 'response content', 'name': 'ai', 'type': 'chat'},
                  {'label': 'refer info', 'name': 'refer', 'type': 'refer'}  # type, chat refer text string bool float ...
                  ]
)

```

- step2: run web


In the terminal command line in the same directory as main.py, enter 


```bash
streamlit run main.py
```


## LICENSE

Apache License Version 2.0





