import os
import csv
import requests


# =========================
# Cloudflare配置
# =========================

API_TOKEN = os.environ.get("CF_API_TOKEN")

ZONE_ID = os.environ.get("CF_ZONE_ID")


# 修改成你的优选域名
DOMAIN = "cf.789446.xyz"



if not API_TOKEN:
    raise Exception("缺少 CF_API_TOKEN")


if not ZONE_ID:
    raise Exception("缺少 CF_ZONE_ID")



# =========================
# 读取CFST结果
# =========================

RESULT_FILE = "result.csv"



if not os.path.exists(RESULT_FILE):

    raise Exception("找不到 result.csv")



best_ip = None



with open(
    RESULT_FILE,
    "r",
    encoding="utf-8-sig"
) as f:


    reader = csv.DictReader(f)



    for row in reader:


        print(row)


        # CloudflareSpeedTest v2.3.5
        if "IP 地址" in row:

            best_ip = row["IP 地址"]

            break



        # 兼容英文
        elif "IP" in row:

            best_ip = row["IP"]

            break



if not best_ip:

    raise Exception(
        "没有找到测速IP"
    )



print("================")

print(
    "最佳IP:",
    best_ip
)

print("================")



# =========================
# 查询DNS
# =========================


headers = {


    "Authorization":
    f"Bearer {API_TOKEN}",


    "Content-Type":
    "application/json"

}



dns_url = (

    "https://api.cloudflare.com/client/v4/zones/"
    f"{ZONE_ID}/dns_records"

)



params = {


    "type":"A",


    "name":DOMAIN

}



response = requests.get(

    dns_url,

    headers=headers,

    params=params

)



data=response.json()



if not data["success"]:

    raise Exception(data)



records=data["result"]



if len(records)==0:

    raise Exception(
        "Cloudflare没有找到该DNS记录"
    )



record_id=records[0]["id"]




# =========================
# 更新DNS
# =========================


update_url=(

    f"{dns_url}/{record_id}"

)



payload={


    "type":"A",


    "name":DOMAIN,


    "content":best_ip,


    "ttl":60,


    "proxied":True

}



response=requests.put(

    update_url,

    headers=headers,

    json=payload

)



result=response.json()



if result["success"]:


    print(
        "DNS更新成功"
    )


    print(
        DOMAIN,
        "=>",
        best_ip
    )


else:


    print(result)

    raise Exception(
        "DNS更新失败"
    )
