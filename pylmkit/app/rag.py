from pylmkit.llms import EmbeddingsHuggingFaceBge
from pylmkit.perception.text import Dict2Document, Text2Document
from typing import Any, Iterable, List, Optional, Tuple, Type


class VectorDB(object):
    def __init__(self, init_vdb=None):
        self.vdb = init_vdb

    @classmethod
    def preload(cls, corpus, embed_model, vector_db_model, is_return=True, extend=True):
        corpus = cls().any2doc(corpus)
        _vdb = vector_db_model.from_documents(corpus, embed_model, ids=[i for i in range(1, len(corpus)+1)])
        cls()._base(_vdb, is_return=is_return, extend=extend)

    @classmethod
    def load(cls, vector_db, folder_path, embeddings, index_name="index", is_return=True, extend=True, **kwargs):
        _vdb = vector_db.load_local(folder_path, embeddings, index_name=index_name, **kwargs)
        cls()._base(_vdb, is_return=is_return, extend=extend)

    @classmethod
    def save(cls, folder_path: str, index_name: str = "index", vector_db=None):
        if vector_db is None:
            vector_db = cls().vdb
        vector_db.save_local(folder_path=folder_path, index_name=index_name)

    @classmethod
    def add(cls, corpus, vector_db=None, is_return=True, extend=True):
        if vector_db is None:
            vector_db = cls().vdb
        corpus = cls().any2doc(corpus)
        vdb = vector_db.add_documents(documents=corpus)
        cls()._base(vdb, is_return=is_return, extend=extend)

    @classmethod
    def update(cls, ids, corpus, vector_db=None, is_return=True, extend=True):
        if vector_db is None:
            vector_db = cls().vdb
        corpus = cls().any2doc(corpus)
        vector_db.update_documents(ids=ids, documents=corpus)
        cls()._base(vector_db, is_return=is_return, extend=extend)

    def get(self, ids, vector_db=None):
        if vector_db is None:
            vector_db = self.vdb
        return vector_db._collection.get(ids=ids)

    def delete(self, ids, vector_db=None, is_return=False, extend=False):
        if vector_db is None:
            vector_db = self.vdb
        vector_db = vector_db._collection.delete(ids=ids)
        self._base(vector_db, is_return=is_return, extend=extend)

    def count(self, vector_db=None):
        if vector_db is None:
            vector_db = self.vdb
        return vector_db._collection.count()

    def any2doc(self, corpus):
        if corpus and isinstance(corpus[0], str):
            corpus = Text2Document.get(texts=corpus, is_return=True, return_mode='doc', extend=False)
        elif corpus and isinstance(corpus[0], dict):
            corpus = Dict2Document.get(doc_dict=corpus, is_return=True, extend=False, return_mode='doc')
        else:
            corpus = corpus
        return corpus

    def _base(self, vector_db, is_return=True, extend=False):
        if extend:
            self.vdb = vector_db
        if is_return:
            return vector_db


class BaseRA(VectorDB):
    def __init__(self, init_vdb):
        super().__init__(init_vdb)

    def retriever(self,
                  k,
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
        for kwarg in [k, filter_metadata, fetch_k, lambda_mult, score_threshold]:
            if kwarg:
                search_kwargs[str(kwarg)] = kwarg
        return self.vdb.as_retriever(search_kwargs=search_kwargs, search_type=search_type)

    def ra(self,
           query: str,
           k: int = 5,
           search_language=[],
           lambda_val: float = 0.025,
           filter: Optional[str] = None,
           n_sentence_context: int = 2,
           **kwargs: Any, ):
        return self.vdb.similarity_search(
            query=query,
            k=k,
            lambda_val=lambda_val,
            filter=filter,
            n_sentence_context=n_sentence_context,
            **kwargs
        )


class DocRAG(BaseRA):
    pass


class WebRAG(BaseRA):
    pass


class DBRAG(BaseRA):
    pass


