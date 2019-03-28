#!/usr/bin/nev python3
# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import datetime
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

browser = webdriver.Chrome()

def login():

    browser.get(loginURL)
    # 设置显式等待

    # accountInput = browser.find_element_by_xpath("//*[@id='app']/div/div/div/div[2]/div[4]/ul/li[2]/a")
    accountInput = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[4]/ul/li[2]/a')))
    print("accountInput ok!")
    accountInput.click()
    # usernameInput = browser.find_element_by_id("all")
    usernameInput = wait.until(EC.presence_of_element_located((By.ID, "all")))
    print("usernameInput ok!")
    # passwordInput = browser.find_element_by_id("password-number")
    passwordInput = wait.until(EC.presence_of_element_located((By.ID, "password-number")))
    print("passwordInput ok!")
    usernameInput.clear()
    usernameInput.send_keys(username)
    passwordInput.clear()
    passwordInput.send_keys(password)
    loginBtn = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div[2]/div[4]/form/div/div[6]/div/button')
    loginBtn.click()
    print("login...")
    print(1)
    wait.until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#all"), username))
    print(2)
    wait.until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#password-number"), password))
    print(3)
    # submit.click()
    time.sleep(3)


def getList():
    browser.get(listURL)
    # wait.until(EC.presence_of_element_located((By.XPATH)))
    # html = browser.find_element_by_id('content_views').get_attribute('innerHTML').strip()
    html = browser.page_source
    # print(html)
    contentTree = etree.HTML(html)
    missionList = contentTree.xpath('//*[@id="content_views"]/p/text()')
    print(missionList)
#     return missionList
#
# def todayList(missionList):
    missionTodo = []
    today = datetime.date.today().strftime("%m-%d").replace("-", "月") + "日"
    print(today)
    for mission in missionList:
        # print(mission.split()[0])
        if mission.split()[0] == today:
            missionTodo.append(" ".join(mission.split()[1:]))
            # print(mission.split()[1:])
    print(missionTodo)
    return today, '  \n'.join(missionTodo)

def sendMsg(data , content):
    myURL = "https://sc.ftqq.com/SCU47116T8a9ae0489e90d09ff9d1e94ad605b8715c9881e8b91dd.send"
    title = data + '待办事项'
    print(title)
    params = {
        'text': title,
        'desp': content
    }
    response = requests.get(myURL, params=params)

    if response.json()['errno'] == 0:
        print("ok")
    else:
        print("notok %s" %response.json()['errmsg'])

def main():
    scheduler = BlockingScheduler()
    print("test started")
    scheduler.add_job(entrance, 'cron',
                      day_of_week='0-6',
                      hour='12',
                      minute='11',
                      second='0')
    scheduler.start()

if __name__ == '__main__':
    # loginURL = "https://passport.csdn.net/login"
    # username = '15086672013'
    # password = 'Hhy3.1415926'
    # listURL = "https://blog.csdn.net/sinat_34937826/article/details/88838120"
    # listURL = "https://blog.csdn.net/sinat_34937826/article/details/88845359"
    loginURL = "https://passport.csdn.net/login"
    username = '15086672013'
    password = 'Hhy3.1415926'
    listURL = "https://note.youdao.com/web/#/file/recent/note/WEBf64ce040155b76a2826a3472e36e3916/"
    wait = WebDriverWait(browser, 10)


    # login()
    getList()
    data, content = getList()
    sendMsg(data, content)
    browser.quit()

