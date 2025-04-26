import telebot
TOKEN = '7657731654:AAG2uzH4PFB968zABFKhvzyF0ODPZ68qMNg'
LUFFY_PHOTO = 'https://i.postimg.cc/zv4r5gX0/luffy-girl.jpg'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: message.text.lower() == "لوفي")
def send_luffy(message):
    bot.send_photo(message.chat.id, LUFFY_PHOTO)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! اكتب لوفي لعرض الصورة.")

print("Bot is running...")
bot.infinity_polling()
