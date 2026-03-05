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
    return render_template('index.html', data_oggi=datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))

@app.route('/api/updates')
def get_updates():
    news_list = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    keywords = ["furto", "rapina", "ladri", "rubato", "spaccata", "sicurezza"]

    for url in RSS_FEEDS:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                feed = feedparser.parse(response.read())
                for entry in feed.entries:
                    # Filtro per parole chiave legate ai furti
                    if any(key in entry.title.lower() or key in entry.summary.lower() for key in keywords):
                        fn = feed.feed.title.split('-')[0].strip() if 'title' in feed.feed else "News"
                        news_list.append({"fonte": fn, "titolo": entry.title.upper()})
        except: continue

    # SOCIAL DATA con Date (anche di ieri)
    ieri = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%d/%m")
    oggi = datetime.datetime.now().strftime("%d/%m")

    social_data = [
        {"tipo": "X", "comune": "Arezzo", "ora": f"{oggi} 14:20", "testo": "Segnalata auto sospetta vicino a villette zona Giotto. Possibile sopralluogo ladri.", "lat": 43.461, "lon": 11.882, "colore": "#ffffff"},
        {"tipo": "FB", "comune": "Montevarchi", "ora": f"{ieri} 22:15", "testo": "Furto in appartamento via Roma. Rubati gioielli e contanti. Forze ordine sul posto.", "lat": 43.523, "lon": 11.567, "colore": "#1877F2"},
        {"tipo": "TG", "comune": "Cortona", "ora": f"{ieri} 19:30", "testo": "Tentata rapina presso stazione di servizio. Malviventi fuggiti verso Perugia.", "lat": 43.275, "lon": 11.985, "colore": "#0088cc"}
    ]

    # VIE DI FUGA (Statistiche)
    stats_data = [
        {"label": "SR71 (DIREZIONE SUD)", "valore": 8.5, "status": "OTTIMA"},
        {"label": "E45 (SANSEPOLCRO)", "valore": 4.2, "status": "RALLENTATA"},
        {"label": "A1 (AREZZO-V_DARNO)", "valore": 9.1, "status": "LIBERA"},
        {"label": "VALDICHIANA (INTERNE)", "valore": 6.5, "status": "DISCRETA"}
    ]

    return jsonify({"ticker_news": news_list, "social_feed": social_data, "stats": stats_data})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
