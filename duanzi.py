# conding: utf-8
import requests
from lxml import etree
from fake_useragent import UserAgent
import time
from threading import Thread


url_list = ['https://www.xiaohua.com/duanzi?page=1']
abandon_url = []


def start_request(url):
    global url_list
    ua = UserAgent()
    header = ua.chrome

    text = requests.get(url=url, headers={"UserAgent": header}).text
    html = etree.HTML(text)

    next_url = html.xpath('//*[@id="Pager"]/a/@href')[-2]

    if next_url and next_url not in url_list:
        url_list.append(next_url)
        start_request(next_url)
       
    # return html


def porse(url):
    # html = start_request(url)
    global url_list
    global abandon_url

    ua = UserAgent()
    header = ua.chrome

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
            "不行" : down_click,
            "收藏": collect
        }

        print(item)
    if url_list != []:
        url = url_list.pop(index=0)
        abandon_url.append(url)

        porse(url)


if __name__ == "__main__":
    # 取出来用过的url列表
    """
    这样会有共享全局变量冲突的问题，导致全局变量数据不正确
    """
    t1 = Thread(target=start_request)
    t1.start()

    t2 = Thread(target=porse)
    t2.start()
    
