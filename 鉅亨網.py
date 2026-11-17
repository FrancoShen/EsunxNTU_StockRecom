import time
import random
import requests
import json
import csv
import pandas as pd


class CnyesNewsSpider():
    
    def get_newslist_info(self, page=1, limit=100):
        """ 房屋詳情

        :param page: 頁數
        :param limit: 一頁新聞數量
        :return newslist_info: 新聞資料
        """
        headers = {
            'Origin': 'https://news.cnyes.com/',
            'Referer': 'https://news.cnyes.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        r = requests.get(f"https://api.cnyes.com/media/api/v1/newslist/category/headline?page={page}&limit={limit}", headers=headers)
        if r.status_code != requests.codes.ok:
            print('請求失敗', r.status_code)
            return None
        newslist_info = r.json()['items']
        return newslist_info


if __name__ == "__main__":
    cnyes_news_spider = CnyesNewsSpider()
    newslist_info = cnyes_news_spider.get_newslist_info()
    
    # print(f'搜尋結果 > 全部新聞總數：{newslist_info["total"]}')
    # print(f'搜尋結果 > 一頁新聞數：{newslist_info["per_page"]}')
    # print(f'搜尋結果 > 當前頁數：{newslist_info["current_page"]}')
    # print(f'搜尋結果 > 最後頁數：{newslist_info["last_page"]}')
    # print(f'搜尋結果 > 前一頁網址：{newslist_info["prev_page_url"]}')
    # print(f'搜尋結果 > 下一頁網址：{newslist_info["next_page_url"]}')
    # print(f'搜尋結果 > 此頁新聞第一筆：{newslist_info["from"]}')
    # print(f'搜尋結果 > 此頁新聞最後一筆：{newslist_info["to"]}')

    for news in newslist_info["data"]:
        print(f'    ------------ {news["newsId"]} ------------')
        print(f'    新聞 > URL：https://news.cnyes.com/news/id/{news["newsId"]}')
        print(f'    新聞 > 標題：{news["title"]}')
        print(f'    新聞 > 概要：{news["summary"]}')
        print(f'    新聞 > 內文：{news["content"]}')
        print(f'    新聞 > 關鍵字：{news["keyword"]}')
        print(f'    新聞 > 發布時間：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(news["publishAt"]))}')
        # news["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(news["publishAt"]))
        print(f'    新聞 > 分類：{news["categoryName"]} (id:{news["categoryId"]})')
        print()
        break
        
    # with open('鉅亨網0501.json', 'w') as file:
    #     json.dump(newslist_info['data'], file)

    # csv_headers = list(newslist_info["data"][0].keys())
    # with open('鉅亨網0501.csv', 'w', newline='') as file:
    #     writer = csv.DictWriter(file, fieldnames=csv_headers)
    #     writer.writeheader()
    #     writer.writerows(newslist_info['data'])
    # Create a DataFrame from the data
    df = pd.DataFrame(newslist_info['data'])

    # Define the Excel file path
    xlsx_file = '鉅亨網0603.xlsx'

    # Write the DataFrame to an Excel file
    df.to_excel(xlsx_file, index=False, engine='openpyxl')
    # 如果要爬取多頁新聞，建議加入隨機 delay 一段時間，避免被反爬蟲偵測
    # time.sleep(random.uniform(2, 5))

