import logging


class BaseLogging(object):
    def __init__(self):
        # logging setting
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(name)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',  # 定义日期格式
                            )

        self.logger = logging.getLogger(__file__)  # 当前.py文件路径


