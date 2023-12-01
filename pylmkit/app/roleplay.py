from pylmkit.utils.data_utils import message_as_string
from pylmkit.utils.data_utils import document_as_string
from pylmkit.utils.data_utils import document_as_refer
from pylmkit.core.prompt import return_language


class RolePlay(object):
    from pylmkit.utils.logging import BaseLogging
    log = BaseLogging().logger

    def __init__(self,
                 role_template="",
                 llm_model=None,
                 memory=None,
                 online_search_kwargs={},
                 return_language="English",
                 **kwargs
                 ):
        self.role_template = role_template
        self.model = llm_model
        self.return_language = return_language
        self.memory = memory
        if online_search_kwargs:
            from pylmkit.tools.search import WebSearch
            self.search = WebSearch(**online_search_kwargs)
        else:
            self.search = None

    def invoke(self, query: str, ra_documents=[], **kwargs):
        prompt, refer = self._invoke(query, ra_documents=ra_documents, **kwargs)
        response = self.model.invoke(prompt)
        response = [response if isinstance(response, str) else response.content][0]
        if self.memory:
            if not refer:
                self.memory.add(role='ai', content=response)  # add ai output
            else:
                self.memory.add(role='ai', content=response, refer=refer)
        return response, refer

    def stream(self, query: str, ra_documents=[], **kwargs):
        prompt, refer = self._invoke(query, ra_documents=ra_documents, **kwargs)
        response = self.model.stream(prompt)
        if self.memory:
            if not refer:
                self.memory.add(role='ai',
                                content="".join([i.content if not isinstance(i, str) else i for i in response])
                                )  # add ai output
            else:
                self.memory.add(role='ai',
                                content="".join([i.content if not isinstance(i, str) else i for i in response]),
                                refer=refer
                                )  # add ai output
        return response, refer

    def return_memory(self):
        return self.memory.memory_messages

    def clear_memory(self):
        self.memory.clear()

    def _invoke(self, query, ra_documents=[], **kwargs):
        # search
        search_content = ""
        search_documents = []
        if self.search and query:
            try:
                search_documents = self.search.get(keyword=query)
                search_content = document_as_string(documents=search_documents)
            except Exception as e:
                # print(f">>> Online search except: {e}")
                self.log.error(f"{e}")
        # ra base
        ra_content = ""
        if ra_documents:
            ra_content = document_as_string(documents=ra_documents)
        # refer
        refer = []
        refer.extend(search_documents)
        refer.extend(ra_documents)
        refer = document_as_refer(refer)
        # memory
        memory_content = ""
        if self.memory and query:
            memory_content = self.memory.get()
            if isinstance(memory_content, list):
                memory_content = message_as_string(memory_content)
            self.memory.add(content=query, role='human')  # add user input
        # prompt
        try:
            prompt_kwargs = {"search": search_content,
                             'memory': memory_content,
                             "query": query,
                             "ra": ra_content,
                             }
            prompt_kwargs.update(kwargs)
            prompt = self.role_template.format(**prompt_kwargs)
        except Exception as e:
            prompt = query
            # print(f"role template except: {e}")
            self.log.error(f"Role template except: {e}")
        # return language
        if self.return_language:
            prompt += return_language(language=self.return_language)
        return prompt, refer

