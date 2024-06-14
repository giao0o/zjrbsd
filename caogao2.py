import requests
from bs4 import BeautifulSoup

# 修改 fetch_and_print_shendu 函数
def fetch_and_print_shendu(date):
    base_url = 'https://xh.xhby.net/pc/layout/{}/node_{}.html'
    for i in range(1, 11):  # 遍历每个版面
        url = base_url.format(date, i)
        print(f"Fetching {url}")
        response = requests.get(url)
        response.encoding = 'utf-8'  # 设置请求编码为utf-8
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')  # 解析时使用utf-8编码

        # 获取标题为“深读”的内容
        divs = soup.find_all('div', class_='newsshow')
        found = False
        for div in divs:
            if '深读' in div.get_text(strip=True):
                print(f"Found '深读' in {url}")
                print(div.get_text(strip=True))
                found = True
                break
        if not found:
            print(f"No '深读' found in the content of {url}")

# 指定日期
date = '202406/06'
fetch_and_print_shendu(date)
