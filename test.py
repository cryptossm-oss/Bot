import asyncio
import logging
import threading
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Тохиргоо
TOKEN = "8939418709:AAH7z4FNLDjU8LeujEMpffySJ_zexBafFqs"
AGENT_USERNAME = "KasaDota"
CHANNEL_ID = -1001812791576  # Таны канал ID

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
scheduler = AsyncIOScheduler(timezone="Asia/Ulaanbaatar")

# --- RENDER-ИЙГ ХУУРАХ ХУУРАМЧ ВЭБ СЕРВЕР ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running perfectly!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()
# ---------------------------------------------

# Автомат пост оруулах функц
async def send_auto_post():
    try:
        post_text = (
            "🔥 **1XBET & MELBET ОДЫН САНАЛ!** 🔥\n\n"
            "🎯 1XBET Промо код: `Kasadota77`\n"
            "🎯 Melbet Промо код: `Dari11`\n\n"
            "💸 Хамгийн өндөр бонус авч, хожих боломжоо өсгөөрэй!\n"
            "⚡️ Цэнэглэх болон таталт хийх бол манай агент руу бичнэ үү."
        )

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="💳 Цэнэглэх / Таталт хийх (Агент)",
                        url=f"https://t.me/{AGENT_USERNAME}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🤖 Бот руу орох", url=f"https://t.me/{(await bot.get_me()).username}"
                    )
                ],
            ]
        )

        photo = FSInputFile("poster.jpg")

        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photo,
            caption=post_text,
            reply_markup=keyboard,
            parse_mode="Markdown",
        )
        print("✅ Автомат пост амжилттай илгээгдлээ!")
    except Exception as e:
        print(f"❌ Автомат пост илгээхэд алдаа гарлаа: {e}")


# /start команд 
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎯 1XBET & Melbet Promo Code", callback_data="promo_codes"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💳 Цэнэглэх / Таталт хийх (Агент)",
                    url=f"https://t.me/{AGENT_USERNAME}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ Зааварчилгаа авах", callback_data="help"
                )
            ],
        ]
    )

    welcome_text = (
        "🔥 **1XBET & MELBET АЛБАН ЁСНЫ АГЕНТ** 👋\n\n"
        "Энэхүү цэсээр дамжуулан та албан ёсны промо кодыг ашиглан бүртгүүлж, "
        "цэнэглэлт болон таталтын үйл ажиллагааг агентаар дамжуулан түргэн шуурхай хийлгээрэй."
    )

    try:
        photo = FSInputFile("poster.jpg")
        
        await bot.send_photo(
            chat_id=CHANNEL_ID, 
            photo=photo, 
            caption=welcome_text, 
            reply_markup=keyboard
        )
        await message.reply("✅ Үндсэн цэсийг зурагтайгаар суваг руу амжилттай нийтэллээ!")
    except Exception as e:
        await message.reply(f"❌ Суваг руу илгээхэд алдаа гарлаа: {e}")


# Промо код харах
@dp.callback_query(F.data == "promo_codes")
async def show_promo_codes(callback: types.CallbackQuery):
    promo_text = (
        "🔥 **Бүртгүүлэхэд ашиглах Промо Кодууд:**\n\n"
        "🔹 **1XBET Promo Code:** `Kasadota77`\n"
        "*(Энэ кодыг ашигласнаар бонус болон бусад урамшууллыг авах боломжтой)*\n\n"
        "🔹 **Melbet Promo Code:** `Dari11`\n"
        "*(Шинэ хэрэглэгчийн урамшуулал авах)*\n\n"
        "📌 *Бүртгүүлэхдээ дээрх кодуудыг яг хэвээр нь оруулахаа мартуузай!*"
    )

    try:
        await bot.send_message(chat_id=callback.from_user.id, text=promo_text, parse_mode="Markdown")
        await callback.answer("📩 Таны хувийн чат руу мэдээллийг илгээлээ!", show_alert=False)
    except Exception:
        await callback.answer("⚠️ Та эхлээд манай бот руу орж /start дарж идэвхжүүлсний дараа энэ товчийг ашиглана уу!", show_alert=True)


# Зааварчилгаа 
@dp.callback_query(F.data == "help")
async def show_help(callback: types.CallbackQuery):
    help_text = (
        "📖 **Бот ашиглах болон Бонус авах заавар:**\n\n"
        "1️⃣ **Бүртгэл:** Дээрх промо кодуудыг ашиглан 1XBET эсвэл Melbet системд шинээр бүртгүүлээрэй.\n\n"
        "2️⃣ **Бонус:** Та манай промо кодыг ашигласнаар эхний цэнэглэлтээсээ **100-130% хүртэлх урамшуулал (бонус)** авах бүрэн боломжтой!\n\n"
        "3️⃣ **Мөнгө болгох нууц:** Энэхүү авсан бонусаа хэрхэн жинхэнэ бэлэн мөнгө болгож татах аргыг манай админ танд тусгайлан зааж өгөх болно.\n\n"
        "4️⃣ **Орлого/Зарлага:** Дансаа цэнэглэх болон хожсон мөнгөө хурдан шуурхай, ямар ч шимтгэлгүй татаж авахын тулд **'Цэнэглэх / Таталт хийх'** товч дээр дарж манай албан ёсны агенттай холбогдоорой."
    )

    try:
        await bot.send_message(chat_id=callback.from_user.id, text=help_text, parse_mode="Markdown")
        await callback.answer("📩 Таны хувийн чат руу зааварчилгаа илгээгдлээ!", show_alert=False)
    except Exception:
        await callback.answer("⚠️ Та эхлээд манай бот руу орж /start дарж идэвхжүүлсний дараа энэ товчийг ашиглана уу!", show_alert=True)


async def main():
    # Хуурамч серверийг асаах
    threading.Thread(target=run_dummy_server, daemon=True).start()

    scheduler.add_job(send_auto_post, "interval", hours=2)
    scheduler.start()

    print("Бот амжилттай асаж байна...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
