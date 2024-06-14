import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import concurrent.futures

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

# 函数：处理单个日期的版面
def process_date(date_str):
    results = []
    for i in range(1, 21):  # 遍历每个版面
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
                    break  # 如果找到深度内容，则跳出循环
                else:
                    print(f"No '深读' found in {url}")
            else:
                print(f"No response from {url}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    return results

# 函数：遍历指定日期范围，获取并打印“深读”内容
def fetch_and_print_shendu(start_date, end_date):
    results = []

    current_date = start_date
    date_list = []
    while current_date <= end_date:
        date_str = current_date.strftime('%Y%m/%d')
        date_list.append(date_str)
        current_date += timedelta(days=1)

    # 使用并发请求处理每个日期
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_date = {executor.submit(process_date, date_str): date_str for date_str in date_list}
        for future in concurrent.futures.as_completed(future_to_date):
            date_str = future_to_date[future]
            try:
                result = future.result()
                if result:
                    results.extend(result)
            except Exception as e:
                print(f"Error processing {date_str}: {e}")

    return results

# 函数：保存数据到一个Excel表格
def save_results_to_excel(results):
    if not results:
        print("No '深读' content found in the specified date range.")
        return

    df = pd.DataFrame(results)
    output_file = 'xhrb_results_10plus.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    start_date = datetime(2021, 12, 1)
    end_date = datetime(2024, 6, 13)

    # 获取并打印深度内容
    results = fetch_and_print_shendu(start_date, end_date)

    # 将结果保存为一个Excel文件
    save_results_to_excel(results)
