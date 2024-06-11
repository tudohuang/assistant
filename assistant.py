import speech_recognition as sr
import pyttsx3
import subprocess
import requests
from datetime import datetime, timedelta
import threading
import os
import asyncio
import aiohttp
from urllib.parse import unquote
import webbrowser
from colorama import Fore
import time
import png_to_ascii
from utils import *
from gtts import gTTS
import pygame
import os
from langdetect import detect
import bert
import re
import math
import random
from googletrans import Translator

# 初始化語音引擎
engine = pyttsx3.init()
recognizer = sr.Recognizer()
recognizer.energy_threshod = 4000

done = 'false'
translator = Translator()
notes = []

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
            command = recognizer.recognize_google(audio, language='zh-TW')
            print(f"User said: {command}\n")
            return command.lower()
        except sr.UnknownValueError:
            say("抱歉，我沒有聽清楚。")
        except sr.RequestError:
            say("抱歉，語音服務不可用。")
        except Exception as e:
            print(f"Error in listen function: {e}")
        return ""

def open_application(app_name):
    try:
        if "瀏覽器" in app_name:
            subprocess.Popen(["start", "chrome"], shell=True)  # 使用 shell=True 來啟動應用程序
            say("打開瀏覽器")
        elif "記事本" in app_name:
            subprocess.Popen(["notepad"])  # For Windows
            say("打開記事本")
        else:
            subprocess.Popen(["start", app_name], shell=True)
            say(f"打開{app_name}")
    except Exception as e:
        say(f"無法打開{app_name}")
        print(f"Error in open_application: {e}")

def search_youtube(query):
    try:
        search_url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(search_url)
        print(f"在 YouTube 上搜尋 {query}")
    except Exception as e:
        print(f"無法搜尋 {query}")
        print(f"Error in search_youtube: {e}")

def search_web(query):
    try:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        say(f"在網頁上搜尋 {query}")
    except Exception as e:
        say(f"無法搜尋 {query}")
        print(f"Error in search_web: {e}")

async def get_weather_async(city):
    if city == "台北":
        city = "Taipei"

    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&lang=zh"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            weather_data = await response.json()
            if response.status == 200 and weather_data.get("current"):
                weather = weather_data["current"]["condition"]["text"]
                temperature = weather_data["current"]["temp_c"]
                return f"{city}的天氣是{weather}，溫度約為{temperature:.1f}度"
            else:
                return "無法獲取天氣信息"

def get_weather(city):
    try:
        loop = asyncio.get_event_loop()
        weather_info = loop.run_until_complete(get_weather_async(city))
        say(weather_info)
        print(f"AI said: {weather_info}")
    except Exception as e:
        say("無法獲取天氣信息")
        print(f"Error in get_weather: {e}")

def add_reminder(task, time):
    try:
        reminder_time = datetime.now() + timedelta(minutes=time)
        say(f"設置提醒，{time}分鐘後提醒你{task}")
        threading.Timer(time * 60, remind, args=[task]).start()
    except Exception as e:
        say("無法設置提醒")
        print(f"Error in add_reminder: {e}")

def remind(task):
    say(f"提醒你：{task}")

def search_google(query):
    try:
        url = "https://www.google.com/search?q=" + query
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for g in soup.find_all('a', href=True):
            link = g['href']
            if link.startswith("/url?q="):
                link = link.split("&")[0].replace("/url?q=", "")
                results.append(link)
        return results
    except Exception as e:
        print(f"Error!: {e}")
        return []

def google(query):
    global done
    done = 'false'
    if query == "quit":
        done = 'true'
        return query
    type_writer(Fore.GREEN + f"root@terminal:~$ Searching for: {query}\n" + Fore.RESET)
    loading_thread = threading.Thread(target=animate)
    loading_thread.start()
    done = 'true'
    loading_thread.join()
    results = search_google(query)
    if results:
        print(Fore.GREEN + "Results found:" + Fore.RESET)
        for idx, result in enumerate(results, 1):
            print(Fore.GREEN + f"{idx}: {result}" + Fore.RESET)
        selected_indices = input(Fore.GREEN + "Please enter the indices of the results you want to open (e.g. 1,3,5) or 'q' to quit: " + Fore.RESET)
        if selected_indices.lower() == 'q':
            return
        selected_indices = selected_indices.split(',')
        for idx_str in selected_indices:
            idx = int(idx_str)
            if idx > 0 and idx <= len(results):
                result = results[idx - 1]
                decoded_url = unquote(result)
                webbrowser.open(decoded_url, new=2)
                print(Fore.GREEN + f"Opening {decoded_url} ..." + Fore.RESET)
            else:
                print(Fore.GREEN + f"Index {idx} is invalid." + Fore.RESET)
    else:
        print(Fore.GREEN + "No results found" + Fore.RESET)
    return query

def type_writer(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.05)
    print()

def say(text):
    lang = detect(text)
    tts = gTTS(text=text, lang='zh-tw')
    filename = "temp.mp3"
    tts.save(filename)
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()
    try:
        os.remove(filename)
    except PermissionError:
        print("Could not delete the audio file. It might still be in use.")

def animate():
    while done == 'false':
        for c in '|/-\\':
            print(Fore.YELLOW + f'\rLoading {c}', end='', flush=True)
            time.sleep(0.1)
    print('\r', end='', flush=True)

def calculate(expression):
    try:
        result = eval(expression, {"__builtins__": {}})
        say(f"結果是{result}")
        print(f"計算結果: {result}")
    except Exception as e:
        say("無法計算")
        print(f"Error in calculate: {e}")

def tell_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    say(f"現在的時間是{current_time}")
    print(f"當前時間: {current_time}")

def tell_date():
    today = datetime.today().strftime("%Y年%m月%d日")
    say(f"今天是{today}")
    print(f"今天的日期: {today}")


def translate_text(text, dest_language):
    try:
        translated = translator.translate(text, dest=dest_language)
        say(translated.text)
        print(f"翻譯結果: {translated.text}")
    except Exception as e:
        say("無法翻譯")
        print(f"Error in translate_text: {e}")

def add_note(note):
    notes.append(note)
    say("備忘錄已記錄")
    print(f"備忘錄: {note}")

def list_notes():
    if notes:
        say("這是你的備忘錄")
        for note in notes:
            print(f"- {note}")
            say(note)
    else:
        say("你沒有備忘錄")

def process_command(command):
    best_category, best_match, similarity = bert.find_best_match(command)

    if best_category == "app":
        app_name = re.sub(r'(打開|開啟|應用程式|APP|程式|軟體|工具|服務)', '', command).strip()
        open_application(app_name)
    elif best_category == "browser":
        search_query = re.sub(r'(搜尋|開啟|啟動|瀏覽器|網頁|上網程式|網路瀏覽器|瀏覽程式)', '', command).strip()
        search_web(search_query)
    elif best_category == "google":
        query = re.sub(r'(Google搜尋|Google查找|Google搜索|Google查詢|Google找|Google)', '', command).strip()
        google(query)
    elif best_category == "video":
        query = re.sub(r'(YouTube搜尋|YouTube查找|YouTube搜索|YouTube查詢|YouTube找|YouTube影片|YouTube視頻|YouTube)', '', command).strip()
        search_youtube(query)
    elif best_category == "weather":
        city = re.sub(r'(天氣怎麼樣|天氣如何|的天氣|天氣|現在的天氣)', '', command).strip()
        get_weather(city)
    elif "提醒" in command:
        parts = command.split("提醒我")
        if len(parts) > 1:
            task_and_time = parts[1].split("分鐘")
            if len(task_and_time) == 2:
                task = task_and_time[1].strip()
                try:
                    time = int(task_and_time[0].strip())
                    add_reminder(task, time)
                except ValueError:
                    say("無法解析時間，請提供正確的分鐘數。")
            else:
                say("請提供正確的提醒格式，例如：提醒我10分鐘後喝水。")
    elif best_category == "leave":
        say("再見")
        return False
    elif best_category == "time":
        tell_time()
    elif best_category == "date":
        tell_date()
    elif best_category == "translate":
        match = re.match(r'翻譯(.+)到(.+)', command)
        if match:
            text = match.group(1).strip()
            dest_language = match.group(2).strip()
            translate_text(text, dest_language)
        else:
            say("請提供正確的翻譯格式，例如：翻譯你好到英文。")
    return True

def main():
    attempts = 1
    max_attempts = 5
    password = "AI"
    from tqdm import trange
    import sys
    import time

    for ii in trange(1, 101):
        time.sleep(0.01)
        sys.stdout.flush()

    while attempts <= max_attempts:
        try:
            password_try = get_password()
            if password_try == password:
                name = input("username:")
                start = threading.Thread(target=png_to_ascii.image_to_ascii, args=("image.png", 200))
                start.start()
                print_title(f"     Welcome-{name}    ")
                time.sleep(2)
                break
            else:
                print("Incorrect password. Try again.")
                attempts += 1
        except Exception as e:
            print(f"An error occurred: {e}")
            attempts += 1
    
    if attempts > max_attempts:
        print("Max attempts reached. Exiting...")
        return
    
    current_time = datetime.now()
    formated_time = int(current_time.strftime("%H"))
    
    if formated_time >= 18 and formated_time < 24:
        say(f"晚上好{name}，我是您的AI助手")
    elif formated_time >= 13 and formated_time < 18:
        say(f"下午好{name}，我是您的AI助手")
    elif formated_time >= 12 and formated_time < 13:
        say(f"中午好{name}，我是您的AI助手")
    elif formated_time >= 6 and formated_time < 12:
        say(f"早上好{name}，我是您的AI助手")
    else:
        say(f"您好{name}，我是您的AI助手")
    
    while True:
        command = input("請輸入指令（或輸入 '語音' 使用語音指令）: ")
        if command.lower() == '語音':
            command = listen()
        if command:
            if not process_command(command):
                break

if __name__ == "__main__":
    main()
