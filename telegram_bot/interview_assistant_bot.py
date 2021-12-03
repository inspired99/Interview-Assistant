import telebot
import config
import random
import os
from telebot import types
import psycopg2
from config import USER_NAME, DATABASE_NAME, PASSWORD, HOST_NAME, PORT

# To load sql_server module
import sys
sys.path.insert(1, '../sql_server')
from sql_server import *

bot = telebot.TeleBot(config.API_KEY)
# Connection to the database
conn = psycopg2.connect(
    host=HOST_NAME,
    database=DATABASE_NAME,
    user=USER_NAME,
    password=PASSWORD,
    port=PORT)

all_companies = ['Google', 'Microsoft', 'Amazon', 'Facebook', 'Uber', 'Airbnb']
status = ["next task", "skip", "postpone"]
additional_info = ["examples", "constraints", "hints"]
all_stages = ['Phone screen', 'Online assessment', 'Onsite']


# Extract all files with data in directory
def extract_file_names(path):
    file_list = [file for file in os.listdir(path) if
                 os.path.isfile(os.path.join(path, file))]
    return file_list


def create_keyboard_companies(companies):
    # Keyboard for companies
    keyboard = [[], [], [types.InlineKeyboardButton("Continue to the stage selection...", callback_data='stage')]]
    for index in range(6):
        company = all_companies[index]
        if company in companies:
            button = types.InlineKeyboardButton(f"✅ {company}", callback_data=company)
        else:
            button = types.InlineKeyboardButton(f"  {company}", callback_data=company)

        if index < 3:
            keyboard[0].append(button)
        else:
            keyboard[1].append(button)

    return keyboard


def create_keyboard_stages(stages):
    # Keyboard for companies
    keyboard = [[], [types.InlineKeyboardButton("Let's get started!", callback_data='next task')]]
    for stage in all_stages:
        if stage in stages:
            button = types.InlineKeyboardButton(f"✅ {stage}", callback_data=stage)
        else:
            button = types.InlineKeyboardButton(f"  {stage}", callback_data=stage)

        keyboard[0].append(button)

    return keyboard


@bot.message_handler(commands=['start'])
def welcome(message):
    # Send greeting sticker
    sticker = open('resources/pictures/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
 
    # Create keyboard and buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Finish")
    item2 = types.KeyboardButton("Process")
    item3 = types.KeyboardButton("New companies")

    # Add buttons into keyboard
    markup.add(item1, item2, item3)

    # Greeting message
    start_message = ("Hi, "
                     f"{message.from_user.first_name}!\n"
                     "I'm <b>"
                     f"{bot.get_me().first_name}"
                     "</b>, a bot created to help you get an internship in your dream company.\n"
                     "Good luck! 😊")

    # Send greeting message
    bot.send_message(message.chat.id, text=start_message, parse_mode='html', reply_markup=markup)

    # We check if user is registered
    user = read_table(conn, "Users", user_id=message.from_user.id)
    if not user:
        register_user(conn, user_id=message.from_user.id)
    user_companies = read_table(conn, "UsersCompanies", user_id=message.from_user.id)
    # Create initial keyboard
    companies = []
    for data in user_companies:
        companies.append(data[1])
    keyboard = create_keyboard_companies(companies)

    inline_markup = types.InlineKeyboardMarkup(keyboard)
    bot.send_message(message.chat.id, text="Please, choose the companies you're interested in:",
                     reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        if call.message:
            if call.data in status:
                # Move previous task
                prev_task_id = read_table(conn, "Current", user_id=call.from_user.id)
                if (call.data == "next task" or call.data == "skip") and prev_task_id:
                    insert_task(conn, table_name="Solved", user_id=call.from_user.id, task_id=prev_task_id[0][0])

                # Take next task
                task = read_table(conn, "Tasks", flag_take_task=1, user_id=call.from_user.id)
                if not task:
                    task_message = ("I am out of tasks for you...\n"
                                    "Please, change the companies, so I can find more problems for you.")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text=task_message)
                else:
                    if call.data == "next task":
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="Remember, you're amazing! Your next task:", reply_markup=None)
                    elif call.data == "skip":
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="That's okay. Let's try another one!", reply_markup=None)
                    else:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="I put this task in queue. Now let's try another one!",
                                              reply_markup=None)

                    # Delete previous task from Current
                    if prev_task_id:
                        remove_task(conn, table_name="Current", user_id=call.from_user.id, task_id=prev_task_id[0][0])

                    # Show new task
                    task_id = task[0][0]
                    insert_task(conn, table_name="Current", user_id=call.from_user.id, task_id=task_id)
                    task_title = task[0][1]
                    task_description = task[0][2]
                    task_message = f"<b>{task_title}</b>" + "\n" * 2 + task_description + "\n" * 2 + \
                                   f"<a href=\"{task[0][10]}\">Link to the LeetCode with this problem</a>"
                    bot.send_message(call.message.chat.id, text=task_message,
                                     parse_mode='html', disable_web_page_preview=True)

            elif call.data in additional_info:
                task_id = read_table(conn, "Current", user_id=call.from_user.id)[0][0]
                task = read_table(conn, "Tasks", task_id=task_id)[0]

                if call.data == "examples":
                    task_message = task[3]
                elif call.data == "constraints":
                    task_message = task[5]
                else:
                    task_message = task[7] + "\n\n" + task[4]  # hints

                if task_message is not None:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text=task_message, parse_mode='html')
                else:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Unfortunately, there is no information about this. Try other options!")

            elif call.data == "memes":
                gifs_names = extract_file_names('resources/gifs')
                gif_name = random.choice(gifs_names)
                gif = open(f'resources/gifs/{gif_name}', 'rb')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Here is your gif 🙃")
                bot.send_animation(call.message.chat.id, gif)

            elif call.data == "help":
                task_id = read_table(conn, "Current", user_id=call.from_user.id)[0][0]
                task_link = read_table(conn, "Tasks", task_id=task_id)[0][10]
                text_for_link = "Link to the LeetCode with the discussions for this problem"
                text_message_beginning = f"<b>You can try to find tips and solutions here:</b>" + "\n" * 2

                if task_link[-1] == "/":
                    text_message = text_message_beginning + f"<a href=\"{task_link}discuss/\">{text_for_link}</a>"
                else:
                    text_message = text_message_beginning + f"<a href=\"{task_link}/discuss/\">{text_for_link}</a>"

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=text_message, parse_mode='html', disable_web_page_preview=True)

            elif call.data in all_stages or call.data == "stage":
                stage = call.data
                user_stages = read_table(conn, "UsersStages", user_id=call.from_user.id)
                stages = []
                for data in user_stages:
                    stages.append(data[1])

                if stage in stages:
                    delete_element(conn, "UsersStages", call.from_user.id, "stage", stage)
                    stages.remove(stage)
                elif call.data != "stage":
                    insert_element(conn, "UsersStages", call.from_user.id, "stage", stage)
                    stages.append(stage)

                keyboard = create_keyboard_stages(stages)
                inline_markup = types.InlineKeyboardMarkup(keyboard)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Please, choose stage of the interview you are interested in:",
                                      reply_markup=inline_markup)
            else:
                company = call.data
                user = read_table(conn, "UsersCompanies", user_id=call.from_user.id)
                companies = []
                for data in user:
                    companies.append(data[1])

                if company in companies:
                    delete_element(conn, "UsersCompanies", call.from_user.id, "company", company)
                    companies.remove(company)
                else:
                    insert_element(conn, "UsersCompanies", call.from_user.id, "company", company)
                    companies.append(company)

                keyboard = create_keyboard_companies(companies)
                inline_markup = types.InlineKeyboardMarkup(keyboard)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Please, choose the companies you're interested in:",
                                      reply_markup=inline_markup)

    except Exception as e:
        print(repr(e))


# Processing of the text
@bot.message_handler(content_types=['text'])
def message_handler(message):
    if message.text == "Finish":
        keyboard = [[types.InlineKeyboardButton("Done", callback_data='next task'),
                     types.InlineKeyboardButton('Skip', callback_data='skip')],
                    [types.InlineKeyboardButton('Postpone', callback_data='postpone'),
                     types.InlineKeyboardButton('Memes', callback_data='memes')]]
        inline_markup = types.InlineKeyboardMarkup(keyboard)
        bot.send_message(message.chat.id, text="What is your status?", reply_markup=inline_markup)
    elif message.text == "Process":
        keyboard = [[types.InlineKeyboardButton("Examples", callback_data='examples'),
                     types.InlineKeyboardButton('Constraints', callback_data='constraints'),
                     types.InlineKeyboardButton('Hints', callback_data='hints')],
                    [types.InlineKeyboardButton('Ask for help', callback_data='help')]]
        inline_markup = types.InlineKeyboardMarkup(keyboard)
        bot.send_message(message.chat.id, text="What do you want me to show?", reply_markup=inline_markup)
    elif message.text == "New companies":
        # Check current task
        task_id = read_table(conn, "Current", user_id=message.from_user.id)
        if task_id:
            remove_task(conn, table_name="Current", user_id=message.from_user.id, task_id=task_id[0][0])

        user = read_table(conn, "UsersCompanies", user_id=message.from_user.id)
        companies = []
        for data in user:
            companies.append(data[1])
        keyboard = create_keyboard_companies(companies)
        inline_markup = types.InlineKeyboardMarkup(keyboard)
        bot.send_message(message.chat.id, text="Please, choose the companies you're interested in:",
                         reply_markup=inline_markup)
    elif message.text == "Cat":
        bot.send_message(message.chat.id, text="I love cats!",
                         reply_markup=None)
        sticker = open('resources/pictures/cat.webp', 'rb')
        bot.send_sticker(message.chat.id, sticker)
    else:
        text = "Я бот глупенький, давай общаться кнопками? 😊"
        bot.send_message(message.chat.id, text=text, parse_mode='html')


# RUN
bot.polling(none_stop=True)

conn.close()
