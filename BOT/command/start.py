from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler

async def handle_start(client, message):
    await message.reply("你好，我是Bot。你可以使用我来发送消息到频道。也可以发送 /help 获取帮助信息。")

def register_handlers(app: Client):
    app.add_handler(MessageHandler(handle_start, filters.command("start")))