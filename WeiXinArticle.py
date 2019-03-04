import requests
from urllib.parse import urlencode
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
headers = {
    'Cookie': 'IPLOC=CN4419; SUID=9EBA4E713320910A000000005C7D02AF; SUV=1551696558427502; ABTEST=0|1551696562|v1; SNUID=B590655A2A2EA969A844994A2B61B53C; weixinIndexVisited=1; JSESSIONID=aaaV9_aeMCm1m9E3lyZKw; sct=3; ppinf=5|1551696912|1552906512|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTYlOTclQUQlRTUlOEQlODd8Y3J0OjEwOjE1NTE2OTY5MTJ8cmVmbmljazoxODolRTYlOTclQUQlRTUlOEQlODd8dXNlcmlkOjQ0Om85dDJsdURBa3pTUV9TRmhpRFlfa0tmSGUwUEVAd2VpeGluLnNvaHUuY29tfA; pprdig=jcFOsL6HSfRfgKVylywFLYDvsXoVSR2sv88FbKmofrlluwI1o54luAtmDxJu80ClGAG-P1j3KLkTD9GAmZ5yUKSQCe-LIsG8e-3rTZNpHxbCoY1_9euK5aDo_ZaW2moZ38oKJUKadRJSBj3IYfl1mV8h1YVw71rbCo1qzNDI9QQ; sgid=01-37461965-AVx9BBArqPa3vV9Fs1K8oicc; ppmdig=15516969120000006bef6c7cff0eb520c30dff289163d78f',
    'Host': 'weixin.sogou.com',
    'Referer': 'https://weixin.sogou.com/weixin?query=%E5%A3%81%E7%BA%B8&type=2&page=10',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
base_url = 'https://weixin.sogou.com/weixin?'
keyword = '风光'
proxy_pool_url = 'http://127.0.0.1:5555/random'
proxy = None
max_count = 5

def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError :
        return None



def get_html(url,count=1):
    global proxy
    if count >= max_count:
        print('Tried Too Many Counts')
        return None

    try:
        if proxy:
            proxies = {
                'http':'http://' + proxy
            }
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            proxy = get_proxy()
            if proxy:
                print('Using proxy',proxy)
                count += 1
            return get_html(url)
        else:
            print('Get proxy Failed')
            return None
    except ConnectionError as e:
        print('Error Occurred', e.args)
        proxy = get_proxy()
        return get_html(url)

def get_index(keyword,page):
    data = {
        'query': 'keyword',
        'type': '2',
        'page': page,
        'ie': 'utf8',
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    print(html)

def parse_index(html):
    doc = pq(html)
    items = doc('')
def main():
    for page in range(1,101):
        html = get_index(keyword,page)
if __name__ == '__main__':
    main()
