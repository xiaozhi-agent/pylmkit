import os
from zhipuai import ZhipuAI


class ChatZhipu(object):
    def __init__(self, zhipu_apikey="", model="glm-4", temperature=0.95, top_p=0.7):
        self.api_key = os.environ.get("zhipu_apikey", zhipu_apikey)
        self.model = model
        self.temperature = temperature
        self.top_p = top_p

    def invoke(self, query, system_prompt="You need to answer user questions", **kwargs):
        client = ZhipuAI(api_key=self.api_key)  # 请填写您自己的APIKey
        response = client.chat.completions.create(
            model=self.model,  # 填写需要调用的模型名称
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            stream=False,
            temperature=self.temperature,
            top_p=self.top_p,
            **kwargs
        )
        return response.choices[0].message.content

    def stream(self, query, system_prompt="You need to answer user questions", **kwargs):
        client = ZhipuAI(api_key=self.api_key)  # 请填写您自己的APIKey
        response = client.chat.completions.create(
            model=self.model,  # 填写需要调用的模型名称
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            stream=True,
            temperature=self.temperature,
            top_p=self.top_p,
            **kwargs
        )
        for chunk in response:
            yield chunk.choices[0].delta.content
