# conding: utf-8
import requests
from lxml import etree
from fake_useragent import UserAgent
from threading import Thread, Lock
import json
import time
import logging


url_list = ['https://www.xiaohua.com/duanzi?page=1']
abandon_url = []


def start_request():
    global url_list
    ua = UserAgent()
    header = ua.chrome
    mutex.acquire()
    url = url_list[-1]
    logging.info('The next url is {}'.format(url))

    text = requests.get(url=url, headers={"UserAgent": header}).text
    html = etree.HTML(text)

    next_url = html.xpath('//*[@id="Pager"]/a/@href')[-2]

    if next_url and next_url not in url_list:
        url_list.append("https://www.xiaohua.com" + next_url)
        mutex.release()
        start_request()
    else:
        mutex.release()
        return 0


def porse():
    # html = start_request(url)
    global url_list
    global abandon_url

    ua = UserAgent()
    header = ua.chrome
    while len(url_list) == 1 and t1.isAlive():
        logging.info('wait............')
        time.sleep(0.5)
    # 上锁
    mutex.acquire()
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

        with open("duanzi.json", "a+", encoding="utf-8") as f:
            f.write(json.dumps(item) + "\n")

    if url_list != []:
        abandon_url.append(url)
        porse()
    else:
        return 0


if __name__ == "__main__":
    """
    这样会有共享全局变量冲突的问题，导致全局变量数据不正确
    """
    logging.basicConfig(
        filename='app.log',
        level=logging.INFO,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
        )
    logging.info('Start Spider..')

    mutex = Lock()
    t1 = Thread(target=start_request)
    t1.start()

    t2 = Thread(target=porse)
    t2.start()

    # while t1.isAlive():
    #     t2.join()
