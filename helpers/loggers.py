#coding:utf-8
import logging
import logging.handlers
from manager.settings import crawl_failure_log,shed_failure_log,tactics_log

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger_crawl = logging.getLogger("crawl")
logger_crawl.setLevel(logging.DEBUG)
handler_crawl = logging.handlers.RotatingFileHandler(
              crawl_failure_log, maxBytes=100000000, backupCount=100)
handler_crawl.setLevel(logging.DEBUG)
handler_crawl.setFormatter(formatter)
logger_crawl.addHandler(handler_crawl)


logger_sched = logging.getLogger("schedErrJob")
logger_sched.setLevel(logging.DEBUG)
handler_sched = logging.handlers.RotatingFileHandler(
              shed_failure_log, maxBytes=100000000, backupCount=100)
handler_sched.setLevel(logging.DEBUG)
handler_sched.setFormatter(formatter)
logger_sched.addHandler(handler_sched)


logger_tactics = logging.getLogger("tactics")
logger_tactics.setLevel(logging.DEBUG)
handler_tactics = logging.handlers.RotatingFileHandler(
             tactics_log, maxBytes=100000000, backupCount=100)
handler_tactics.setLevel(logging.DEBUG)
handler_tactics.setFormatter(formatter)
logger_tactics.addHandler(handler_tactics)


logger_dict = {"crawl":logger_crawl,"schedErrJob":logger_sched,"tactics":logger_tactics}

def get_logger(name):
    return logger_dict[name]
