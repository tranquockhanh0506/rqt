from array import array
import scrapy
import re
from crawl_baomoi import crawl
from mongo_baomoi import check_code_exist, insert_many_news, client

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://baomoi.com/giao-thong.epi'
    ]

    def parse(self, response):
        decode_response = response.body.decode('utf-8')
        dict_link_thumbs = {}
        set_link_news = set(re.findall(r"\/[a-zA-Z0-9_.-]*\/c\/[0-9]*.epi", decode_response))
        set_link_thumbs = set(re.findall(r"(?:https:\/\/photo-baomoi.bmcdn.me)\/w[3|7]00\_[a-zA-Z0-9_]*\/[a-zA-Z0-9_]*\/[a-zA-Z0-9]*\.(?:gif|jpg)", decode_response))
        
        pat = re.compile("[0-9]{8}")
        for lt in set_link_thumbs:
            code = re.findall(pat, lt)[0]
            link_thumb_by_code = dict_link_thumbs.get(code, [])
            link_thumb_by_code.append(lt)
            dict_link_thumbs[code] = link_thumb_by_code

        array_inserts = []
        print(len(set_link_news))
        for ln in set_link_news:
            code = re.findall(pat, ln)[0]
            url = "https://baomoi.com" + ln

            if check_code_exist(code):
                print(code)
            else:
                dict_news = crawl(url, code)
                dict_news["thumbs"] = dict_link_thumbs.get(code, [])
                array_inserts.append(dict_news)

        if len(array_inserts) > 0:
            insert_many_news(array_inserts)
        
        client.close()
        