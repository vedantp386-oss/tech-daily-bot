import requests
import os
from datetime import datetime, time
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Application, CommandHandler
import asyncio

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

bot = Bot(token=TOKEN)

async def send_daily_tech_update():
    try:
        url = f"https://newsapi.org/v2/top-headlines?category=technology&apiKey={NEWS_API_KEY}&pageSize=8"
        response = requests.get(url)
        data = response.json()

        message = f"🚀 **Daily Tech Update - {datetime.now().strftime('%B %d, %Y')}**\n\n"

        for article in data.get("articles", [])[:8]:
            title = article.get('title', 'No Title')
            url_link = article.get('url', '#')
            source = article.get('source', {}).get('name', 'Unknown')
            message += f"• <b>{title}</b>\n   📌 {source} • <a href='{url_link}'>Read full →</a>\n\n"

        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='HTML', disable_web_page_preview=True)
        print("✅ Daily tech news sent!")

    except Exception as e:
        print("Error:", e)

async def start(update, context):
    await update.message.reply_text("✅ Vedant Tech Daily Bot is Active!\nUse /now to get latest news immediately.")

async def now(update, context):
    await update.message.reply_text("📡 Fetching latest tech news for you...")
    await send_daily_tech_update()

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("now", now))
    
    # Runs every day at 8:00 AM
    app.job_queue.run_daily(send_daily_tech_update, time=time(hour=8, minute=0))
    
    print("🤖 Your Tech Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())