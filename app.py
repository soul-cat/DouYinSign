from functools import wraps
from flask import Flask
from flask import request
from selenium import webdriver
from threading import Thread
from time import sleep


app = Flask(__name__)


def keep_bro():
    global driver
    option = webdriver.FirefoxOptions()
    # option.set_headless()
    driver = webdriver.Firefox(options=option)
    # script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
    # driver.execute_script(script)
    while True:
        driver.get("https://www.iesdouyin.com/share/user/96956380265")
        sleep(30)


@app.before_first_request
def open_service():
    Thread(target=keep_bro).start()


def refresh_driver(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        driver.refresh()
        return result
    return wrapper


def gen_sign(user_id):
    js = '''
    _byteacrawl = __M.require("douyin_falcon:node_modules/byted-acrawler/dist/runtime");
    signature = _byteacrawl.sign('{}');
    return signature
    '''.format(user_id)
    return {
        'code': 1,
        'signature': driver.execute_script(js)
    }


@app.route('/get_sign/')
def get_sign():
    user_id = request.args.get('user_id')
    return gen_sign(user_id)


if __name__ == '__main__':
    app.run()
