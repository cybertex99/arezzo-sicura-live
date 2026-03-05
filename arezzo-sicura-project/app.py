from flask import Flask, render_template, jsonify
import feedparser
import datetime
import os
import urllib.request

app = Flask(__name__)

RSS_FEEDS = [
    "https://www.arezzonotizie.it/rss",
    "https://www.lanazione.it/arezzo/rss",
    "https://www.corrierediarezzo.it/rss",
    "https://www.arezzo24.it/feed",
    "https://valdarnopost.it/feed/",
    "https://www.casentino2000.it/feed/",
    "https://www.teverepost.it/feed/"
]

@app.route('/')
def index():
    return render_template('index.html', data_oggi=datetime.datetime.now().strftime("%d/%m/%Y"))

@app.route('/api/updates')
def get_updates():
    news_list = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for url in RSS_FEEDS:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read()
                feed = feedparser.parse(content)
                for entry in feed.entries[:5]:
                    fn = feed.feed.title.split('-')[0].strip() if 'title' in feed.feed else "News"
                    news_list.append({"fonte": fn, "titolo": entry.title})
        except: continue

    # SOCIAL DATA CON COORDINATE PER MAPPA
    social_data = [
        {"tipo": "ALERT", "comune": "Arezzo Centro", "testo": "Vie di fuga monitorate: SR71 fluida.", "lat": 43.463, "lon": 11.878, "colore": "#ffffff"},
        {"tipo": "TRAFFICO", "comune": "Pescaiola", "testo": "Rallentamenti via Dante. Svincolo consigliato: via Galvani.", "lat": 43.455, "lon": 11.865, "colore": "#ffcc00"}
    ]

    stats_data = [
        {"label": "Indice Affollamento Arezzo", "valore": 4.5, "color": "#00ff00"},
        {"label": "Rischio Logistico Valdarno", "valore": 8.2, "color": "#ff3b3b"}
    ]

    return jsonify({"ticker_news": news_list, "social_feed": social_data, "stats": stats_data})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
