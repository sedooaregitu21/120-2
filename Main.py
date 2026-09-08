import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '8893936599:AAH6EVwJDOVbbCERjTbXVKX6jDcptGOrqi8'
ADMIN_ID = 8609938129  # የአድሚን ቴሌግራም User ID
CHANNEL_ID = -1003794082614  # የቻናልህ ትክክለኛ ቁጥር ID

bot = telebot.TeleBot(TOKEN)

user_languages = {}
admin_pending_posts = {}

# የተጠቃሚዎችን መረጃ (User ID እና Name) በዲክሽነሪ መያዝ
active_users = {}

# አድሚኑ አሁን የትኛውን ትዕዛዝ እየፈፀመ እንደሆነ ለመያዝ (Add ወይስ Remove)
admin_states = {}

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
            keyboard.add(
                InlineKeyboardButton("👥 ተጠቃሚዎች ዝርዝር", callback_data="list_users")
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
            keyboard.add(
                InlineKeyboardButton("👥 Users List", callback_data="list_users")
            )
        
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "ወዳጄ"
    
    # ተጠቃሚውን በዝርዝር ውስጥ እንመዘግባለን
    active_users[user_id] = user_name
    
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

# ----------------- የአድሚን ተጠቃሚ አስተዳደር እና ዝርዝር -----------------
@bot.callback_query_handler(func=lambda call: call.data in ['add_user', 'remove_user', 'list_users'])
def handle_user_management_buttons(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "⚠️ ይህ መብት ያለው ለአድሚን ብቻ ነው!")
        return
        
    if call.data == 'add_user':
        admin_states[ADMIN_ID] = 'waiting_to_add'
        bot.answer_callback_query(call.id, "➕ ተጠቃሚ የመጨመሪያ ተግባር")
        bot.send_message(call.message.chat.id, "✍️ ለመጨመር የፈለጉትን የተጠቃሚ 🆔 (ID) ብቻውን ይላኩላቸው:")
        
    elif call.data == 'remove_user':
        admin_states[ADMIN_ID] = 'waiting_to_remove'
        bot.answer_callback_query(call.id, "➖ ተጠቃሚ የማስወገጃ ተግባር")
        bot.send_message(call.message.chat.id, "✍️ ለማስወገድ (Reject ለማድረግ) የፈለጉትን የተጠቃሚ 🆔 (ID) ብቻውን ይላኩላቸው:")
        
    elif call.data == 'list_users':
        bot.answer_callback_query(call.id, "👥 የተጠቃሚዎች ዝርዝር እየተዘጋጀ ነው...")
        total_count = len(active_users)
        if total_count == 0:
            bot.send_message(call.message.chat.id, "⚠️ እስካሁን የተመዘገበ ተጠቃሚ የለም።")
            return
        
        # እያንዳንዱን ተጠቃሚ በቀጥታ ጠቅ በማድረግ (Click አድርጎ) ማጥፋት እንዲችል Inline ቁልፎችን እንፈጥራለን
        users_keyboard = InlineKeyboardMarkup(row_width=1)
        for uid, name in active_users.items():
            users_keyboard.add(
                InlineKeyboardButton(f"❌ {name} ({uid}) - አስወግድ", callback_data=f"del_user_{uid}")
            )
        
        bot.send_message(
            call.message.chat.id, 
            f"👥 **አጠቃላይ ተጠቃሚዎች ብዛት:** {total_count}\n\n👇 ከዚህ በታች ከሚገኙት ስሞች ውስጥ ማስወገድ (Delete ማድረግ) የሚፈልጉትን ይጫኑ፦", 
            reply_markup=users_keyboard, 
            parse_mode="Markdown"
        )

# አድሚኑ ከዝርዝሩ ውስጥ በአንድ ክሊክ (Click) ተጠቃሚን ሲያጠፋ
@bot.callback_query_handler(func=lambda call: call.data.startswith('del_user_'))
def handle_inline_delete_user(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "⚠️ መብት አለዎት!")
        return
    
    target_id = int(call.data.split('_')[2])
    
    if target_id in active_users:
        removed_name = active_users.pop(target_id)
        bot.answer_callback_query(call.id, f"✅ {removed_name} ከዝርዝር ውጪ ሆኗል!")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"🗑️ **ተጠቃሚው ተወግዷል!**\n• ስም: {removed_name}\n• ID: `{target_id}`",
            parse_mode="Markdown"
        )
    else:
        bot.answer_callback_query(call.id, "⚠️ ተጠቃሚው በዝርዝር ውስጥ አልተገኘም!")

# አድሚኑ ቁጥር ብቻ ሲልክ (Add ወይም Remove)
@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID and message.text and message.text.isdigit())
def process_admin_id_input(message):
    state = admin_states.get(ADMIN_ID)
    target_id = int(message.text)
    
    if state == 'waiting_to_add':
        active_users[target_id] = "በአድሚን የተጨመረ"
        bot.reply_to(message, f"✅ ተጠቃሚ (ID: {target_id}) በተሳካ ሁኔታ ተጨመረ!")
        admin_states[ADMIN_ID] = None
    elif state == 'waiting_to_remove':
        if target_id in active_users:
            del active_users[target_id]
            bot.reply_to(message, f"🗑️ ተጠቃሚ (ID: {target_id}) ከዝርዝሩ ውጪ ሆኗል (Rejected)!")
        else:
            bot.reply_to(message, f"⚠️ ተጠቃሚ (ID: {target_id}) በዝርዝር ውስጥ አልተገኘምም።")
        admin_states[ADMIN_ID] = None
    else:
        bot.reply_to(message, "እባክዎ መጀመሪያ ከምናሌው '➕ ተጠቃሚ ጨምር' ወይም '➖ ተጠቃሚ አስወግድ' የሚለውን ይጫኑ።")

# ----------------- ቻናል ላይ ፖስት ሲደረግ -----------------
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

@bot.edited_channel_post_handler(content_types=['document', 'audio', 'video', 'photo', 'text', 'voice'])
def handle_edited_channel_post(message):
    handle_channel_post(message)

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
