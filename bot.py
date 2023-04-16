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
    log = open("log.txt", "a")
    log.write("[" + str(time.ctime(time.time())) + "] bot has been stopped\n")
    log.close()

    exit()


# /start
@dp.message_handler(commands=["chemequation_bot", "start"], commands_prefix=["@", "/"])
async def start_command(message: types.Message):
    await message.answer('Hello')


# /help
@dp.message_handler(commands=["help"])
async def start_command(message: types.Message):
    await message.answer("'/help' '/kick' '/stop'")


# echo
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
