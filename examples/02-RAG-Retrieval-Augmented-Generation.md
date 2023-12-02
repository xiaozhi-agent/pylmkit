# RAG: Retrieval Augmented Generation
## 0.Project Information
- date： 2023-12-2
- author：xiaozhi
- TASK: RAG (Retrieval Augmented Generation) is a method of using knowledge base retrieval to provide content relevant to user queries, thereby enhancing the accuracy and specificity of model answers. RAG includes local knowledge base, Web-based knowledge base, memory knowledge base and database knowledge base.

**PyLMKit has designed four RAG functionalities**

    - DocRAG: Knowledge base based on local documents.
    - WebRAG: Knowledge base based on web pages.
    - DBRAG: Knowledge base based on databases.
    - MemoryRAG: Knowledge base based on memory.


- GitHub：[https://github.com/52phm/pylmkit](https://github.com/52phm/pylmkit)
- PyLMKit Tutorial
    - [PyLMKit应用（online application）](http://app.pylmkit.cn)
    - [English document](http://en.pylmkit.cn)
    - [中文文档](http://zh.pylmkit.cn)

**PyLMKit RAG**

![https://github.com/52phm/pylmkit/blob/main/docs/images/RAG.png](images/RAG.png)


## 1.Install

```python
# install
pip install pylmkit -U --user
pip install sentence-transformers --user
pip install faiss-cpu --user
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

## 6.Load knowledge base

**PyLMKit has designed four RAG functionalities**

- DocRAG: Knowledge base based on local documents.
- WebRAG: Knowledge base based on web pages.
- DBRAG: Knowledge base based on databases.
- MemoryRAG: Knowledge base based on memory.

This case introduces `DocRAG` and `WebRAG`, and then shows how to quickly load local documents and web knowledge base.

- Loading local knowledge base: `DocumentLoader`


```python
from pylmkit.perception.text import DocumentLoader


# Loader: You can load a single document or batch load documents in a specified folder
# loader = DocumentLoader(path='./document_test/aaa.txt')
loader = DocumentLoader(path='./document_test', show_progress=True)

# splitter
docs1 = loader.split(chunk_size=200, chunk_overlap=50)

print(len(docs1))
print(docs1[0])
```

      0%|                                                                                            | 0/5 [00:00<?, ?it/s]2023-12-02 12:20:29 - pylmkit.perception.directory - WARNING - Error loading file document_test\loader.yaml: Invalid file document_test\loader.yaml. The FileType.UNK file type is not supported in partition.
     20%|████████████████▊                                                                   | 1/5 [00:01<00:07,  1.90s/it]2023-12-02 12:20:29 - pylmkit.perception.directory - WARNING - Error loading file document_test\qqqqq.yaml: Invalid file document_test\qqqqq.yaml. The FileType.UNK file type is not supported in partition.
    100%|████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:03<00:00,  1.45it/s]

    144
    page_content='电机（俗称“马达”）是指依据电磁感应定律实现电能转换或传递的一种电磁装置。分为电动机（符号为M）和发电机（符号为G）。\n\n中文名电机\n\n外文名Electric machinery\n\n依据原理电磁感应定律\n\n电路中表示电动机为M，发电机为G\n\n定    义电能转换或传递的一种电磁装置\n\n目录\n\n1划分\n\n2直流式\n\n3电磁式\n\n4直流电机\n\n▪他励\n\n▪并励\n\n▪串励\n\n▪复励\n\n5永磁式' metadata={'source': 'document_test\\aaa.txt'}
    

    
    

- Loading web knowledge base: `WebLoader`


```python
from pylmkit.perception.text import WebLoader

# Loader: Can load a web page, can also load a batch of web pages
loader = WebLoader(path='https://zhuanlan.zhihu.com/p/339971541')
# loader = WebLoader(
#     path=[
#         'https://zhuanlan.zhihu.com/p/339971541',
#         'https://zhuanlan.zhihu.com/p/339971541',
        
#     ]
# )

# splitter
docs2 = loader.split(chunk_size=200, chunk_overlap=50)

print(len(docs2))
print(docs2[-1])

```

    2023-12-02 12:20:31 - langchain.document_loaders.web_base - INFO - fake_useragent not found, using default user agent.To get a realistic header for requests, `pip install fake_useragent`.
    

    44
    page_content='，因此相比竞品而言 上 汽魔方电池在各个容量电池包的体积效率转换和重量效率转换都更为出色。上汽魔方电池躺式布局https://www.zhihu.com/video/1549353400738979841编辑于 2022-09-03 11:19动力电池锂电池\u200b赞同 183\u200b\u200b7 条评论\u200b分享\u200b喜欢\u200b收藏\u200b申请转载\u200b' metadata={'source': 'https://zhuanlan.zhihu.com/p/339971541', 'title': '一文读懂汽车动力电池 - 知乎', 'description': '动力电池作为电动汽车的三大件（电池、电机、电控）之一，是整个车辆系统的动力来源，一直以来被视为电动汽车发展的标志性技术，其性能好坏直接关系到车辆续航里程的长短，重要性不言而喻。今天小七带大家拨开迷雾…', 'language': 'zh'}
    

The local knowledge base and web knowledge base can be integrated.


```python
docs = []
docs.extend(docs1)
docs.extend(docs2)
print(len(docs))
```

    188
    

## 7.Load the word vector model

Text is an unstructured data type, so it needs to use word embedding technology to vectorialize text, PyLMKit provides two types of word vector model calls:

- Use a paid word vector model: Tune the word vector model through the API，such as OpenAI的`EmbeddingsOpenAI`，Baidu Qianfan `EmbeddingsQianfan`
- Download the open source model for local free use: Download the model in `huggingface`, such as`EmbeddingsHuggingFace`，`EmbeddingsHuggingFaceBge`和`EmbeddingsHuggingFaceInstruct`

In addition to calling through `PyLMKit`, import via `langchain` is also supported.

In addition, it is worth noting that the accuracy of different word vector models is different, so it is necessary to choose the right word vector model to play a greater role.


```python
# Paid call
from pylmkit.llms import EmbeddingsQianfan  # 百度-千帆-词向量模型
from pylmkit.llms import EmbeddingsOpenAI  # OpenAI-词向量模型

# 本地调用
from pylmkit.llms import EmbeddingsHuggingFace  # 使用 HuggingFace 中开源模型
from pylmkit.llms import EmbeddingsHuggingFaceBge
from pylmkit.llms import EmbeddingsHuggingFaceInstruct


# This case uses a local model, in order to facilitate the use of a small model
embed_model = EmbeddingsHuggingFace(model_name="all-MiniLM-L6-v2")

```

    G:\anzhuangqu\anaconda2023\envs\gradio_env\Lib\site-packages\tqdm\auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html
      from .autonotebook import tqdm as notebook_tqdm
    2023-12-02 12:20:37 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: all-MiniLM-L6-v2
    2023-12-02 12:20:38 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device: cpu
    

## 8.Load vector database

Vector database is undoubtedly a big hot spot this year, because RAG, or vertical domain knowledge Q&A based on local knowledge base, this low-cost and feasible technical solution is particularly hot this year, and vector database as a way to store vectors and retrieve similar documents plays an important role.

The following is a demonstration using the `FAISS` vector database.


```python
from langchain.vectorstores import FAISS

vdb_model = FAISS
```

## 9.Load RAG APP

**PyLMKit has designed four RAG functionalities**

- DocRAG: Knowledge base based on local documents.
- WebRAG: Knowledge base based on web pages.
- DBRAG: Knowledge base based on databases.
- MemoryRAG: Knowledge base based on memory.

RAG is composed of two parts based on knowledge base retrieval and RolePlay role playing, so RAG has the parameters and functions of RolePlay application.


```python
from pylmkit.app import DocRAG
from pylmkit.app import WebRAG


# This is a simple example of a role template that can be designed to suit your situation
role_template = "{ra}\n user question: {query}"  
rag = DocRAG(
    embed_model=embed_model,
    vdb_model=vdb_model,
    llm_model=llm_model,
    corpus=docs,
    role_template=role_template,
    return_language="中文",
    online_search_kwargs={},
    # online_search_kwargs={'topk': 2, 'timeout': 20},  # Search engine configuration, if not enabled, can be set to online_search_kwargs={}
)
```

    Batches: 100%|███████████████████████████████████████████████████████████████████████████| 6/6 [00:06<00:00,  1.02s/it]
    2023-12-02 12:20:44 - faiss.loader - INFO - Loading faiss with AVX2 support.
    2023-12-02 12:20:44 - faiss.loader - INFO - Could not load library with AVX2 support due to:
    ModuleNotFoundError("No module named 'faiss.swigfaiss_avx2'")
    2023-12-02 12:20:44 - faiss.loader - INFO - Loading faiss.
    2023-12-02 12:20:44 - faiss.loader - INFO - Successfully loaded faiss.
    

## 10.Run in python


```python
while True:
    query = input("User query：")
    response, refer = rag.invoke(query, topk=10)  # Use topk to retrieve the most similar =10
    print("\nAI：\n", response)
    print("\nRefer：\n", refer)
```

    User query：电机有哪些类型？
    

    Batches: 100%|███████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 33.42it/s]
    

    >>><<< 10
    
    AI：
     电机主要有以下几种类型：
    
    1. 直流电机：它是一种将直流电能转换为机械能的旋转电机。
    
    2. 交流电机：它是一种将交流电能转换为机械能的旋转电机，最常见的类型是异步电机和同步电机。
    
    3. 无刷电机：它是一种无需机械式转动部件的电机，通常使用直流电源或交流电源驱动。
    
    4. 永磁电机：它使用永久磁铁产生磁场，通常用于高速旋转设备，如吹风机或电动工具。
    
    此外，软启动器通常使用交流电机，因为它没有碳刷和整流子，所以它具有免维护、坚固、应用广的特点。在控制方面，它使用复杂控制技术来达到相当于直流电机的性能。在微处理机和功率组件发展迅速的今天，通过适当控制交流电机的电流分量，可以实现对交流电机的控制并达到类似于直流电机的性能。在某些特定的场合下，软启动器还会提供软停车功能，以避免自由停车引起的转矩冲击。在推广无刷电机的使用和维护时，我们也需要加强宣传和培训工作。
    
    至于你提到的“为什么动力电池偏偏用的是锂电池呢？”这个问题，能量密度是一个重要的考虑因素。锂电池具有较高的能量密度，可以提供更长的行驶距离或工作时间，因此被广泛应用于电动汽车等动力系统中。同时，锂电池的充电和放电性能也较好，适合于大功率和快速充电的应用场景。当然，在选择动力电池时还需要考虑其他因素，如安全性、寿命、成本等。
    
    Refer：
     [1] **document_test\aaa.txt**  固定磁场无刷电机
    
    [2] **document_test\aaa.txt**  弱磁控制：当电机转速超过一定数值后，励磁电流已经相当小，基本不能再调节，此时进入弱磁控制阶段。
    
    [3] **document_test\aaa.txt**  于环境极为恶劣的场合，如潮湿、高温、多尘、腐蚀等场合。所有这些，造成了电机更容易损坏，尤其是过载、短路、缺相、扫膛等故障出现频率最高。
    
    [4] **document_test\aaa.txt**  机床上传统的“旋转电机 +
    
    [5] **document_test\aaa.txt**  三、磁阻同步电动机
    
    [6] **https://zhuanlan.zhihu.com/p/339971541**  电池，就不得不拉回正题，谈谈动力电池，目前市面上电动汽车基本上都采用的是锂离子电池（以下简称锂电池），可能会有很多朋友会问，为什么动力电池偏偏用的是锂电池呢？回答这个问题前，我们先来看看一个概念——能量密度。能量密度（Energy
    
    [7] **document_test\aaa.txt**  定电压，以降低晶闸管的热损耗，延长软启动器的使用寿命，提高其工作效率，又使电网避免了谐波污染。软启动器同时还提供软停车功能，软停车与软启动过程相反，电压逐渐降低，转数逐渐下降到零，避免自由停车引起的转矩冲击。
    
    [8] **document_test\aaa.txt**  控制原理
    
    [9] **document_test\aaa.txt**  到限制。交流电机没有碳刷及整流子，免维护、坚固、应用广，但特性上若要达到相当于直流电机的性能须用复杂控制技术才能达到。现今半导体发展迅速功率组件切换频率加快许多，提升驱动电机的性能。微处理机速度亦越来越快，可实现将交流电机控制置于一旋转的两轴直交坐标系统中，适当控制交流电机在两轴电流分量，达到类似直流电机控制并有与直流电机相当的性能。
    
    [10] **document_test\aaa.txt**  五、加强宣传培训
    
    
    User query：动力电池有哪些分类？
    

    Batches: 100%|███████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 83.53it/s]
    

    >>><<< 10
    
    AI：
     您好！动力电池根据不同标准有不同分类方式，常见分类如下：
    
    1. 按照工作性质可分为：动力电池、牵引电池（含蓄电池）、起动电池；
    2. 按照正极材料种类可分为：钴酸锂电池、锰酸锂电池、三元材料（NCM）电池、磷酸铁锂（LFP）电池；
    3. 按照电池的形状可分为：圆柱形电池、方壳电池、软包电池。
    
    以上是动力电池常见的分类方式，具体到上汽魔方电池，其采用的是躺式布局的锂离子电池，具有能量密度高、体积小、重量轻等优势。同时，上汽魔方电池还具有高低温性能优异、安全性好、寿命长等优势。
    
    以上信息仅供参考，如果您还有疑问，建议咨询专业人士意见。
    
    Refer：
     [1] **https://zhuanlan.zhihu.com/p/339971541**  一文读懂汽车动力电池 -
    
    [2] **https://zhuanlan.zhihu.com/p/339971541**  电池，就不得不拉回正题，谈谈动力电池，目前市面上电动汽车基本上都采用的是锂离子电池（以下简称锂电池），可能会有很多朋友会问，为什么动力电池偏偏用的是锂电池呢？回答这个问题前，我们先来看看一个概念——能量密度。能量密度（Energy
    
    [3] **document_test\aaa.txt**  固定磁场无刷电机
    
    [4] **document_test\aaa.txt**  弱磁控制：当电机转速超过一定数值后，励磁电流已经相当小，基本不能再调节，此时进入弱磁控制阶段。
    
    [5] **document_test\aaa.txt**  直流电动机工作原理
    
    导体受力的方向用左手定则确定。这一对电磁力形成了作用于电枢一个力矩，这个力矩在旋转电机里称为电磁转矩，转矩的方向是逆时针方向，企图使电枢逆时针方向转动。如果此电磁转矩能够克服电枢上的阻转矩（例如由摩擦引起的阻转矩以及其它负载转矩），电枢就能按逆时针方向旋转起来。
    
    [6] **https://zhuanlan.zhihu.com/p/339971541**  ，因此相比竞品而言 上 汽魔方电池在各个容量电池包的体积效率转换和重量效率转换都更为出色。上汽魔方电池躺式布局https://www.zhihu.com/video/1549353400738979841编辑于 2022-09-03 11:19动力电池锂电池​赞同 183​​7 条评论​分享​喜欢​收藏​申请转载​
    
    [7] **document_test\aaa.txt**  二、认真组织电机生产企业执行强制性能效标准
    
    [8] **document_test\aaa.txt**  机床上传统的“旋转电机 +
    
    [9] **document_test\aaa.txt**  到限制。交流电机没有碳刷及整流子，免维护、坚固、应用广，但特性上若要达到相当于直流电机的性能须用复杂控制技术才能达到。现今半导体发展迅速功率组件切换频率加快许多，提升驱动电机的性能。微处理机速度亦越来越快，可实现将交流电机控制置于一旋转的两轴直交坐标系统中，适当控制交流电机在两轴电流分量，达到类似直流电机控制并有与直流电机相当的性能。
    
    [10] **document_test\aaa.txt**  控制原理


## 11.Run in streamlit web

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
    obj=rag.invoke,
    input_param=[{"name": "query", "label": "User input content", "type": "chat"},
                 {"name": "topk", "label": "most similar topk", "type": "int"},
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
