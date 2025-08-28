import os
import json
import yt_dlp
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from keep_alive import keep_alive

# 🔹 Load token
with open("config.json") as f:
    TOKEN = json.load(f)["TELEGRAM_TOKEN"]

# 🔹 Folder download
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# 🔹 Menu utama
main_menu = [["🎥 Download Video", "🎵 Download Audio"], ["🖼️ Download Gambar"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Selamat datang di Bot Downloader!\n\n"
        "Kirim link dari YouTube, TikTok, Instagram, atau Facebook.\n\n"
        "Pilih salah satu menu di bawah ini:",
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = update.message.from_user.id
    user_dir = os.path.join(DOWNLOAD_DIR, str(user_id))
    os.makedirs(user_dir, exist_ok=True)

    # Kalau bukan link
    if not text.startswith("http"):
        await update.message.reply_text("❌ Kirim link yang valid ya...")
        return

    # 🔹 Opsi download
    ydl_opts = {
        "outtmpl": os.path.join(user_dir, "%(title).100s.%(ext)s"),
        "format": "bestvideo+bestaudio/best",
        "quiet": True
    }

    try:
        await update.message.reply_text("📥 Sedang memproses, tunggu sebentar...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text, download=True)
            filename = ydl.prepare_filename(info)

        # Kirim file ke user
        if os.path.exists(filename):
            await update.message.reply_video(video=open(filename, "rb"))
            os.remove(filename)  # hapus setelah terkirim
        else:
            await update.message.reply_text("❌ Error: File tidak ditemukan.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    keep_alive()  # biar Replit stay awake
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
  
