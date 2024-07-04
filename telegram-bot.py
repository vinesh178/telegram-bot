from typing import Final

from twitter_downloader import download_twitter_video

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

import re

TOKEN: Final = "7110292564:AAEsh6RiqxK7xv0WBL0G-Gr4J7wE69UR82o"
BOT_USERNAME: Final = "@tvideov_bot"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello!!  Thanks for using the twitter video downloader"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please give a video url to download ")

async def handle_response(text: str, update: Update) -> str:

    p_text: str = text.lower()

    
    if is_valid_twitter_video_url(p_text):
        await update.message.reply_text(
            "Please Wait..Your video is being downloaded..."
        )
        video_file = await download_twitter_video(p_text)
        await update.message.reply_video(video_file, supports_streaming=False)
        return "Video sent"
    else: 
        return "Please provide a valid url"


def is_valid_twitter_video_url(url: str) -> bool:

    twitter_video_url_pattern = re.compile(
        r"^https://x\.com/[^/]+/status/\d+$"
    )
    return bool(twitter_video_url_pattern.match(url))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = await handle_response(new_text, update)
        else:
            return
    else:
        response = await handle_response(text, update)

    print("Bot : ", response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused {context.error}")


if __name__ == "__main__":
    try:
        print("Starting bot")
        app = Application.builder().token(TOKEN).read_timeout(60).write_timeout(60).build()

        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("help", help_command))

        app.add_handler(MessageHandler(filters.TEXT, handle_message))

        app.add_error_handler(error)

        print("Polling ...")
        app.run_polling(poll_interval=3)
    except:
        print("Bot stopped")
