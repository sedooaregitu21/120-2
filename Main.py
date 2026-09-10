import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '8893936599:AAEjIqkOGYpTt5CPuHrQ_4CwnFUSzgFawbY'
ADMIN_ID = 8609938129  # የአድሚን ቴሌግራም User ID
CHANNEL_ID = -1003794082614  # የቻናልህ ትክክለኛ ቁጥር ID

bot = telebot.TeleBot(TOKEN)

user_languages = {}
admin_states = {}

# የተጠቃሚዎችን መረጃ (User ID እና Name) እንዲሁም ቦቱን ስንት ጊዜ እንደተጠቀሙ (የመጠቀም ብዛት/Count) ለመያዝ
active_users = {}
user_interaction_counts = {}  # 🔑 አዲስ: እያንዳንዱ ተጠቃሚ ቦቱን ስንት ጊዜ እንደተጠቀመ ይመዝግበታል

# የሰፈሩ መዝሙሮች እና ግጥሞቻቸው (አንድ አይነት ስም/ቁልፍ ያላቸው)
hymns_data = {
    "hymn_1": {
        "title": "እግዚአብሔር ይመስገን",
        "audio_msg_id": 123,  # ከቻናል የሚመጣው የኦዲዮ ፋይል ID
        "from_chat_id": CHANNEL_ID,
        "lyrics": "🎵 እግዚአብሔር ይመስገን፣ ስሙ የተባረከ ይሁን...\nሁሉን በሰዓቱ የሚያደርግ አምላክ ክብር ይገባው..."
    },
    "hymn_2": {
        "title": "ሰላም ላንቺ ይሁን",
        "audio_msg_id": 124,
        "from_chat_id": CHANNEL_ID,
        "lyrics": "🎵 ሰላም ላንቺ ይሁን እመ ብርሃን ቅድስት ድንግል...\nየሰማይና የምድር ንግሥት..."
    }
}

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
                InlineKeyboardButton("👥 ተጠቃሚዎች ዝርዝር", callback_data="list_users"),
                InlineKeyboardButton("📊 የተጠቃሚዎች ድግግሞሽ (Stats)", callback_data="user_stats"), # 🔑 አዲስ ስታቲስቲክስ ቁልፍ
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
                InlineKeyboardButton("👥 Users List", callback_data="list_users"),
                InlineKeyboardButton("📊 User Stats", callback_data="user_stats"),
                InlineKeyboardButton("📢 Send Broadcast", callback_data="broadcast_menu")
            )
        
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "ወዳጄ"
    
    # ተጠቃሚውን በዝርዝር ውስጥ እንመዘግባለን
    active_users[user_id] = user_name
    
    # 🔑 የተጠቃሚን የመጠቀም ድግግሞሽ (Interaction Count) እንመዝግባለን/እንጨምራለን
    user_interaction_counts[user_id] = user_interaction_counts.get(user_id, 0) + 1
    
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

# ----------------- የአድሚን ተጠቃሚ አስተዳደር፣ ስታቲስቲክስ እና ማስታወቂያ (Broadcast) -----------------
@bot.callback_query_handler(func=lambda call: call.data in ['add_user', 'remove_user', 'list_users', 'user_stats', 'broadcast_menu'])
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
        
    elif call.data == 'user_stats':
        # 🔑 🔑 🔑 እዚህ ጋር ነው እያንዳንዱ ተጠቃሚ በፐርሰንት (%) እና 1ኛ፣ 2ኛ፣ 3ኛ እየተባለ የሚወጣው 
        bot.answer_callback_query(call.id, "📊 የሰዎች የአጠቃቀም ድግግሞሽ እና ፐርሰንት እየተሰላ ነው...")
        
        total_interactions = sum(user_interaction_counts.values())
        
        if total_interactions == 0 or len(active_users) == 0:
            bot.send_message(call.message.chat.id, "⚠️ እስካሁን የተመዘገበ የቦት አጠቃቀም መረጃ (Activity) የለም።")
            return
            
        # ተጠቃሚዎችን ከhighest ወደ lowest አጠቃቀም እንለያቸዋለን (Sorting)
        sorted_users = sorted(user_interaction_counts.items(), key=lambda x: x[1], reverse=True)
        
        stats_text = "📊 **የቦቱ ተጠቃሚዎች የአጠቃቀም ድግግሞሽ እና ፐርሰንት (%)**\n\n"
        stats_text += f"📌 **አጠቃላይ መስተጋብሮች (Total Hits):** {total_interactions}\n\n"
        
        rank = 1
        for uid, count in sorted_users:
            name = active_users.get(uid, "ያልታወቀ ተጠቃሚ")
            # ፐርሰንቱን ማስላት
            percentage = (count / total_interactions) * 100
            
            # ለ 1ኛ፣ 2ኛ፣ 3ኛ ልዩ ምልክቶች እንሰጣለን
            if rank == 1:
                medal = "🥇 1ኛ"
            elif rank == 2:
                medal = "🥈 2ኛ"
            elif rank == 3:
                medal = "🥉 3ኛ"
            else:
                medal = f"▫️ {rank}ኛ"
                
            stats_text += f"{medal} • **{name}** (`{uid}`)\n   └ አጠቃቀም: **{count} ጊዜ** ({percentage:.1f}%)\n\n"
            rank += 1
            
        bot.send_message(call.message.chat.id, stats_text, parse_mode="Markdown")
        
    elif call.data == 'broadcast_menu':
        admin_states[ADMIN_ID] = 'waiting_for_broadcast'
        bot.answer_callback_query(call.id, "📢 ማስታወቂያ መላኪያ")
        bot.send_message(
            call.message.chat.id, 
            "📢 **ለተጠቃሚዎች በሙሉ የሚተላለፍ ማስታወቂያ (ጽሑፍ፣ ፎቶ ወይም ቪዲዮ) አሁን ይላኩላቸው:**\n\n(ያስተላልፉ የሚለውን መልእክት በቀጥታ እዚህ ቻት ላይ ጻፉ ወይም ፎቶ ፕቴ አድርጉ)"
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
        if target_id in user_interaction_counts:
            del user_interaction_counts[target_id]
            
        bot.answer_callback_query(call.id, f"✅ {removed_name} ከዝርዝር ውጪ ሆኗል!")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"🗑️ **ተጠቃሚው ተወግዷል!**\n• ስም: {removed_name}\n• ID: `{target_id}`",
            parse_mode="Markdown"
        )
    else:
        bot.answer_callback_query(call.id, "⚠️ ተጠቃሚው በዝርዝር ውስጥ አልተገኘም!")

# አድሚኑ ቁጥር ብቻ ሲልክ (Add ወይም Remove) ወይም ማስታወቂያ ጽሁፍ/ሚዲያ ሲልክ
@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID, content_types=['text', 'photo', 'video', 'document', 'audio', 'voice'])
def process_admin_inputs(message):
    state = admin_states.get(ADMIN_ID)
    
    # 1. ተጠቃሚ ለመጨመር ቁጥር ሲልክ
    if state == 'waiting_to_add' and message.text and message.text.isdigit():
        target_id = int(message.text)
        active_users[target_id] = "በአድሚን የተጨመረ"
        user_interaction_counts[target_id] = user_interaction_counts.get(target_id, 0)
        bot.reply_to(message, f"✅ ተጠቃሚ (ID: {target_id}) በተሳካ ሁኔታ ተጨመረ!")
        admin_states[ADMIN_ID] = None
        return
        
    # 2. ተጠቃሚ ለማስወገድ ቁጥር ሲልክ
    elif state == 'waiting_to_remove' and message.text and message.text.isdigit():
        target_id = int(message.text)
        if target_id in active_users:
            del active_users[target_id]
            if target_id in user_interaction_counts:
                del user_interaction_counts[target_id]
            bot.reply_to(message, f"🗑️ ተጠቃሚ (ID: {target_id}) ከዝርዝሩ ውጪ ሆኗል (Rejected)!")
        else:
            bot.reply_to(message, f"⚠️ ተጠቃሚ (ID: {target_id}) በዝርዝር ውስጥ አልተገኘምም።")
        admin_states[ADMIN_ID] = None
        return
        
    # 3. ማስታወቂያ (Broadcast) በጅምላ ለመላክ ሲልክ
    elif state == 'waiting_for_broadcast':
        success, fail = 0, 0
        bot.reply_to(message, "⏳ ማስታወቂያው ለተጠቃሚዎች በመላክ ላይ ነው፣ እባክዎ ትንሽ ይጠብቁ...")
        
        for uid in active_users.keys():
            if uid == ADMIN_ID:
                continue
            try:
                bot.copy_message(chat_id=uid, from_chat_id=message.chat.id, message_id=message.message_id)
                success += 1
            except Exception as e:
                print(f"ለ {uid} መላክ አልቻለም: {e}")
                fail += 1
                
        bot.send_message(ADMIN_ID, f"✅ **ማስታወቂያው በተሳካ ሁኔታ ተጠናቋል!**\n\n• የደረሰላቸው: {success}\n• ያልደረሰባቸው: {fail}")
        admin_states[ADMIN_ID] = None
        return

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

# ----------------- ተጠቃሚዎች ምድብ/ፋይል ሲፈልጉ -----------------
@bot.callback_query_handler(func=lambda call: call.data.startswith('view_'))
def user_view_category(call):
    user_id = call.from_user.id
    # ተጠቃሚው ምድብ ሲመርጥ ድግግሞሹን እንጨምራለን
    user_interaction_counts[user_id] = user_interaction_counts.get(user_id, 0) + 1
    
    category = call.data.split('_')[1]
    
    # ልዩ ጉዳይ ለአውዲዮ/መዝሙር (በስም እና ከታች ግጥም እንዲኖረው ከተፈለገ)
    if category == "audio":
        markup = InlineKeyboardMarkup()
        for key, hymn in hymns_data.items():
            markup.add(InlineKeyboardButton(f"🎧 {hymn['title']}", callback_data=f"play_{key}"))
        
        markup.add(InlineKeyboardButton("⬅️ ወደ ዋናው ምናሌ ተመለስ", callback_data="back_to_main"))
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🎧 **እባክዎ ማዳመጥ የሚፈልጉትን መዝሙር ይምረጡ፦**",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return

    items = stored_files.get(category, [])
    
    if not items:
        bot.answer_callback_query(call.id, "⚠️ በዚህ ምድብ ስር እስካሁን የተለቀቀ ፋይል የለም።")
        back_markup = InlineKeyboardMarkup()
        back_markup.add(InlineKeyboardButton("⬅️ ወደ ዋናው ምናሌ ተመለስ", callback_data="back_to_main"))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="⚠️ ይቅርታ፣ በዚህ ምድብ ውስጥ እስካሁን የተጨመረ ፋይል አልተገኘምም 🙏",
            reply_markup=back_markup
        )
        return
    
    bot.answer_callback_query(call.id, f"📂 የ{category} ዝርዝር እየተላከ ነው...")
    
    back_markup = InlineKeyboardMarkup()
    back_markup.add(InlineKeyboardButton("⬅️ ወደ ዋናው ምናሌ ተመለስ", callback_data="back_to_main"))
    
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
            print(f"ፋይል መላክ አልቻለም: {e}")

# ----------------- መዝሙር መምረጫ እና ግጥም ማሳያ -----------------
@bot.callback_query_handler(func=lambda call: call.data.startswith('play_'))
def play_selected_hymn(call):
    user_id = call.from_user.id
    user_interaction_counts[user_id] = user_interaction_counts.get(user_id, 0) + 1
    
    hymn_key = call.data.split('_', 1)[1]
    hymn = hymns_data.get(hymn_key)
    
    if not hymn:
        bot.answer_callback_query(call.id, "⚠️ መዝሙሩ አልተገኘም!")
        return

    bot.answer_callback_query(call.id, f"🎶 '{hymn['title']}' እየተጫነ ነው...")
    
    try:
        bot.copy_message(
            chat_id=call.message.chat.id,
            from_chat_id=hymn["from_chat_id"],
            message_id=hymn["audio_msg_id"]
        )
    except Exception as e:
        print(f"ኦዲዮ መላክ አልቻለም: {e}")

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📜 ግጥሙን (Lyrics) አሳይ", callback_data=f"lyrics_{hymn_key}"))
    markup.add(InlineKeyboardButton("🎧 ወደ መዝሙር ዝርዝር ተመለስ", callback_data="view_audio"))

    bot.send_message(
        chat_id=call.message.chat.id,
        text=f"🎵 **{hymn['title']}**\n\nማጀቢያ ግጥም ማየት ከፈለጉ ከታች ያለውን ቁልፍ ይጫኑ።",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('lyrics_'))
def show_lyrics(call):
    user_id = call.from_user.id
    user_interaction_counts[user_id] = user_interaction_counts.get(user_id, 0) + 1
    
    hymn_key = call.data.split('_', 1)[1]
    hymn = hymns_data.get(hymn_key)
    
    if not hymn:
        bot.answer_callback_query(call.id, "⚠️ ግጥሙ አልተገኘም!")
        return

    bot.answer_callback_query(call.id, "📜 ግጥሙ ተጭኗል")
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🎧 ወደ መዝሙር ዝርዝር ተመለስ", callback_data="view_audio"))
    markup.add(InlineKeyboardButton("⬅️ ወደ ዋናው ምናሌ ተመለስ", callback_data="back_to_main"))

    bot.send_message(
        chat_id=call.message.chat.id,
        text=f"📜 **የ{hymn['title']} ግጥም፦**\n\n{hymn['lyrics']}",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_main')
def back_to_main_menu(call):
    user_id = call.from_user.id
    markup = get_main_menu(user_id)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🙏 ወደ ዋናው ምናሌ ተመልሰዋል፦\n\nከታች ካሉት አማራጮች የሚፈልጉትን ይምረጡ፦",
        reply_markup=markup,
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    print("ቦቱ በመጀመር ላይ ነው...")
    bot.infinity_polling()
