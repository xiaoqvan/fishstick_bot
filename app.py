import os
import sys
import asyncio
from pyrogram import Client, idle, filters
from dotenv import load_dotenv
from config.proxy_config import get_proxy_config
from BOT.command.video import register_handlers
from BOT.command.dc import register_dc_handler
from BOT.command.Music import register_music_163
from BOT.command.help import register_help


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


load_dotenv()

api_id = int(os.getenv("api_id"))
api_hash = os.getenv("api_hash")
bot_token = os.getenv("bot_token")

proxy = get_proxy_config()

async def main():
    async with Client("my_bot", api_id, api_hash, bot_token=bot_token, proxy=proxy) as app:
    
        @app.on_message(filters.command("start"))
        async def handle_start(client, message):
            await message.reply("你好，我是Bot。你可以使用我来发送消息到频道。\n也可以发送 /help 获取帮助信息。")
        
        @app.on_message(filters.command("ban"))
        async def handle_ban(client, message):
            await message.reply("你只能在群聊中使用")

        register_dc_handler(app) # 注册 dc 处理程序
        register_help(app) # 注册帮助处理程序
        register_music_163(app) # 注册音乐处理程序
        register_handlers(app) # 注册视频处理程序
        await idle()  # 保持客户端运行

asyncio.run(main())