# conding: utf-8
import json
import logging
import sys
import time
from threading import Lock, Thread, Condition

import requests
from fake_useragent import UserAgent
from lxml import etree

# 防止递归次数过多导致报错，但仅是更改了递归深度的阙值，没有从根本上解决问题
# RecursionError: maximum recursion depth exceeded in comparison
# sys.setrecursionlimit(99999999)
url_list = ['https://www.xiaohua.com/duanzi?page=1']
abandon_url = []
ua = UserAgent()
header = ua.random
thread_status = True


class TailRecurseException(BaseException):
    """
    自定义异常
    """
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs


def tail_call_optimized(g):
    """
    自定义装饰器，尾递归优化，当这个函数是其本身的祖父时，使它等于它自己，防止栈溢出。
    但是效率约为之前的1/5左右。（不完全统计）
    """
    def func(*args, **kwargs):
        f = sys._getframe()
        if f.f_back and f.f_back.f_back and f.f_back.f_back.f_code == f.f_code:
            raise TailRecurseException(args, kwargs)
        else:
            while True:
                try:
                    return g(*args, **kwargs)
                except TailRecurseException as e:
                    args = e.args
                    kwargs = e.kwargs
    func.__doc__ = g.__doc__
    return func


@tail_call_optimized
def get_header():
    global header
    time.sleep(5)
    mutex.acquire()
    header = ua.random
    logging.info("write a header is [{}]".format(header))
    mutex.release()
    if t2.isAlive():
        return get_header()
    else:
        logging.info("def get_header() is stop.")
        return 0


@tail_call_optimized
def start_request():
    global url_list
    global header
    global thread_status

    mutex.acquire()
    if len(url_list) == 2 and thread_status is False:
        logging.info("Wake up the thread....")
        thread_status = True
        cv.notify()
    url = url_list[-1]
    logging.info('The next url is {}'.format(url))

    text = requests.get(url=url, headers={"UserAgent": header}).text
    html = etree.HTML(text)
    is_next = html.xpath('//*[@id="Pager"]/a')[-2]

    if is_next.xpath('./@href') == []:
        thread_status = True
        logging.info("def start_request() is stop.")
        mutex.release()
        return 0
    next_url = html.xpath('//*[@id="Pager"]/a/@href')[-2]

    if next_url and next_url not in url_list:
        url_list.append("https://www.xiaohua.com" + next_url)
        mutex.release()
        return start_request()
    else:
        logging.info("def start_request() is stop.")
        mutex.release()
        return 0


@tail_call_optimized
def parse():
    global url_list
    global abandon_url
    global header
    global thread_status

    # 互斥锁
    mutex.acquire()
    if len(url_list) == 1 and t1.isAlive():
        logging.info('url_list is empty, please wait a minute...')
        thread_status = False

        cv.wait()
    url = url_list.pop(0)
    mutex.release()

    logging.info('The spider url is {}'.format(url))

    text = requests.get(url=url, headers={"UserAgent": header}).text
    html = etree.HTML(text)

    div = html.xpath('/html/body/div/div[8]/div[2]/div[2]/div[@class="one-cont"]')

    for d in div:
        item = {}
        author = d.xpath('./div/div/a/i/text()')[0]
        context = d.xpath('./p/a/text()')[0]
        up_click = d.xpath('./ul/li[1]/span/text()')[0]
        down_click = d.xpath('./ul/li[2]/span/text()')[0]
        collect = d.xpath('./ul/li[3]/span/text()')[0]

        item = {
            "作者": author,
            "内容": context,
            "点赞": up_click,
            "不行": down_click,
            "收藏": collect
        }

        with open("jokes.json", "a+", encoding="utf-8") as f:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    if url_list != []:
        abandon_url.append(url)
        return parse()
    else:
        logging.info("def parse() is stop.")
        return 0


if __name__ == "__main__":
    """
    (这样会有共享全局变量冲突的问题，导致全局变量数据不正确)
    使用互斥锁，不会出现问题
    """
    logging.basicConfig(
        filename='app.log',
        level=logging.INFO,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
        )
    logging.info('Start Spider..')

    cv = Condition()
    mutex = Lock()
    t1 = Thread(target=start_request)
    logging.info("def start_request() is start.")
    t1.start()

    t2 = Thread(target=parse)
    logging.info("def parse() is start.")
    t2.start()

    t3 = Thread(target=get_header)
    logging.info("def get_header() is start.")
    t3.start()

    # while t1.isAlive():
    #     t2.join()
