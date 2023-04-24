import time

import aiogram.utils.exceptions

import config
import logging

from aiogram import Bot, Dispatcher, executor, types
from filters import IsAdminFilter, IsCreatorFilter
from algorithm import get_coef

# log level
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# activate filters
dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(IsCreatorFilter)

# create buttons of menu
buttons = [types.KeyboardButton(text="/help"), types.KeyboardButton(text="/periodic_table"),
           types.KeyboardButton(text="/solubility_table"), types.KeyboardButton(text="/get_coef"),
           types.KeyboardButton(text="/commands")]

# [types.BotCommand("/help", "выводит хелпу"),
#            types.BotCommand("/periodic_table", "показывает таблицу Менделеева"),
#            types.BotCommand("/solubility_table", "показывает таблицу растворимостей"),
#            types.BotCommand("/commands", "показывает все команды")]

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(*buttons)


# /kick
@dp.message_handler(is_admin=True, commands=["kick"])
async def kick_command(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение")
        return
    try:
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)

        log = open("log.txt", "a")
        log.write("[" + str(time.ctime(time.time())) + f"] {member['user']['name']} {member['user']['lastname']}"
                                                       f" has been kicked from {message.bot.get_chat(message.chat.id)}\n")
        log.close()
        await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)
        await message.reply("Пользователь был кикнут")
    except aiogram.utils.exceptions.BadRequest:
        await message.reply("Я не могу кикнуть человека из приватного чата")


# /stop <- This command stops work of the bot (can only be used by the creator)
@dp.message_handler(is_creator=True, commands=["stop"])
async def stop_command(message: types.Message):
    await message.reply("Бот был остановлен")
    with open("log.txt", "a") as log:
        log.write("[" + str(time.ctime(time.time())) + "] bot has been stopped\n")
    exit()


@dp.message_handler(commands=["commands"], commands_prefix=["/"])
async def send_welcome(message: types.Message):
    await message.reply("Лови", reply_markup=keyboard)


# /start
@dp.message_handler(commands=["chemequation_bot", "start"], commands_prefix=["@", "/"])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, который поможет тебе решать химические уравнения", reply_markup=keyboard)


# /help
@dp.message_handler(commands=["help"])
async def start_command(message: types.Message):
    await message.reply("'/help' '/kick' '/stop'\n\n"
                        "1) Вводите все элементы так, как они написаны в таблице Менделеева\n"
                        "2) Используйте латинские буквы\n"
                        "3) НЕ используйте пробелы\n"
                        "4) Все элементы вводите ровно так, как они записаны в таблице Менделеева, "
                        "без изменений кегля букв\n"
                        "Примеры ввода:\n"
                        "/get_coef Ca(OH)2+H3PO4=Ca3(PO4)2+H2O", reply_markup=keyboard)


@dp.message_handler(commands=["get_coef"])
async def get_coefficient(message: types.Message):
    try:
        args = message.text.split()[1].split('=')

        await message.reply("Чекай, я расставил коэффициенты:\n{}".format(get_coef(args[0], args[1])))
    except IndexError:
        await message.reply("А где уравнения собственно говоря?")


# echo
# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(message.text)


# /solubility_table
@dp.message_handler(commands="solubility_table")
async def solubility_table(message: types.Message):
    with open('data/tables/solubility_table.png', mode='rb') as solubility_table:
        await message.reply_photo(solubility_table)


# /periodic_table
@dp.message_handler(commands="periodic_table")
async def periodic_table(message: types.Message):
    with open('data/tables/periodic_table.png', mode='rb') as periodic_table:
        await message.reply_photo(periodic_table)


# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
