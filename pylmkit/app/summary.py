import requests, os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


def split_text(text, chunk_size=3000):
    # 将文本分割成指定大小的段落
    return [text[i: i + chunk_size] for i in range(0, len(text), chunk_size)]


def merge_abstracts(abstracts):
    # 将多个摘要合并为一个字符串
    return ' '.join(abstracts)


def summary(text, worker, max_chunk_size: int = 3000, max_summary_size: int = 500, show_progress: bool = True,
            max_workers: int = 5):
    """支持短文本、长文本摘要提取。

        ## 输入参数
        - text，str，需要提取摘要的文本
        - worker，function，大模型提取摘要函数
        - max_chunk_size，int，最大文本块，当大于最大长度时，将采用分段提取摘要，然后在汇总摘要，默认取 3000，
        - max_summary_size，int，最大摘要长度，当汇总后的摘要长度大于最大长度时，将采用分段提取摘要，然后在汇总摘要，默认取 500，
        - show_progress，bool，是否显示进度条，默认取 True，
        - max_workers，int，最大线程数，默认取 5，

        ## 输出参数
        - combined_abstract，str，摘要
    """
    text = text if isinstance(text, str) else text.content
    # 分段提取摘要
    chunks = split_text(text, chunk_size=max_chunk_size)
    # 用于存储摘要的列表
    abstracts = []
    # 使用多线程并发处理每个段的摘要生成
    # with ThreadPoolExecutor(max_workers=5) as executor:  # 根据实际情况调整线程数量
    #     futures = [executor.submit(worker, chunk) for chunk in chunks]
    #     abstracts = [future.result() for future in futures]
    with ThreadPoolExecutor(max_workers=max_workers) as executor:  # 根据实际情况调整线程数量
        if show_progress:
            # 使用tqdm显示进度
            for future in tqdm(executor.map(worker, chunks), total=len(chunks), desc="extract summary ..."):
                abstracts.append(future)
        else:
            # 不显示进度
            for future in executor.map(worker, chunks):
                abstracts.append(future)
    # 合并摘要
    combined_abstract = merge_abstracts(abstracts)
    # 如果合并后的摘要长度大于 max_summary_size，则递归调用函数
    if len(combined_abstract) > max_summary_size:
        return summary(combined_abstract,
                       worker=worker,
                       max_chunk_size=max_chunk_size,
                       max_summary_size=max_summary_size,
                       show_progress=show_progress,
                       max_workers=max_workers
                       )
    else:
        combined_abstract = worker(combined_abstract)
        return combined_abstract


# 主函数
def batch_summary(texts: list, worker, max_chunk_size: int = 3000, max_summary_size: int = 500, show_progress: bool = True,
                  max_workers: int = 5):
    """支持批量短文本、长文本摘要提取。

        ## 输入参数
        - text，list，需要提取摘要的多个文本
        - worker，function，大模型提取摘要函数
        - max_chunk_size，int，最大文本块，当大于最大长度时，将采用分段提取摘要，然后在汇总摘要，默认取 3000，
        - max_summary_size，int，最大摘要长度，当汇总后的摘要长度大于最大长度时，将采用分段提取摘要，然后在汇总摘要，默认取 500，
        - show_progress，bool，是否显示进度条，默认取 True，
        - max_workers，int，最大线程数，默认取 5，

        ## 输出参数
        - abstracts，list[str]，摘要
    """
    abstracts = []
    texts = [text if isinstance(text, str) else text.content for text in texts]
    if show_progress:
        for text in tqdm(texts, desc="extract batch summary ..."):
            combined_abstract = summary(text,
                                        worker=worker,
                                        max_chunk_size=max_chunk_size,
                                        max_summary_size=max_summary_size,
                                        show_progress=show_progress,
                                        max_workers=max_workers
                                        )
            abstracts.append(combined_abstract)
    else:
        for text in texts:
            combined_abstract = summary(text,
                                        worker=worker,
                                        max_chunk_size=max_chunk_size,
                                        max_summary_size=max_summary_size,
                                        show_progress=show_progress,
                                        max_workers=max_workers
                                        )
            abstracts.append(combined_abstract)
    return abstracts








