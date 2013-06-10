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
    "smzdm":[u"母婴用品",u"儿童玩具",u"日常食品",u"旅行箱包",u"时尚女包"]    
    
}
