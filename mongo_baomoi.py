import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

bao_moi = client["bao_moi"]
giao_thong_news = bao_moi["giao_thong_news"]

def check_code_exist(code):
    prr = giao_thong_news.find_one({'code': code})
    if prr is None:
        return False
    return True

def insert_many_news(array_inserts):
    giao_thong_news.insert_many(array_inserts)

def find_one(code):
    prr = giao_thong_news.find_one({'code': code}, {'_id': 0})

    return prr

def find_all(page = 1, size = 10):

    if page <= 0:
        page = 1

    skip = (page - 1) * size
    dict_project = {
        "_id": 0,
        "code": 1,
        "url": 1,
        "title": 1,
        "time_in_bao_moi": 1,
        "raw_publisher_name": 1,
        "raw_publisher_img": 1,
        "description": 1,
        "thumbs": 1
    }

    list_sort = [("time_in_bao_moi", -1), ("created_time", -1)]
    list_bao_moi = giao_thong_news.find({}, dict_project).sort(list_sort).limit(size).skip(skip)
    data = []
    for lbm in list_bao_moi:
        data.append(lbm)

    return data
