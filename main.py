import asyncio
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from config import API_TOKEN
from bd import add_or_update_user, initialize_database, check_spam
from record_log import log_error

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


router = Router()

initialize_database()


@router.message(Command('start'))
async def index(message: types.Message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    username = message.from_user.username
    language = message.from_user.language_code
    is_bot = message.from_user.is_bot


    check = check_spam(user_id)

    if check == True:
        add_or_update_user(user_id, user_first_name, user_last_name, username, language, is_bot)
        await message.answer(
            text=(
                f"👋 Hi! 👋\n\n"
                f"🆔 Your unique ID: `{user_id}`\n\n"
                f"🤖 This bot is simple: it only sends your ID when you start it.\n\n"
                f"🔒 Spam protection is enabled!\n"
                f"I respond once every 3 minutes to avoid abuse.\n\n"
                f"💻 The bot is open source!\n"
                f"You can view and contribute to the code on GitHub [here](https://github.com/u004226-ctrl/GetMyID-Bot)\n\n"
                f"😊 Thanks for understanding!"
            ),
            parse_mode='Markdown',  # Хотя бы MarkdownV2 может быть необходимым для большей совместимости
            disable_web_page_preview=True
        )



@dp.message(F.content_type == types.ContentType.STICKER)
async def handle_sticker(message: types.Message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    username = message.from_user.username
    language = message.from_user.language_code
    is_bot = message.from_user.is_bot
    sticker_id = message.sticker.file_id


    check = check_spam(user_id)

    if check == True:
        add_or_update_user(user_id, user_first_name, user_last_name, username, language, is_bot)
        await message.answer(
            text=(
                f"😊 *Thanks for the sticker!* 😊\n\n"
                f"🆔 *Your unique ID:* `{user_id}`\n\n"
                f"📌 *Sticker ID:* `{sticker_id}`\n\n"
                f"🤖 *I don’t know how to react to it yet, but I’ll learn soon!*"
            ),
            parse_mode="Markdown"
        )




def register_handlers(dp: Dispatcher):
    dp.include_router(router)


async def main():
    register_handlers(dp)
    while True:
        try:
            await dp.start_polling(bot)

        except (KeyboardInterrupt, SystemExit):
            break


        except Exception as e:
            log_error(f"An error occurred: {e}")
            await asyncio.sleep(5)
            continue



if __name__ == '__main__':
    asyncio.run(main())