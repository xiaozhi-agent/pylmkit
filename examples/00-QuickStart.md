# PyLMKit QuickStart

## 0.Install

```python
pip install -U pylmkit --user
```

## 1.Set API KEY


- A convenient method is to create a new .env file and configure all API key information within it, enabling easy utilization of different models. The format of the .env file is as follows:

```python
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

The method to load the .env file is as follows (it is recommended to place the .env file in the same path as your running .py file).

```python
from dotenv import load_dotenv

# load .env
load_dotenv()
```

- Another method is to configure it through os.environ. Here's an example.
```python
import os


# openai
os.environ['openai_api_key'] = ""

# 百度
os.environ['qianfan_ak'] = ""
os.environ['qianfan_sk'] = ""
```

## 2.Use LLM Model

The LLM model can be imported using `PyLMKit` and also supports importing models with `LangChain`. Importing other models:

```python
from pylmkit.llms import ChatQianfan  # 百度-千帆
from pylmkit.llms import ChatSpark  # 讯飞-星火
from pylmkit.llms import ChatZhipu  # 清华-智谱
from pylmkit.llms import ChatHunyuan  # 腾讯-混元
from pylmkit.llms import ChatBaichuan  # 百川
from pylmkit.llms import ChatTongyi  # 阿里-通义
from pylmkit.llms import ChatOpenAI  # OpenAI


model = ChatOpenAI()

# 普通模式
res = model.invoke(query="如何学习python？")
print(res)

# 流式模式
res = model.stream(query="如何学习python？")
for i in res:
    print(i)

```

## 3.RolePlay App

- role template

Users can adjust the role template according to their own circumstances. In the template, `{memory}` represents the location where context memories are placed, `{search}` represents the content of the search engine, and `{query}` represents the user's input question.

- return

The algorithm returns two values: "response" and "refer." The "response" represents the content returned, while "refer" refers to the citation information, such as the webpage citation when using a search engine.

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
    return_language='中文'
)

while True:
    query = input("input...")
    response, refer = rp.invoke(query)
    print(response)


```

## 4.Run in Streamlit Web 

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
    return_language='中文'
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

```python
streamlit run main.py
```

