from flask import Flask, render_template, jsonify
import feedparser, datetime, os, urllib.request, ssl

app = Flask(__name__)

# Fonti RSS Arezzo
RSS_FEEDS = ["https://www.arezzonotizie.it/rss", "https://www.lanazione.it/arezzo/rss"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/updates')
def get_updates():
    news_list = []
    # Bypass SSL per evitare blocchi certificati sui server cloud
    context = ssl._create_unverified_context()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for url in RSS_FEEDS:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=context, timeout=8) as response:
                feed = feedparser.parse(response.read())
                for entry in feed.entries[:8]:
                    news_list.append({
                        "fonte": "CRONACA", 
                        "titolo": entry.title.upper()
                    })
        except Exception as e:
            print(f"Errore feed: {e}")
            continue
    
    if not news_list:
        news_list = [{"fonte": "SISTEMA", "titolo": "MONITORAGGIO ATTIVO - IN ATTESA DI NUOVI DATI"}]

    social_data = [
        {"tipo": "WHATSAPP", "comune": "AREZZO OLMO", "testo": "Segnalata auto sospetta vicino scuole.", "data_ora": "2 MIN FA", "link": "https://web.whatsapp.com/"},
        {"tipo": "TELEGRAM", "comune": "VALDARNO", "testo": "Tentativo di furto a Terranuova.", "data_ora": "15 MIN FA", "link": "https://t.me/s/ArezzoNotizie"},
        {"tipo": "FACEBOOK", "comune": "SOS VALDICHIANA", "testo": "Targhe rubate segnalate in zona.", "data_ora": "25 MIN FA", "link": "https://www.facebook.com/"}
    ]

    stats_data = [
        {"label": "MONTEVARCHI (A1)", "valore": 9.8},
        {"label": "CORTONA (SR71)", "valore": 9.5},
        {"label": "CIVITELLA", "valore": 9.2}
    ]

    return jsonify({"ticker_news": news_list, "social_feed": social_data, "stats": stats_data})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
