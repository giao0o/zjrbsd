import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

# 函数：获取特定日期和版面的URL
def generate_url(date, edition):
    return f"https://xh.xhby.net/pc/layout/{date}/node_{edition}.html"

# 函数：获取页面内容
def fetch_page_content(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text

# 函数：解析页面内容，查找并返回包含“深读”的内容
def parse_page_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all('div', class_='newsshow')
    for div in divs:
        if '深读' in div.get_text(strip=True):
            return div.get_text(strip=True)
    return None

# 函数：遍历指定日期范围，获取并打印“深读”内容
def fetch_and_print_shendu(start_date, end_date):
    results = []

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y%m/%d')
        for i in range(1, 11):  # 遍历每个版面
            url = generate_url(date_str, i)
            print(f"Fetching {url}")
            try:
                html = fetch_page_content(url)
                if html:
                    content = parse_page_content(html)
                    if content:
                        print(f"Found '深读' in {url}")
                        print(content)
                        results.append({'Date': date_str, 'URL': url, 'Content': content})
                    else:
                        print(f"No '深读' found in {url}")
                else:
                    print(f"No response from {url}")
            except Exception as e:
                print(f"Error fetching {url}: {e}")
        current_date += timedelta(days=1)

    return results

if __name__ == "__main__":
    start_date = datetime(2021, 12, 1)
    end_date = datetime(2024, 6, 13)

    # 获取并打印深度内容
    results = fetch_and_print_shendu(start_date, end_date)

    # 将结果保存为Excel文件
    if results:
        df = pd.DataFrame(results)
        output_file = 'xhrb_2020_2024.xlsx'
        df.to_excel(output_file, index=False)
        print(f"Results saved to {output_file}")
    else:
        print("No '深读' content found in the specified date range.")
