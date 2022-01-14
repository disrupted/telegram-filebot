from __future__ import annotations

from telethon.sync import TelegramClient, events

from telegram_filebot.config import API_HASH, API_ID, BOT_TOKEN, DL_PATH


def filter_start(message):
    return message == "/start"


def download_progress(current, total):
    print(
        "Downloaded", current, "out of", total, "bytes: {:.2%}".format(current / total)
    )


def run():
    bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

    with bot:

        @bot.on(events.NewMessage(incoming=True, pattern=filter_start))
        async def start(event: events.NewMessage.Event):
            await bot.send_message(
                event.sender_id,
                "Started",
            )

        @bot.on(events.NewMessage(incoming=True, pattern=lambda m: not filter_start(m)))
        async def message_handler(event: events.NewMessage.Event):
            if not event.media:
                await event.reply("message doesn't contain media")
                return

            print(event.media)
            filepath = await event.message.download_media(
                file=DL_PATH, progress_callback=download_progress
            )
            if not filepath:
                await event.reply("error saving media")
                return

            print(filepath)
            await event.reply(f"saved {filepath}")

        bot.run_until_disconnected()
