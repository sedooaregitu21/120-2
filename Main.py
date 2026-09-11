import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '8893936599:AAEjIqkOGYpTt5CPuHrQ_4CwnFUSzgFawbY'
ADMIN_ID = 8609938129  # የአድሚን ቴሌግራም User ID
ADMIN_USERNAME = 'Power_werked' 
CHANNEL_ID = -1003794082614  # የቻናልህ ትክክለኛ ቁጥር ID

bot = telebot.TeleBot(TOKEN)

user_languages = {}
admin_states = {}

active_users = {}
user_interaction_counts = {}

# የተከማቹ ፋይሎች ዝርዝር (ከቻናል የሚመጡት እዚህ ይከማቻሉ)
stored_files = {
    "books": [],
    "audio": [],
    "teachings": [],
    "videos": [],
    "art": []
}

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
            InlineKeyboardButton("💬 ለማንኛውም ጥያቄ", url=f"https://t.me/{ADMIN_USERNAME}"),
            InlineKeyboardButton("✍️ አስተያየት", callback_data="feedback_prompt")
        )
        keyboard.add(
            InlineKeyboardButton("👥 ለግሩፕ አስተያየት መስጠት", callback_data="group_feedback")
        )
        keyboard.add(
            InlineKeyboardButton("⚙️ ቋንቋ", callback_data="settings_lang")
        )
        if is_admin:
            keyboard.add(
                InlineKeyboardButton("➕ ተጠቃሚ ጨምር", callback_data="add_user")
            )
            keyboard.add(
                InlineKeyboardButton("👥 ተጠቃሚዎች ዝርዝር", callback_data="list_users"),
                InlineKeyboardButton("📊 የተጠቃሚዎች ድግግሞሽ (Stats)", callback_data="user_stats"),
                InlineKeyboardButton("📢 ማስታወቂያ ላክ", callback_data="broadcast_menu")
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
            InlineKeyboardButton("💬 For Any Questions", url=f"https://t.me/{ADMIN_USERNAME}"),
            InlineKeyboardButton("✍️ Feedback", callback_data="feedback_prompt")
        )
        keyboard.add(
            InlineKeyboardButton("👥 Group Feedback", callback_data="group_feedback")
        )
        keyboard.add(
            InlineKeyboardButton("⚙️ Language", callback_data="settings_lang")
        )
        if is_admin:
            keyboard.add(
                InlineKeyboardButton("➕ Add User", callback_data="add_user")
            )
            keyboard.add(
                InlineKeyboardButton("👥 Users List", callback_data="list_users"),
                InlineKeyboardButton("📊 User Stats", callback_data="user_stats"),
                InlineKeyboardButton("📢 Send Broadcast", callback_data="broadcast_menu")
            )
        
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "ወዳጄ"
    
    if user_id not in active_users:
        active_users[user_id] = user_name
    
    user_interaction_counts[user_id] = user_interaction_counts.get(user_id, 0) + 1
    lang = user_languages.get(user_id, "am")
    
    if lang == "am":
        welcome_text = f"ሰላም ውድ {user_name}! እንኳን ወደ sedoo የፍቅር ቤተሰቦች ቦት በሰላም መጡ! 🙏✨\n\nከታች ካሉት ማራኪ አማራጮች የሚፈልጉትን ይምረጡ፦"
    else:
        welcome_text = f"Hello dear {user_name}! Welcome to sedoo's Family Bot! 🙏✨\n\nPlease choose an option from below:"
        
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu(user_id))

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
    lang = user_languages.get(user_id, "am")
    text = f"ሰላም ውድ {call.from_user.first_name or 'ወዳጄ'}! እንኳን ወደ sedoo የፍቅር ቤተሰቦች ቦት በሰላም መጡ! 🙏✨\n\nከታች ካሉት ማራኪ አማራጮች የሚፈልጉትን ይምረጡ፦" if lang == "am" else f"Hello dear {call.from_user.first_name or 'dear'}! Welcome to sedoo's Family Bot! 🙏✨\n\nPlease choose an option:"
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=get_main_menu(user_id))

@bot.callback_query_handler(func=lambda call: call.data == 'group_feedback')
def handle_group_feedback(call):
    bot.answer_callback_query(call.id, "አስተያየትዎ ስለተሰጠን እናመሰግናለን! 🙏", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == 'feedback_prompt')
def feedback_prompt_handler(call):
    user_id = call.from_user.id
    admin_states[user_id] = 'waiting_for_feedback'
    bot.answer_callback_query(call.id, "✍️ አስተያየትዎን ይጻፉ")
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⬅️ ወደ ዋና ገጽ ተመለስ", callback_data="back_to_main"))
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="✍️ **እባክዎ የሚፈልጉትን አስተያየት ከታች በቀጥታ ይጻፉልን (ጽሁፍ፣ ፎቶ ወይም ድምፅ ልከው መላክ ይችላሉ):**",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data in ['add_user', 'list_users', 'user_stats', 'broadcast_menu'])
def handle_user_management_buttons(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "⚠️ ይህ መብት ያለው ለአድሚን ብቻ ነው!")
        return
        
    if call.data == 'add_user':
        admin_states[ADMIN_ID] = 'waiting_to_add'
        bot.answer_callback_query(call.id, "➕ ተጠቃሚ የመጨመሪያ ተግባር")
        bot.send_message(call.message.chat.id, "✍️ ለመጨመር የፈለጉትን የተጠቃሚ 🆔 (ID) ብቻውን ይላኩላቸው:")
        
    elif call.data == 'list_users':
        bot.answer_callback_query(call.id, "👥 የተጠቃሚዎች ዝርዝር እየተዘጋጀ ነው...")
        total_count = len(active_users)
        if total_count == 0:
            bot.send_message(call.message.chat.id, "⚠️ እስካሁን የተመዘገበ ተጠቃሚ የለም።")
            return
        
        users_keyboard = InlineKeyboardMarkup(row_width=1)
        for uid, name in active_users.items():
            users_keyboard.add(
                InlineKeyboardButton(f"❌ {name} ({uid}) - አስወግድ", callback_data=f"del_user_{uid}")
            )
        
        bot.send_message(
            call.message.chat.id, 
            f"👥 **አጠቃላይ ተጠቃሚዎች ብዛት:** {total_count}\n\n👇 ከዚህ በታች ከሚገኙት ስሞች ውስጥ ማስወገድ የሚፈልጉትን ይጫኑ፦", 
            reply_markup=users_keyboard, 
            parse_mode="Markdown"
        )
        
    elif call.data == 'user_stats':
        bot.answer_callback_query(call.id, "📊 ከፍተኛ ተጠቃሚዎች (Top 10) በደረጃ እየተሰላ ነው...")
        total_interactions = sum(user_interaction_counts.values())
        
        if total_interactions == 0 or len(active_users) == 0:
            bot.send_message(call.message.chat.id, "⚠️ እስካሁን የተመዘገበ የቦት አጠቃቀም መረጃ (Activity) የለም።")
            return
            
        sorted_users = sorted(user_interaction_counts.items(), key=lambda x: x[1], reverse=True)
        top_10_users = sorted_users[:10]
        
        stats_text = "📊 **ቦቱን በንቃት የሚጠቀሙ ከፍተኛ ተጠቃሚዎች ደረጃ (Top 10)**\n\n"
        stats_text += f"📌 **አጠቃላይ መስተጋብሮች (Total Hits):** {total_interactions}\n\n"
        
        rank = 1
        for uid, count in top_10_users:
            name = active_users.get(uid, "ያልታወቀ ተጠቃሚ")
            percentage = (count / total_interactions) * 100
            stats_text += f"ውድ **{name}** ({rank}ኛ) ፦ **{count} ጊዜ** ({percentage:.1f}%)\n"
            rank += 1
            
        bot.send_message(call.message.chat.id, stats_text, parse_mode="Markdown")
        
    elif call.data == 'broadcast_menu':
        admin_states[ADMIN_ID] = 'waiting_for_broadcast'
        bot.answer_callback_query(call.id, "📢 ማስታወቂያ መላኪያ")
        bot.send_message(
            call.message.chat.id, 
            "📢 **ለተጠቃሚዎች በሙሉ የሚተላለፍ ማስታወቂያ አሁን ይላኩላቸው:**"
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith('del_user_'))
def handle_inline_delete_user(call):
    if call.from_user.id != ADMIN_ID:
        return
    target_id = int(call.data.split('_')[2])
    if target_id in active_users:
        removed_name = active_users.pop(target_id)
        if target_id in user_interaction_counts:
            del user_interaction_counts[target_id]
        bot.answer_callback_query(call.id, f"✅ ተወግዷል!")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"🗑️ **ተጠቃሚው ተወግዷል!** ID: `{target_id}`",
            parse_mode="Markdown"
        )

@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID, content_types=['text', 'photo', 'video', 'document', 'audio', 'voice'])
def process_admin_inputs(message):
    state = admin_states.get(ADMIN_ID)
    if state == 'waiting_to_add' and message.text and message.text.isdigit():
        target_id = int(message.text)
        active_users[target_id] = "በአድሚን የተጨመረ"
        user_interaction_counts[target_id] = 0
        bot.reply_to(message, f"✅ ተጠቃሚ (ID: {target_id}) በተሳካ ሁኔታ ተጨመረ!")
        admin_states[ADMIN_ID] = None
        return
    elif state == 'waiting_for_broadcast':
        success, fail = 0, 0
        bot.reply_to(message, "⏳ ማስታወቂያው በመላክ ላይ ነው...")
        for uid in active_users.keys():
            if uid == ADMIN_ID:
                continue
            try:
                bot.copy_message(chat_id=uid, from_chat_id=message.chat.id, message_id=message.message_id)
                success += 1
            except Exception:
                fail += 1
        bot.send_message(ADMIN_ID, f"✅ **ተጠናቋል!**\nደረሰላቸው: {success}\nያልደረሰባቸው: {fail}")
        admin_states[ADMIN_ID] = None
        return

@bot.message_handler(func=lambda message: admin_states.get(message.from_user.id) == 'waiting_for_feedback', content_types=['text', 'photo', 'video', 'document', 'audio', 'voice'])
def receive_user_feedback(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "ስም አልባ"
    bot.reply_to(message, "አስተያየትዎ ስለሰጡን ከልብ እናመሰግናለን! 🙏")
    try:
        bot.send_message(ADMIN_ID, f"📩 **አዲስ አስተያየት ደርሷል!**\n• ከተጠቃሚ: {user_name}\n• ID: `{user_id}`", parse_mode="Markdown")
        bot.copy_message(chat_id=ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        print(e)
    admin_states[user_id] = None

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
                "🔔 **አዲስ ፖስት ቻናል ላይ ተለቀቀ!**\n\n❓ ይህንን ፋይል የየትኛው ምድብ ላይ ማከማቸት ይፈልጋሉ?",
                reply_markup=keyboard
            )
        except Exception as e:
            print(e)

@bot.edited_channel_post_handler(content_types=['document', 'audio', 'video', 'photo', 'text', 'voice'])
def handle_edited_channel_post(message):
    handle_channel_post(message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('ch_save_'))
def save_channel_file(call):
    data_parts = call.data.split('_')
    category = data_parts[2]
    msg_id = int(data_parts[3])
    
    # ድግግሞሽ እንዳይኖር ማረጋገጥ
    exists = any(item['message_id'] == msg_id for item in stored_files[category])
    if not exists:
        stored_files[category].append({
            "from_chat_id": CHANNEL_ID,
            "message_id": msg_id
        })
    
    bot.answer_callback_query(call.id, "✅ ፋይሉ በትክክል ተከማችቷል!")
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"✅ የቻናሉ ፖስት በተሳካ ሁኔታ በ **{category}** ምድብ ስር ተቀምጧል! 🚀"
    )

# ----------------- ተጠቃሚዎች ምድብ/ፋይል ሲፈልጉ -----------------
@bot.callback_query_handler(func=lambda call: call.data.startswith('view_'))
def user_view_category(call):
    user_id = call.from_user.id
    user_interaction_counts[user_id] = user_interaction_counts.get(user_id, 0) + 1
    
    category = call.data.split('_')[1]
    items = stored_files.get(category, [])
    
    back_markup = InlineKeyboardMarkup()
    back_markup.add(InlineKeyboardButton("⬅️ ወደ ዋና ገጽ ተመለስ", callback_data="back_to_main"))

    if not items:
        bot.answer_callback_query(call.id, "⚠️ በዚህ ምድብ ስር እስካሁን የተለቀቀ ፋይል የለም።")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="⚠️ ይቅርታ፣ በዚህ ምድብ ውስጥ እስካሁን የተጨመረ ፋይል አልተገኘም 🙏",
            reply_markup=back_markup
        )
        return
    
    bot.answer_callback_query(call.id, f"📂 የ{category} ዝርዝር እየተላከ ነው...")
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"📂 **የተመረጠው ምድብ ({category}) ፋይሎች፦**",
        reply_markup=back_markup,
        parse_mode="Markdown"
    )
    
    for item in items:
        try:
            bot.copy_message(
                chat_id=call.message.chat.id,
                from_chat_id=item["from_chat_id"],
                message_id=item["message_id"]
            )
        except Exception as e:
            print(e)

if __name__ == "__main__":
    print("ቦቱ በመጀመር ላይ ነው...")
    bot.infinity_polling()
