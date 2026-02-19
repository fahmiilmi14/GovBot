import os
import requests
from groq import Groq

# Ambil API Key dari Environment Variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def get_funny_motivation():
    """Mengambil kutipan motivasi lucu ala anak IT dari AI"""
    prompt = (
        "Berikan satu kalimat motivasi yang sangat lucu, sarkas, dan 'relatable' "
        "pokoknya lucu gak harus satu kalimat kok"
        "Gunakan bahasa gaul anak muda Indonesia."
    )
    
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8 # Sedikit lebih tinggi biar makin kreatif/ngaco
        )
        return completion.choices[0].message.content
    except Exception as e:
        return "Tetap semangat! Ingat, error itu seni, yang nggak seni itu kalau kamu menyerah sebelum 'commit'."

def send_telegram(message):
    """Mengirim pesan ke Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID, 
        "text": message, 
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Gagal kirim Telegram: {e}")

def main():
    # Header pesan
    greeting = "✨ *Mood Booster Hari Ini* ✨\n\n"
    
    # Ambil motivasi dari AI
    motivation = get_funny_motivation()
    
    # Gabungkan dan kirim
    full_message = f"{greeting}{motivation}\n\n🚀 _Keep debugging, keep praying!_"
    send_telegram(full_message)

if __name__ == "__main__":
    main()
