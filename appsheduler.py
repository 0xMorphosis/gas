from aiogram import Bot, Dispatcher, F
import asyncio
from pymongo.mongo_client import MongoClient
import logging
from core.settings import settings
from core.handlers.basic import on_start, get_price
import certifi
from core.handlers.sander import go
import asyncio
import pprint
import json
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from aiogram.types import Message
import time
from requests import request
from bs4 import BeautifulSoup
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from requests import Request, Session

import random
from threading import Lock



client = MongoClient(settings.bots.mongo_db,tlsCAFile=certifi.where())

collection = client.AppBase.Users

async def parse(bot: Bot):
    client = MongoClient(settings.bots.mongo_db)
    collection = client.AppBase.Users
    admin_id = settings.bots.admin_id

    driver = webdriver.Chrome()

    # Parse the first page
    driver.get("https://explorer.mantle.xyz/address/0x319B69888b0d11cEC22caA5034e25FfFBDc88421/transactions#address-tabs")
    time.sleep(10)

    try:
    driver.implicitly_wait(10)  # Чекаємо, коли елементи з'являться на сторінці
    # Шукаємо другий div елемент з класом 'chakra-skeleton css-mkh3pz', що містить Fee MNT
    fee_elements = driver.find_elements(By.CSS_SELECTOR, ".css-5ujltp .chakra-skeleton.css-mkh3pz")
    if len(fee_elements) > 1:
        fee_text = fee_elements[1].text.strip()  # Витягуємо текст з другого div елемента
        fee_parts = fee_text.split(' ')
        if len(fee_parts) > 0:
            fee_amount = fee_parts[0][:4]  # Отримуємо перші 4 цифри з суми комісії
        else:
            fee_amount = "0"  # Якщо не вдалося отримати текст, повертаємо "0" (або інше значення за замовчуванням)
    print(fee_amount)
except Exception as e:
    print(e)
finally:
    driver.quit()

    # Update the Price field of the admin user
    collection.update_one(
        {"_id": admin_id},
        {"$set": {"Price": text}},
    )





