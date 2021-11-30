import telebot
import config
from telebot import types
import json
import random

bot = telebot.TeleBot(config.API_KEY)

file_names = []

for i in range(1, 12):
    name = "sample_task" + f"{i}" + ".json"
    file_names.append(name)

companies = []
all_companies = [("Google", "00"), ("Microsoft", "01"), ("Amazon", "02"), ("Facebook", '03'), ("Uber", '10'),
                 ("Adobe", '11'), ("Apple", '12'), ("Twitter", '13')]

callback_data_list = ["00", "01", "02", "03", "10", "11", "12", "13"]
status = ["next task", "skip", "postpone"]
additional_info = ["examples", "constraints", "hints"]


# all_companies = [["Google", "Microsoft", "Amazon", "Facebook", "Uber", "Adobe", "Apple", "Twitter"],
#                  ["00", "01", "02", "03", "10", "11", "12", "13"]]


def create_keyboard():
    # Keyboard for companies
    keyboard = [[], [], [types.InlineKeyboardButton("Let's get started!", callback_data='next task')]]
    for index, data in enumerate(all_companies):
        company, callback_data = data
        if company in companies:
            button = types.InlineKeyboardButton(f"{company} ✅", callback_data=callback_data)

        else:
            button = types.InlineKeyboardButton(f"{company}", callback_data=callback_data)

        if index < 4:
            keyboard[0].append(button)
        else:
            keyboard[1].append(button)

    return keyboard


@bot.message_handler(commands=['start'])
def welcome(message):
    # Send greeting sticker
    sti = open('pictures/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
 
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
                     "I'm - <b>"
                     f"{bot.get_me().first_name}"
                     "</b>, a bot created to help you get an internship in your dream company.\n"
                     "Good luck! 😊")

    # Send greeting message
    bot.send_message(message.chat.id, text=start_message, parse_mode='html', reply_markup=markup)

    keyboard = create_keyboard()
    inline_markup = types.InlineKeyboardMarkup(keyboard)
    bot.send_message(message.chat.id, text="Please, choose the companies you're interested in:", reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data in status:
                if call.data == "next task":
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="You're amazing! Keep working!", reply_markup=None)
                elif call.data == "skip":
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="That's okay. Let's try another one!", reply_markup=None)
                elif call.data == "postpone":
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="I put this task in queue. Now let's try another one!",
                                          reply_markup=None)

                file_name = random.choice(file_names)
                with open("./files/" + file_name, 'r') as json_f:
                    data = json.load(json_f)
                    x = data['title']
                    result = f"{x}" + '\n\n' + data['description']
                    bot.send_message(call.message.chat.id, text=result)

            elif call.data in additional_info:
                if call.data == "examples":
                    pass
                elif call.data == "constraints":
                    pass
                elif call.data == "hints":
                    pass
            else:
                last_callback_index = callback_data_list.index(call.data)
                company = all_companies[last_callback_index][0]

                if company in companies:
                    companies.remove(company)
                else:
                    companies.append(company)

                keyboard = create_keyboard()
                inline_markup = types.InlineKeyboardMarkup(keyboard)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Please, choose the companies you're interested in:",
                                      reply_markup=inline_markup)

    except Exception as e:
        print(repr(e))


# Processing of the text
@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.text == "Finish":
        keyboard = [[types.InlineKeyboardButton("Done!", callback_data='next task'),
                     types.InlineKeyboardButton('Nah (skip)', callback_data='skip')],
                    [types.InlineKeyboardButton('Postpone', callback_data='postpone')]]
        inline_markup = types.InlineKeyboardMarkup(keyboard)
        bot.send_message(message.chat.id, text="What is your status?", reply_markup=inline_markup)
    elif message.text == "Process":
        keyboard = [[types.InlineKeyboardButton("Examples", callback_data='examples'),
                     types.InlineKeyboardButton('Constraints', callback_data='constraints'),
                     types.InlineKeyboardButton('Hints', callback_data='hints')]]
        inline_markup = types.InlineKeyboardMarkup(keyboard)
        bot.send_message(message.chat.id, text="What do you want me to show?", reply_markup=inline_markup)
    elif message.text == "New companies":
        keyboard = create_keyboard()
        inline_markup = types.InlineKeyboardMarkup(keyboard)
        bot.send_message(message.chat.id, text="Please, choose the companies you're interested in:",
                         reply_markup=inline_markup)
    # elif message.text == "@InterviewAssistant_bot Эй, бот, а ты че бездельничаешь? Иди работай!":
    #     bot.send_message(message.chat.id, text="Э, слыш!",
    #                      reply_markup=None)
    else:
        text = "Я бот глупенький, давай общаться кнопками? 😊"
        bot.send_message(message.chat.id, text=text, parse_mode='html')


# RUN
bot.polling(none_stop=True)
