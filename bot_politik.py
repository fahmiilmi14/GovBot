import os
import requests
from groq import Groq
from tavily import TavilyClient
from datetime import date

hari_ini = date.today().strftime("%d %B %Y")

def get_government_blunder():
    try:
        with open("prompt.md", "r", encoding="utf-8") as f:
            base_prompt = f.read()

        tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        query = "berita blunder kebijakan pemerintah indonesia viral terbaru"
        
        search_result = tavily.search(
            query=query, 
            search_depth="advanced", 
            max_results=5,
            days=2,
            include_domains=["x.com", "twitter.com", "detik.com", "tempo.co", "kompas.com", "cnnindonesia.com"]
        )

        context = ""
        for res in search_result['results']:
            context += f"Judul: {res['title']}\nKonten: {res['content'][:500]}\nURL: {res['url']}\n\n"

        final_prompt = f"{base_prompt}\n\nDATA TERBARU (PASTIKAN KEJADIAN 2026):\n{context}"

        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": final_prompt}]
        )
        report = completion.choices[0].message.content

        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        full_message = f"🚩 **SATU HARI SATU BERITA BODOH DARI PEMERINTAH**\n📅 _{hari_ini}_\n\n{report}"

        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": full_message,
            "parse_mode": "Markdown"
        }

        requests.post(url, json=payload)
        print("Done")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_government_blunder()
