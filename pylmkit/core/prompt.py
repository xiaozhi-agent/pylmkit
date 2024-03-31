

def input_prompt(**kwargs):
    return kwargs


def return_language(language='English'):
    return f"\nReply in {language}"


def get_summary_default_prompt():
    _prompt = "提取下面内容的摘要：\n\ncontent: {content}"
    return _prompt


sql_prompt = """你是一个MySQL专家。给定一个输入问题，首先创建一个语法正确的MySQL查询来运行，然后查看查询的结果并返回输入问题的答案。
永远不要查询表中的所有列。您必须只查询回答问题所需的列。将每个列名用双引号(")括起来，以表示它们为分隔符。
注意，只使用您可以在下面的表中看到的列名。注意不要查询不存在的列。另外，要注意哪个列在哪个表中。
注意，不局限单表查询，如果用户问题涉及多个表关联查询，则需要多表关联查询，比如：
```sql
SELECT pi.project_name
FROM tabel1 AS pi
INNER JOIN tabel2 AS pm ON pi.id = pm.id
WHERE pm.age = 26;
```
Use the following format:
```sql
SELECT xx1 FROM database.table WHERE xx2 = '882399'
```

Only use the following tables:
{table_info}

Question: {question}
"""

sql_qa_prompt = """Given the following user question, corresponding SQL query, and SQL result, answer the user question.
Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """




