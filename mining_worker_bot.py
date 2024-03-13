from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from tinydb import TinyDB, Query

# Initialize TinyDB
db = TinyDB('mining_workers.json')

# Command to start the bot
def start(update, context):
    update.message.reply_text("Welcome to the Mining Worker Manager Bot!")

# Command to save a mining worker link
def save_link(update, context):
    user_id = update.message.from_user.id
    link = ' '.join(context.args)
    
    # Save link to database with user_id as key
    db.insert({'user_id': user_id, 'link': link})

    update.message.reply_text("Link saved successfully!")

# Command to display saved links with buttons
def display_links(update, context):
    user_id = update.message.from_user.id
    user_links = db.search(Query().user_id == user_id)

    if user_links:
        keyboard = [[InlineKeyboardButton(link['link'], callback_data=str(link.doc_id))] for link in user_links]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Your saved links:", reply_markup=reply_markup)
    else:
        update.message.reply_text("You have not saved any links yet.")

# Callback function to handle button clicks and display link names
def button_click(update, context):
    query = update.callback_query
    link_id = int(query.data)
    
    link_data = db.get(doc_id=link_id)
    
    query.answer()
    query.edit_message_text(text=f"Link: {link_data['link']}")

# Set up the Telegram bot handlers and start polling
updater = Updater('YOUR_TELEGRAM_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('savelink', save_link))
dispatcher.add_handler(CommandHandler('displaylinks', display_links))
dispatcher.add_handler(CallbackQueryHandler(button_click))

updater.start_polling()
updater.idle()
