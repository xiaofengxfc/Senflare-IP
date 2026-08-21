import os
import requests
import re



# ==================
# Cloudflare配置
# ==================

API_TOKEN = os.environ.get("CF_API_TOKEN")

ZONE_ID = os.environ.get("CF_ZONE_ID")



# 修改成你的优选域名

DOMAIN = "cf.789446.xyz"





if not API_TOKEN:

    raise Exception("缺少 CF_API_TOKEN")



if not ZONE_ID:

    raise Exception("缺少 CF_ZONE_ID")





# ==================
# 读取Senflare排名
# ==================


FILE="Ranking.txt"



if not os.path.exists(FILE):

    raise Exception(
        "找不到 Ranking.txt"
    )





best_ip=None



with open(
    FILE,
    "r",
    encoding="utf-8"
) as f:


    text=f.read()



# 匹配IPv4

ips=re.findall(

    r"\b(?:\d{1,3}\.){3}\d{1,3}\b",

    text

)



if ips:


    best_ip=ips[0]





if not best_ip:

    raise Exception(
        "没有找到优选IP"
    )



print(
    "最佳IP:",
    best_ip
)





# ==================
# Cloudflare DNS
# ==================



headers={


"Authorization":
f"Bearer {API_TOKEN}",


"Content-Type":
"application/json"


}



url=(

"https://api.cloudflare.com/client/v4/zones/"

+ZONE_ID+

"/dns_records"

)



r=requests.get(

url,

headers=headers,

params={

"type":"A",

"name":DOMAIN

}

)



data=r.json()



if not data["success"]:

    raise Exception(data)



record=data["result"][0]



update_url=(

url+

"/"+record["id"]

)



payload={


"type":"A",


"name":DOMAIN,


"content":best_ip,


"ttl":60,


"proxied":True


}



r=requests.put(

update_url,

headers=headers,

json=payload

)



result=r.json()



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

    raise Exception(result)
