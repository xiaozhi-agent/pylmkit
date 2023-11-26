from duckduckgo_search import DDGS
from pylmkit.utils.data_utils import Document
from pylmkit.core.base import BaseKnowledgeBase


class WebSearch(DDGS, BaseKnowledgeBase):
    def __init__(
            self,
            topk=5,
            backend="api",
            region="wt-wt",
            timelimit=None,
            safesearch="moderate",
            init_documents=None,
            timeout=10,
            headers=None,
            proxies=None
    ):
        DDGS.__init__(
            self,
            timeout=timeout,
            headers=headers,
            proxies=proxies
        )
        BaseKnowledgeBase.__init__(self, init_documents=init_documents)
        self.topk = int(topk)
        self.backend = backend
        self.region = region
        self.timelimit = timelimit
        self.safesearch = safesearch

    def get(self, keyword):
        if keyword:
            search_gen = super().text(keywords=keyword,
                                      backend=self.backend,
                                      region=self.region,
                                      max_results=self.topk,
                                      timelimit=self.timelimit,
                                      safesearch=self.safesearch
                                      )
            for i, page in enumerate(list(search_gen)):
                if page:
                    self.documents.append(Document(
                        page_content=page['body'],
                        metadata={"source": page.get('href', ''), "title": page.get('title', '')},
                        type="Web search"
                    ))
            return self.documents
        else:
            raise Exception("Keyword cannot be empty")


