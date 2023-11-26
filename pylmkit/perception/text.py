from abc import ABC

from typing import Any, Optional, Union, Sequence, Dict
from pylmkit.perception.directory import DirectoryLoader
from pylmkit.perception.directory import UnstructuredFileLoader
from langchain.document_loaders import WebBaseLoader
from pylmkit.utils.data_utils import text_as_document, dict_as_document, document_as_dict
from pylmkit.core.base import BaseKnowledgeBase
from pylmkit.perception.directory import RecursiveCharacterTextSplitter


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

    def __init__(self, init_documents=None):
        super().__init__(init_documents=init_documents)

    def get(self,
            web_path: Union[str, Sequence[str]] = "",
            is_return=True,
            return_mode='doc',
            extend=True,
            default_parser: str = "html.parser",
            requests_kwargs: Optional[Dict[str, Any]] = None,
            requests_per_second: int = 2,
            raise_for_status: bool = False,
            bs_get_text_kwargs: Optional[Dict[str, Any]] = None,
            bs_kwargs: Optional[Dict[str, Any]] = None,
            header_template: Optional[dict] = None,
            **kwargs
            ):
        data = WebBaseLoader(web_path=web_path,
                             default_parser=default_parser,
                             requests_kwargs=requests_kwargs,
                             requests_per_second=requests_per_second,
                             raise_for_status=raise_for_status,
                             bs_get_text_kwargs=bs_get_text_kwargs,
                             bs_kwargs=bs_kwargs,
                             header_template=header_template,
                             **kwargs
                             ).load()
        self._base(documents=data, is_return=is_return, return_mode=return_mode, extend=extend)


class DocumentLoader(BaseKnowledgeBase, ABC):
    """
    dl = DocumentLoader(path='./aaa.txt')
    a = dl.load()
    print(a)
    b = dl.split(chunk_size=100, chunk_overlap=50)
    print(b)
    dl.save_loader_documents('doc.json')
    """

    def __init__(self, init_documents=None):
        super().__init__(init_documents=init_documents)

    def get(self, path, loader=None, loader_kwargs={}, is_return=True, return_mode='doc', extend=True):
        if loader is None:
            loader = UnstructuredFileLoader
        data = loader(str(path), **loader_kwargs).load()
        self._base(documents=data, is_return=is_return, return_mode=return_mode, extend=extend)


class DocumentGlobLoader(BaseKnowledgeBase):
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

    def __init__(self, init_documents=None):
        super().__init__(init_documents=init_documents)

    def get(self,
            path: str,
            glob: str = "**/[!.]*",
            suffixes: Optional[Sequence[str]] = None,
            loader_cls=None,
            loader_kwargs: Union[dict, None] = None,
            is_return=True,
            return_mode='doc',
            extend=True,
            recursive: bool = False, show_progress: bool = True,
            use_multithreading: bool = False,
            max_concurrency: int = 4,
            silent_errors: bool = False,
            load_hidden: bool = False,
            **kwargs
            ):
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
        self._base(documents=data, is_return=is_return, return_mode=return_mode, extend=extend)

