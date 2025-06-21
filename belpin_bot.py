import logging
import requests
from langdetect import detect
from telegram import Update, constants
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters
)
from config import TELEGRAM_BOT_TOKEN, OPENROUTER_API_KEY, MODEL_NAME

# Konfigurasi logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Deteksi bahasa pesan user
def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return "id"  # Default ke Bahasa Indonesia

# Prompt sistem dengan gaya manusiawi, rapi, dan responsif
def build_system_prompt(lang_code: str) -> str:
    if lang_code == "id":
        return (
            "Kamu adalah Belpin Bot, asisten AI yang sopan, cerdas, gaul, ramah dan menyenangkan.\n"
            "Jawablah dalam Bahasa Indonesia yang santai namun jelas. Gunakan kalimat yang mengalir, tidak kaku, dan mudah dipahami oleh orang awam.\n"
            "Bayangkan kamu sedang ngobrol dengan teman yang ingin tahu sesuatu, jadi jangan terlalu teknis.\n"
            "Gunakan ejaan dan tata bahasa yang rapi.\n"
            "Tujuanmu adalah memberi jawaban yang bikin orang merasa nyaman dan tercerahkan."
        )

# Fungsi kirim pertanyaan ke OpenRouter AI
async def ai_reply(prompt: str) -> str:
    lang = detect_language(prompt)
    system_prompt = build_system_prompt(lang)

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=20
        )
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        logging.error(f"❌ Error dari AI: {e}")
        return "Maaf, saya sedang mengalami gangguan. Coba beberapa saat lagi ya."

# Tangani pesan biasa
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat.send_action(action=constants.ChatAction.TYPING)

    ai_response = await ai_reply(user_message)
    reply = f"🤖 *Belpin Bot:*\n\n{ai_response}"
    await update.message.reply_text(reply, parse_mode="Markdown")

# Respon saat /start ditekan
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = (
        "👋 *Halo! Saya Belpin Bot.*\n\n"
        "Saya bisa membantu menjawab pertanyaan kamu, ngobrol santai, atau bantu jelasin hal-hal rumit dengan cara yang gampang dimengerti.\n"
    )
    await update.message.reply_text(welcome, parse_mode="Markdown")

# Jalankan bot
if __name__ == "__main__":
    logging.info("🤖 Belpin Bot sedang dijalankan...")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logging.info("✅ Belpin Bot siap menerima pesan!")
    app.run_polling()
