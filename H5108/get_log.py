import logging
import time


class GetLog:
    """ 记录Log日志 """

    def __init__(self, log_name, logger_name="root"):
        """ 构造方法 
        log_name: 日志保存路径。
        logger_name: 
        """
        self.logger = logging.Logger(logger_name)
        self.logger.setLevel(logging.INFO)
        timer = time.strftime("_%Y%m%d_%H%M%S", time.localtime())
        self.log_file_path = ".".join([log_name.split(".")[0] + timer, log_name.split(".")[-1]])

        self.fmts = "%(asctime)s-:%(levelname)s: -- %(message)s"  # 定义输出log的格式
        self.dmt = "%Y-%m-%d %H:%M:%S"

    def logger_ini(self):
        """ 配置 logger """
        self.handler = logging.FileHandler(self.log_file_path, 'a+')
        formatter = logging.Formatter(self.fmts, self.dmt)
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)

    def info(self, message):
        """ 记录 log 信息 """
        self.logger_ini()
        self.logger.info(message)

        # self.handler.close()
        self.logger.removeHandler(self.handler)

    def error(self, message):
        """ 记录 error 信息 """
        self.logger_ini()
        self.logger.error(message)

        # self.handler.close()
        self.logger.removeHandler(self.handler)


if __name__ == "__main__":
    log = GetLog("debug.log", "debug")
    log.info("tetete")
    log.error("debug log")
