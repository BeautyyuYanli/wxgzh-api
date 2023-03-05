import os
from flask import Flask,  request, make_response
from wxgzh_api.updater import Updater
from wxgzh_api.updater.exceptions import CookieException

app = Flask(__name__)


@app.route('/json_feeds', methods=['GET'])
def json_feeds():
    try:
        updater = Updater(cookiefile=os.getenv('COOKIE_FILE'))
    except CookieException as e:
        return make_response(str(e), 500)
    except Exception as e:
        return make_response(str(e), 500)
    result = updater.update(request.args.getlist('target'))
    content = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": "微信公众号",
        "home_page_url": "https://github.com/BeautyyuYanli/wxgzh-api",
        "description": "微信公众号文章更新推送",
        "items": [item for sublist in result.values() for item in sublist]
    }
    return make_response(content, 200, {'Content-Type': 'application/feed+json'})
