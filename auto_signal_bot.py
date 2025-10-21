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
    data = request.json

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
⚙️ *Source:* TradingView  
"""
        send_to_telegram(message)
        return {"status": "success", "message": "Signal sent to Telegram!"}, 200
    else:
        return {"status": "error", "message": "No signal key found"}, 400


# --- Start the Flask server ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

