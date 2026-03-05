from flask import Flask, render_template, jsonify
import feedparser
import datetime
import os
import urllib.request

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
    # Invia la data corrente al template per il display in alto a destra
    return render_template('index.html', data_oggi=datetime.datetime.now().strftime("%d/%m/%Y"))

@app.route('/api/updates')
def get_updates():
    news_list = []
    # User-Agent per simulare un browser ed evitare blocchi dai server dei giornali
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for url in RSS_FEEDS:
        try:
            # Creazione della richiesta con headers per bypassare i filtri anti-bot
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read()
                feed = feedparser.parse(content)
                
                # Estraiamo le ultime 5 notizie per ogni fonte
                for entry in feed.entries[:5]:
                    # Pulizia del nome della fonte dal titolo del feed
                    fonte_name = feed.feed.title.split('-')[0].strip() if 'title' in feed.feed else "News Locale"
                    news_list.append({
                        "fonte": fonte_name,
                        "titolo": entry.title
                    })
        except Exception as e:
            # Log dell'errore nella console di Render per debugging
            print(f"Errore caricamento feed {url}: {e}")

    # Dati simulati per Social e Mappa (Placeholder per future API reali)
    social_data = [
        {"tipo": "X", "comune": "Arezzo", "testo": "Segnalazione live: traffico rallentato zona San Donato.", "lat": 43.458, "lon": 11.872, "colore": "#ffffff"},
        {"tipo": "FB", "comune": "San Giovanni V.", "testo": "Post gruppo sicurezza: Avvistamenti sospetti zona Oltrarno.", "lat": 43.564, "lon": 11.532, "colore": "#1877F2"},
        {"tipo": "TG", "comune": "Sansepolcro", "testo": "Allerta meteo locale: attesi temporali forti.", "lat": 43.571, "lon": 12.140, "colore": "#0088cc"}
    ]

    # Statistiche di rischio simulate
    stats_data = [
        {"label": "Montevarchi", "valore": 9.2, "color": "#ff3b3b"},
        {"label": "Cortona", "valore": 8.5, "color": "#ffcc00"},
        {"label": "Sansepolcro", "valore": 7.8, "color": "#ffcc00"},
        {"label": "Bibbiena", "valore": 6.4, "color": "#00ff00"}
    ]

    return jsonify({
        "ticker_news": news_list,
        "social_feed": social_data,
        "stats": stats_data
    })

if __name__ == "__main__":
    # Configurazione per il deploy su Render (usa la porta assegnata dal sistema)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
