"""
Reuse existing LM APIs from langchain.
Additionally, add non-existent APIs.
And further standardize the API name
"""
from typing import Any


def _import_ChatQianfan() -> Any:
    from langchain.llms import QianfanLLMEndpoint
    from langchain.chat_models import QianfanChatEndpoint

    return QianfanLLMEndpoint


def _import_ChatOpenAI() -> Any:
    from langchain.chat_models import ChatOpenAI

    return ChatOpenAI


def _import_ChatTongyi() -> Any:
    from langchain.chat_models.tongyi import ChatTongyi

    return ChatTongyi


def _import_ChatHunyuan() -> Any:
    from langchain.chat_models import ChatHunyuan

    return ChatHunyuan


def _import_ChatBaichuan() -> Any:
    from langchain.chat_models import ChatBaichuan

    return ChatBaichuan


def _import_ChatZhipu() -> Any:
    from pylmkit.llms._zhipu import ChatZhipu

    return ChatZhipu


def _import_ChatSpark() -> Any:
    from pylmkit.llms._spark import ChatSpark

    return ChatSpark


def _import_EmbeddingsQianfan() -> Any:
    from langchain.embeddings import QianfanEmbeddingsEndpoint

    return QianfanEmbeddingsEndpoint


def _import_EmbeddingsHuggingFace() -> Any:
    from langchain.embeddings import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings


def _import_EmbeddingsHuggingFaceInstruct() -> Any:
    from langchain.embeddings import HuggingFaceInstructEmbeddings

    return HuggingFaceInstructEmbeddings


def _import_EmbeddingsHuggingFaceBge() -> Any:
    from langchain.embeddings import HuggingFaceBgeEmbeddings

    return HuggingFaceBgeEmbeddings


def _import_EmbeddingsOpenAI() -> Any:
    from langchain.embeddings import OpenAIEmbeddings

    return OpenAIEmbeddings


def __getattr__(name: str) -> Any:
    if name == "ChatQianfan":
        return _import_ChatQianfan()
    elif name == "ChatOpenAI":
        return _import_ChatOpenAI()
    elif name == "ChatHunyuan":
        return _import_ChatHunyuan()
    elif name == "ChatBaichuan":
        return _import_ChatBaichuan()
    elif name == "ChatZhipu":
        return _import_ChatZhipu()
    elif name == "ChatSpark":
        return _import_ChatSpark()
    elif name == "ChatTongyi":
        return _import_ChatTongyi()
    elif name == "EmbeddingsQianfan":
        return _import_EmbeddingsQianfan()
    elif name == "EmbeddingsHuggingFace":
        return _import_EmbeddingsHuggingFace()
    elif name == "EmbeddingsHuggingFaceInstruct":
        return _import_EmbeddingsHuggingFaceInstruct()
    elif name == "EmbeddingsHuggingFaceBge":
        return _import_EmbeddingsHuggingFaceBge()
    elif name == "EmbeddingsOpenAI":
        return _import_EmbeddingsOpenAI()
    else:
        raise AttributeError(f"Could not find: {name}")


__all__ = [
    "ChatQianfan",
    "ChatBaichuan",
    "ChatHunyuan",
    "ChatOpenAI",
    "ChatTongyi",
    "ChatSpark",
    "ChatZhipu",
    "EmbeddingsQianfan",
    "EmbeddingsHuggingFace",
    "EmbeddingsHuggingFaceInstruct",
    "EmbeddingsHuggingFaceBge",
    "EmbeddingsOpenAI",

]




