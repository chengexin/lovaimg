import requests
def love():
    url = r'https://chp.shadiao.app/api.php'
    respon = requests.get(url)
    lovetalk_text = respon.text
    return lovetalk_text

if __name__ == '__main__':
    love = love()
    print(love)