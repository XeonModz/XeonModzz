# from pyrogram import filters
# from xeonmodz import app
# from xeonmodz.lib.mode import isPrivate
# from config import FB_API
# import requests


# @app.on_message(filters.command("fb"))
# @isPrivate
# async def facebook_dl(_, message):

#     try:
#         await message.react("⚡")
#     except Exception:
#         pass

#     if len(message.command) < 2:
#         return await message.reply_text(
#             "Usage:\n/fb <facebook_url>"
#         )

#     fb_url = message.command[1]

#     try:
#         r = requests.get(
#             FB_API,
#             params={"url": fb_url},
#             timeout=60
#         )

#         if r.status_code != 200:
#             return await message.reply_text(
#                 f"❌ API Error\nHTTP {r.status_code}"
#             )

#         try:
#             data = r.json()
#         except Exception:
#             return await message.reply_text(
#                 "❌ Invalid API Response"
#             )

#         if not data.get("success"):
#             return await message.reply_text(
#                 "❌ Failed to fetch Facebook video."
#             )

#         video_url = (
#             data.get("videos", {})
#             .get("hd", {})
#             .get("url")
#         )

#         if not video_url:
#             video_url = (
#                 data.get("videos", {})
#                 .get("sd", {})
#                 .get("url")
#             )

#         if not video_url:
#             return await message.reply_text(
#                 "❌ No video URL found."
#             )

#         await message.reply_video(
#             video=video_url,
#             caption="𝚾𝛆𝛐𝛈𝚳𝛐𝛛𝐳"
#         )

#     except requests.exceptions.Timeout:
#         await message.reply_text(
#             "❌ API Timeout"
#         )

#     except Exception as e:
#         await message.reply_text(
#             f"❌ Error:\n{e}"
#         )