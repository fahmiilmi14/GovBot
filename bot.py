import os
import requests
import datetime
import pytz
from groq import Groq

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
CITY = "Surabaya"
COUNTRY = "Indonesia"

client = Groq(api_key=GROQ_API_KEY)

def get_ai_response(prompt):
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return completion.choices[0].message.content
    except:
        return "Selamat menunaikan ibadah sholat, semoga berkah."

def get_prayer_times():
    url = f"http://api.aladhan.com/v1/timingsByCity?city={CITY}&country={COUNTRY}&method=2"
    response = requests.get(url).json()
    return response['data']['timings']

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def main():
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    current_time = now.strftime("%H:%M")
    
    timings = get_prayer_times()
    prayers = {
        "Fajr": "Subuh",
        "Dhuhr": "Dzuhur",
        "Asr": "Ashar",
        "Maghrib": "Maghrib",
        "Isha": "Isya"
    }

    for key, name in prayers.items():
        prayer_time = timings[key]
        if current_time == prayer_time:
            prompt = f"Berikan satu kalimat singkat pengingat sholat {name} yang keren untuk mahasiswa teknik informatika."
            ai_msg = get_ai_response(prompt)
            pesan = f"🔔 *Waktunya Sholat {name}!*\n⌚ {prayer_time} WIB\n\n{ai_msg}"
            send_telegram(pesan)
            break

if __name__ == "__main__":
    main()
  
