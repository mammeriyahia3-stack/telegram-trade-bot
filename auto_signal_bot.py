import requests

# --- Your bot details ---
BOT_TOKEN = "8293039835:AAH2sLDHfPEWS7fQZY66LkeS-MWdzss9uJw"
CHAT_ID = "7939950441"

# --- Your message ---
MESSAGE = "🚀 Hello Yahya! Your trading bot is now connected and ready to send signals!"

# --- Send message ---
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": MESSAGE
}

try:
    response = requests.post(url, data=payload)
    print("✅ Message sent successfully!")
    print(response.json())  # Show Telegram's response
except Exception as e:
    print("❌ Failed to send message:", e)


  
