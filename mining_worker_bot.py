#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Telegram bot for managing mining worker links.

This Telegram bot allows users to manage their mining worker links. Users can send one or more links of their mining pool workers, which are then stored in a database using TinyDB. Each link is associated with the user's Telegram user ID. Users can request their saved links using buttons and optionally give a name to each link.
"""

import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Welcome to the Mining Worker Link Manager.",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("To manage your mining worker links, send them to me. You can also request your saved links using buttons.")


async def save_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Save the user's mining worker link."""
    # Implement saving the link to a database like TinyDB here
    await update.message.reply_text("Your mining worker link has been saved successfully.")


async def show_links(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the user's saved mining worker links."""
    # Implement retrieving and displaying saved links here
    await update.message.reply_text("Here are your saved mining worker links:")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6508650560:AAF87aY-aLaMo7LkTYJcKuxtHZ-iPOdgtzs").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Save mining worker link when received from user
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_link))

    # Show saved mining worker links when requested by user
    application.add_handler(CommandHandler("showlinks", show_links))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
