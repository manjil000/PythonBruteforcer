import requests
import sys
from bs4 import BeautifulSoup
#from urllib.parse import urlparse


utl="http://hacknet.htb/profile"


out="users.txt"
#---------------------step 1 connect to website with cookieis-----------
#creates a session objects
session=requests.Session()

session.headers.update({
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
    })

a=input("Enter the csrf cookie")
b=input("Enter the session cookie")
domain="hacknet.htb"
session.cookies.set("csrftoken",a,domain=domain)
session.cookies.set("sessionid",b,domain=domain)

#requests.get(...) → one-off request. You’d have to manually pass cookies every time.
#session = requests.Session() → remembers cookies, headers, login state, etc. If you set cookies once in the session, every session.get() will automatically use them.

#usernames=[]
found_users=set()
for i in range(1,30):
    url=f"{utl}/{i}"
    try:
        resp=session.get(url,timeout=5)
    except Exception as e:
        print(f"Error at {i}:{e}")
        continue
    if any(h.status_code in (301,302,303) for h in resp.history) or "login" in resp.url.lower():
        print(f"{i} not logged in")
        continue
    if resp.status_code != 200:
        print(f"[{i}] Skipping: status {resp.status_code}")
        continue
    soup=BeautifulSoup(resp.text,'html.parser')
    profile_div=soup.find("div",id="profile-info")
    if not profile_div:
       print("Error inside beautiful soup")
       continue
    h2=profile_div.find("h2")
    if not h2:
        print("Error inside h2")
        continue

    username=h2.get_text(strip=True)
    if username:
        print(f"username of id{i}: is {username}")
        found_users.add(username)
    else:
        print("h2 found but empty")
if found_users:
    with open(out,"w",encoding="utf-8") as f:
        for name in found_users:
            f.write(name+"\n")
            print("wrote to wordlists")
else:
    print("no username found")
#clean ans show requestssults
#usernames=list(set(usernames))
#print(f"collected usernames: {usernames}")




