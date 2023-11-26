from pylmkit.core import BaseMemory


class MemoryHistoryLength(BaseMemory):
    """

    例子
    >>> from pylmkit.memory import MemoryHistoryLength
    >>> mhl = MemoryHistoryLength(memory_length=100)
    >>> mhl.add(role="user", content="中国首都在哪个城市？")
    >>> mhl.add(role="ai", content="北京")
    >>> mhl.add(role="user", content="广州属于哪个省？")
    >>> mhl.add(role="ai", content="广东")
    >>> print(mhl.get())
    >>> print(mhl.memory_length)
    """

    def __init__(self, memory_length=1000, init_memory=None, streamlit_web=False):
        super().__init__(init_memory=init_memory, streamlit_web=streamlit_web)
        self.memory_length = int(memory_length)

    def get(self):
        history_memory = super()._get(mode="string")
        return history_memory[-self.memory_length:]

    def origin_memory(self):
        return self.memory_messages


class MemoryConversationsNumber(BaseMemory):
    """
    >>> from pylmkit.memory import MemoryConversationsNumber
    >>> mcn = MemoryConversationsNumber(number=1)
    >>> mcn.add(role="user", content="中国首都在哪个城市？")
    >>> mcn.add(role="ai", content="北京")
    >>> mcn.add(role="user", content="广州市属于中国哪个省？")
    >>> mcn.add(role="ai", content="广东省")
    >>> print(mcn.get())
    """

    def __init__(self, number=5, init_memory=None, streamlit_web=False):
        super().__init__(init_memory=init_memory, streamlit_web=streamlit_web)
        self.number = int(number)

    def get(self):
        conversations_memory = super()._get(mode="message")
        return conversations_memory[-self.number * 2:]

    def origin_memory(self):
        return self.memory_messages


class MemorySummary(BaseMemory):
    def __init__(self, llm_model, history_memory_length=1000, prompt_template: str = "", init_memory=None, streamlit_web=False):
        super().__init__(init_memory=init_memory, streamlit_web=streamlit_web)
        self.model = llm_model
        self.history_memory_length = int(history_memory_length)
        self.prompt_template = str(prompt_template)
        if not prompt_template:
            self.prompt_template = "根据下面历史对话内容提取摘要\n"

    def get(self):
        history_memory = super()._get(mode="string")[-self.history_memory_length:]
        query = self.prompt_template + history_memory
        summary_memory = self.model.invoke(query)
        return summary_memory

    def origin_memory(self):
        return self.memory_messages


