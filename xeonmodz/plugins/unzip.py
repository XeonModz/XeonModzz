from pyrogram import filters
from xeonmodz import app
from xeonmodz.lib.mode import isPrivate
import zipfile
import os
import shutil


@app.on_message(filters.command("unzip") & filters.reply)
@isPrivate
async def unzip_file(client, message):

    status = await message.reply_text("📦 Extracting ZIP...")

    try:

        reply = message.reply_to_message

        if not reply.document:
            return await status.edit(
                "❌ Reply to a ZIP file."
            )

        file_name = reply.document.file_name or ""

        if not file_name.lower().endswith(".zip"):
            return await status.edit(
                "❌ This is not a ZIP file."
            )

        zip_path = await reply.download()

        extract_dir = f"extract_{message.id}"

        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_dir)

        files_sent = 0

        for root, dirs, files in os.walk(extract_dir):

            for file in files:

                path = os.path.join(root, file)

                try:

                    await message.reply_document(
                        document=path,
                        caption=f"📂 {file}"
                    )

                    files_sent += 1

                except Exception:
                    pass

        await status.edit(
            f"✅ Extracted {files_sent} file(s)."
        )

        try:
            os.remove(zip_path)
            shutil.rmtree(extract_dir)
        except:
            pass

    except Exception as e:

        await status.edit(
            f"❌ Error:\n{e}"
        )