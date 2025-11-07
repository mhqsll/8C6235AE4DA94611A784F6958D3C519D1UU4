import requests
import time

headers = {
    'Host': 'proservice.powerlong.com',
    'Connection': 'keep-alive',
    'Content-Length': '1289',
    'content-type': 'application/json',
    'uid': '7d63c6f83d9543e3b80b389bfc42c841',
    'token': '157374fe698440b2a56d19eaf895aa61',
    'platformType': '1',
    'charset': 'utf-8',
    # 'Referer': 'https://servicewechat.com/wxefc15bc9d0cb36b1/259/page-frame.html',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 14; 23078RKD5C Build/UP1A.230905.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.103 Mobile Safari/537.36 XWEB/1300259 MMWEBSDK/20241103 MMWEBID/7927 MicroMessenger/8.0.55.2780(0x2800373B) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android',
    'Accept-Encoding': 'gzip, deflate, br',
}

post_data={
    "miniAppKey": "MAIN_MINIAPP",
    "projectId": "WLKJ7E1C7AFAFB43E986670A81CF4258",
    "uid": "7d63c6f83d9543e3b80b389bfc42c841",
    "openId": "oWIV75WK0axPVPfsSE7z5wU6vNaA",
    "parkOrderNum": "190119663E7oGD1XxJ3oS2ylnL4V0D",
    "sign": "9cc88f7baefec382f90174aa92c7a592e58c6e8e",
    "encryptedData": "TWY/+Y2hgY5jcvMLAjEk5wQRSA24Isw0p7KX+LzL5teci6XpBCwWV22mWcgUtxS9nb07qBxkBU5PYqu6Kv1ZHN00mjDIb6BnFoncJFHSavVNsHtcjzNJhAfc7JEwrvOqxq68WLGhdduMbSKLMx8A1fQ9bTnhNMw5A0fFiae6WPuELgfO4xr6L4PsAvbA+WuYaLXN9VBBdNAcCsfMJOP+j+ChAGedbBs6N7gqfbcNRje287786n8R5IHML7So4oiRvSqw5ZbKU+Ip+4Yct3VkXUo1WJuhxQNfL9Hc9XqhFNFuDoNb3BgAwP5rHydOnOUtxC9lSDHr2gYdk15FBcA35lCZovgs6To8WBaq7s1fKL1gTjLplttWQ7lNMl5HsNRDA567T+BZFYCK1NzK3cSaa7l0yDaWfpFx09XwwZ6D/l4hwDkQN7poMWvrNMq97UkeoLK1+XXiLCwu+9/whXsaLGFccT6nsRpC4Zrrl6WbDWcKlebtFbwD5eKq3aSy0L4h4wBudTBUM5vFu5MP8DNMGeJ/9FD7dZd+QP4rpAVA78UWek7j7B58NOmCBH6PHipToXf7hitIDLd2Yq5+6ngsjPICK+ccwKEFM/aIEk/g490YZIvzY7rGLJi22yfPiBoSuPtzgSayUwKhslyB3OaLpVF8rk0txXQ2ZqwRYLFRmaw=",
    "timestamp": 1735981778411
}

# 刷新token
def refreshToken():
    global headers
    url = "https://proservice.powerlong.com/member/refresh/token"
    res = requests.post(url, headers=headers, json=post_data,verify=False)
    print(res.text)
    token = res.json()["data"]["token"]
    headers["token"] = token
    print("token",token)
    return token


def sign():
    params = (
        ('miniAppKey', 'MAIN_MINIAPP'),
        ('projectId', 'WLKJ7E1C7AFAFB43E986670A81CF4258'),
        ('uid', '7d63c6f83d9543e3b80b389bfc42c841'),
    )

    response = requests.get('https://proservice.powerlong.com/signinApply/doWiexinSignin', headers=headers, params=params,verify=False)
    print(response.text)


def main():
    refreshToken()
    sign()
    # 测试
        
main()
