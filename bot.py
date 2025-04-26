import telebot
import os
import json

TOKEN = '7657731654:AAG2uzH4PFB968zABFKhvzyF0ODPZ68qMNg'
ADMIN_ID = 7981551122

bot = telebot.TeleBot(TOKEN)
IMAGES_FOLDER = 'images'
COMMANDS_FILE = 'commands.json'
user_states = {}

if os.path.exists(COMMANDS_FILE):
    with open(COMMANDS_FILE, 'r', encoding='utf-8') as f:
        commands = json.load(f)
else:
    commands = {}

os.makedirs(IMAGES_FOLDER, exist_ok=True)

def save_commands():
    with open(COMMANDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(commands, f, ensure_ascii=False, indent=4)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا بك! استخدم زر \"إضافة أمر\" لإضافة صورة جديدة.")

@bot.message_handler(commands=['menu'])
def show_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('➕ إضافة أمر')
    bot.send_message(message.chat.id, "اختر أمرًا:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text.strip()

    if text == '➕ إضافة أمر' and user_id == ADMIN_ID:
        bot.send_message(message.chat.id, "أرسل اسم الأمر الجديد.")
        user_states[user_id] = 'awaiting_command_name'

    elif user_id in user_states:
        state = user_states[user_id]

        if state == 'awaiting_command_name':
            command_name = text
            user_states[user_id] = {'awaiting_photo_for': command_name}
            bot.send_message(message.chat.id, f"تم تسجيل اسم الأمر: {command_name}. الآن أرسل الصورة الخاصة به.")

    elif text in commands:
        image_path = os.path.join(IMAGES_FOLDER, commands[text])
        if os.path.exists(image_path):
            with open(image_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        else:
            bot.send_message(message.chat.id, "عذرًا، لم يتم العثور على الصورة!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id

    if user_id in user_states and isinstance(user_states[user_id], dict):
        state_info = user_states[user_id]
        command_name = state_info.get('awaiting_photo_for')

        if command_name:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            image_filename = f"{command_name}.jpg"
            image_path = os.path.join(IMAGES_FOLDER, image_filename)

            with open(image_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            commands[command_name] = image_filename
            save_commands()

            bot.send_message(message.chat.id, f"تم حفظ الأمر '{command_name}' بنجاح!")
            user_states.pop(user_id)

print("Bot is running...")
bot.infinity_polling()