import os
import requests
from groq import Groq

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def get_funny_motivation():
    prompt = (
        "Berikan satu kalimat motivasi yang sangat lucu, sarkas, dan 'relatable' "
        "untuk orang yang lagi malas atau capek. Gunakan bahasa gaul Indonesia yang santai."
    )
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return "Tetap semangat! Ingat, rebahan itu perlu, tapi bayar tagihan itu fardu."

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID, 
        "text": message, 
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except:
        pass

def main():
    motivation = get_funny_motivation()
    full_message = f"✨ *Mood Booster Hari Ini* ✨\n\n{motivation}\n\n🚀 _Keep moving, keep smiling!_"
    send_telegram(full_message)

if __name__ == "__main__":
    main()
