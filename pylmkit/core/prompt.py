

def input_prompt(**kwargs):
    return kwargs


def return_language(language='English'):
    return f"\nReply in {language}"


def get_summary_default_prompt():
    _prompt = "提取下面内容的摘要：\n\ncontent: {content}"
    return _prompt







