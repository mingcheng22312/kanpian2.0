from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

ADMIN_ID = 7899684492  # 你的管理员ID

custom_keyboard = [
    ["📌 如何买币", "💎 VIP群介绍"],
    ["💰 代码价格", "📖 代码有什么用"],
    ["📢 分享推广"]  # 新增按钮
]
reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)

# 存储管理员收到的转发消息ID和用户ID的映射关系
forward_mapping = {}

# 存储积分（此处为内存方式，如需长期保存建议改为文件或数据库）
user_points = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # 初始化积分
    if user_id not in user_points:
        user_points[user_id] = 0

    # 是否通过专属链接进来的
    if context.args:
        referrer_id = int(context.args[0])
        if referrer_id != user_id:
            user_points[referrer_id] = user_points.get(referrer_id, 0) + 1
            points = user_points[referrer_id]
            await context.bot.send_message(chat_id=referrer_id,
                text=f"🎉 有人通过你的专属链接加入了机器人！当前积分：{points}")
            if points == 40:
                await context.bot.send_message(chat_id=referrer_id,
                    text="🎁 你已满 40 积分，请联系管理员 @jisouTGhao 获取免费视频代码！")

    await update.message.reply_text("欢迎，请选择一个操作：", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message_text = update.message.text

    try:
        if user_id == ADMIN_ID:
            # 管理员回复消息逻辑
            if update.message.reply_to_message:
                replied_msg_id = update.message.reply_to_message.message_id
                target_user_id = forward_mapping.get(replied_msg_id)
                if target_user_id:
                    await context.bot.send_message(chat_id=target_user_id, text=message_text)
                    await update.message.reply_text("✅ 消息已发送给用户。", reply_markup=reply_markup)
                else:
                    await update.message.reply_text("⚠️ 找不到对应用户，无法发送消息。", reply_markup=reply_markup)
            else:
                await update.message.reply_text("⚠️ 请回复转发给你的消息后再发送内容。", reply_markup=reply_markup)
        else:
            # 普通用户消息，先转发给管理员
            forwarded_message = await context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=user_id, message_id=update.message.message_id)
            forward_mapping[forwarded_message.message_id] = user_id

            # 判断按钮文字，发送对应内容
            if message_text == "📌 如何买币":
                await update.message.reply_text("这里有简单教程 虚拟币交易更安全 为了你我能活得更久🤣 https://t.me/+vh3QPpfhD_g0YTg1", reply_markup=reply_markup)
            elif message_text == "💎 VIP群介绍":
                await update.message.reply_text("Vip群内上万视频 每周三与周六会更新一次 四年内未中断更新", reply_markup=reply_markup)
            elif message_text == "💰 代码价格":
                await update.message.reply_text("代码价格 150U 大约国内1000+国外20000+视频", reply_markup=reply_markup)
            elif message_text == "📖 代码有什么用":
                await update.message.reply_text(
                    "拿到代码后你会收到一个文字的文件夹，和一个机器人，里面是代码，复制任意一条代码发送给机器人,你就会收到相应的视频。代码使用消息教学🔜 @Zhengqian66",
                    reply_markup=reply_markup)
            elif message_text == "📢 分享推广":
                share_link = f"https://t.me/{context.bot.username}?start={user_id}"
                await update.message.reply_text(
                    "📣 分享介绍：\n分享本机器人到群中，有人通过你的专属链接进入本机器人后会增加积分。\n积分满 40 会自动收到免费视频代码 150 条（紫面具、张婉莹等等）\n\n🎯 你的专属链接：\n" + share_link,
                    reply_markup=reply_markup)
            else:
                await update.message.reply_text("✅ 已发送给管理员，请稍候回复。", reply_markup=reply_markup)

    except Exception as e:
        await update.message.reply_text(f"⚠️ 发生错误：{e}")

def main():
    app = ApplicationBuilder().token("7686336735:AAHAjzWPkRNEF51kNYr6qJRGZxHG3LuAwBw").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("🤖 Bot 正在运行...")
    app.run_polling()

if __name__ == "__main__":
    main()
