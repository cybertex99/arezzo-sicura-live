from flask import Flask, render_template, jsonify
import feedparser
import datetime
import os
import urllib.request
import ssl

app = Flask(__name__)

# Fonti feed RSS Arezzo
RSS_FEEDS = [
    "https://www.arezzonotizie.it/rss",
    "https://www.lanazione.it/arezzo/rss",
    "https://www.corrierediarezzo.it/rss",
    "https://www.arezzo24.it/feed"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/updates')
def get_updates():
    news_list = []
    keywords = ["furto", "rapina", "ladri", "sicurezza", "fuga", "spaccata", "cronaca"]
    context = ssl._create_unverified_context()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36'}

    for url in RSS_FEEDS:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=context, timeout=8) as response:
                feed = feedparser.parse(response.read())
                for entry in feed.entries[:5]:
                    if any(k in entry.title.lower() for k in keywords):
                        fonte = "CRONACA"
                        if "nazione" in url: fonte = "LA NAZIONE"
                        elif "arezzo24" in url: fonte = "AREZZO24"
                        elif "arezzonotizie" in url: fonte = "AREZZO NOTIZIE"
                        news_list.append({"fonte": fonte, "titolo": entry.title.upper()})
        except: continue

    # Social Feed con link cliccabili
    social_data = [
        {"tipo": "WHATSAPP", "comune": "AREZZO OLMO", "testo": "Auto sospetta AR... segnalata.", "data_ora": "2 min fa", "link": "https://web.whatsapp.com/"},
        {"tipo": "TELEGRAM", "comune": "@ControlloVicinato_Ar", "testo": "Furgone bianco via Romana.", "data_ora": "5 min fa", "link": "https://t.me/s/ArezzoNotizie"},
        {"tipo": "X", "comune": "@ArezzoCronaca", "testo": "Inseguimento SR71 in corso.", "data_ora": "10 min fa", "link": "https://twitter.com/search?q=arezzo"}
    ]

    stats_data = [
        {"label": "Montevarchi", "valore": 9.8},
        {"label": "Cortona", "valore": 9.5},
        {"label": "Civitella", "valore": 9.2},
        {"label": "Lucignano", "valore": 8.9},
        {"label": "Castiglion F.", "valore": 8.6}
    ]

    return jsonify({"ticker_news": news_list, "social_feed": social_data, "stats": stats_data})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
