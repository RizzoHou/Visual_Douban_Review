# 一个定页获取豆瓣电影评论的函数


import requests
from bs4 import BeautifulSoup
from string import punctuation as p_en
from zhon.hanzi import punctuation as p_ch
import sys


def remove_punctuation(text_str):
    # 功能：删除文本中的标点符号
    # 形参：text_str[str]：需要处理的文本
    # 返回：r_str[str]：无标点符号的文本
    r_str = ''.join(my_str for my_str in text_str if my_str not in p_ch and my_str not in p_en)
    return r_str


def get_one_page_reviews(reviews_url_str):
    # 功能：获取指定网址的评论
    # 形参：reviews_url_str[str]：指定网址
    # 返回：r_reviews_str[str]：指定网址的评论
    # 设置请求头
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"}
    req = requests.get(url=reviews_url_str, headers=headers)
    print(req)
    html_str = req.text
    # print(type(html_str))
    # print(html_str)
    bs = BeautifulSoup(html_str, 'lxml')
    # 获取本页所有评论
    comment_item_list = bs.find_all('div', class_="comment-item")
    # print(len(comment_content_list))
    r_reviews_str = ''
    for comment_item in comment_item_list:
        # html_div_str = comment_item.text
        # print(comment_item)
        bs_div = BeautifulSoup(str(comment_item), 'lxml')
        comment_content_list = bs_div.find_all('p', class_='comment-content')
        # print(len(comment_content_list))
        # print(comment_content_list[0].text.strip())
        # 获取评论主干部分
        comment_content_list[0] = comment_content_list[0].text.strip().replace('\n', '').replace(' ', '')
        r_reviews_str += ('。' + comment_content_list[0])
    print(r_reviews_str)
    print('get_one_page_reviews:DONE')
    return r_reviews_str


def get_next_url(now_url_str, serve_url_str):
    # 功能：得到下一页评论的网址
    # 形参：now_url_str[str]：当前评论的网址
    # 形参：serve_url_str[str]：评论网址的共同url，可用于获取下一页评论
    # 返回：r_url_str[str]：下一页评论的网址
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"}
    req = requests.get(url=now_url_str, headers=headers)
    html_str = req.text
    bs = BeautifulSoup(html_str, 'lxml')
    next_list = bs.find_all('a', class_='next')
    # print(len(next_list))
    try:
        href_str = next_list[0].get('href')
    except IndexError:
        print('get_next_url:\n\tERROR 豆瓣可能启动了反爬虫措施，请稍后重试(检测到有异常请求从你的 IP 发出，请 登录 使用豆瓣)')
        sys.exit()
    else:
        r_url_str = serve_url_str + href_str
        print(r_url_str)
        print('get_next_url:DONE')
        return r_url_str


def get_reviews(all_reviews_url_str, num_pages_int=10):
    # 功能：一个定页获取豆瓣电影评论的函数
    # 形参：all_reviews_url_str[str]:豆瓣上电影全部评论的http网址
    # 形参：num_analysis_int[int]:用户想分析的评论页数，默认为10页
    # 返回：r_reviews_str[str]：定页获取的豆瓣电影评论
    # 得到评论网址的共同url，可用于获取下一页评论
    serve_url_str = all_reviews_url_str.split('?')[0]
    # print(type(serve_url_str))
    # print(serve_url_str)
    r_reviews_str = ''
    reviews_int = 0
    while reviews_int < num_pages_int:
        # 获取定页评论
        r_reviews_str += ('。' + get_one_page_reviews(all_reviews_url_str))
        reviews_int += 1
        # 更新url
        all_reviews_url_str = get_next_url(all_reviews_url_str, serve_url_str)
    # print(str(reviews_int))
    print('get_reviews:DONE')
    return r_reviews_str


if __name__ == '__main__':
    m_reviews_str = get_reviews('https://movie.douban.com/subject/34841067/comments?limit=20&status=P&sort=new_score')
    # print(m_reviews_str)
    print('\nAll done')
