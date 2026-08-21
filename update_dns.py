import os
import requests


TOKEN=os.environ["CF_API_TOKEN"]
ZONE=os.environ["CF_ZONE_ID"]


DOMAIN="cf.789446.xyz"


headers={
    "Authorization":
    f"Bearer {TOKEN}",

    "Content-Type":
    "application/json"
}


API=f"https://api.cloudflare.com/client/v4/zones/{ZONE}/dns_records"



def get_ip():

    with open(
        "IPlist-Pro.txt",
        encoding="utf-8"
    ) as f:

        for line in f:

            line=line.strip()

            if line:

                return line



def get_record():

    r=requests.get(
        API,
        headers=headers,
        params={
            "type":"A",
            "name":DOMAIN
        }
    )

    return r.json()["result"][0]



def update(ip):

    record=get_record()

    url=f"{API}/{record['id']}"


    data={

        "type":"A",

        "name":DOMAIN,

        "content":ip,

        "ttl":60,

        "proxied":False

    }


    r=requests.put(

        url,

        headers=headers,

        json=data

    )


    print(r.json())




ip=get_ip()

record=get_record()


print(
    "当前:",
    record["content"]
)


print(
    "新的:",
    ip
)


if ip != record["content"]:

    update(ip)

    print("更新完成")

else:

    print("无需更新")
