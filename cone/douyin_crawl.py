import requests
import re


def get_dytk(share_url):
    """
    传入个人主页分享出来的链接
    :param share_url:
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
    }
    res = requests.get(share_url, headers=headers, allow_redirects=True)
    user_id = re.findall(r'uid: "(.*?)"', res.text, re.S)[0]
    dytk = re.findall(r"dytk: '(.*?)'", res.text, re.S)[0]
    return {
        'user_id': user_id,
        'dytk': dytk
    }


def get_sign(user_id):
    """
    调用服务生成signature
    :param user_id:
    :return:
    """
    url = 'http://127.0.0.1:5000/get_sign/?user_id={}'.format(user_id)
    headers = {
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987'
        #               '.149 Safari/537.36',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
    }
    return requests.get(url, headers=headers).json()['signature']


def get_s_url(url):
    """
    获取在哪都能访问的无水印链接
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Geck'
                      'o) Chrome/34.0.1847.114 Mobile Safari/537.36'
    }
    s = requests.get(url, headers=headers)
    return s.url


def get_list(user_id: str, dytk: str):
    """
    测试
    :param user_id:
    :param dytk:
    :return:
    """
    sign = get_sign(user_id)
    if user_id.isdigit():
        url = f'https://www.iesdouyin.com/web/api/v2/aweme/post/?user_id={user_id}&sec_uid=&count=21&max_cursor=0&a' \
            f'id=1128&_signature={sign}&dytk={dytk}'
    else:
        url = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=' \
            f'{user_id}&count=21&max_cursor=0&a' \
            f'id=1128&_signature={sign}&dytk={dytk}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
    }
    res = requests.get(url, headers=headers).json()
    for aweme in res.get('aweme_list'):
        author_name = aweme.get('author').get('nickname')
        desc = aweme.get('desc')
        download_url = aweme.get('video').get('play_addr').get('url_list')[0]
        download_url = get_s_url(download_url)
        upda = {
            'author_name': author_name,
            'desc': desc,
            'download_url': download_url
        }
        print(upda)
        print('*' * 50)


if __name__ == '__main__':
    u_t = get_dytk('https://v.douyin.com/vduFju/')
    print(u_t)
    u = u_t['user_id']
    t = u_t['dytk']
    get_list(u, t)
