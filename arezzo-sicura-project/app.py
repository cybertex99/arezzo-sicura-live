from flask import Flask, render_template, jsonify
import feedparser, datetime, os, urllib.request, ssl

app = Flask(__name__)

RSS_FEEDS = ["https://www.arezzonotizie.it/rss", "https://www.lanazione.it/arezzo/rss", "https://www.corrierediarezzo.it/rss"]

@app.route('/')
def index(): return render_template('index.html')

@app.route('/api/updates')
def get_updates():
    news_list = []
    keywords = ["furto", "rapina", "ladri", "sicurezza", "fuga", "spaccata", "cronaca", "arresto"]
    context = ssl._create_unverified_context()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0 Safari/537.36'}

    for url in RSS_FEEDS:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=context, timeout=8) as response:
                feed = feedparser.parse(response.read())
                for entry in feed.entries[:10]:
                    if any(k in entry.title.lower() for k in keywords):
                        news_list.append({"fonte": "CRONACA", "titolo": entry.title.upper()})
        except: continue
    
    if not news_list: news_list.append({"fonte": "SISTEMA", "titolo": "MONITORAGGIO ATTIVO - NESSUNA NOTIZIA RSS"})

    social_data = [
        {"tipo": "WHATSAPP", "comune": "AREZZO OLMO", "testo": "Segnalata auto sospetta vicino scuole.", "data_ora": "2 MIN FA", "link": "https://web.whatsapp.com/"},
        {"tipo": "TELEGRAM", "comune": "VALDARNO", "testo": "Tentativo di spaccata fallito. Ladri fuggiti.", "data_ora": "15 MIN FA", "link": "https://t.me/s/ArezzoNotizie"}
    ]

    stats_data = [{"label": "MONTEVARCHI (A1)", "valore": 9.8}, {"label": "CORTONA (SR71)", "valore": 9.5}, {"label": "CIVITELLA", "valore": 9.2}]

    return jsonify({"ticker_news": news_list, "social_feed": social_data, "stats": stats_data})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
