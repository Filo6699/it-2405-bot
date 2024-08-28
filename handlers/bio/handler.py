from typing import Dict, Optional
from random import choice, random
from asyncio import sleep

from telegram import Update, MessageEntity
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    ConversationHandler,
    filters,
)
from telegram.error import TelegramError

from core.bot import app
from handlers.bio.storage import Storage
from tools.escape import escape_markdown_v2


(
    ASK_NAME,
    ASK_AGE,
    ASK_GENDER,
    ASK_LOCATION,
    ASK_INTERESTS,
    ASK_PROJECTS,
    ASK_GOALS,
    ASK_ABOUT_ME,
) = range(8)


def generate_bio_message(data: Dict[str, str]) -> str:
    return "".join(
        [
            f"**📝 Bio of {data['name']}**\n\n"
            f"👤 **Name:** {data['name']}\n"
            f"🎂 **Age:** {data['age']}\n"
            f"🔢 **Gender:** {data['gender']}\n"
            f"🌐 **Hometown:** {data['hometown']}\n"
            f"💡 **Interests:** {data['interests']}\n"
            f"📚 **Current Projects:** {data['current_projects']}\n"
            f"📈 **Goals:** {data['goals']}\n\n"
            f"📖 **About Me:** {data['about_me']}"
        ]
    )


async def get_bio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if len(args) != 1:
        await update.message.reply_text("Usage: /bio username")
        return

    user = Storage.get_user(args[0])
    if user == None:
        user = Storage.get_user(args[0][1:])
    if user == None:
        await update.message.reply_text("Username not found")

    msg = generate_bio_message(user)
    await update.message.reply_markdown_v2(msg)


async def start_bio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Great! Let's get started with your bio.\nWhat's your name?"
    )
    return ASK_NAME


async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = escape_markdown_v2(update.message.text)
    await update.message.reply_text("How old are you?")
    return ASK_AGE


async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["age"] = escape_markdown_v2(update.message.text)
    await update.message.reply_text("What's your gender?")
    return ASK_GENDER


async def ask_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["gender"] = escape_markdown_v2(update.message.text)
    await update.message.reply_text("Where are you from?")
    return ASK_LOCATION


async def ask_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["hometown"] = escape_markdown_v2(update.message.text)
    await update.message.reply_text("What are your interests?")
    return ASK_INTERESTS


async def ask_interests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["interests"] = escape_markdown_v2(update.message.text)
    await update.message.reply_text("What current projects are you working on?")
    return ASK_PROJECTS


async def ask_projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["current_projects"] = escape_markdown_v2(update.message.text)
    await update.message.reply_text("What are your goals?")
    return ASK_GOALS


async def ask_goals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["goals"] = escape_markdown_v2(update.message.text)
    await update.message.reply_text("Tell us a bit about yourself.")
    return ASK_ABOUT_ME


async def ask_about_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["about_me"] = escape_markdown_v2(update.message.text)

    data = context.user_data

    Storage.save_user(update.effective_user.username, data)

    bio_message = generate_bio_message(data)

    await update.message.reply_text(bio_message, parse_mode="MarkdownV2")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Conversation cancelled.")
    return ConversationHandler.END


app.add_handler(
    ConversationHandler(
        entry_points=[CommandHandler("my_bio", start_bio)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
            ASK_GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_gender)],
            ASK_LOCATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_location)
            ],
            ASK_INTERESTS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_interests)
            ],
            ASK_PROJECTS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_projects)
            ],
            ASK_GOALS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_goals)],
            ASK_ABOUT_ME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_about_me)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
)
app.add_handler(CommandHandler("bio", get_bio))
