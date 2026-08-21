import csv
import os
import requests


# Cloudflare配置

API_TOKEN = os.environ["CF_API_TOKEN"]

ZONE_ID = os.environ["CF_ZONE_ID"]


# 你的优选域名

DOMAIN = "cf.789446.xyz"


headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}



# 获取第一名IP

with open("result.csv", "r", encoding="utf-8") as f:

    reader = csv.DictReader(f)

    first = next(reader)

    ip = first["IP"]



print("最佳IP:", ip)



# 查询DNS记录

url = (
    f"https://api.cloudflare.com/client/v4/"
    f"zones/{ZONE_ID}/dns_records"
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



record_id = data["result"][0]["id"]



# 修改DNS

update_url = (

    f"https://api.cloudflare.com/client/v4/"
    f"zones/{ZONE_ID}/dns_records/{record_id}"

)



payload = {

    "type": "A",

    "name": DOMAIN,

    "content": ip,

    "ttl": 60,

    "proxied": True

}



r = requests.put(

    update_url,

    headers=headers,

    json=payload

)



print(r.json())

print("DNS更新完成")
