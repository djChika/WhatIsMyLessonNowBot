import authentication
import keyboards
import main
import settings
import system
import users

# STARTUP PARAMETERS
from main import bot

system_message = "[{0}] Bot Launched".format(settings.get_current_date_and_time())
system.alert(system_message)
main.send_to_admin(system_message)

week_file = settings.week_file_path
week = system.read_file(week_file)
settings.set_week(week)


# STARTUP PARAMETERS


@bot.message_handler(content_types=["text"])
def handle_text(message):
    system.log(message)
    user_id = message.from_user.id
    day = settings.get_current_day()
    week = settings.get_week()

    if not users.exist(user_id):
        authentication.login(user_id,
                             message)

    else:
        main.handle_text_main(user_id,
                              message,
                              day,
                              week)

    if user_id == settings.admin_id:
        main.handle_text_admin(user_id,
                               message,
                               day)


@bot.message_handler(commands=["start"])
def handle_text(message):
    user_id = message.from_user.id
    day = settings.get_current_day()
    main.send_keyboard(user_id,
                       keyboards.DaysKeyboard.get_answer(day),
                       keyboards.DaysKeyboard.markup)


@bot.message_handler(commands=["settings"])
def handle_text(message):
    user_id = message.from_user.id
    main.send_keyboard(user_id,
                       keyboards.SettingsKeyboard.answer,
                       keyboards.SettingsKeyboard.get_markup(user_id))


@bot.message_handler(commands=['about'])
def handle_text(message):
    user_id = message.from_user.id
    day = settings.get_current_day()
    answer = "Schedule Bot by Chika.\nNow only for 647M RSREU group\nhttps://vk.com/chikalkin"
    bot.send_message(user_id,
                     answer)
    main.send_keyboard(user_id,
                       keyboards.DaysKeyboard.get_answer(day),
                       keyboards.DaysKeyboard.markup)


bot.polling(none_stop=True)
