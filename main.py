import asyncio
import logging
from dotenv import load_dotenv

from app.handlers import bot, dp,user_router


async def main():
    load_dotenv()
    dp.include_router(user_router)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot turned off")