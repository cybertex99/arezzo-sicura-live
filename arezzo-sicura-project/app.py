from flask import Flask, render_template, jsonify
import feedparser
import datetime
import os
import urllib.request

app = Flask(__name__)

RSS_FEEDS = [
    "https://www.arezzonotizie.it/rss",
    "https://www.lanazione.it/arezzo/rss",
    "https://www.corrierediarezzo.it/rss"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/updates')
def get_updates():
    # FILTRO NOTIZIE
    news_list = []
    keywords = ["furto", "rapina", "ladri", "sicurezza", "fuga"]
    headers = {'User-Agent': 'Mozilla/5.0'}

    for url in RSS_FEEDS:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                feed = feedparser.parse(response.read())
                for entry in feed.entries[:3]:
                    if any(k in entry.title.lower() for k in keywords):
                        news_list.append({"fonte": "NEWS", "titolo": entry.title.upper()})
        except: continue

    # SOCIAL STREAM (Come da immagine)
    social_data = [
        {"tipo": "WA", "comune": "Sicurezza Olmo", "testo": "Auto sospetta AR... segnalata.", "data_ora": "1 min fa"},
        {"tipo": "TG", "comune": "@ControlloVicinato_Ar", "testo": "Furgone bianco via Romana.", "data_ora": "3 min fa"},
        {"tipo": "X", "comune": "@ArezzoCronaca", "testo": "Inseguimento SR71...", "data_ora": "5 min fa"}
    ]

    # STATS (Top 5 Rischio)
    stats_data = [
        {"label": "Montevarchi", "valore": 9.8},
        {"label": "Cortona", "valore": 9.5},
        {"label": "Civitella", "valore": 9.2},
        {"label": "Lucignano", "valore": 8.9},
        {"label": "Castiglion F.", "valore": 8.6}
    ]

    return jsonify({
        "ticker_news": news_list if news_list else [{"fonte": "INFO", "titolo": "MONITORAGGIO ATTIVO"}],
        "social_feed": social_data,
        "stats": stats_data
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
