import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN='8893936599:AAGZ1ezzjPPym2GhoBh7nXMKQTmj6gcQcYI'
ADMIN_ID = 8609938129  # የራስህን የቴሌግራም User ID እዚህ አስገባ
CHANNEL_ID =  -1003794082614  # የቻናልህ ትክክለኛ ቁጥር ID (በኔጌቲቭ ምልክት መጀመሩን አረጋግጥ)

bot = telebot.TeleBot(TOKEN)

user_languages = {}
admin_pending_posts = {}

# የተከማቹ ፋይሎች ዝርዝር (ስዕለ ዓድኖን ጨምሮ)
stored_files = {
    "books": [],
    "audio": [],
    "teachings": [],
    "videos": [],
    "art": []  # ስዕለ ዓድኖ
}

# ----------------- የተጠቃሚዎች እና የአድሚን ምናሌዎች -----------------
def get_main_menu(user_id: int = 0):
    lang = user_languages.get(user_id, "am")
    keyboard = InlineKeyboardMarkup(row_width=2)
    is_admin = (user_id == ADMIN_ID)
    
    if lang == "am":
        keyboard.add(
            InlineKeyboardButton("📚 መጽሐፍ", callback_data="view_books"),
            InlineKeyboardButton("🎧 ኦዲዮ / መዝሙር", callback_data="view_audio")
        )
        keyboard.add(
            InlineKeyboardButton("📖 መንፈሳዊ ትምህርት", callback_data="view_teachings"),
            InlineKeyboardButton("🎬 ቪዲዮ", callback_data="view_videos")
        )
        keyboard.add(
            InlineKeyboardButton("🖼️ ስዕለ ዓድኖ", callback_data="view_art")
        )
        keyboard.add(
            InlineKeyboardButton("📞ለማንኛውም ጥያቄ", url="https://t.me/Power_werked")
        )
        keyboard.add(
            InlineKeyboardButton("⚙️ ቋንቋ", callback_data="settings_lang")
        )
        if is_admin:
            keyboard.add(
                InlineKeyboardButton("➕ ተጠቃሚ ጨምር", callback_data="add_user"),
                InlineKeyboardButton("➖ ተጠቃሚ አስወግድ", callback_data="remove_user")
            )
    else:
        keyboard.add(
            InlineKeyboardButton("📚 Books", callback_data="view_books"),
            InlineKeyboardButton("🎧 Audio", callback_data="view_audio")
        )
        keyboard.add(
            InlineKeyboardButton("📖 Teachings", callback_data="view_teachings"),
            InlineKeyboardButton("🎬 Video", callback_data="view_videos")
        )
        keyboard.add(
            InlineKeyboardButton("🖼️ Sacred Art", callback_data="view_art")
        )
        keyboard.add(
            InlineKeyboardButton("📞 For Any Questions", url="https://t.me/Power_werked")
        )
        keyboard.add(
            InlineKeyboardButton("⚙️ Language", callback_data="settings_lang")
        )
        if is_admin:
            keyboard.add(
                InlineKeyboardButton("➕ Add User", callback_data="add_user"),
                InlineKeyboardButton("➖ Remove User", callback_data="remove_user")
            )
        
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "ወዳጄ"
    lang = user_languages.get(user_id, "am")
    
    if lang == "am":
        welcome_text = (
            f"ሰላም ውድ {user_name}! እንኳን ወደ sedoo የፍቅር ቤተሰቦች ቦት በሰላም መጡ! 🙏✨\n\n"
            "ከታች ካሉት ማራኪ አማራጮች የሚፈልጉትን ይምረጡ፦"
        )
    else:
        welcome_text = (
            f"Hello dear {user_name}! Welcome to sedoo's Family Bot! 🙏✨\n\n"
            "Please choose an option from below:"
        )
        
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu(user_id))

# ቋንቋ መቀየሪያ
@bot.callback_query_handler(func=lambda call: call.data == 'settings_lang')
def handle_language_settings(call):
    user_id = call.from_user.id
    lang = user_languages.get(user_id, "am")
    
    lang_keyboard = InlineKeyboardMarkup(row_width=2)
    lang_keyboard.add(
        InlineKeyboardButton("አማርኛ 🇪🇹", callback_data="lang_am"),
        InlineKeyboardButton("English 🇬🇧", callback_data="lang_en")
    )
    
    back_text = "⬅️ ተመለስ" if lang == "am" else "⬅️ Back"
    lang_keyboard.add(InlineKeyboardButton(back_text, callback_data="back_to_main"))
    
    text = "🌐 የሚፈልጉትን ቋንቋ ይምረጡ:" if lang == "am" else "🌐 Choose your preferred language:"
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=lang_keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def handle_lang_selection(call):
    user_id = call.from_user.id
    user_name = call.from_user.first_name or "ወዳጄ"
    selected_lang = "am" if call.data == "lang_am" else "en"
    user_languages[user_id] = selected_lang
    
    lang_name = "አማርኛ" if selected_lang == "am" else "English"
    bot.answer_callback_query(call.id, f"ቋንቋው ወደ {lang_name} ተቀይሯል! ✅")
    
    text = f"ሰላም ውድ {user_name}! እንኳን ወደ sedoo የፍቅር ቤተሰቦች ቦት በሰላም መጡ! 🙏✨\n\nከታች ካሉት ማራኪ አማራጮች የሚፈልጉትን ይምረጡ፦" if selected_lang == "am" else f"Hello dear {user_name}! Welcome to sedoo's Family Bot! 🙏✨\n\nPlease choose an option:"
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=get_main_menu(user_id))

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_main')
def handle_back_to_main(call):
    user_id = call.from_user.id
    user_name = call.from_user.first_name or "ወዳጄ"
    lang = user_languages.get(user_id, "am")
    text = f"ሰላም ውድ {user_name}! እንኳን ወደ sedoo የፍቅር ቤተሰቦች ቦት በሰላም መጡ! 🙏✨\n\nከታች ካሉት ማራኪ አማራጮች የሚፈልጉትን ይምረጡ፦" if lang == "am" else f"Hello dear {user_name}! Welcome to sedoo's Family Bot! 🙏✨\n\nPlease choose an option:"
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=get_main_menu(user_id))

# ----------------- የአድሚን ተጠቃሚ መጨመሪያ/ማስወገጃ ቁልፎች ምላሽ -----------------
@bot.callback_query_handler(func=lambda call: call.data in ['add_user', 'remove_user'])
def handle_user_management_buttons(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "⚠️ ይህ መብት ያለው ለአድሚን ብቻ ነው!")
        return
        
    if call.data == 'add_user':
        bot.answer_callback_query(call.id, "➕ ተጠቃሚ የመጨመሪያ ተግባር")
        bot.send_message(call.message.chat.id, "➕ አዲስ ተጠቃሚ ለመጨመር የጠየቁትን መመሪያ ይከተሉ ወይም የሚመለከተውን መረጃ ያስገቡ:")
    elif call.data == 'remove_user':
        bot.answer_callback_query(call.id, "➖ ተጠቃሚ የማስወገጃ ተግባር")
        bot.send_message(call.message.chat.id, "➖ ተጠቃሚ ለማስወገድ (Reject ለማድረግ) የትኛውን ተጠቃሚ እንደሆነ ይምረጡ:")

# ----------------- ቻናል ላይ ፖስት ሲደረግ (ፎቶዎችን ጨምሮ) -----------------
@bot.channel_post_handler(content_types=['document', 'audio', 'video', 'photo', 'text', 'voice'])
def handle_channel_post(message):
    if str(message.chat.id) == str(CHANNEL_ID):
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("📚 መጽሐፍ ላይ ጨምር", callback_data=f"ch_save_books_{message.message_id}"),
            InlineKeyboardButton("🎧 ኦዲዮ ላይ ጨምር", callback_data=f"ch_save_audio_{message.message_id}")
        )
        keyboard.add(
            InlineKeyboardButton("📖 ትምህርት ላይ ጨምር", callback_data=f"ch_save_teachings_{message.message_id}"),
            InlineKeyboardButton("🎬 ቪዲዮ ላይ ጨምር", callback_data=f"ch_save_videos_{message.message_id}")
        )
        # ስዕለ ዓድኖ ላይ ለመጨመር የተስተካከለ ቁልፍ
        keyboard.add(
            InlineKeyboardButton("🖼️ ስዕለ ዓድኖ ላይ ጨምር", callback_data=f"ch_save_art_{message.message_id}")
        )
        
        try:
            bot.send_message(
                ADMIN_ID,
                "🔔 **አዲስ ፖስት/ፎቶ ቻናል ላይ ተለቀቀ!**\n\n❓ ይህንን ፋይል የየትኛው ምድብ ላይ ማከማቸት ይፈልጋሉ?",
                reply_markup=keyboard
            )
        except Exception as e:
            print(f"ማሳወቂያ መላክ አልተቻለም: {e}")

# አድሚኑ ቻናል ፖስቱን እንደቀየረ (Edit ሲደረግም እንዲሰራ)
@bot.edited_channel_post_handler(content_types=['document', 'audio', 'video', 'photo', 'text', 'voice'])
def handle_edited_channel_post(message):
    handle_channel_post(message)

# አድሚኑ ምድብ ሲመርጥ
@bot.callback_query_handler(func=lambda call: call.data.startswith('ch_save_'))
def save_channel_file(call):
    data_parts = call.data.split('_')
    category = data_parts[2]
    msg_id = int(data_parts[3])
    
    stored_files[category].append({
        "from_chat_id": CHANNEL_ID,
        "message_id": msg_id
    })
    
    bot.answer_callback_query(call.id, "✅ ፋይሉ በትክክል ተከማችቷል!")
    success_msg = f"✅ የቻናሉ ፖስት በተሳካ ሁኔታ በ **{category}** ምድብ ስር ተቀምጧል! 🚀"
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=success_msg
    )

# ----------------- ተጠቃሚዎች ፋይል ሲፈልጉ -----------------
@bot.callback_query_handler(func=lambda call: call.data.startswith('view_'))
def user_view_category(call):
    user_id = call.from_user.id
    category = call.data.split('_')[1]
    
    items = stored_files.get(category, [])
    
    if not items:
        bot.answer_callback_query(call.id, "⚠️ በዚህ ምድብ ስር እስካሁን የተለቀቀ ፋይል የለም።")
        bot.send_message(call.message.chat.id, "⚠️ ይቅርታ፣ በዚህ ምድብ ውስጥ እስካሁን የተጨመረ ፋይል አልተገኘም። 🙏")
        return
    
    bot.answer_callback_query(call.id, f"📂 የ{category} ዝርዝር እየተላከ ነው...")
    bot.send_message(call.message.chat.id, f"📂 **የተገኙ ፋይሎች ዝርዝር፦**")
    
    for item in items:
        try:
            bot.copy_message(
                chat_id=call.message.chat.id,
                from_chat_id=item["from_chat_id"],
                message_id=item["message_id"]
            )
        except Exception as e:
            print(f"ፋይል መላክ አልቻለም: {e}")

if __name__ == "__main__":
    print("ቦቱ በመጀመር ላይ ነው...")
    bot.infinity_polling()
