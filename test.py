import requests
from bs4 import BeautifulSoup

# 指定日期的界面URL
url = 'https://zjrb.zjol.com.cn/html/2022-06/30/zjrbindex.htm'

# 发送HTTP请求获取页面内容
response = requests.get(url)
response.encoding = 'utf-8'  # 设置正确的编码

# 解析HTML内容
soup = BeautifulSoup(response.text, 'html.parser')

# 查找包含“深读”的内容
articles = soup.find_all(string=lambda text: '深读' in text)

# 输出找到的内容
for article in articles:
    print(article)
