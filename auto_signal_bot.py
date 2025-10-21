import requests
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

# --- Telegram Bot details ---
BOT_TOKEN = "8293039835:AAH2sLDHfPEWS7fQZY66LkeS-MWDzss9uJw"
CHAT_ID = "7939950441"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


# --- Function to send message to Telegram ---
def send_to_telegram(message):
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    response = requests.post(TELEGRAM_URL, data=payload)
    print(response.json())


# --- Route to receive webhook from TradingView ---
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data:
        return {"status": "error", "message": "No data received"}, 400

    signal = data.get('signal')
    pair = data.get('pair', 'Unknown Pair')

    if signal:
        # Get current time in readable format
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Build fancy message
        emoji = "🔼" if signal.lower() == "buy" else "🔽"
        message = f"""
{emoji} *{signal.upper()} SIGNAL*
💰 *Pair:* {pair}
🕒 *Time:* {now}
📊 *Source:* TradingView
"""
        send_to_telegram(message)
        return {"status": "success", "message": "Signal sent to Telegram"}, 200
    else:
        return {"status": "error", "message": "No signal found"}, 400


# --- Route to handle Telegram messages ---
@app.route('/', methods=['POST'])
def telegram_webhook():
    data = request.get_json()

    if not data or "message" not in data:
        return {"status": "error", "message": "No message data"}, 400

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "").lower()

    # Simple replies
    if text == "/start":
        message = "Hello Yahya 👋, your trading bot is active and connected!"
    elif "hi" in text or "hello" in text:
        message = "Hey Yahya! The bot is running perfectly on Render 🚀"
    else:
        message = f"You said: {text}"

    payload = {"chat_id": chat_id, "text": message}
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data=payload)

    return {"ok": True}, 200


# --- Route to test bot from browser ---
@app.route('/', methods=['GET'])
def home():
    return "✅ Yahya's Trading Bot is Live and Ready!", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)


