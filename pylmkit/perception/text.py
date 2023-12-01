from abc import ABC

from typing import Any, Optional, Union, Sequence, Dict
from pylmkit.perception.directory import DirectoryLoader
from pylmkit.perception.directory import UnstructuredFileLoader
from langchain.document_loaders import WebBaseLoader
from pylmkit.utils.data_utils import text_as_document, dict_as_document, document_as_dict
from pylmkit.core.base import BaseKnowledgeBase
from pylmkit.perception.directory import RecursiveCharacterTextSplitter
from pathlib import Path


class Text2Document(BaseKnowledgeBase):
    """
    td = Text2Document(texts=['2222222', '5555555555'], metadatas=[{}, {}])
    a = td.load(mode='dict')
    print(a)
    """

    def __init__(self, init_documents=None):
        super().__init__(init_documents=init_documents)

    @classmethod
    def get(cls, texts, metadatas=None, types="Document", is_return=True, return_mode='doc', extend=True):
        data = text_as_document(texts=texts, metadatas=metadatas, types=types)
        cls()._base(documents=data, is_return=is_return, return_mode=return_mode, extend=extend)


class Dict2Document(BaseKnowledgeBase):
    def __init__(self, init_documents=None):
        super().__init__(init_documents=init_documents)

    @classmethod
    def get(cls, doc_dict, is_return=True, return_mode='doc', extend=True):
        data = dict_as_document(doc_dict)
        cls()._base(documents=data, is_return=is_return, return_mode=return_mode, extend=extend)


class BaseDocument(BaseKnowledgeBase):
    def __init__(self, init_documents=None):
        super().__init__(init_documents=init_documents)


class BaseSplitter(BaseKnowledgeBase):

    def __init__(self, splitter=None, chunk_size=500, chunk_overlap=100, **kwargs):
        if splitter is None:
            self.splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, **kwargs)
        else:
            self.splitter = splitter

    def get_split_documents(self, documents, return_mode='doc'):
        self.splitter_documents.extend(self.splitter.split_documents(documents))
        self._base_return(documents=self.splitter_documents, return_mode=return_mode)

    def get_split_text(self, text, return_mode='doc'):
        self.splitter_documents.extend(self.splitter.split_text(text))
        self._base_return(documents=self.splitter_documents, return_mode=return_mode)

    def get_split_texts(self, texts, return_mode='doc'):
        for text in texts:
            self.splitter_documents.extend(self.splitter.split_text(text))
        self._base_return(documents=self.splitter_documents, return_mode=return_mode)

    def _base_return(self, documents, return_mode='doc'):
        if return_mode == 'doc':
            return documents
        else:
            return document_as_dict(documents)


class WebLoader(BaseKnowledgeBase):
    """
    x = WebLoader(web_path="https://www.espn.com/")
    a = x.load()
    x.save_splitter_documents('qqqqq.yaml', chunk_size=20, chunk_overlap=10)
    print(a)
    b = x.split(chunk_size=100, chunk_overlap=20)
    print(b)
    """

    def __init__(self,
                 path: Union[str, Sequence[str]] = "",
                 default_parser: str = "html.parser",
                 requests_kwargs: Optional[Dict[str, Any]] = None,
                 requests_per_second: int = 2,
                 raise_for_status: bool = False,
                 bs_get_text_kwargs: Optional[Dict[str, Any]] = None,
                 bs_kwargs: Optional[Dict[str, Any]] = None,
                 header_template: Optional[dict] = None,
                 init_documents=None,
                 **kwargs
                 ):
        super().__init__(init_documents=init_documents)
        data = WebBaseLoader(web_path=path,
                             default_parser=default_parser,
                             requests_kwargs=requests_kwargs,
                             requests_per_second=requests_per_second,
                             raise_for_status=raise_for_status,
                             bs_get_text_kwargs=bs_get_text_kwargs,
                             bs_kwargs=bs_kwargs,
                             header_template=header_template,
                             **kwargs
                             ).load()
        self._base(documents=data, is_return=False, extend=True)

    def get(self,
            is_return=True,
            return_mode='doc',
            extend=True,
            ):
        result = self._base(documents=self.documents, is_return=is_return, return_mode=return_mode, extend=extend)
        if is_return:
            return result


class DocumentLoader(BaseKnowledgeBase):
    """
    dgl = DocumentGlobLoader(path='./',
                         # suffixes=['.txt', '.py', '.json'],  # 只加载指定格式的文件
                         show_progress=True,
                         silent_errors=True,  # 为 True 时，忽略报错
                         )
    a = dgl.load()
    print(len(a), a)
    b = dgl.split(chunk_size=100, chunk_overlap=50)
    print(len(b), b)
    """
    def __init__(self,
                 path: str,
                 loader_cls=None,
                 loader_kwargs: Union[dict, None] = None,
                 glob: str = "**/[!.]*",
                 suffixes: Optional[Sequence[str]] = None,
                 recursive: bool = False, show_progress: bool = True,
                 use_multithreading: bool = True,
                 max_concurrency: int = 10,
                 silent_errors: bool = True,
                 load_hidden: bool = False,
                 init_documents=None,
                 **kwargs
                 ):
        super().__init__(init_documents=init_documents)
        if loader_kwargs is None:
            loader_kwargs = {}
        if Path(path).is_dir():  # is dir?
            data = DirectoryLoader(path=path,
                                   glob=glob,
                                   suffixes=suffixes,
                                   loader_cls=loader_cls,
                                   loader_kwargs=loader_kwargs,
                                   recursive=recursive,
                                   show_progress=show_progress,
                                   use_multithreading=use_multithreading,
                                   max_concurrency=max_concurrency,
                                   silent_errors=silent_errors,
                                   load_hidden=load_hidden,
                                   **kwargs
                                   ).load()
            self._base(documents=data, is_return=False, extend=True)
        else:
            if loader_cls is None:
                loader_cls = UnstructuredFileLoader
            data = loader_cls(str(path), **loader_kwargs).load()
            self._base(documents=data, is_return=False, extend=True)

    def get(self,
            is_return=True,
            return_mode='doc',
            extend=True,
            ):
        result = self._base(documents=self.documents, is_return=is_return, return_mode=return_mode, extend=extend)
        if is_return:
            return result


