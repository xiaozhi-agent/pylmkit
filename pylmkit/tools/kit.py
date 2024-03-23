import re
import inspect


def tool(func):
    name = func.__name__
    # 获取函数签名
    signature = inspect.signature(func)
    # 获取参数信息
    param_str = ", ".join([str(param) for param in signature.parameters.values()])
    # 提取返回类型
    return_str = signature.return_annotation
    if return_str != inspect.Signature.empty:
        if isinstance(return_str, list):
            return_str = '-> [' + ', '.join(re.search(r"'([\w.]+)'", str(t)).group(1) for t in return_str) + ']'
        else:
            if return_str is None:
                return_str = "-> None"
            else:
                return_str = "-> " + str(re.search(r"'([\w.]+)'", str(return_str)).group(1))
    else:
        return_str = ''
    describe = (f"({param_str.strip()}) {return_str.strip()} - " +
                func.__doc__.replace('\n', ' ').replace('    ', ' ').replace('  ', ' ').strip())
    func.name = name
    func.desc = f"{name}{describe}"
    func.all = f"{name}: {name}{describe}"
    return func

