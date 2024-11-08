# FILE: command/dc.py
from pyrogram import Client, filters

async def handle_dc(client, message):
    user = await client.get_users(message.from_user.id)
    user_info = (
        f"用户名: {'@'+user.username}\n"
        f"ID: {user.id}\n"
        f"DC: {user.dc_id if user.dc_id else '请公开你的头像'}"
    )
    await message.reply(user_info)

def register_dc_handler(app):
    app.on_message(filters.command("dc"))(handle_dc)