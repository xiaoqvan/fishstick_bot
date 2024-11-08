from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import httpx

def search_song(song_name):
    url = f"http://music.163.com/api/search/get?s={song_name}&type=1&offset=0&total=true&limit=20"
    response = httpx.get(url)
    data = response.json()
    return data['result']['songs']

def download_song(song_id):
    url = f"http://music.163.com/song/media/outer/url?id={song_id}.mp3"
    return url

async def music_163(client, message):
    music_name = message.text.replace("/music", "").strip()
    if music_name == "": 
        await message.reply("请输入 /music+歌曲名称搜索或歌曲ID")
    else:
        if music_name.isdigit():
            music_url = download_song(music_name)
            music_url = download_song(music_name)
            await client.send_message(message.chat.id, f"歌曲ID {music_name} 的链接为: {music_url} \n如果是404则是会员歌曲无法下载", disable_web_page_preview=False)
        else:
            songs = search_song(music_name)
            response_message = f"搜索关键词 {music_name} 的搜索结果:\n"
            for index, song in enumerate(songs, start=1):
                response_message += f"{index}. {song['name']}-{song['artists'][0]['name']} id: `{song['id']}`\n"
            response_message += "使用 /music +id 可获取歌曲"
            await message.reply(response_message)
        

def register_music_163(app):
    app.add_handler(MessageHandler(music_163, filters.command("music")))
