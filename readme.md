# wxgzh-api - 获取任意微信公众号的最近文章

本项目提供一种基于微信公众平台的方法，获取任意微信公众号的最近文章。

## 开始使用

### Step 1. 准备

0. 创建一个`微信公众平台订阅号`
1. 若使用`docker`和`docker-compose`部署, 则安装`docker`和`docker-compose`

   若手动部署，则安装`python3.10+`, `firefox`, `geckodriver`, 以及`requirements.txt`中的依赖
2. 将项目克隆至本地
    ```
    git clone https://github.com/BeautyYuYanli/wxgzh-api.git
    ```
3. 登录`微信公众平台`, 将`mp.weixin.qq.com`域名下的cookie以`json`格式保存至`wxgzh-api/cookies.json`. 你可以使用这个插件:[chrome](https://chrome.google.com/webstore/detail/%E3%82%AF%E3%83%83%E3%82%AD%E3%83%BCjson%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E5%87%BA%E5%8A%9B-for-puppet/nmckokihipjgplolmcmjakknndddifde) [firefox](https://addons.mozilla.org/en-US/firefox/addon/%E3%82%AF%E3%83%83%E3%82%AD%E3%83%BCjson%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E5%87%BA%E5%8A%9B-for-puppeteer/)

### Step 2. 部署

#### 方法一、 docker + docker-compose

1. `docker-compose up -d`

#### 方法二、 手动部署

1. `pip3 install waitress`
2. `python3 -m waitress --port=11459 server:app`

### Step 3. 使用

已部署的服务默认在 `localhost:11459` 监听。

`/json_feed`: `GET`, 多个参数 `target`, 返回 [RSS JSON Feed](https://www.jsonfeed.org/2020/08/07/json-feed-version.html) (`application/feed+json`)格式的数据:
```
http://127.0.0.1:11459/json_feeds?target=声动活泼&target=汪小喵爱大工
```
```json
{
  "title": "微信公众号",
  "version": "https://jsonfeed.org/version/1.1",
  "description": "微信公众号文章更新推送",
  "home_page_url": "https://github.com/BeautyyuYanli/wxgzh-api",
  "items": [
    {
      "authors": [
        {
          "name": "声动活泼"
        }
      ],
      "date_published": "2023-03-05T00:00:00+08:00",
      "title": "一年了！声动胡同有了这些新变化，邀请你来加入",
      "url": "http://mp.weixin.qq.com/s?__biz=MzIwMDczNTE3OQ==&mid=2247496071&idx=1&sn=7024a904a4cf6f448ebbcc2888cf282c&chksm=96fa1123a18d983599aba221d7d1a8cbd0c80d2773f9cdb1b13c2ead9cadcfe905f8ad94fe4f#rd"
    },
    {
      "authors": [
        {
          "name": "汪小喵爱大工"
        }
      ],
      "date_published": "2023-03-05T00:00:00+08:00",
      "title": "公告&amp;记录 | 查询汪小喵精神状态",
      "url": "http://mp.weixin.qq.com/s?__biz=MzI4NzYwMTYxMQ==&mid=2247487382&idx=1&sn=7774bfc2e7fed6473982b191fac1c225&chksm=ebca6932dcbde024ed77f52f855fe61beb6fcfb49f3700482a52d7c6e0185ddab043968ab052#rd"
    }
  ]
}

```

也可以在不部署的情形下直接拉取数据:
```
python standalone.py -h
```
```
usage: standalone.py [-h] [--cookiefile COOKIEFILE] [--target TARGET [TARGET ...]]

options:
  -h, --help            show this help message and exit
  --cookiefile COOKIEFILE
  --target TARGET [TARGET ...]

```

## 开发

本项目还可以直接作为 Python 模块使用(TODO)

## 其他

- 频繁请求可能导致账号被风控。
- Cookies 有效期为 3 天，过期后需要重新获取。

本项目还可能对账号造成其它未知的影响, 请自行承担风险。
