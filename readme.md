# wxgzh-api - 获取微信公众号的最近文章

本项目提供一种基于微信公众平台的方法获取微信公众号的最近文章

## 开始使用

### 前置

你应当创建一个`微信公众平台订阅号`

你应当安装`docker`和`docker-compose`

### 配置

1. 将本项目克隆至本地
```
git clone https://github.com/BeautyYuYanli/wxgzh-api.git
```

2. 登录`微信公众平台`, 将`mp.weixin.qq.com`域名下的cookie以`json`格式保存至`wxgzh-api/cookies.json`. 你可以使用这个插件:[chrome](https://chrome.google.com/webstore/detail/%E3%82%AF%E3%83%83%E3%82%AD%E3%83%BCjson%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E5%87%BA%E5%8A%9B-for-puppet/nmckokihipjgplolmcmjakknndddifde) [firefox](https://addons.mozilla.org/en-US/firefox/addon/%E3%82%AF%E3%83%83%E3%82%AD%E3%83%BCjson%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E5%87%BA%E5%8A%9B-for-puppeteer/)

3. 其它配置在`docker-compose.yml`自行修改

### 部署

完成配置后在`wxgzh-api`目录下执行
```
docker-compose up -d
```
以启动服务

### 使用

服务默认在`localhost:11459`监听. 你可以发送一个`get`请求, 并携带参数`query=公众号1$公众号2$...$公众号n`, 如:
```
requests.get("http://127.0.0.1:11459?query=大连理工大学$大连理工大学学生会").text
```
如果服务正常运行, 将返回`json`格式的字符串:
```json
{
    "大连理工大学":[
        {"date": "2021-01-16", "author": "大连理工大学", "title": "文章1", "link": "http://mp.weixin.qq.com/s?..."},
        {"date": "2021-01-15", "author": "大连理工大学", "title": "文章2", "link": "http://mp.weixin.qq.com/s?..."},
    ],
    "大连理工大学学生会":[
        {"date": "2021-01-15", "author": "大连理工大学学生会", "title": "文章3", "link": "http://mp.weixin.qq.com/s?..."},
        {"date": "2021-01-14", "author": "大连理工大学学生会", "title": "文章4", "link": "http://mp.weixin.qq.com/s?..."},
    ]
}
```
否则返回错误信息

### Warning

**为了避免被微信后台风控, 查询过程将长达`1min`以上**

**出于同样的理由, 请谨慎地控制调用该API的频率**

### Demo

本项目**可能触发微信后台的风险管控**, 故不提供demo. 你可以查看姊妹项目[wxgzh2tg](https://github.com/BeautyYuYanli/wxgzh2tg.git)的demo:

- Telegram Channel: [DUT_News](https://t.me/s/DUT_News)

- 与[RSSHub](https://github.com/DIYgod/RSSHub)协作, 将文章进一步转为[rss订阅链接](https://rsshub.app/telegram/channel/DUT_News)

## Todo

- [ ] 增加查询失败处理
