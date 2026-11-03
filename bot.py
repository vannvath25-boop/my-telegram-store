import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# បើកប្រព័ន្ធ Log
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    message = f"សូមអរគុណ {user_name} ដែលបានមកកាន់ហាងយើងខ្ញុំ! 🙏"
    await update.message.reply_text(message)

if __name__ == '__main__':
    # ទាញយក Token ដោយស្វ័យប្រវត្តិពី Railway Server
    TOKEN = os.environ.get("TOKEN")
    
    if not TOKEN:
        raise ValueError("មិនទាន់បានកំណត់ TOKEN នៅក្នុង Environment Variables ទេ។")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("Bot កំពុងដំណើរការនៅលើ Cloud...")
    app.run_polling()
