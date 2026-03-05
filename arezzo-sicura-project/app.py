from flask import Flask, render_template, jsonify
import feedparser
import datetime
import os

app = Flask(__name__)

# Configurazione Fonti REALI Provincia di Arezzo
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
    # Estrazione News Reali
    news_list = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:8]:  # Limite per fonte per varietà
                news_list.append({
                    "fonte": feed.feed.title.split('-')[0].strip() if 'title' in feed.feed else "NEWS LOCALE",
                    "titolo": entry.title
                })
        except Exception as e:
            print(f"Errore caricamento feed {url}: {e}")

    # Logica Social Reali (Placeholder per integrazione API)
    # Su Render, queste chiamate non verranno bloccate
    social_data = [
        {"tipo": "X", "comune": "Arezzo", "testo": "Segnalazione live: traffico rallentato zona San Donato.", "lat": 43.458, "lon": 11.872, "dest_lat": 43.450, "dest_lon": 11.860, "colore": "#ffffff"},
        {"tipo": "FB", "comune": "San Giovanni V.", "testo": "Post gruppo sicurezza: Avvistamenti sospetti zona Oltrarno.", "lat": 43.564, "lon": 11.532, "dest_lat": 43.570, "dest_lon": 11.540, "colore": "#1877F2"},
        {"tipo": "TG", "comune": "Sansepolcro", "testo": "Allerta meteo locale: attesi temporali forti.", "lat": 43.571, "lon": 12.140, "dest_lat": 43.580, "dest_lon": 12.150, "colore": "#0088cc"}
    ]

    return jsonify({
        "ticker_news": news_list[:50], # Visualizza fino a 50 news reali
        "social_feed": social_data,
        "stats": [
            {"label": "Montevarchi", "valore": 9.8, "color": "#ff3b3b"},
            {"label": "Cortona", "valore": 9.5, "color": "#ff3b3b"},
            {"label": "Sansepolcro", "valore": 8.9, "color": "#ffcc00"},
            {"label": "Bibbiena", "valore": 8.5, "color": "#ffcc00"}
        ]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port
