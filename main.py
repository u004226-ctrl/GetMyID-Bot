import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from config import API_TOKEN
from bd import add_user
from record_log import log_error

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

router = Router()

@router.message(Command('start'))
async def welcome(message: types.Message):
    print('hi')
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    username = message.from_user.username
    language = message.from_user.language_code
    is_bot = message.from_user.is_bot

    add_user(user_id, user_first_name, user_last_name, username, language, is_bot)

    await message.answer(text=f'Hi!\nYour ID: `{user_id}`', parse_mode='Markdown')



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
            continue # restart



if __name__ == '__main__':
    asyncio.run(main())