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
        # Замість implicitly_wait можемо використати WebDriverWait для більшої точності
        paragraph = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.chakra-text.css-1gdcvrl"))
        )
        full_text = paragraph.text.strip()
        parts = full_text.split('.')

        # Забезпечуємо, що залишаємо лише чотири цифри після крапки, як в вашому оргінальному коді
        if len(parts) > 1:
            text = f'{parts[0]}.{parts[1][:4]}'
        else:
            text = parts[0]
    finally:
        driver.quit()

    # Update the Price field of the admin user
    collection.update_one(
        {"_id": admin_id},
        {"$set": {"Price": text}},
    )





