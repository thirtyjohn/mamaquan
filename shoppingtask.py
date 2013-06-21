#coding:utf8

from manager.shoppings.pickitem import startupdate
from manager.danpings import pickdp
from apscheduler.scheduler import Scheduler
from helpers.loggers import get_logger


def err_listener(ev):  
    err_logger = get_logger('schedErrJob')  
    if ev.exception:  
        err_logger.exception('%s %s %s error.',str(ev.job),str(ev.exception), str(ev.traceback))  
    else:  
        err_logger.info('%s', str(ev.job))  


# Start the scheduler
sched = Scheduler(daemonic = False)
sched.add_listener(err_listener)
# Crawl Scheduler Taobao
"""
sched.add_cron_job(startupdate, minute=1, args=['nvzhuang'])
sched.add_cron_job(startupdate, minute=5, args=['nvxie'])
sched.add_cron_job(startupdate, minute=10, args=['wenxiong'])
sched.add_cron_job(startupdate, minute=15, args=['shuiyi'])
sched.add_cron_job(startupdate, minute=20, args=['sushen'])
sched.add_cron_job(startupdate, minute=25, args=['danjianbao'])
sched.add_cron_job(startupdate, minute=30, args=['shoutibao'])
sched.add_cron_job(startupdate, minute=35, args=['xiekuabao'])
sched.add_cron_job(startupdate, minute=40, args=['qianbao'])
sched.add_cron_job(startupdate, minute=45, args=['shounabao'])
sched.add_cron_job(startupdate, minute=50, args=['tongzhuang'])
sched.add_cron_job(startupdate, minute=55, args=['chuangshang'])
sched.add_cron_job(startupdate, minute=27, args=['jiajushipin'])
sched.add_cron_job(startupdate, minute=37, args=['peishi'])
sched.add_cron_job(startupdate, minute=47, args=['maorongwanju'])
"""
sched.add_cron_job(pickdp.startupdate,minute=7,args=['smzdm'])

sched.start()



