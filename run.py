import time
import json
import random
import wget
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager as CM

accountfile = open('account.json')
account=json.load(accountfile)

with open('Subject.txt','r') as s:
    subjects= [line.strip() for line in s]

def main(account):

    #opening the browser
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    bot = webdriver.Chrome(options=options, executable_path=CM().install())
    bot.get("https://www.instagram.com/")

    #Login section
    time.sleep(3)

    username_field = bot.find_element("xpath",  '//*[@id="loginForm"]/div/div[1]/div/label/input')
    username_field.send_keys(account["username"])
    time.sleep(1)

    pwd_field = bot.find_element("xpath", '//*[@id="loginForm"]/div/div[2]/div/label/input')
    pwd_field.send_keys(account["password"])
    time.sleep(1)

    bot.find_element("xpath", '//*[@id="loginForm"]/div/div[3]/button').click()
    time.sleep(6)

    # tags
    subject = random.choice(subjects)
    Hashtaglink = "https://www.instagram.com/explore/tags/"+subject
    bot.get(Hashtaglink)
    time.sleep(10)

    row1 = bot.find_element("xpath",'/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/article/div[1]/div/div/div[1]')
    row2 = bot.find_element("xpath",'/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/article/div[1]/div/div/div[2]')

    r1_link = row1.find_elements("tag name",'a')
    r2_link = row2.find_elements("tag name",'a')
    a_Links = r1_link + r2_link

    urls=[]
    for i in a_Links:
        if i.get_attribute('href') != None:
            urls.append(i.get_attribute('href'))

    #print(urls) 

    # Comments     
   
    for url in urls:
        bot.get(url)

        image = bot.find_element("tag name",'img').get_attribute('src')
        save_as = os.path.join('\images', subject + '.jpg') 
        wget.download(image,save_as )
        
        comBox = bot.find_element("xpath",'//*[@id="mount_0_0_gu"]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/ul[2]/div/li/div/div/div[2]/div[1]')

        comments = comBox.find_elements("tag name",'span')
        print(comments)


        bot.implicitly_wait(10)





main(account)



