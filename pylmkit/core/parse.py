

class CodeBlockParse(object):
    def __init__(self):
        pass

    def base(self, code_text, code_type):
        """
        # 解析提取代码块

        ## 输入参数
        - code_text，string，代码块文本
        - code_type，string，编程语言类型

        ## 输出参数
        - code_result，dict，返回状态码和代码文本
            - code，string，代码文本
            - status，bool，表示输入的代码块是否符合代码块标准

        """
        code_result = {'output': "", "status": False, "error": None}
        if f'```{code_type}' in code_text and '```' in code_text:
            code_result['output'] = str(code_text).split(f'```{code_type}')[1].split('```')[0]
            code_result['status'] = True
        else:
            code_result['error'] = f'不存在代码块格式：```{code_type}\n```'
        return code_result

    @classmethod
    def parse_sql(cls, code_text):
        result = cls().base(code_text, code_type='sql')
        if result['status']:
            result['output'] = result['output'].replace('\n', ' ')
        return result

    @classmethod
    def parse_python(cls, code_text):
        result = cls().base(code_text, code_type='python')
        if result['status']:
            result['output'] = result['output']
        return result

    @classmethod
    def parse_json(cls, code_text):
        result = cls().base(code_text, code_type='json')
        if result['status']:
            result['output'] = result['output'].replace(' ', '')
        return result



