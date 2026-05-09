import os
import requests
import schedule
import time
from datetime import datetime

BOT_TOKEN  = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "@ISLLAM1123")
SEND_TIME  = os.environ.get("SEND_TIME", "04:00")

API_URL = "https://eldwanapp.jeeteak.com/api/prayer-times"
HEADERS = {
    "Host": "eldwanapp.jeeteak.com",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "ar,en;q=0.9",
}

PRAYERS = {
    "fajr":    "🌙 الفجر",
    "dhuhr":   "☀️ الظهر",
    "asr":     "🌤️ العصر",
    "maghrib": "🌅 المغرب",
    "isha":    "🌃 العشاء",
}

def fetch_prayer_times():
    res = requests.get(API_URL, headers=HEADERS, timeout=15)
    res.raise_for_status()
    data = res.json()
    if data.get("success"):
        return data["data"]
    raise Exception("فشل جلب المواقيت")

def format_message(data):
    lines = [
        f"🕌 *مواقيت الصلاة ليوم {data['date']}*",
        f"{'─' * 28}",
    ]
    for key, name in PRAYERS.items():
        lines.append(f"  {name} :  `{data[key]}`")
    lines.append(f"{'─' * 28}")
    lines.append("_تحديث تلقائي من ديوان الوقف السني_ 🇮🇶")
    return "\n".join(lines)

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown",
    }
    res = requests.post(url, json=payload, timeout=15)
    res.raise_for_status()
    return res.json()

def job():
    print(f"\n⏰ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] جاري الإرسال...")
    try:
        data = fetch_prayer_times()
        message = format_message(data)
        send_to_telegram(message)
        print("✅ تم الإرسال بنجاح!")
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    print(f"🤖 بوت مواقيت الصلاة | القناة: {CHANNEL_ID} | وقت الإرسال: {SEND_TIME}")
    job()
    schedule.every().day.at(SEND_TIME).do(job)
    while True:
        schedule.run_pending()
        time.sleep(30)
