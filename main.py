import asyncio
import os
import random
import string
import db
import logging

from aiohttp import web

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, BotCommand, BotCommandScopeDefault, MenuButtonCommands, CallbackQuery

TOKEN = os.getenv("TOKEN")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8888"))
confirm_code = ""

logger = logging.getLogger(__name__)


async def handle(request):
    global bot
    body = await request.json()
    body = body["embeds"][0]
    msg = f"Новый пост на форуме\n\nТема: {body['title']}\n\nСодержание: {body['description']}\n\n{html.link('Ссылка', body['url'])}\n\nВремя: {body['timestamp']}\n\nАвтор: {body['author']['name']}"
    try:
        chats = await db.get_chat_id()
        for chat in chats:
            await bot.send_message(chat_id=int(chat), text=msg)
    except Exception as e:
        logger.error(e)
    return web.Response(text="OK")


app = web.Application()
app.add_routes([web.route('*', '/', handle)])

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(Command("start"))
async def command_start_handler(message: Message):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Показать справку")
    ]
    try:
        await message.answer(
            f"Привет {html.bold(message.from_user.full_name)}! 👋\n\nотправляй сюда свои постройки/сообщения/новости. если они окажутся интересными, мы опубликуем их в нашем канале\n\n❗️ этот бот - исключительно для предложки в телеграм-канал. здесь не рассматриваются предложения по модам/крафтам и любым другим изменениям на сервере")
        await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
        await bot.set_chat_menu_button(menu_button=MenuButtonCommands())
    except Exception as e:
        logger.error(e)


@dp.message(Command("help"))
async def command_help_handler(message: Message):
    admins = await db.get_admin_id()
    builder = InlineKeyboardBuilder()
    if not admins:
        builder.button(text="Я администратор", callback_data="I-am-admin")
    if str(message.from_user.id) in admins:
        try:
            await message.answer(
                f"Команды администратора\n\n/list - вывод всех чатов с активными уведомлениями\n\n/sub - Подписать чат на уведомления\n\n/unsub - отписать чат от уведомлений")
        except Exception as e:
            logger.error(e)
    else:
        try:
            await message.answer("Просто отправьте всё что хотите", reply_markup=builder.as_markup())
        except Exception as e:
            logger.error(e)


@dp.message(Command("confirm"))
async def command_confirm_handler(message: Message):
    global confirm_code
    if confirm_code:
        if message.text.split(' ')[1] == "код":
            try:
                await message.answer("Услышал тебя родной!")
            except Exception as e:
                logger.error(e)
        elif message.text.split(' ')[1] == confirm_code:
            try:
                await db.add_admin_id(message.from_user.id)
                await message.answer("Успех! Вы администратор")
            except Exception as e:
                logger.error(e)
        else:
            try:
                await message.answer("Ошибка! Код не верный")
            except Exception as e:
                logger.error(e)
        confirm_code = None
    else:
        try:
            await message.answer("Код не сгенерирован")
        except Exception as e:
            logger.error(e)


@dp.callback_query(F.data == "I-am-admin")
async def make_admin(callback: CallbackQuery):
    global confirm_code
    try:
        await callback.answer()
        await callback.message.delete()
        confirm_code = ''.join(random.choices(string.digits, k=16))
        logger.info(f"Confirm code: {confirm_code}")
        await callback.message.answer(f"Для подтверждения введите код из консоли бота\n{html.code('/confirm код')}")
    except Exception as e:
        logger.error(e)


@dp.message(Command("sub"))
async def command_sub(message: Message):
    admins = await db.get_admin_id()
    if str(message.from_user.id) in admins:
        try:
            await db.add_chat_id(message.chat.id, message.chat.full_name)
            await message.answer(f"Чат {message.chat.full_name} подписан на уведомления")
        except Exception as e:
            logger.error(e)


@dp.message(Command("unsub"))
async def command_sub(message: Message):
    admins = await db.get_admin_id()
    if str(message.from_user.id) in admins:
        try:
            await db.remove_chat_id(message.chat.id)
            await message.answer(f"Чат {message.chat.full_name} отписан от уведомлений")
        except Exception as e:
            logger.error(e)


@dp.message(Command("list"))
async def command_sub(message: Message):
    admins = await db.get_admin_id()
    if str(message.from_user.id) in admins:
        try:
            msg = ""
            for item in await db.get_chat_name():
                msg = msg + f"{item}, "
            await message.answer(f"Чаты подписанные на уведомления: {msg}")
        except Exception as e:
            logger.error(e)


@dp.message()
async def offer(message: Message):
    global bot
    chats = await db.get_chat_id()
    for chat in chats:
        await bot.send_message(chat_id=int(chat), text=f"Новое предложение от пользователя {message.from_user.full_name} (@{message.from_user.username})")
        await message.send_copy(chat_id=int(chat))
    await message.answer("Ваше предложение передано администрации")


async def main():
    global bot
    admins = await db.get_admin_id()
    if admins:
        for admin in admins:
            await bot.send_message(chat_id=int(admin), text=f"Bot loaded")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=HOST, port=PORT)
    await site.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
