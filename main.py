import telebot
import pyshorteners
import sqlite3
from telebot.types import *

bot = telebot.TeleBot("5633334039:AAGdBKlPX1huycKAHOxBevY8rgfosmu-I_Q")

BITLY_TOKEN = "4250ad46e3b175b9e3b506893eea7ba7ef1fd673"

admin = [1365625365]

az = InlineKeyboardMarkup()
a01 = InlineKeyboardButton(text ="🔔Channel", url="t.me/Oro_Tech_Tips")
az.add(a01)



share = InlineKeyboardMarkup()
sh = InlineKeyboardButton(text ="📎Share",url="https://t.me/share/url?url=t.me/UrlShortnerfastBot")
share.add(sh)


back = InlineKeyboardMarkup()
backbtn = InlineKeyboardButton(text ="🔙back", callback_data ="back")
back.add(backbtn)

a = InlineKeyboardMarkup()
aa = InlineKeyboardButton(text ="📢Broadcast📢", callback_data = "b")
aaa = InlineKeyboardButton(text ="🚀Statistics🚀", callback_data ="s")
a.add(aa)
a.add(aaa)

@bot.message_handler(commands = ["start"])
def send_messag(message):
	users_id = message.chat.id
	with sqlite3.connect("sql6511731.db") as connection:
		cursor = connection.cursor()
		cursor.execute("select * from bitly;")
		for y in cursor.fetchall():
			if users_id ==y[0]:
				bot.send_message(message.chat.id, f"👋🏻{message.chat.first_name} Baga Nagaan gara bot kanaa dhuftan. bot kun liinkii isin itti ergitan gabaabsee bifa biraatiin isiniif erga!😊\n\n📎Link natti ergaa...", reply_markup = az)
				#time.sleep(5)
				bot.delete_message(message.chat.id, message.message_id)
			if message.chat.id in admin:
				bot.send_message(message.chat.id, " 🙂Hi admin! welcome to your bot", reply_markup =a)
				break
			else:
				pass
		else:
			cursor.execute(f"insert into bitly values({message.chat.id});")
			bot.send_message(message.chat.id,f"👋🏻{message.chat.first_name} Baga Nagaan gara bot kanaa dhuftan. bot kun liinkii isin itti ergitan gabaabsee bifa biraatiin isiniif erga!😊\n\n📎Link natti ergaa...", reply_markup = az)

@bot.message_handler(func = lambda msg: True)
def make_short(msg):
    z = bot.get_chat_member("@Oro_tech_tips", msg.chat.id)
    if z.status=="left":
    	bot.send_message(msg.chat.id, "⚠️Bot Kana fayyadamuuf Channel keenya Join jechuu qabdu! 🔔 @Oro_Tech_Tips")
    	return
    else:
    	pass
    link = msg.text
    shortener = pyshorteners.Shortener(api_key = BITLY_TOKEN)
    try:
    	link_shortener = shortener.bitly.short(link)
    except:
    	link_shortener = 'An error occured:\n📎Liinkiin isin ergitan hin hojjatu! Maaloo liinkii sirrii ergaa!😊'
    bot.reply_to(msg, link_shortener)
    bot.send_message(msg.chat.id, "🤖Bot kana hiriyoota keetiif share gochuun nu deeggari!😊", reply_markup = share)


@bot.callback_query_handler(func=lambda callback: True)
def hi(callback):
	if callback.data =="b":
		bot.send_message(callback.message.chat.id, "Send me the message to deliver", reply_markup = back)
		bot.delete_message(callback.message.chat.id, callback.message.message_id)
		bot.register_next_step_handler(callback.message, send_to_all)
	if callback.data=="back":
		bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id,text= f"This message is not showing for users🙂. only for you😎", parse_mode ="html", reply_markup = a)
	if callback.data=="s":
			count = 0
			with sqlite3.connect("sql6511731.db") as connection:
			 	   cursor = connection.cursor()
			 	   cursor.execute("SELECT * FROM bitly;")
			 	   for item in cursor.fetchall():
			 	   	count = count + 1
			 	   else:
			 	       bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id,text= f"👨‍💼Total subscribers: {count}", parse_mode ="html", reply_markup = back)
			 	       count = 0

def send_to_all(message):
    with sqlite3.connect("sql6511731.db") as connection:
        count = 0
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM bitly;")
        for item in cursor.fetchall():
            users_id = item
            try:
                   if message.content_type == "text":
                   	bot.send_message(item[0], f"""{message.text}""")
            except:
            	pass

bot.infinity_polling()
