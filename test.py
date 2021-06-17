from conf import TOKEN
import logging
from datetime import datetime, timedelta

from telegram import * 
from telegram.ext import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
#btn
location_keyboard = KeyboardButton(text="Lokatsiyani yuborish", request_location=True)
contact_keyboard =KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)
custom_keyboard = [[location_keyboard, contact_keyboard]]
reply_markup = ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
        
def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("O'zbekcha", callback_data="lan_uz"),
            InlineKeyboardButton("Руский",callback_data="lan_ru"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    user = update.message.from_user.first_name
    try:
        msg=f"Assalomu aleykum <b>{user}</b> !\n\nmarxamat kerakli tilni tanlang\nпривет  <b>{user}</b> !\nвибриты своий язику "
        context.bot.send_message(chat_id=update.effective_chat.id,text=msg ,parse_mode='HTML',reply_markup=reply_markup)
    except Exception as e:
        print('error ', str(e))
        
def lan_uz(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(text="<b>Siz o'zbek tilini tanladingiz \nendi raqamingizni yuboring.</b>\n\nTelefon raqamini yuborish uchun \npastdagi tugmani bosing",parse_mode='HTML')
    query = update.callback_query
    user_id = query.from_user.id
    
    #query.message.delete()
    query.message.reply_html(text='👇👇👇👇👇👇👇👇', reply_markup=reply_markup)

    
def lan_ru(update: Update, context: CallbackContext):
    query = update.callback_query  
    query.answer()
    
    query.edit_message_text(text="Selected option: lan ru")
    
def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    query.answer()

    choese=query.data
    
    if choese=="lan_uz":
        lan_uz(update,context)
    if choese=="lan_ru":
        lan_ru(update,context)
        
def inline_callback(update, context):
    try:
        query = update.callback_query
        user_id = query.from_user.id
        
    except Exception as e:
        print('error ', str(e))
        
def help_command(update: Update, _: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")
    
def add(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Choose an object.")
    

def main() -> None:
    """Run the bot."""
    # updaterga bot tokenini beramiz
    updater = Updater(TOKEN,use_context=True)
    dispatcher = updater.dispatcher
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    
    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()