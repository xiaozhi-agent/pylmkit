from pylmkit.llms import EmbeddingsHuggingFaceBge
from pylmkit.llms import EmbeddingsHuggingFace
from pylmkit.perception.text import Dict2Document, Text2Document
from typing import Any, Iterable, List, Optional, Tuple, Type
from pylmkit.perception.text import DocumentLoader, WebLoader
from pylmkit.app import RolePlay


class VectorDB(object):
    def __init__(self, corpus=None, embed_model=None, vdb_model=None, init_vdb=None):
        self.vdb = init_vdb
        if corpus and embed_model and vdb_model:
            corpus = self.any2doc(corpus)
            self.vdb = vdb_model.from_documents(corpus, embed_model, ids=[i for i in range(1, len(corpus) + 1)])

    @classmethod
    def load(cls, vdb_model, embed_model, vdb_path, vdb_name="index", is_return=True, extend=True, **kwargs):
        _vdb = vdb_model.load_local(vdb_path, embed_model, index_name=vdb_name, **kwargs)
        cls()._base(_vdb, is_return=is_return, extend=extend)

    @classmethod
    def save(cls, vdb_path: str, vdb_name: str = "index", vdb_model=None):
        if vdb_model is None:
            vdb_model = cls().vdb
        vdb_model.save_local(folder_path=vdb_path, index_name=vdb_name)

    @classmethod
    def add(cls, corpus, vdb_model=None, is_return=True, extend=True):
        if vdb_model is None:
            vdb_model = cls().vdb
        corpus = cls().any2doc(corpus)
        vdb = vdb_model.add_documents(documents=corpus)
        cls()._base(vdb, is_return=is_return, extend=extend)

    @classmethod
    def update(cls, ids, corpus, vdb_model=None, is_return=True, extend=True):
        if vdb_model is None:
            vdb_model = cls().vdb
        corpus = cls().any2doc(corpus)
        vdb_model.update_documents(ids=ids, documents=corpus)
        cls()._base(vdb_model, is_return=is_return, extend=extend)

    def get(self, ids, vdb_model=None):
        if vdb_model is None:
            vdb_model = self.vdb
        return vdb_model._collection.get(ids=ids)

    def delete(self, ids, vdb_model=None, is_return=False, extend=False):
        if vdb_model is None:
            vdb_model = self.vdb
        vdb_model = vdb_model._collection.delete(ids=ids)
        self._base(vdb_model, is_return=is_return, extend=extend)

    def count(self, vdb_model=None):
        if vdb_model is None:
            vdb_model = self.vdb
        return vdb_model._collection.count()

    def any2doc(self, corpus):
        # any, str dict doc
        if corpus and isinstance(corpus[0], str):
            corpus = Text2Document.get(texts=corpus, is_return=True, return_mode='doc', extend=False)
        elif corpus and isinstance(corpus[0], dict):
            corpus = Dict2Document.get(doc_dict=corpus, is_return=True, extend=False, return_mode='doc')
        else:
            corpus = corpus
        return corpus

    def _base(self, vdb_model, is_return=True, extend=False):
        if extend:
            self.vdb = vdb_model
        if is_return:
            return vdb_model

    def ra(self,
           query: str,
           topk: int = 5,
           search_language=[],
           lambda_val: float = 0.025,
           filter: Optional[str] = None,
           n_sentence_context: int = 2,
           **kwargs: Any, ):
        return self.vdb.similarity_search(
            query=query,
            k=topk,
            lambda_val=lambda_val,
            filter=filter,
            n_sentence_context=n_sentence_context,
            **kwargs
        )

    def retriever(self,
                  topk,
                  filter_metadata={},
                  fetch_k=20,
                  lambda_mult=0.5,
                  score_threshold=0.8,
                  search_type="similarity"
                  ):
        """from langchain: Return VectorStoreRetriever initialized from this VectorStore.

                Args:
                    search_type (Optional[str]): Defines the type of search that
                        the Retriever should perform.
                        Can be "similarity" (default), "mmr", or "similarity_score_threshold".
                    search_kwargs (Optional[Dict]): Keyword arguments to pass to the
                        search function. Can include things like:

                            public setting:
                                k: Amount of documents to return (Default: 4)
                                filter: Filter by document metadata

                            similarity_score_threshold setting:
                                score_threshold: Minimum relevance threshold
                                    for similarity_score_threshold

                            mmr setting:
                                fetch_k: Amount of documents to pass to MMR algorithm (Default: 20)
                                lambda_mult: Diversity of results returned by MMR;
                                    1 for minimum diversity and 0 for maximum. (Default: 0.5)


                Returns:
                    VectorStoreRetriever: Retriever class for VectorStore.

                Examples:

                .. code-block:: python

                    # Retrieve more documents with higher diversity
                    # Useful if your dataset has many similar documents
                    docsearch.as_retriever(
                        search_type="mmr",
                        search_kwargs={'k': 6, 'lambda_mult': 0.25}
                    )

                    # Fetch more documents for the MMR algorithm to consider
                    # But only return the top 5
                    docsearch.as_retriever(
                        search_type="mmr",
                        search_kwargs={'k': 5, 'fetch_k': 50}
                    )

                    # Only retrieve documents that have a relevance score
                    # Above a certain threshold
                    docsearch.as_retriever(
                        search_type="similarity_score_threshold",
                        search_kwargs={'score_threshold': 0.8}
                    )

                    # Only get the single most similar document from the dataset
                    docsearch.as_retriever(search_kwargs={'k': 1})

                    # Use a filter to only retrieve documents from a specific paper
                    docsearch.as_retriever(
                        search_kwargs={'filter': {'paper_title':'GPT-4 Technical Report'}}
                    )
                """
        search_kwargs = {}
        for kwarg in [topk, filter_metadata, fetch_k, lambda_mult, score_threshold]:
            if kwarg:
                search_kwargs[str(kwarg)] = kwarg
        return self.vdb.as_retriever(search_kwargs=search_kwargs, search_type=search_type)


class BaseRAG(VectorDB, RolePlay):
    def __init__(self,
                 embed_model,
                 vdb_model,
                 llm_model,
                 corpus=None,
                 vdb_path=None,
                 vdb_name="index",
                 init_vdb=None,
                 role_template="",
                 memory=None,
                 online_search_kwargs={},
                 return_language="English",
                 ):
        VectorDB.__init__(self, init_vdb=None)
        RolePlay.__init__(self,
                          role_template=role_template,
                          llm_model=llm_model,
                          memory=memory,
                          online_search_kwargs=online_search_kwargs,
                          return_language=return_language
                          )
        if init_vdb:
            VectorDB.__init__(self, init_vdb=init_vdb)
        elif vdb_path and vdb_name:
            super().load(vdb_model=vdb_model,
                         embed_model=embed_model,
                         vdb_path=vdb_path,
                         vdb_name=vdb_name,
                         is_return=False,
                         extend=True
                         )
        elif corpus:
            super().__init__(corpus=corpus, embed_model=embed_model, vdb_model=vdb_model)
        else:
            raise Exception("`corpus`, `vdb_path`, `init_vdb` Cannot all be None!")

    def invoke(
            self,
            query: str,
            topk: int = 5,
            search_language=[],
            lambda_val: float = 0.025,
            filter: Optional[str] = None,
            n_sentence_context: int = 2,
            ra_kwargs={},
            **kwargs
    ):
        ra_documents = super().ra(
            query=query,
            topk=topk,
            search_language=search_language,
            lambda_val=lambda_val,
            filter=filter,
            n_sentence_context=n_sentence_context,
            **ra_kwargs
        )
        return super().invoke(query=query, ra_documents=ra_documents, **kwargs)

    def stream(
            self,
            query: str,
            topk: int = 5,
            search_language=[],
            lambda_val: float = 0.025,
            filter: Optional[str] = None,
            n_sentence_context: int = 2,
            ra_kwargs={},
            **kwargs
    ):
        ra_documents = super().ra(
            query=query,
            topk=topk,
            search_language=search_language,
            lambda_val=lambda_val,
            filter=filter,
            n_sentence_context=n_sentence_context,
            **ra_kwargs
        )
        return super().stream(query=query, ra_documents=ra_documents, **kwargs)


class DocRAG(BaseRAG):
    def __init__(self,
                 embed_model,
                 vdb_model,
                 llm_model,
                 corpus=None,
                 vdb_path=None,
                 vdb_name="index",
                 init_vdb=None,
                 role_template="",
                 memory=None,
                 online_search_kwargs={},
                 return_language="English",
                 ):
        super().__init__(
            embed_model=embed_model,
            vdb_model=vdb_model,
            llm_model=llm_model,
            corpus=corpus,
            vdb_path=vdb_path,
            vdb_name=vdb_name,
            init_vdb=init_vdb,
            role_template=role_template,
            memory=memory,
            online_search_kwargs=online_search_kwargs,
            return_language=return_language
        )


class WebRAG(BaseRAG):
    def __init__(self,
                 embed_model,
                 vdb_model,
                 llm_model,
                 corpus=None,
                 vdb_path=None,
                 vdb_name="index",
                 init_vdb=None,
                 role_template="",
                 memory=None,
                 online_search_kwargs={},
                 return_language="English",
                 ):
        super().__init__(
            embed_model=embed_model,
            vdb_model=vdb_model,
            llm_model=llm_model,
            corpus=corpus,
            vdb_path=vdb_path,
            vdb_name=vdb_name,
            init_vdb=init_vdb,
            role_template=role_template,
            memory=memory,
            online_search_kwargs=online_search_kwargs,
            return_language=return_language
        )



