from abc import ABC
import time
from pathlib import Path
from tqdm import tqdm
import streamlit as st
from pydantic import Field, BaseModel
from pylmkit.utils.data_utils import read_yaml, read_json, write_yaml, write_json
from pylmkit.utils.data_utils import message_as_string, document_as_dict, dict_as_document
from typing import Any, List, Optional, Type, Union, Sequence, Literal
from pylmkit.perception.directory import BaseLoader
from pylmkit.utils.data_utils import text_as_document
from pylmkit.perception.directory import RecursiveCharacterTextSplitter
from functools import partial
from pylmkit.core.html import init_css, init_footer, init_logo
from pylmkit.core.html import _zh, _en


class BaseMemory(object):
    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    system_prefix: str = "System"

    def __init__(self, init_memory=None, streamlit_web=False):
        self.memory_messages = []
        self.streamlit_web = streamlit_web
        if self.streamlit_web:  # streamlit rerun page, so need cache
            if "memory" not in st.session_state:
                st.session_state["memory"] = self.memory_messages
        if isinstance(init_memory, list):
            self.memory_messages = init_memory
            if self.streamlit_web:
                st.session_state['memory'] = self.memory_messages
        if self.streamlit_web:  # streamlit rerun page, so need cache
            self.memory_messages = st.session_state['memory']

    def add(self, role, content, refer=''):
        """
        role，human ai system
        """
        if role in ['user', 'User', 'USER', 'human', 'Human', 'HUMAN']:
            role = self.human_prefix
        elif role in ['ai', 'Ai', 'AI', 'assistant']:
            role = self.ai_prefix
        elif role in ['sys', 'system', 'System', 'SYS', 'SYSTEM']:
            role = self.system_prefix
        else:
            raise Exception(f"The role `{role}` does not exist")
        self.memory_messages.append(
            {"role": role, "content": content, "refer": refer, "date": time.strftime('%Y-%m-%d %H:%M:%S')})
        if self.streamlit_web:  # streamlit rerun page, so need cache
            st.session_state['memory'] = self.memory_messages

    def save(self, filepath):
        data = self.memory_messages
        if filepath.endswith('.json'):
            write_json(data, filepath=filepath)
        elif filepath.endswith('.yaml') or filepath.endswith('.yml'):
            write_yaml(data, filepath=filepath)
        else:
            raise Exception(f"The file type is not supported")

    def clear(self):
        self.memory_messages = []
        if self.streamlit_web:  # streamlit rerun page, so need cache
            st.session_state['memory'] = self.memory_messages

    def _get(self, mode='message'):
        if mode == 'message':
            return self.memory_messages
        elif mode == 'string':
            return message_as_string(self.memory_messages)
        else:
            raise Exception(f"There is no such `{mode}` mode. Support modes: message, string")


class BaseKnowledgeBase(object):
    def __init__(self, init_documents=None):
        self.documents = []
        self.splitter_documents = []
        if isinstance(init_documents, list):
            self.documents = init_documents

    @classmethod
    def load(cls, filepath, is_return=True, return_mode="doc", extend=True):
        if filepath.endswith('.json'):
            data = read_json(filepath)
        elif filepath.endswith('.yaml') or filepath.endswith('yml'):
            data = read_yaml(filepath)  # data=[{},{}]
        else:
            raise Exception(f"The file type is not supported")
        data_dict_as_document = dict_as_document(data)
        result = cls()._base(documents=data_dict_as_document, return_mode=return_mode, is_return=is_return,
                             extend=extend)
        if is_return:
            return result

    @classmethod
    def add(cls, texts, metadatas=None, is_return=True, return_mode="doc", extend=True, types="Document"):
        data_dict_as_document = text_as_document(texts=texts, metadatas=metadatas, types=types)
        result = cls()._base(documents=data_dict_as_document, return_mode=return_mode, is_return=is_return,
                             extend=extend)
        if is_return:
            return result

    def split(self, splitter=None, chunk_size=500, chunk_overlap=100, return_mode='doc', **kwargs):
        if splitter is None:
            splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, **kwargs)
        else:
            splitter = splitter
        self.splitter_documents = splitter.split_documents(self.documents)
        if return_mode == 'doc':
            return self.splitter_documents
        else:
            return document_as_dict(self.splitter_documents)

    def save_loader_documents(self, filepath):
        self._save(filepath=filepath, documents=self.documents)

    def save_splitter_documents(self, filepath, splitter=None, chunk_size=500, chunk_overlap=100, **kwargs):
        if not self.splitter_documents:
            self.splitter_documents = self.split(splitter=splitter, chunk_size=chunk_size,
                                                 chunk_overlap=chunk_overlap, **kwargs)
        self._save(filepath=filepath, documents=self.splitter_documents)

    def clear(self, mode='doc'):
        if mode == 'doc':
            self.documents = []
        else:
            self.splitter_documents = []

    def _save(self, filepath, documents):
        data = document_as_dict(documents)
        if filepath.endswith('.json'):
            write_json(data, filepath=filepath)
        elif filepath.endswith('.yaml') or filepath.endswith('.yml'):
            write_yaml(data, filepath=filepath)
        else:
            raise Exception(f"The file type is not supported")

    def _base(self, documents, is_return=True, return_mode='doc', extend=True):
        if extend:
            self.documents.extend(documents)  # # dict -> Document
            if is_return:
                if return_mode == 'doc':
                    return self.documents
                else:
                    return document_as_dict(self.documents)
        else:
            # self.documents = documents  # when extend is False, just reset documents
            if is_return:
                if return_mode == 'doc':
                    return documents
                else:
                    return document_as_dict(documents)


def load_memory(filepath):
    if filepath.endswith('.json'):
        data = read_json(filepath)
    elif filepath.endswith('.yaml') or filepath.endswith('yml'):
        data = read_yaml(filepath)
    else:
        raise Exception(f"The file type is not supported")
    return data


def load_multi_memory(path: str, suffixes=None, show_progress: bool = True):
    data = []
    if suffixes is None:
        suffixes = [".yaml", '.json']
    if show_progress:
        for suffixe in tqdm(suffixes):
            for filepath in tqdm(list(Path(path).rglob(f"*{suffixe}"))):
                try:
                    data += load_memory(filepath)
                except Exception as e:
                    raise e
    else:
        for suffixe in suffixes:
            for filepath in list(Path(path).rglob(f"*{suffixe}")):
                try:
                    data += load_memory(filepath)
                except Exception as e:
                    raise e
    return data


def input_widget(input1, input2, type, value):
    if type == "int":
        return st.number_input(format='%d', step=1, **input1)
    if type == "float":
        return st.number_input(format='%f', **input1)
    elif type in ['list', 'List', 'select']:
        return st.selectbox(options=value, **input2)
    elif type == "bool":
        if value in [True, 'True', 'true']:
            options = [True, False]
        else:
            options = [False, True]
        return st.radio(options=options, horizontal=True, **input2)
    elif type == "file":
        uploaded_file = st.file_uploader(**input2)
        if uploaded_file is not None:
            res = str(Path().cwd() / uploaded_file.name)
            with open(res, "wb") as f:
                f.write(uploaded_file.getbuffer())
        else:
            res = None
        return res
    elif type in ['multiselect']:
        return st.multiselect(options=value, **input2)
    else:
        return st.text_input(**input1)


def generate_input_widget(mode="main", **kwargs):  # 在前端生成输入框
    """
    mode, default "main" ,other "sidebar"
    """
    label = kwargs.get('label', "")
    value = kwargs.get('value', None)
    name = kwargs.get('name', None)
    _input1 = {"label": label, "value": value, "key": f"{name}-{label}"}
    _input2 = {"label": label, "key": f"{name}-{label}"}
    _type = kwargs.get('type', None)  # int float bool string chat file
    if mode == 'main':
        return input_widget(
            input1=_input1,
            input2=_input2,
            type=_type,
            value=value
        )
    else:
        with st.sidebar:
            return input_widget(
                input1=_input1,
                input2=_input2,
                type=_type,
                value=value
            )


class BaseWebUI(object):
    def __init__(self,
                 title=None,
                 page_icon=None,
                 layout="centered",
                 language='en',
                 sidebar_title=None,
                 sidebar_describe=None,
                 footer_describe=None,
                 logo1=None,
                 logo2=None,
                 greetings=None,
                 placeholder=None,
                 refer_name=None,
                 ):
        self.title = title
        self.layout = layout
        self.page_icon = page_icon
        self.footer_describe = footer_describe
        self.sidebar_title = sidebar_title
        self.sidebar_describe = sidebar_describe
        self.logo1 = logo1
        self.logo2 = logo2
        self.greetings = greetings
        self.placeholder = placeholder
        self.refer_name = refer_name
        if language in ['zh', '中国', 'china']:
            self.lang = _zh
        else:
            self.lang = _en
        if self.title is None:
            self.title = self.lang.get('_title', '')
        if self.page_icon is None:
            self.page_icon = self.lang.get('_page_icon', None)
        if self.footer_describe is None:
            self.footer_describe = self.lang.get('_footer_describe', '')
        if self.sidebar_title is None:
            self.sidebar_title = self.lang.get('_sidebar_title', '')
        if self.sidebar_describe is None:
            self.sidebar_describe = self.lang.get('_sidebar_describe', '')
        if self.logo1 is None:
            self.logo1 = self.lang.get('_logo1', '')
        if self.logo2 is None:
            self.logo2 = self.lang.get('_logo2', '')
        if self.greetings is None:
            self.greetings = self.lang.get('_greetings', '')
        if self.placeholder is None:
            self.placeholder = self.lang.get('_placeholder', '')
        if self.refer_name is None:
            self.refer_name = self.lang.get('_refer_name', 'refer')

        self.base_page()
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": self.greetings}]
        self.input_kwargs = {}
        st.session_state["output_kwargs"] = {}
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
            # refer setting
            refer = msg.get("refer", False)
            if refer:
                with st.expander(label=self.refer_name, expanded=False):
                    st.markdown(refer, unsafe_allow_html=True)

    def _input(self, content, role="user"):
        st.chat_message(role).write(content, unsafe_allow_html=True)
        msg = {"role": role, "content": content}
        st.session_state.messages.append(msg)

    def _output(self, content, refer=None, role="assistant"):
        st.chat_message(role).write(content, unsafe_allow_html=True)
        if refer:  # refer setting
            with st.expander(label=self.refer_name, expanded=False):
                st.markdown(refer, unsafe_allow_html=True)
        msg = {"role": role, "content": content, "refer": refer}
        st.session_state.messages.append(msg)

    def output_parse(self, output_param, output_result):
        refer = None
        if len(output_param) == 0:
            response = None
        elif len(output_param) == 1:
            response = output_result
            st.session_state["output_kwargs"][output_param[0]['name']] = response
        else:
            response = output_result[0]
            for i, arg in enumerate(output_param):
                st.session_state["output_kwargs"][arg['name']] = output_result[i]
                if arg['type'] == 'chat':
                    response = output_result[i]
                if arg['type'] == 'refer':
                    refer = output_result[i]
        return response, refer

    def run(self, obj, input_param: list, output_param: list):
        chat_variable = ""
        obj = self.wrapper(obj)
        for arg in input_param:
            if arg['type'] != 'chat':
                self.input_kwargs[arg['name']] = generate_input_widget(mode='sidebar', **arg)
            else:
                chat_variable = arg['name']
        if chat_variable:
            if prompt := st.chat_input(placeholder=self.placeholder):
                self.input_kwargs[chat_variable] = prompt
                self._input(content=prompt)
                with st.spinner('pylmkit: Generating, please wait...'):  # 正在生成，请稍候...
                    result = obj(**self.input_kwargs)
                    response, refer = self.output_parse(output_param, result)
                    self._output(content=response, refer=refer)
        else:
            with st.spinner('pylmkit: Generating, please wait...'):  # 正在生成，请稍候...
                result = obj(**self.input_kwargs)
                response, refer = self.output_parse(output_param, result)
                # self._output(content=response, refer=refer)
                with st.expander(label="output", expanded=True):
                    st.json(st.session_state["output_kwargs"], expanded=True)

    def wrapper(self, fun):
        return partial(fun)

    def param(self, label, type, value, mode='sidebar'):
        input_kwargs = {
            "label": label,
            "type": type,
            "value": value
        }
        key = f"{label}-{type}-{str(value)}"
        if key not in st.session_state.keys():
            st.session_state[key] = ""
        renew_value = generate_input_widget(
            mode=mode,
            **input_kwargs
        )
        return renew_value

    def base_page(self):
        st.set_page_config(
            page_title=self.title,
            layout=self.layout,
            page_icon=self.page_icon,
        )
        st.markdown(init_css, unsafe_allow_html=True)
        if self.footer_describe:
            st.sidebar.markdown(init_footer.format(self.footer_describe), unsafe_allow_html=True)
        if self.sidebar_title:
            st.sidebar.title(self.sidebar_title)
        if self.sidebar_describe:
            st.sidebar.markdown(self.sidebar_describe, unsafe_allow_html=True)
        if self.logo2:
            st.markdown(init_logo.format(**self.logo2), unsafe_allow_html=True)
        if self.logo1:
            st.markdown(init_logo.format(**self.logo1), unsafe_allow_html=True)


