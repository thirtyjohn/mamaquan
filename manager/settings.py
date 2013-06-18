#coding:utf-8
import web
from web.contrib.template import render_mako

render = render_mako(
        directories=['manager/templates'],
        input_encoding='utf-8',
        output_encoding='utf-8'
        )

dbconn = web.database(dbn='mysql', user="root", host="127.0.0.1", db="mmquan")
localdir = "/Users/macbookpro/workspace/interest/taobaoyouhui/"

crawl_failure_log = "/Users/macbookpro/workspace/log/mmquan/crawl_failure_log"
shed_failure_log = "/Users/macbookpro/workspace/log/mmquan/shed_failure_log"
tactics_log = "/Users/macbookpro/workspace/log/mmquan/tactics_log"
general_log = "/Users/macbookpro/workspace/log/mmquan/general_log"
filter_class = {
    "smzdm":[u"日常食品",u"实用工具",u"护肤品",u"母婴用品",u"日常穿着",u"名品手表",u"洗发护发",u"生活电器",u"保健品",u"个人护理",u"厨房电器",u"香水",u"儿童玩具",u"厨房用品",u"化妆品",u"卫生用品",u"口腔护理",u"生活家具",u"卫浴用品",u"个护化妆",u"宠物用品",u"时尚女包"],

}
