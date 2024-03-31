import functools
import logging
import multiprocessing
import sys
from io import StringIO
from typing import Dict, Optional
from pydantic import Field, BaseModel
logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=None)
def warn_once() -> None:
    """Warn once about the dangers of PythonREPL."""
    logger.warning("Python REPL can execute arbitrary code. Use with caution.")


class PythonREPL(BaseModel):
    """运行python代码"""
    globals: Optional[Dict] = Field(default_factory=dict, alias="_globals")
    locals: Optional[Dict] = Field(default_factory=dict, alias="_locals")

    @classmethod
    def worker(
            cls,
            command: str,
            globals: Optional[Dict],
            locals: Optional[Dict],
            queue: multiprocessing.Queue,
    ) -> None:
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            exec(command, globals, locals)
            sys.stdout = old_stdout
            queue.put(mystdout.getvalue())
        except Exception as e:
            sys.stdout = old_stdout
            queue.put(repr(e))

    def run(self, command: str, timeout: Optional[int] = None) -> str:
        """Run command with own globals/locals and returns anything printed.
        Timeout after the specified number of seconds."""

        # Warn against dangers of PythonREPL
        warn_once()

        queue: multiprocessing.Queue = multiprocessing.Queue()

        # Only use multiprocessing if we are enforcing a timeout
        if timeout is not None:
            # create a Process
            p = multiprocessing.Process(
                target=self.worker, args=(command, self.globals, self.locals, queue)
            )
            # start it
            p.start()
            # wait for the process to finish or kill it after timeout seconds
            p.join(timeout)
            if p.is_alive():
                p.terminate()
                return "Execution timed out"
        else:
            self.worker(command, self.globals, self.locals, queue)
        # get the result from the worker function
        return queue.get()


class Executor(object):
    def __init__(self):
        pass

    @classmethod
    def run_python(cls, code_text: str, timeout: Optional[int] = None):
        results = {'output': None, "status": False, "error": None}
        try:
            results['output'] = PythonREPL().run(command=code_text, timeout=timeout)
            results['status'] = True
        except Exception as e:
            results['error'] = str(e)
        return results

    @classmethod
    def run_mysql(cls, connect, code_text):
        results = {'output': {"data": None, "columns": []}, "status": False, "error": None}
        with connect.cursor() as cursor:
            try:
                # 执行SQL语句
                cursor.execute(code_text)
                results['output']['columns'] = [i[0] for i in cursor.description]
                # 获取所有记录列表
                results['output']['data'] = list(cursor.fetchall())
                results['status'] = True
            except Exception as e:
                results['error'] = str(e)
        return results





