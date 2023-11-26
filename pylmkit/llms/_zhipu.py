import os
import zhipuai


class ChatZhipu(object):
    def __init__(self, zhipu_apikey="", model="chatglm_turbo", temperature=0.95, top_p=0.7, incremental=True):
        zhipuai.api_key = os.environ.get("zhipu_apikey", zhipu_apikey)
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.incremental = incremental

    def invoke(self, query, **kwargs):
        response = zhipuai.model_api.invoke(
            prompt=[{"role": "user", "content": query}],
            model=self.model,
            temperature=self.temperature,
            top_p=self.top_p,
            incremental=self.incremental,
            **kwargs
        )
        return response['data']['choices'][0]['content']

    def stream(self, query, **kwargs):
        response = zhipuai.model_api.sse_invoke(
            prompt=[{"role": "user", "content": query}],
            model=self.model,
            temperature=self.temperature,
            top_p=self.top_p,
            incremental=self.incremental,
            **kwargs
        )
        '''
          说明：
          add: 事件流开启
          error: 平台服务或者模型异常，响应的异常事件
          interrupted: 中断事件，例如：触发敏感词
          finish: 数据接收完毕，关闭事件流
        '''
        for event in response.events():
            if event.event == "add":
                yield event.data
            elif event.event == "error" or event.event == "interrupted":
                yield event.data
            elif event.event == "finish":
                yield event.data
                yield event.meta
            else:
                yield event.data

