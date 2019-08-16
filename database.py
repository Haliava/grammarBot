import pyautogui
import webbrowser
import bs4
import requests
import selenium

# TODO pyautogui.typewrite(word, interval=.1)
# TODO pyautogui.hotkey('ctrl', 'shift', 'w')
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
chosen_words = ['iphone']
url = f'https://www.google.com.ua/search?q={chosen_words[0]}'
res = requests.get(url)
soup = bs4.BeautifulSoup(res.text, 'html.parser')
ads = soup.find_all(class_='ads-ad')
print(ads)
#webbrowser.get(chrome_path).open(url)
#screenWidth, screenHeight = pyautogui.size()
#pyautogui.hotkey('alt', 'left')
