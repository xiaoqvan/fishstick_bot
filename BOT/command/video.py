import re
import html
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import InputMediaPhoto, InputMediaVideo

#抖音
from .videos.parser.douyin import DouYin
#皮皮虾
from .videos.parser.pipixia import PiPiXia
#快手
from .videos.parser.kuaishou import KuaiShou
#皮皮搞笑
from .videos.parser.pipigaoxiao import PiPiGaoXiao
#微博
from .videos.parser.weibo import WeiBo
#西瓜视频
from .videos.parser.xigua import XiGua
#最右
from .videos.parser.zuiyou import ZuiYou

def extract_url(text):
    url_pattern = re.compile(r'(https?://[^\s]+)')
    match = url_pattern.search(text)
    return match.group(0) if match else None

async def handle_video_parse(client, message):
    text = message.text
    if not text:
        return  

    url = extract_url(text)
    if not url:
        return  

    video_info = None
    parser = None
    if "douyin.com" in url:
        parser = DouYin()
    elif "pipix.com" in url:
        parser = PiPiXia()
    elif "kuaishou.com" in url:
        parser = KuaiShou()
    elif "ishare.ippzone.com" in url:
        parser = PiPiGaoXiao()
    elif "weibo.com" in url:
        parser = WeiBo()
    elif "ixigua.com" in url:
        parser = XiGua()
    elif "share.xiaochuankeji.cn" in url:
        parser = ZuiYou()   
    else:
        return  

    parsing_message = await message.reply("正在解析，请稍候...")

    try:
        video_info = await parser.parse_share_url(url)
    except Exception as e:
        await parsing_message.edit_text(f"解析失败: {str(e)} 多试几遍 \n如果仍然不行请联系管理员反馈。")
        return

    if video_info:
        caption = video_info.title or ""
        caption = re.sub(r'(?<!\s)#', ' #', caption)
        if isinstance(parser, DouYin):
            caption += f"\n\nBy [@{video_info.author.name}](https://www.douyin.com/user/{video_info.author.uid})"
        else:
            caption += f"\n\nBy [@{video_info.author.name}]({url})"
        
        if video_info.video_url:
            try:
                await message.reply_video(video_info.video_url, caption=caption)
            except Exception as e:
                await parsing_message.edit_text(f"发送失败: 遇到防盗链CDN\n重试几次，你也可以尝试访问视频链接\n{video_info.video_url}")
                return
        else:
            images = video_info.images
            if len(images) > 18:
                await parsing_message.edit_text("图像过多，发送失败\n建议小于18张图片的图集")
                return

            for i in range(0, len(images), 9):
                media_group = [InputMediaPhoto(image_url) for image_url in images[i:i+9]]
                if i == 0:
                    media_group[0].caption = caption  # 仅为第一个图片添加说明文字
                try:
                    await message.reply_media_group(media_group)
                except Exception as e:
                    await parsing_message.edit_text(f"发送失败: 遇到防盗链CDN\n重试几次，你也可以尝试访问图集链接\n{url}")
                    return
        
        await parsing_message.delete()

def register_handlers(app: Client):
    app.add_handler(MessageHandler(handle_video_parse, filters.command("video")))
    app.add_handler(MessageHandler(handle_video_parse, filters.private))