from pylmkit.app import RolePlay
import streamlit as st
from pylmkit.core.base import BaseWebUI


class RAGWebUI(BaseWebUI):
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
        super().__init__(
            title=title,
            page_icon=page_icon,
            layout=layout,
            language=language,
            sidebar_title=sidebar_title,
            sidebar_describe=sidebar_describe,
            footer_describe=footer_describe,
            logo1=logo1,
            logo2=logo2,
            greetings=greetings,
            placeholder=placeholder,
            refer_name=refer_name
        )


class ChatDBWebUI(BaseWebUI):
    def __init__(self,
                 language='zh',
                 **kwargs
                 ):

        super().__init__(language=language, **kwargs)
        st.sidebar.title('ChatDB')
        st.sidebar.markdown("与你的结构化数据聊天：支持主流数据库、表格型excel等数据！")



