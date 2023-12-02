# RolePlay APP
## 0.Project Information
- date： 2023-12-2
- author：xiaozhi
- TASK: By setting up role templates and combining online search, memory, and knowledge base functionalities, typical conversational application features can be implemented. This feature serves as the foundation for large-scale model applications and will be utilized in other functionalities such as RAG in the subsequent stages.
- Function and effect：RolePlay is a fundamental and essential functionality. Nowadays, in the apps of major large-scale model enterprises, you can see that many underlying logics of features such as short video copywriting, Xiaohongshu (Little Red Book) copywriting, and emotionally intelligent social media posts are based on setting different role templates in role-playing.
- GitHub：[https://github.com/52phm/pylmkit](https://github.com/52phm/pylmkit)
- PyLMKit Tutorial
    - [PyLMKit应用（online application）](http://app.pylmkit.cn)
    - [English document](http://en.pylmkit.cn)
    - [中文文档](http://zh.pylmkit.cn)
    
**PyLMKit RolePlay**

![https://github.com/52phm/pylmkit/blob/main/docs/images/RolePlay.png](images/RolePlay.png)


## 1.Install
```python
# install
pip install pylmkit -U --user
```

## 2.Set API KEY

Which big model is applied, set the `API KEY` corresponding to the big model in advance

```python
import os


# openai chatgpt
os.environ['openai_api_key'] = ""

# 百度
os.environ['qianfan_ak'] = ""
os.environ['qianfan_sk'] = ""

# 阿里
os.environ["DASHSCOPE_API_KEY"] = ""

# 科大讯飞-星火
os.environ["spark_appid"] = ""
os.environ["spark_apikey"] = ""
os.environ["spark_apisecret"] = ""
os.environ["spark_domain"] = "generalv3"

# 智谱AI
os.environ['zhipu_apikey'] = ""

```

Or load the set `API KEY` in batch in the `.env` file as follows:

```python
from dotenv import load_dotenv

# load .env
load_dotenv()
```

## 3.Load the large language model

Import large language model, in this case use `Baidu Qianfan` large model as an example to introduce.

```python
from pylmkit.llms import ChatQianfan  # 百度-千帆
from pylmkit.llms import ChatSpark  # 讯飞-星火
from pylmkit.llms import ChatZhipu  # 清华-智谱
from pylmkit.llms import ChatHunyuan  # 腾讯-混元
from pylmkit.llms import ChatBaichuan  # 百川
from pylmkit.llms import ChatTongyi  # 阿里-通义
from pylmkit.llms import ChatOpenAI  # OpenAI

model = ChatQianfan()
```

## 4.Selective memory function

PyLMKit has designed four memory functions, as follows:

- MemoryHistoryLength：Memory history length, emphasizing how long the recent memory content is used;
- MemoryConversationsNumber：Memorizing pairs of numbers, emphasizing the use of recent N groups of conversations as memorized content;
- MemorySummary：Memory summarization, emphasizing concise retrieval of memory;
- Amelia


This case uses the `MemoryHistoryLength` memory function to enable the large language model to remember the context according to this history memory in order to answer the user's questions in a coherent manner. (More on the use of memory can be found in a future topic on Memory.)

```python
from pylmkit.memory import MemoryHistoryLength


memory = MemoryHistoryLength(memory_length=500, streamlit_web=False)  # run in python
# memory2 = MemoryHistoryLength(memory_length=500, streamlit_web=True)  # run in streamlit web
```

## 5.Design role template

Large language model is a `one-to-many` relationship model architecture, where `one represents` the large language model, and `many represents` downstream tasks, such as writing, customer service, data analysis, etc. These are downstream tasks.
Therefore, we need to guide the large language model to complete the specified 'downstream task' efficiently and qualitatively by designing the prompt word template.


Before designing the role template, let's understand some key words that must be fixed in `PyLMKit`:


- `{query}`：Indicates that this is the user input question content;
- `{search}`：Represents the content returned by online real-time search engine search;
- `{memory}`：Representing the contents of memory;
- `{ra}`：Represents the content returned by the knowledge base search.

Let's look at an example of a role template:

```python
# Their location indicates where their content is embedded
role_template = "{memory}\n {search}\n User question:{query}"

# Of course, you can further design the template
role_template = "Historical dialogue content: {memory}\n Similar content searched for:{search} {ra}\n Please answer the questions based on the above:{query}"

model.invoke(query="how to learn python？")
```


The role template determines the quality of the answer of the large language model, so the role template needs to be polished repeatedly to design a high-quality role template, which can achieve twice the result with half the effort.


In addition, it is worth noting that if the keywords of your role template are not in `[query, search, ra, memory]`, then you need to add new variables and variable values, such as:

```python
role_template = "{memory}\n Please recommend me {query} of {topic}"

# Additional keywords can be added like topic=" food ", and multiple keywords can be added in the same steps
model.invoke(query='Beijing', topic="food")
```



```python
role_template = "{memory}\n Please recommend me {query} of {topic}"
```

## 6.Load the role-playing application

RolePlay is a fundamental and important feature. Now in the APP of various large model enterprises, you can see a lot of the underlying logic of these functions such as' short video copy, small red book copy, and high emotional intelligence circle of friends' is based on the role template set in the role playing to achieve.


```python
from pylmkit.app import RolePlay


rp = RolePlay(
    role_template=role_template,  # Role template
    llm_model=model,  # Large language model
    memory=memory,  # Memory 
    # online_search_kwargs={},
    online_search_kwargs={'topk': 2, 'timeout': 20},  # Search engine configuration, if not enabled, can be set to online_search_kwargs={}
    return_language="English"  # Answer the questions in English
)
```

## 7.Run in python


```python
while True:
    query = input("User query：")
    topic = input("User topic：")
    response, refer = rp.invoke(query, topic=topic)
    print("\nAI：", response)
    print("\nRefer\n：", refer)
```

    User query：北京
    User topic：美食
    

    2023-12-02 01:28:27 - httpx - INFO - HTTP Request: POST https://duckduckgo.com "HTTP/2 200 OK"
    2023-12-02 01:28:29 - httpx - INFO - HTTP Request: GET https://links.duckduckgo.com/d.js?q=%E5%8C%97%E4%BA%AC&kl=wt-wt&l=wt-wt&s=0&df=&vqd=4-45222965241755774163610013696327482249&o=json&sp=0&ex=-1 "HTTP/2 200 OK"
    

    
    AI： 北京有很多美食，以下是为您推荐的一些美食：
    
    1. 北京烤鸭：是北京最著名的传统美食，具有独特的皮脆肉嫩、肥而不腻的口味。
    
    2. 炸酱面：是一道非常受欢迎的主食，面条劲道，炸酱味道浓郁，可以搭配各种蔬菜和肉类。
    
    3. 炒肝：是一种传统早点，主要原料是猪大肠和猪肝，口感鲜美，适合早餐食用。
    
    4. 羊肉串：是北京街头巷尾最常见的烧烤之一，肉质鲜嫩，味道鲜美。
    
    5. 豆汁儿：是北京传统特色小吃之一，由绿豆制作而成，味道独特，需要慢慢品尝。
    
    6. 爆肚：是北京传统小吃，口感鲜美，特别适合夏天食用。
    
    7. 涮羊肉：是一种传统的火锅美食，口感鲜美，涮出的羊肉非常嫩滑。
    
    除此之外，北京还有各种烤肉、烧麦、饺子、包子、馄饨等美食，您可以根据自己的口味选择尝试。
    
    Refer
    ： [1] **https://zh.wikipedia.org/wiki/北京市**  北京古迹众多，著名的有紫禁城、天坛、颐和园、圆明园、北海公园等；胡同和四合院作为北京老城的典型民居形式，已经是北京历史重要的文化符号 。北京是中国重要的旅游城镇，被《米其林旅游指南》评为"三星级旅游推荐"（最高级别）目的地 。
    
    [2] **https://baike.baidu.com/item/北京市/126069**  北京市（Beijing），简称"京"，古称燕京、北平，中华民族的发祥地之一，是中华人民共和国首都、直辖市、国家中心城市、超大城市，国务院批复确定的中国政治中心、文化中心、国际交往中心、科技创新中心，中国历史文化名城和古都之一，世界一线城市。截至2023年10月，北京市下辖16个区，总 ...


## Run in streamlit web

To run in terminal: Assuming `.py` file name is `main.py`, then run in terminal:

```bash
streamlit run main.py
```


```python
# main.py
from pylmkit.core.base import BaseWebUI
from pylmkit.memory import MemoryHistoryLength


web = BaseWebUI(language='en')  # Use English websites
memory = MemoryHistoryLength(memory_length=web.param(label="memory length", type='int', value=500),  # Add page interaction parameters
                             streamlit_web=True
                            )

web.run(
    obj=rp.invoke,
    input_param=[{"name": "query", "label": "place", "type": "chat"},
                 {"name": "topic", "label": "topic", "type": "text"},
                 ],
    output_param=[{'label': 'result', 'name': 'response', 'type': 'chat'},
                  {'label': 'reference', 'name': 'refer', 'type': 'refer'}
                  ]
)
```


```python

```


```python

```


```python

```


```python

```


```python

```
