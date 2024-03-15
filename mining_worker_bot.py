import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from tinydb import TinyDB, Query

db = TinyDB('user_links.json')
User = Query()

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
        rf"Hi {user.mention_html()}! Welcome to the Mining Worker Link Manager! You can easily add or save links by pasting them directly, or utilize one of the available commands. Feel free to start managing your links efficiently!",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text('''Welcome to the Mining Worker Links Bot! Here are the available commands:

/start - Start the bot
/help - Get help and see all available commands
/save_link - Add and save mining pool worker link. To give a name to the link, format your message as follows(name(optional) spaced from link ): Name URL
/showlinks - Show saved mining worker links when requested by user

Feel free to explore and manage your mining worker links with ease!''')

# Modify save_link function to store link in the database
async def save_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    message_text = update.message.text

    # Extract link and link name from the message text
    link_parts = message_text.split(' ')
    if len(link_parts) >= 2:
        link_name = link_parts[0]
        link = ' '.join(link_parts[1:])
    else:
        link_name = "Unnamed Link"
        link = message_text

    # Store user ID, link, and link name in the database
    db.insert({'user_id': user_id, 'link': link, 'link_name': link_name})
    
    await update.message.reply_text("Your mining worker link has been saved successfully.")


# Modify show_links function to retrieve and display saved links
async def show_links(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    # Retrieve saved links for the user from the database
    user_links = db.search(User.user_id == user_id)

    if user_links:
        message = "Here are your saved mining worker links:\n"
        for link_data in user_links:
            message += f"Name: {link_data['link_name']}\nLink: {link_data['link']}\n\n"
    else:
        message = "You have not saved any mining worker links yet."

    await update.message.reply_text(message)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("YOUR-BOT-TOKEN").build()

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
