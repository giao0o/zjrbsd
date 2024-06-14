import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import calendar
import os

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
        found_deep_reading = False

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
                        found_deep_reading = True
                        break  # 如果找到深度内容，则跳出循环，继续下一天的处理
                    else:
                        print(f"No '深读' found in {url}")
                else:
                    print(f"No response from {url}")
            except Exception as e:
                print(f"Error fetching {url}: {e}")

        if found_deep_reading:
            # 如果找到深度内容，则不再继续当前日期的后续版面遍历
            current_date += timedelta(days=1)
        else:
            current_date = current_date + timedelta(days=1)

    return results

# 函数：按月保存数据到Excel表格
def save_results_to_excel(results):
    if not results:
        print("No '深读' content found in the specified date range.")
        return

    month_files = {}
    for result in results:
        date_str = result['Date']
        year_month = date_str[:6]
        if year_month not in month_files:
            month_files[year_month] = []

        month_files[year_month].append(result)

    for year_month, data in month_files.items():
        df = pd.DataFrame(data)
        output_file = f'xhrb_{year_month}.xlsx'
        df.to_excel(output_file, index=False)
        print(f"Results for {year_month} saved to {output_file}")

if __name__ == "__main__":
    start_date = datetime(2021, 12, 1)
    end_date = datetime(2024, 6, 13)

    # 获取并打印深度内容
    results = fetch_and_print_shendu(start_date, end_date)

    # 将结果按月保存为Excel文件
    save_results_to_excel(results)
