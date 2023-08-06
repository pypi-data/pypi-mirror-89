# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 19:44:55 2018

@author: xiaozhe
"""
import wxpy
import pickle
import os
import logging
import time
import urllib
import json
import random
from IPython import embed
logging.basicConfig(level=logging.DEBUG, format='%(msg)s')
logging.disable(level=logging.DEBUG)
logging.info('logging in...')

if os.path.exists('wechatrobotmsgrecord.pkl'):
    with open('wechatrobotmsgrecord.pkl', 'rb') as file:
        chatRecord = pickle.load(file)
else:
    chatRecord = {'ask': [], 'answer': []}

bot = wxpy.Bot(cache_path=True)
bot.enable_puid('wxpy_puid.pkl')

auto_reply_persons_1 = ['Unney', '另一个我']
auto_friends_1 = []
for person in auto_reply_persons_1:
    auto_friends_1.append(wxpy.ensure_one(bot.chats().search(person)))

manager = wxpy.ensure_one(bot.chats().search('小镇'))
sansan = wxpy.ensure_one(bot.chats().search('Unney'))

# tuling = wxpy.Tuling(api_key='xxxxxxxxxxxxxxxxxx')

APIKEY = "633378fe9e364abfc98c910064c61d46"

# 对特定用户开启智能回复
# auto_friends = auto_friends_1
# 对所有用户开启智能回复
auto_friends = bot.chats()


@bot.register(auto_friends)
def auto_reply_1(msg):
    # global auto_friends
    if msg.type in [wxpy.TEXT]:
        if msg.sender == manager and msg.text == 'LOGOUT':
            bot.logout()
            return
        else:
            # 从下面的列表中随机选择一个回答
            # reply = random.choice(["我是傻逼", "我不配", "好"])
            # 尝试访问智能机器人API
            question = msg.text
            try:
                url = f'http://api.tianapi.com/txapi/robot/index?key={APIKEY}&question={question}'
                res = urllib.request.urlopen(urllib.request.quote(
                    url, safe=";/?:@&=+$,", encoding="utf-8"))
                res = res.read().decode('utf-8')
                reply = json.loads(res)['newslist'][0]['reply']
            except Exception as e:
                logging.error(f"exception: {e}")
                reply = "有点忙，等一会儿再回复"
            logging.info(f"received: {msg}, reply: {reply}")
            time.sleep(0.5)
            return reply
    elif msg.type == wxpy.RECORDING:
        reply = "有点忙，等一会儿再回复"
        return reply
    else:
        reply = "有点忙，等一会儿再回复"
        return reply


logging.warning('listening...')
while bot.alive:
    time.sleep(0.5)