from array import array
from turtle import title
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def crawl(url, code):

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    soup = BeautifulSoup(response.text, 'lxml')

    try:
        all_info = soup.select_one("#__next > div:nth-child(4) > div > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)")
        if all_info is None:
            all_info = soup.select_one("#__next > div:nth-child(3) > div > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)")

        title = all_info.select_one("h1:nth-child(1)").text #tieu de

        info_html = all_info.select_one("div:nth-child(2)")
        time_news = info_html.select_one("time")["datetime"] #2022-09-10T23:18:00.000Z - thoi gian cua bai bao
        raw_publisher = info_html.select_one("a:nth-child(1) > figure > img")
        raw_publisher_name = raw_publisher["alt"] #Báo Đại Đoàn Kết
        raw_publisher_img = raw_publisher["src"] #https://photo-baomoi.bmcdn.me/ad4acb251666ff38a677.png

        description = all_info.select_one("h3:nth-child(3)").text #doan van dau tien

        array_images = []
        array_news = []
        author = "Báo Mới"
        primary_news = all_info.select_one("div:nth-child(4)")
        pns = primary_news.find_all(recursive=False)
        for i, v in enumerate(pns):
            if v.name == "div" and v.has_attr("class") and "body-image" in v["class"] and len(array_images) == 0:
                img = v.select_one("figure:nth-child(1) > img")
                if img is not None and img.has_attr("alt") and img.has_attr("src"):
                    array_images.append({
                        "img_alt": img["alt"],
                        "img_src": img["src"]
                    })

            if v.name == "p":
                if i == len(pns) - 1 and v.select_one("strong:nth-child(1)") is not None:
                    author = v.select_one("strong:nth-child(1)").text
                # elif v.select_one("em") is not None:
                #     print(v)
                #     continue
                else:
                    array_news.append(v.text)


        return {
            "code": code,
            "url": url,
            "title": title,
            "time_in_bao_moi": convert_date(time_news),
            "raw_publisher_name": raw_publisher_name,
            "raw_publisher_img": raw_publisher_img,
            "description": description,
            "array_images": array_images,
            "array_news": array_news,
            "author": author,
            "created_time": datetime.now()
        }
    except:
        return {
            "code": code,
            "url": url,
            "created_time": datetime.now(),
        }

def convert_date(date_time_to_con, format = "%Y-%m-%dT%H:%M:%S.%fZ"):
    date_time_obj = datetime.strptime(date_time_to_con, format)
    return date_time_obj


#print(crawl("https://baomoi.com/bot-cai-lay-bat-dau-thu-phi-thu-nghiem-tu-13-gio-ngay-25-9/c/43823554.epi", 1))
