# SparkApi.py
# 针对spark提供SparkApi.py做一些修改
import os
import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import websocket  # 使用websocket_client
from pylmkit.utils.data_utils import stream_print


class WsParam(object):
    # 初始化
    def __init__(self, spark_appid="", spark_apikey="", spark_apisecret="", spark_domain='', spark_url=None):
        self.spark_appid = os.environ.get("spark_appid", spark_appid)
        self.spark_apikey = os.environ.get("spark_apikey", spark_apikey)
        self.spark_apisecret = os.environ.get("spark_apisecret", spark_apisecret)
        self.spark_domain = os.environ.get("spark_domain", spark_domain)
        self.spark_url = os.environ.get("spark_url", spark_url)
        if not self.spark_url:
            self.spark_url = f"ws://spark-api.xf-yun.com/v{self.spark_domain.split('generalv')[-1]}.1/chat"
        self.host = urlparse(self.spark_url).netloc
        self.path = urlparse(self.spark_url).path
        self.Spark_url = self.spark_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.spark_apisecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.spark_apikey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.Spark_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url


class ChatSpark(WsParam):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.answer = ""

    def on_error(self, ws, error):
        """收到websocket错误的处理"""
        print("### error:", error)

    def on_close(self, ws, one, two):
        """收到websocket关闭的处理"""
        print(" ")

    def on_open(self, ws):
        """收到websocket连接建立的处理"""
        thread.start_new_thread(self.send_run, (ws,))

    def send_run(self, ws, *args):
        """发送信息"""
        data = json.dumps(self.gen_params(appid=ws.appid, domain=ws.domain, question=ws.question))
        ws.send(data)

    def on_message(self, ws, message):
        """收到websocket消息的处理"""
        data = json.loads(message)
        code = data['header']['code']
        if code != 0:
            print(f'请求错误: {code}, {data}')
            ws.close()
        else:
            choices = data["payload"]["choices"]
            status = choices["status"]
            content = choices["text"][0]["content"]
            # print(">>>>>>>>>>>", content, end="")  # 打印响应答案
            self.answer += content
            if status == 2:
                ws.close()

    def gen_params(self, appid, domain, question):
        """
        通过appid和用户的提问来生成请参数
        """
        data = {
            "header": {
                "app_id": appid,
                "uid": "1234"
            },
            "parameter": {
                "chat": {
                    "domain": domain,
                    "random_threshold": 0.5,
                    "max_tokens": 2048,
                    "auditing": "default"
                }
            },
            "payload": {
                "message": {
                    "text": question
                }
            }
        }
        return data

    def clear(self):
        self.answer = ""

    def invoke(self, query):
        question = [{'role': 'user', 'content': query}]
        websocket.enableTrace(False)
        wsUrl = super().create_url()
        ws = websocket.WebSocketApp(wsUrl, on_message=self.on_message, on_error=self.on_error,
                                    on_close=self.on_close, on_open=self.on_open)
        ws.appid = self.spark_appid
        ws.question = question
        ws.domain = self.spark_domain
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        result = self.answer
        self.clear()  # reset
        return result

    def stream(self, query, buffer_size=3):
        response = self.invoke(query)
        return stream_print(response, buffer_size=buffer_size)



