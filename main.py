import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart

# 🔑 ВСТАВЬ СЮДА СВОИ КЛЮЧИ
TELEGRAM_TOKEN = ""
OPENROUTER_API_KEY = ""

# 🔄 Список моделей (если одна не работает — переключаемся)
MODELS = [
    "mistralai/mistral-7b-instruct",
    "openchat/openchat-7b",
]

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

async def ask_ai(prompt: str):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-site.com",
        "X-Title": "Telegram AI Bot"
    }

    for model in MODELS:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": model,
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                    },
                ) as response:

                    if response.status == 200:
                        data = await response.json()
                        return data["choices"][0]["message"]["content"]
                    else:
                        print(f"Модель {model} не работает, пробуем следующую...")

        except Exception as e:
            print(f"Ошибка модели {model}: {e}")

    return "❌ Все модели сейчас недоступны. Попробуй позже."

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я AI бот 🤖 Напиши мне что-нибудь.")

@dp.message()
async def chat(message: Message):
    await message.answer("⏳ Думаю...")
    answer = await ask_ai(message.text)
    await message.answer(answer)

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
