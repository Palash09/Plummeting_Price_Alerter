import requests
import time
from bs4 import BeautifulSoup
from notify_run import Notify
from datetime import datetime 
import smtplib


URL = 'https://www.amazon.in/Puma-Mens-Hip-Perf-Sneakers/dp/B07NHPVXM1/ref=pd_sbs_309_1/258-9123127-7144531?_encoding=UTF8&pd_rd_i=B07NJHHVZS&pd_rd_r=913ec0e6-0cb4-4d23-9958-8ec0bd3e83fc&pd_rd_w=5dpWT&pd_rd_wg=x9n2F&pf_rd_p=b5c4df7b-dc8c-47a6-947a-01271326b67b&pf_rd_r=D3QSWN9RNNA2142KF7M3&refRID=D3QSWN9RNNA2142KF7M3&th=1&psc=1'

url = URL

dp = 999

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"}

page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content,'html.parser')

title = soup.find(id="productTitle").get_text()
price = soup.find(id="priceblock_ourprice").get_text()
actual_price = price[2:]

#For making actual_price an integer
l = len(actual_price)
if l<=6:
    actual_price = price[2:5]
else:
    p1 = price[2]
    p2 = price[4:7]
    pf = str(p1) + str(p2)
    actual_price = int(pf)
       

price_now = int(actual_price)

title_prod = str(title.strip())
actual_price_prod = actual_price
pnmsg = "Rs." +str(actual_price_prod)+"for "+title_prod

print("NAME :"+ title_prod)
print("ACTUAL PRICE :"+ str(actual_price_prod))
print("DESIRED PRICE :"+ str(dp))
    

    

def check_price():
    count = 0
    if(price_now > dp):
        send_mail()
        push_notification()
    else:
        count = count + 1
        print("Rechecking...Last checked at"+str(datetime.now()))
   

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('9798paul@gmail.com','baiktbmqskkdqfqo')

    subject = "Price of "+title_prod+" has fallen down to Rs."+str(actual_price_prod)
    body = "Hey How are you! \n The price of "+title_prod+" on Amazon has fallen down to Rs."+str(actual_price_prod)+",which is less than your desired price of Rs."+str(dp)+". \n So,hurry up and check the amazon link now...  :"+url
    msg = f"Subject: {subject} \n\n {body}"

    server.sendmail(
        '9798paul@gmail.com',
        'palash79sharma@gmail.com',
        msg
    )
    print('Hey Palash! Email has been sent')

    server.quit()

def push_notification():
    notify = Notify()
    notify.send(pnmsg)
    print("Hey Push Notification has been sent successfully")

    
count = 0
while(True):
    count += 1
    print("Count:"+str(count))
    check_price()
    time.sleep(60)




