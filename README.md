## 코드

```sh
# -*- coding: utf-8 -*-
from urllib.parse import DefragResult
from flask import Flask, render_template, request,redirect, url_for, flash,jsonify, send_file, session,escape
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_,text,update
import json
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.sql.elements import Null
from werkzeug.utils import secure_filename
import os, sys, re
import random, string
import pymysql
import sqlalchemy 
from itertools import groupby


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
from urllib.request import urlretrieve

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///craw.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class webtoon(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))

    def __init__(self,id,title):
        self.id=id
        self.title = title

options=webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('window-size=1920x1080') 
options.add_argument("disable-gpu")
options.add_argument("user-data-dir=C:\\environments\\selenium")
driver = webdriver.Chrome('E:/othertest/driver/chromedriver.exe', options=options) #또는 chromedriver.exe
driver.maximize_window()
actions = webdriver.ActionChains(driver)
driver.implicitly_wait(15) # 묵시적 대기, 활성화를 최대 15초가지 기다린다.

element='https://comic.naver.com/webtoon/weekday'
driver.get(element)

time.sleep(3)

# webtext=driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[1]/div/ul')


for i in range(1,51):
    
    webtext=driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[1]/div/ul/li['+str(i)+']/a')
    print(webtext.text)

    webtoon_number=i
    webtoon_text=webtext.text
    inputScDb = webtoon(webtoon_number,webtoon_text) 
    db.session.add(inputScDb)
    db.session.commit()


'''
