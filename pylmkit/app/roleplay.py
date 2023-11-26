from pylmkit.tools.search import WebSearch
from pylmkit.utils.data_utils import message_as_string
from pylmkit.utils.data_utils import document_as_string
from pylmkit.utils.data_utils import document_as_refer
from pylmkit.core.prompt import return_language


class RolePlay(object):
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
        self.refer = []
        if online_search_kwargs:
            self.search = WebSearch(**online_search_kwargs)
        else:
            self.search = None

    def invoke(self, query: str, **kwargs):
        prompt = self._invoke(query)
        response = self.model.invoke(prompt)
        response = [response if isinstance(response, str) else response.content][0]
        if self.memory:
            self.memory.add(role='ai', content=response)  # add ai output
        return response, document_as_refer(self.refer)

    def stream(self, query: str, **kwargs):
        prompt = self._invoke(query)
        response = self.model.stream(prompt)
        if self.memory:
            self.memory.add(role='ai',
                            content="".join([i.content if not isinstance(i, str) else i for i in response])
                            )  # add ai output
        return response, document_as_refer(self.refer)

    def return_memory(self):
        return self.memory.memory_messages

    def return_refer(self):
        return document_as_refer(self.refer)

    def clear_memory(self):
        self.memory.clear()

    def _invoke(self, query, **kwargs):
        # search
        search_content = ""
        search_documents = []
        if self.search and query:
            try:
                search_documents = self.search.get(keyword=query)
                search_content = document_as_string(documents=search_documents)
            except Exception as e:
                print(f"online search except: {e}")
        # refer
        self.refer.extend(search_documents)
        # memory
        memory_content = ""
        if self.memory and query:
            memory_content = self.memory.get()
            if isinstance(memory_content, list):
                memory_content = message_as_string(memory_content)
            self.memory.add(content=query, role='human')  # add user input
        # prompt
        try:
            prompt_kwargs = {"search": search_content, 'memory': memory_content, "query": query}
            prompt_kwargs.update(kwargs)
            prompt = self.role_template.format(**prompt_kwargs)
        except Exception as e:
            prompt = query
            print(f"role template except: {e}")
        # return language
        if self.return_language:
            prompt += return_language(language=self.return_language)
        return prompt


