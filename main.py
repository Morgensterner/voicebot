import os
import uuid
from pydub import AudioSegment
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

BASE_DIR = "sessions"

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    session_dir = os.path.join(BASE_DIR, user_id)
    os.makedirs(session_dir, exist_ok=True)

    voice = update.message.voice
    file = await voice.get_file()
    file_id = str(uuid.uuid4())
    file_path = os.path.join(session_dir, f"{file_id}.ogg")
    await file.download_to_drive(file_path)
    await update.message.reply_text("Голосовое сообщение сохранено!")

async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    session_dir = os.path.join(BASE_DIR, user_id)
    if not os.path.exists(session_dir):
        await update.message.reply_text("Нет сохранённых голосовых сообщений.")
        return

    files = sorted(os.listdir(session_dir))
    if not files:
        await update.message.reply_text("Голосовых сообщений не найдено.")
        return

    combined = AudioSegment.empty()
    for f in files:
        file_path = os.path.join(session_dir, f)
        audio = AudioSegment.from_file(file_path, format="ogg")
        combined += audio

    out_path = os.path.join(session_dir, "result.ogg")
    combined.export(out_path, format="ogg")
    with open(out_path, 'rb') as audio_file:
        await update.message.reply_voice(voice=audio_file)
    await update.message.reply_text("Все голосовые сообщения объединены!")

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise Exception("Не найден токен бота! Добавь переменную TELEGRAM_TOKEN.")
    app = Application.builder().token(token).build()

    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(CommandHandler("finish", finish))

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
