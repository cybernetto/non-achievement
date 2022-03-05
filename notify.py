import  re
import requests
from time import sleep
from notifypy import Notify
import random
import string

API= 'https://api.achievementstats.com/games/239140/achievements/?key=11062228f9083303169868981'

def show_achievement(title, achievement, icon_path):
    r = requests.get(f"https://achievementstats.com/{icon_path}")
    file_name = ''.join([random.choice(string.ascii_letters) for i in range(5)])
    with open(f"/tmp/{file_name}.jpg", "wb") as f:
        f.write(r.content)
        f.truncate()
    notification = Notify()
    notification.title = title
    notification.message = achievement
    notification.icon = f'/tmp/{file_name}.jpg'
    notification.audio = "file.wav"
    notification.send(block=False)
    print(notification)

def codex_data(data):
    codex = re.findall('(\[\w{3}.\d+\]\nAchieved=\d)', data)
    b = {}
    for i in codex:
        i = i.replace("[","")
        i = i.replace("]","") 
        a = i.split('\nAchieved=')
        if a[1] == '1':
                b[a[0].lower()] = a[1]
    data_dict = b
    return data_dict
def get_data(data):
    #if from codex
    return codex_data(data)

def screen_achievement(temp):
    ach = make_request("aaaa","*")
    for i in ach:
        if i['apiName'] in list(temp.keys()):
            print(f"{i['name']}:\n\t{i['description']}")

def make_request(game_id, arch_id):
    response = requests.get(API)
    if arch_id == '*':
        return response.json()
    for i in response.json():
        if i['apiName'] == arch_id:
            return i

path = ['achievements.ini',]
f = open(path[0], 'r')
temp = get_data(f.read())
f.close()
screen_achievement(temp)
while True:
    f = open(path[0],'r')
    current = get_data(f.read())
    if temp != current:
        i = (temp.keys())
        j = (current.keys())
        try:
            temp = list(j - i)
        except:
            temp = []
        for i in temp:
            ach = make_request("aaaa",i)
            show_achievement(ach['name'],ach['description'],ach['iconUnlocked'])   
        temp = current     
    f.close()
