import requests
import pandas as pd
import os
import time

cur_path = os.path.dirname(os.path.abspath(__file__))

COOKIE="gr_user_id=f522933a-dca8-4afd-a712-8e387270454d; _bl_uid=Rnm4d8R42ghgq31jX2jUyd19LC4q; NOWCODERCLINETID=F82BA5CB374562F53877BB94067599B7; NOWCODERUID=85E6A32AC4F6146377387CC1AA5B3360; Hm_lvt_a808a1326b6c06c437de769d1b85b870=1741595293,1742277524; Hm_lvt_58f1fd267305278a5cc3d8b2f469de86=1743384861,1743644086,1743990296,1744594369; Hm_lpvt_58f1fd267305278a5cc3d8b2f469de86=1744594369; HMACCOUNT=405C57DE1D61BDBC; hrat=caa44caf5adc9d2e059d22f3fac55ff223345361e6e8019e4d68d3c0e96cfda0; _clck=soo8yh%7C2%7Cfv2%7C0%7C1895; acw_tc=0a065e8717446151747694194e19b383b931aee1e958a58fc6d8869fa14993; c196c3667d214851b11233f5c17f99d5_gr_session_id=f2baf7da-e01b-48f0-8597-ac7d8730f3ae; c196c3667d214851b11233f5c17f99d5_gr_session_id_f2baf7da-e01b-48f0-8597-ac7d8730f3ae=true"
BEARER_TOKEN="Bearer caa44caf5adc9d2e059d22f3fac55ff223345361e6e8019e4d68d3c0e96cfda0"
headers = {
    'accept': 'text/plain, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'authorization': BEARER_TOKEN,
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': COOKIE,
    'origin': 'https://hr.nowcoder.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://hr.nowcoder.com/console/paper/candidate/exam-result?projectId=47532',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

if not os.path.exists(os.path.join(cur_path, 'pdf')):
    os.makedirs(os.path.join(cur_path, 'pdf'))

if not os.path.exists(os.path.join(cur_path, 'excel')):
    os.makedirs(os.path.join(cur_path, 'excel'))

# 下载成绩报告到本地
def downloadFile(PAPER_NAME,url, fileName):
    r = requests.get(url,headers=headers,stream=True)
    if os.path.exists(os.path.join(cur_path, 'pdf',PAPER_NAME)):
        pass
    else:
        os.makedirs(os.path.join(cur_path, 'pdf',PAPER_NAME))
    with open(os.path.join(cur_path, 'pdf',PAPER_NAME, fileName),'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

dataList = []
def getTestData(PAPER_NAME,PAPER_ID,PROJECT_ID):
    payload = {
        'paperIds': PAPER_ID,
        'keywordType': '0',
        'union': '0',
        'isCheated': 'true',
        'word': '',
        'page': '1',
        'pageSize': '100',
        'orderBy': '0',
        'order': '2',
        'projectIdList': PROJECT_ID
    }

    response = requests.post('https://hr.nowcoder.com/v1/tests/poid-429356', headers=headers, data=payload)
    # print(response.text)
    data = response.json()["data"]["datas"]
    for da in data:
        tempDic={
            "试卷名称": da.get("paperName"),
            "应聘编号":da.get("testUserKey"),
            "人员ID": da.get("actorId"),
            "姓名": da.get("ncUser", {}).get("displayName"),
            "分数": da.get("score"),
            "IP地址": da.get("ipAddress"),
            "成绩报告": da.get("pdfUrl"),
        }
        print(tempDic)
        dataList.append(tempDic)
        downloadFile(PAPER_NAME,tempDic["成绩报告"], tempDic["姓名"]+"-"+tempDic["应聘编号"]+".pdf")

    # print(dataList)
    df = pd.DataFrame(dataList)

    df.to_excel(os.path.join(cur_path,"excel", f"{PAPER_NAME}-{int(time.time())}.xlsx"), index=False)


# 获取paperId
def getPaperId(projectId,date):
    params = (
        ('projectIdList', projectId),
        ('_', '1743579189229'),
    )

    response = requests.get('https://hr.nowcoder.com/v1/papers/oid-429356/simple', headers=headers, params=params)
    data = response.json()["data"]
    for da in data:
        if da["paperName"].endswith(date):
            print(da["paperName"],da["id"])
            return da["id"]
    
    return ""

# 每次修改时间和试卷id
date = "0412"

pageDicData=[
    {
        "PAPER_NAME": "%s-研发" % date,
        "PAPER_ID": "17427963", #修改这个试卷id
        "PROJECT_ID": "47533" 
    },
    {
        "PAPER_NAME": "%s-数据" % date,
        "PAPER_ID": "17427904",
        "PROJECT_ID": "47531" 
    },
    {
        "PAPER_NAME": "%s-算法" % date,
        "PAPER_ID": "17427965",
        "PROJECT_ID": "47532" 
    },
]

def main():
    for pageDic in pageDicData:
        pagerId = getPaperId(pageDic["PROJECT_ID"],date)
        if pagerId!="":
            getTestData(pageDic["PAPER_NAME"],pagerId,pageDic["PROJECT_ID"])
        else:
            print(f"{pageDic['PAPER_NAME']}-没有找到试卷id")

main()
