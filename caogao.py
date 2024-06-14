# import requests
# from bs4 import BeautifulSoup

# # 指定URL
# url = 'https://xh.xhby.net/pc/layout/202406/06/node_5.html'

# # 获取网页内容
# response = requests.get(url)
# response.encoding = 'utf-8'  # 设置编码

# # 解析网页内容
# soup = BeautifulSoup(response.text, 'html.parser')

# # 找到特定版面内容
# section_title = "深读"
# content_div = soup.find('div', class_='newsshow')  # 请根据实际的HTML结构调整class

# # 输出提取到的内容
# if content_div:
#     print(content_div.get_text(strip=True))
# else:
#     print(f"未找到标题为 '{section_title}' 的内容")
    
import requests
from bs4 import BeautifulSoup

# 指定URL
url = 'https://xh.xhby.net/pc/layout/202406/06/node_5.html'

# 获取网页内容
response = requests.get(url)
response.encoding = 'utf-8'  # 设置编码

# 解析网页内容
soup = BeautifulSoup(response.text, 'html.parser')

# 找到特定版面内容
section_title = "深读"
content_div = soup.find('div', class_='newsshow')  # 请根据实际的HTML结构调整class

# 确保找到的div包含section_title
if content_div and section_title in content_div.get_text(strip=True):
    print(content_div.get_text(strip=True))
else:
    print(f"未找到标题为 '{section_title}' 的内容")

