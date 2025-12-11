import requests
import sys
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup

#headers={
#    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
#    "Cookie": "csrftoken=AQq87BuIMx5YRmfRlt1UYjpL4KjxOnTR; sessionid=n1meq3qfff1xuujwbif2u0ghcjyfewia"
#}
cookie_csrftoken="AQq87BuIMx5YRmfRlt1UYjpL4KjxOnTR"
cookie_sessionid="qumsoenqs39163mh06ngkhc7ysf1iudu"

url="http://hacknet.htb/profile"
start_id=1
end_id=30
delay=0.05
outputfile="wordlists.txt"


session=requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0" })
#session.cookies.set("sessionid=n1meq3qfff1xuujwbif2u0ghcjyfewia","csrftoken=AQq87BuIMx5YRmfRlt1UYjpL4KjxOnTR",domain="10.10.11.85")
#this is wrong error
#parameter for set ccookie session.cookies.set(name, value, domain=...)


host=urlparse(url).hostname #will be hacknet.htb

session.cookies.set("sessionid",cookie_sessionid,domain=host)
session.cookies.set("csrftoken",cookie_csrftoken,domain=host)

print("Cookies in session before req:",session.cookies.get_dict(domain=host)) #.get_dict() method returns a Python dictionary of the name-value pairs for cookies held by the Session object.

#alternative session.get(url,cookies={"sessionid":....}




#if any(h.status_code in (301,302,303) for h in response.history) or "login" in response.url.lower():
#    print("Result: NOT LOGGED IN (redirected to login).")
#    return None
#if response.status_code != 200:
#    print(f"[info]{url} returned status {response.status_code}")
#    return None


def fetchpage(url):
    try:
        try:
            response=session.get(url,timeout=5,allow_redirects=True)
        except Exception as e:
            print(f"Failed to fetch url: {e}")
            return None

        if response.status_code in (401,403):
            print("Unauthorized")
            return None
        if any(h.status_code in (301,302,303) for h in response.history) or "login" in response.url.lower():
                print("Result: NOT LOGGED IN (redirected to login")
                return None
            #not doing this bcoz every time prints loged in
#        if response.status_code == 200:
#                 print("loged in")
        if response.status_code !=200:
                print("Error in requests")
                return None
        return response.text
    except KeyboardInterrupt:
        print("Keyboard Interrupted error")
        sys.exit(0)
def extractUsername(html):
 #response=requests.get('http://hacknet.htb/search?page=4')
    soup=BeautifulSoup(html,'html.parser')
   # print(soup.find_all("h2"))
    #webid=soup.find(id="profile-info")
    profile_div=soup.find("div",id="profile-info")
    if not profile_div:
        return None
    h2=profile_div.find("h2")
    if not h2:
        return None
    username=h2.get_text(strip=True) #strip removes duplicate username
    return username


def main():
    found_username=set()
    print(f"Scanning {url}/id from {start_id} to {end_id}")
    for i in range(start_id,end_id):
        url1=f"{url}/{i}"
        html=fetchpage(url1)
        if html is None:
            time.sleep(delay)
            continue

        username=extractUsername(html)
        if username:
            if username not in found_username:
                print(f"[+] id={i} username={username}")
                found_username.add(username)
        else:
                print(f"[+]id={i} no username found")
        time.sleep(delay)

          #save to file
    with open(outputfile,"w",encoding="utf-8") as f:
          for name in sorted(found_username):
            f.write(name + "\n")

    print(f"Done.  {len(found_username)} unique username(s) saved to  {outputfile}")

if __name__== "__main__":
          main()

