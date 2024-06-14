import datetime
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# 生成所有日期
start_date = datetime.date(2024, 1, 1)
end_date = datetime.date(2024, 12, 31)

date_list = [start_date + datetime.timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# 生成所有URL
base_url = "https://zjrb.zjol.com.cn/html/{:%Y-%m/%d}/zjrbindex.htm"
urls = [base_url.format(date) for date in date_list]

def extract_content(url):
    try:
        print(f"Fetching {url}")  # 添加日志信息
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")  # 打印状态码
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # 查找包含“深读”的 <h3> 标签
            deep_read_section = soup.find('h3', text=lambda t: '深读' in t)
            if deep_read_section:
                print(f"Found '深读' section")  # 找到“深读”部分
                # 获取后续的所有 <li> 标签中的文本
                ul = deep_read_section.find_next('ul')
                if ul:
                    content = [li.get_text(strip=True) for li in ul.find_all('li')]
                    print(f"Extracted Content: {content}")  # 打印提取的内容
                    return '\n'.join(content)
            else:
                print("No '深读' section found")
        else:
            print("Failed to fetch page")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
    return None

# 过滤包含“深读”的网页并提取内容
filtered_pages = []

for url in urls:
    content = extract_content(url)
    if content:
        filtered_pages.append((url, content))

# 创建一个Excel工作簿
wb = Workbook()
ws = wb.active
ws.title = "深读内容"

# 添加标题行
ws.append(["日期", "URL", "内容"])

# 添加数据
for url, content in filtered_pages:
    date_parts = url.split('/')[-3:-1]
    date_str = '-'.join(date_parts)
    ws.append([date_str, url, content])

# 保存Excel文件
output_file = "深读内容.xlsx"
wb.save(output_file)
print(f"Saved results to {output_file}")  # 输出日志信息
