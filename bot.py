import time

import aiogram.utils.exceptions

import config
import logging

from aiogram import Bot, Dispatcher, executor, types

from filters import IsAdminFilter, IsCreatorFilter

# log level
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# activate filters
dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(IsCreatorFilter)


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


# /start
@dp.message_handler(commands=["chemequation_bot", "start"], commands_prefix=["@", "/"])
async def send_welcome(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Помощь"),
            types.KeyboardButton(text="Переодическая таблица"),
            types.KeyboardButton(text="Таблица растворимости"),
            types.KeyboardButton(text="Остановить")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)

    await message.reply("Привет!", reply_markup=keyboard)


# /help
@dp.message_handler(commands=["help"])
async def start_command(message: types.Message):
    await message.reply("'/help' '/kick' '/stop'")


# echo
# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(message.text)


# /solubility_table
@dp.message_handler(commands="solubility_table")
async def solubility_table(message: types.Message):
    with open('data/tables/solubility_table.png', mode='rb') as ssolubility_table:
        await message.reply_photo(ssolubility_table)
  

# /periodic_table
@dp.message_handler(commands="periodic_table")
async def periodic_table(message: types.Message):
    with open('data/tables/periodic_table.png', mode='rb') as pperiodic_table:
        await message.reply_photo(pperiodic_table)


# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
