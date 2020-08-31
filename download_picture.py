import json

import pypexels
import requests

# api_documentation : https://www.pexels.com/api/documentation/
# 记得记得记得填入api
api_key = ''
url = r'https://api.pexels.com/v1/photos/'
url_list = []
# 中文搜索，需转换为16进制
query = 'china'
per_page = '5'


# 获取图片下载地址
def get_picture_download_url(api_key, url):
    headers = {'Authorization': api_key}
    print('正在获取图片地址.')
    with requests.get(url=url, headers=headers, stream=True) as respon:
        respon = respon.text
    # 转换成json格式数据
    respon = json.loads(respon)
    # 返回照片地址
    picture_url = respon['src']['large2x']
    return picture_url


# 获取图片id
def get_picture_id(api_key, query, per_page):
    id_list = []
    py_pexel = pypexels.PyPexels(api_key)
    search_results = py_pexel.search(query=query, per_page=per_page)
    print('正在获取图片ID.')
    for photo in search_results.entries:
        id_list.append(photo.id)
        # photo.id, photo.photographer, photo.url
    return id_list


# 下载图片
def dowload_picture(picture_url, path):
    with requests.get(picture_url, stream=True) as picture:
        with open(path, 'wb') as f:
            print('正在下载图片.')
            for chunk in picture.iter_content(chunk_size=8192):
                f.write(chunk)


# 开始新的下载
def start_new_dowload(api_key, query, per_page):
    id_list = get_picture_id(api_key, query, per_page)
    id_list_num = len(id_list)
    for id_num in range(0, id_list_num):
        id = id_list[id_num]
        with open('data.txt', 'w') as f:
            f.write('query:{}\n'.format(query))
            f.write('per_page:{}\n'.format(per_page))
            f.write('id_num:{}'.format(id_num))
        url_id = url + str(id)
        picture_url = get_picture_download_url(api_key, url_id)
        path = r'.\picture\\' + str(id) + '.jpg'
        dowload_picture(picture_url, path)


# 继续上一次下载
def start_last_dowload(api_key):
    # 读取上次下载情况
    with open('data.txt', 'r') as f:
        data = f.readlines()
    # 获取数据
    query = data[0][6:]
    per_page = data[1][9:]
    id_last_num = int(data[2][7:])
    id_list = get_picture_id(api_key, query, per_page)
    id_list_num = len(id_list)
    for id_num in range(id_last_num, id_list_num):
        id = id_list[id_num]
        with open('data.txt', 'w') as f:
            f.write('query:{}'.format(query))
            f.write('per_page:{}'.format(per_page))
            f.write('id_num:{}'.format(id_num))
        url_id = url + str(id)
        picture_url = get_picture_download_url(api_key, url_id)
        path = r'.\picture\\' + str(id) + '.jpg'
        dowload_picture(picture_url, path)


if __name__ == '__main__':
    #start_new_dowload(api_key, 'lovers', 50)
    #start_last_dowload(api_key)
    start_new_dowload(api_key, 'japan', 10)
