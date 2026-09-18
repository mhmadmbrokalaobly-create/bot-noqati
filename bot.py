import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

# تخزين مؤقت للنقاط (يفضل قاعدة بيانات لاحقا)
points = {}

keyboard = ReplyKeyboardMarkup(
    [["نقاطي", "الترتيب"], ["تصفير"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name
    await update.message.reply_text(f"{name} اهلا", reply_markup=keyboard)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    name = update.effective_user.first_name
    text = update.message.text

    if user_id not in points:
        points[user_id] = {"name": name, "pts": 0}

    if text == "نقاطي":
        pts = points[user_id]["pts"]
        await update.message.reply_text(f"{name} نقاطك {pts}", reply_markup=keyboard)
    elif text == "الترتيب":
        sorted_users = sorted(points.values(), key=lambda x: x["pts"], reverse=True)
        msg = "الترتيب:\n"
        for i, u in enumerate(sorted_users[:10], 1):
            msg += f"{i}. {u['name']} - {u['pts']}\n"
        await update.message.reply_text(msg or "لا يوجد نقاط بعد", reply_markup=keyboard)
    elif text == "تصفير":
        points[user_id]["pts"] = 0
        await update.message.reply_text("تم تصفير نقاطك", reply_markup=keyboard)
    else:
        # اي رسالة عادية تزيد نقطة
        points[user_id]["pts"] += 1

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.run_polling()
