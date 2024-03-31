import os, logging
from pylmkit.utils.db_base import DBConnector
# from pylmkit.utils.db_base import TableConnector
from pylmkit.core.base import BaseChatRunnable
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, cast

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',  # 定义日期格式
                    )
logger = logging.getLogger(__name__)


class ChatDB(BaseChatRunnable):
    """和数据库聊天，用于结构化数据问答
    """

    def __init__(self, db_config: dict, model, include_tables: List[str] = None,
                 include_columns: Optional[Dict[str, List]] = {}):
        """初始化参数

        ## input
            - db_config，dict，数据库配置参数，必选
            - model，大语言模型，必选
            - include_tables，List[str]，需要包含哪些表，例子：['table1', 'table2']，可选
            - include_columns，Dict[str, List]，需要包含哪些字段，例子：{'表名1': ['字段1','字段2‘], '表名2': [],}，可选
        """
        logger.info("ChatDB init ...")
        self.model = model
        self.db = DBConnector.from_uri_db(**db_config)
        self.include_tables = include_tables
        self.include_columns = include_columns
        BaseChatRunnable.__init__(self, model=self.model, connector=self.db)

    def invoke(self, question, max_rollback_num: int = 5, return_dict=False, sql_prompt=None):
        """
        ## input
            - question，str，用户问题，必选
            - max_rollback_num，int，最大回滚数，可选

        ## output
            - answer，str，回答的答案
        """
        answer = ""
        results = {"question": question, "query": "", "answer": "", "error": ""}
        table_info = self.db.get_table_describe(include_tables=self.include_tables,
                                                include_columns=self.include_columns)
        if not sql_prompt:
            prompt = self.sql_prompt.format(table_info=table_info, question=question)
        else:
            prompt = sql_prompt
        runnable_results = super().runnable(prompt, max_rollback_num, 'sql')
        if runnable_results['status']:
            prompt = self.sql_qa_prompt.format(question=question,
                                               query=runnable_results['query'],
                                               result=str(runnable_results['result'])
                                               )
            answer = self.model.invoke(prompt)
            answer = answer if isinstance(answer, str) else answer.content
            results['answer'] = answer
            results['query'] = runnable_results['query']
            logger.info(f"Chat Answer: {answer}")
        if return_dict:
            return results
        else:
            return answer


class ChatTable(BaseChatRunnable):
    """和表格（csv,excel,txt,...）聊天，用于结构化数据问答
    """

    def __init__(self,
                 model,
                 table_paths: List[str] or str,
                 include_table_column_comments: Optional[Dict[str, Dict]] = None
                 ):
        """初始化参数

        ## input
            - model，大语言模型，必选
            - table_paths，list/str，数据表的路径，必选
            - include_table_column_comments，Dict[str, Dict]，需要包含哪些字段及字段含义，
                例子：{'表名1': {"name": "", "columns": {'字段1':'字段1含义','字段2':'字段2含义'}}, '表名2': {}，可选
        """
        logger.info("ChatTable init ...")
        import pandas as pd
        self.model = model
        self.table_infos = {}
        self.dfs = {}
        self.include_table_column_comments = include_table_column_comments
        if isinstance(table_paths, str):
            table_paths = [table_paths]
        for path in table_paths:
            if os.path.exists(path) and os.path.isfile(path):
                base_name, ext = os.path.splitext(path)
                ext = ext.lower()
                if ext == '.csv':
                    df = pd.read_csv(path)
                elif ext == '.txt':
                    # Assuming TXT files are CSV-like, but this can be adjusted
                    df = pd.read_csv(path, delimiter='\t' if '\t' in open(path).readline() else ',')
                elif ext == '.xlsx' or ext == '.xls':
                    df = pd.read_excel(path)
                else:
                    raise ValueError(f"Unsupported file format: {ext}")
                table_name = TableConnector.sanitize_table_name(os.path.basename(path).split('.')[0])
                table_columns = list(df.columns)
                self.dfs[table_name] = df
                self.table_infos[table_name] = dict(zip(table_columns, [''] * len(table_columns)))
                logger.info(f"{path} Load complete...")
            else:
                raise FileNotFoundError(f"File not found: {path}")
        self.db = TableConnector(env=globals().update(self.dfs))
        BaseChatRunnable.__init__(self,
                                  model=self.model,
                                  connector=self.db
                                  )

    def invoke(self, question, max_rollback_num: int = 5, return_dict=False, sql_prompt=None):
        """
        ## input
            - question，str，用户问题，必选
            - max_rollback_num，int，最大回滚数，可选

        ## output
            - answer，str，回答的答案
        """
        answer = ""
        results = {"question": question, "query": "", "answer": "", "error": ""}
        table_info = self.db.get_table_describe(origin_=self.table_infos,
                                                input_=self.include_table_column_comments)
        if not sql_prompt:
            prompt = self.sql_prompt.format(table_info=table_info, question=question)
        else:
            prompt = sql_prompt
        runnable_results = super().runnable(prompt, max_rollback_num, 'sql')
        if runnable_results['status']:
            prompt = self.sql_qa_prompt.format(question=question,
                                               query=runnable_results['query'],
                                               result=str(runnable_results['result'])
                                               )
            answer = self.model.invoke(prompt)
            answer = answer if isinstance(answer, str) else answer.content
            results['answer'] = answer
            results['query'] = runnable_results['query']
            logger.info(f"Chat Answer: {answer}")
        if return_dict:
            return results
        else:
            return answer


class TableConnector(object):
    def __init__(self, env=None):
        self.env = env
        if self.env is None:
            self.env = globals()
        from pandasql import sqldf, load_meat, load_births
        self.pysqldf = lambda q: sqldf(q, self.env)

    @classmethod
    def run(cls, command: str) -> Dict:
        logger.info("SQL: " + command)
        results = {"status": False, "error": None, 'output': []}
        try:
            df = TableConnector(TableConnector().env).pysqldf(command)
            dict_from_df = df.to_dict(orient='split')
            results['output'] = dict_from_df['data']
            results['output'].insert(0, list(dict_from_df['columns']))
            results['status'] = True
            return results
        except Exception as e:
            results['error'] = str(e)
            return results

    @classmethod
    def get_table_describe(cls, origin_, input_):
        column_comtents = ''
        for table_name, values in origin_.items():
            columns_dict = {}
            table_describe = ''
            if input_ and input_.get(table_name, False):
                columns_dict = {key: input_[table_name]["columns"][key] for key in
                                list(input_[table_name]["columns"].keys()) if key in list(values.keys())}
                table_describe = input_[table_name].get('name', False)
                if table_describe:
                    table_describe = f"({table_describe})"
            else:
                columns_dict = values
            # '数据库名称为{db_name},
            column_comtents += (f"表{table_describe}:{table_name}': 字段名" +
                                str(columns_dict).replace(' ', '') + '\n')
        return column_comtents

    @classmethod
    def sanitize_table_name(cls, name):
        """Sanitize the table name to be SQL compliant."""
        # Replace non-alphanumeric characters with underscores
        sanitized = ''.join(c if c.isalnum() or c == '_' else '_' for c in name)
        # Remove leading digits or underscores
        sanitized = ''.join(c for i, c in enumerate(sanitized) if c.isalpha() or (c == '_' and i > 0))
        return sanitized
