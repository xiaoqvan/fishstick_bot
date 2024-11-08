from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler

async def handle_help(client, message):
    await message.reply("你好这里是帮助信息 \n发送 /dc 获取你的DC信息 \n发送 /music+音乐名称获取音乐信息 \n发送视频分享链接 获取视频信息  \n\n 群聊发送 /video+视频分享链接 获取视频信息")

def register_handlers(app: Client):
    app.add_handler(MessageHandler(handle_help, filters.command("help")))