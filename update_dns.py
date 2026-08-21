import os
import csv
import requests


# =========================
# Cloudflare配置
# =========================

API_TOKEN = os.environ.get("CF_API_TOKEN")

ZONE_ID = os.environ.get("CF_ZONE_ID")


# 你的优选域名
DOMAIN = "cf.789446.xyz"



if not API_TOKEN:
    raise Exception("没有设置 CF_API_TOKEN")


if not ZONE_ID:
    raise Exception("没有设置 CF_ZONE_ID")



# =========================
# 读取测速结果
# =========================

RESULT_FILE = "result.csv"



if not os.path.exists(RESULT_FILE):

    raise Exception("没有找到 result.csv")



best_ip = None



with open(
    RESULT_FILE,
    "r",
    encoding="utf-8"
) as f:


    reader = csv.DictReader(f)


    for row in reader:


        print(row)


        # CFST新版字段
        if "IP地址" in row:

            best_ip = row["IP地址"]

            break


        # 英文版本兼容
        if "IP" in row:

            best_ip = row["IP"]

            break




if not best_ip:

    raise Exception(
        "没有找到测速IP"
    )



print(
    "最佳IP:",
    best_ip
)



# =========================
# 查询DNS记录
# =========================


headers = {


    "Authorization":
        f"Bearer {API_TOKEN}",


    "Content-Type":
        "application/json"

}



url = (

    f"https://api.cloudflare.com/client/v4/zones/"
    f"{ZONE_ID}/dns_records"

)



params = {


    "name": DOMAIN,


    "type": "A"

}



r = requests.get(

    url,

    headers=headers,

    params=params

)



data = r.json()



if not data["success"]:

    raise Exception(data)



records = data["result"]



if not records:


    raise Exception(
        "找不到DNS记录"
    )



record_id = records[0]["id"]



# =========================
# 修改DNS
# =========================


update_url = (

    f"https://api.cloudflare.com/client/v4/zones/"
    f"{ZONE_ID}/dns_records/{record_id}"

)



payload = {


    "type":"A",


    "name":DOMAIN,


    "content":best_ip,


    "ttl":60,


    "proxied":True

}



r = requests.put(

    update_url,

    headers=headers,

    json=payload

)



result = r.json()



if result["success"]:


    print(
        "DNS更新成功:",
        best_ip
    )


else:


    print(result)


    raise Exception(
        "DNS更新失败"
    )
