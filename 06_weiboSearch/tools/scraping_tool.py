import json
import requests
import time
import logging

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_weibo(url: str):
    '''爬取相关鲜花服务商的资料'''
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Referer": "https://weibo.com"
    }
    cookies = {
        "cookie": '''XSRF-TOKEN=Ln8VielcAuKIJdY0_MtiH6-Y; SUB=_2A25LdDxpDeRhGeFJ7FAS8inNzjSIHXVoCDGhrDV8PUNbmtANLVTGkW9NfycA7gqGnl6snrhNJQGK-EpUftBN0UIv; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5bKd0X3LbJn.ov1JNVn5xM5JpX5KzhUgL.FoMNS0z0eoMpSKn2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNS0MEe0zNeK-R; ALF=02_1721227577; WBPSESS=QE3ameq6TefjM8EMf0g7Glg7GNLLqDLwTplOBDV3sxmh6H9lgIeRKgNvJLx4qtjGwUzfITTO73yphvfSpx8k6iZBFNJyz3eAZ_oASLJ3Js1XpVM6SGzaYoKTO-LhuaWg4YE_ybI4O12-DG47x0XziQ=='''
    }
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        response.raise_for_status()  # 如果响应状态码不是200，引发HTTPError异常
        time.sleep(3)  # 加上3s的延时防止被反爬
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error during requests to {url}: {e}")
        return None

def get_data(id):
    url = "https://weibo.com/ajax/profile/detail?uid={}".format(id)
    html = scrape_weibo(url)
    if html is None:
        logging.error("Failed to retrieve data from URL.")
        return None

    try:
        response = json.loads(html)
        return response
    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding error: {e}")
        return None