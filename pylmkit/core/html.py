from pylmkit.core.prompt import input_prompt

init_css = '''
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .css-z5fcl4 {
        width: 100%;
        padding: 1rem 1rem 1rem;  # 默认 6 1 10，改成1 1 1，修改页面顶部的空白
        padding-top: 0rem;  // 默认6，改成0，修改页面顶部的空白
        padding-right: 2rem;
        padding-bottom: 10rem;
        padding-left: 1rem;
        min-width: auto;
        max-width: initial;
    }
    #logo1 {
                position: fixed;
                display: flex;
                right: 40px;
                top: 20px;
                align-items: center;
            }
    #logo1 img {
      width: 30px;
      margin-right: 10px;
      border-radius: 50%; /* 添加 border-radius 属性 */
    }
    #logo2 {
                    position: fixed;
                    display: flex;
                    right: 80px;
                    top: 20px;
                    align-items: center;
                }
    #logo2 img {
        width: 30px;
        margin-right: 80px;
        border-radius: 50%;
    }
    /* 这个选择器更具体，可以覆盖Streamlit默认样式 */
    footer{
      visibility: hidden;
    }
    /* 在新的div标签中添加你自己的内容 */
    div.my-footer {
      position: fixed;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 50px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      background-color: #333;
    }

</style>
'''

init_footer = '''
<div class="my-footer">{}</div>
'''

init_logo = '''
<div id="{logo_id}">
    <a href="{link}">
        <img src="{logo_rul}" />
    </a>
    <span>{logo_title}</span>
</div>
'''

_zh = input_prompt(
    _title="PyLMKit",
    _page_icon="😄",
    _sidebar_title="😄 PyLMKit",
    _refer_name="引用信息",
    _greetings="您好，我能为您做些什么?",
    _placeholder="请输入您的消息...",
    _footer_describe="Copyright © 2023 PyLMKit  |  Make with Streamlit",
    _sidebar_describe='''
**pylmkit**: 帮助用户快速构建实用的大模型应用! [pylmkit](https://github.com/52phm/pylmkit)

- 开源协议 <br>Apache License 2  [detail](https://www.apache.org/licenses/LICENSE-2.0)
- 下载安装
```bash
pip install pylmkit -U
```
- 学习教程<br>
    - [English document](http://en.pylmkit.cn) 
    - [中文文档](http://zh.pylmkit.cn)
''',
    _logo1=input_prompt(
        logo_id="logo1",
        link="http://app.pylmkit.cn",
        logo_rul="https://img1.baidu.com/it/u=2672705872,739783853&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500",
        logo_title="pylmkit"
    ),
    _logo2=input_prompt(
        logo_id="logo2",
        link="https://github.com/52phm/pylmkit",
        logo_rul="https://github.githubassets.com/favicons/favicon.svg",
        logo_title=""
    ),

)

_en = input_prompt(
    _title="PyLMKit",
    _page_icon="😄",
    _sidebar_title="😄 PyLMKit",
    _greetings="How can I help you?",
    _placeholder="Your message...",
    _refer_name="Citation Information",
    _footer_describe="Copyright © 2023 PyLMKit  |  Make with Streamlit",
    _sidebar_describe='''
**pylmkit**: Help users quickly build practical large model applications! [pylmkit](https://github.com/52phm/pylmkit)

- LICENSE <br>Apache License 2  [detail](https://www.apache.org/licenses/LICENSE-2.0)
- How to install?
```bash
pip install pylmkit -U
```
- How to use?<br>
    - [English document](http://en.pylmkit.cn) 
    - [中文文档](http://zh.pylmkit.cn)
''',
    _logo1=input_prompt(
        logo_id="logo1",
        link="http://app.pylmkit.cn",
        logo_rul="https://img1.baidu.com/it/u=2672705872,739783853&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500",
        logo_title="pylmkit"
    ),
    _logo2=input_prompt(
        logo_id="logo2",
        link="https://github.com/52phm/pylmkit",
        logo_rul="https://github.githubassets.com/favicons/favicon.svg",
        logo_title=""
    ),

)
