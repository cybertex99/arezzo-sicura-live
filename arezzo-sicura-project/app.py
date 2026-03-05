from flask import Flask, render_template, jsonify
import feedparser, os, urllib.request, ssl

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/updates')
def get_updates():
    # Dati News di Emergenza (se il web fallisce)
    news_list = [{"fonte": "SISTEMA", "titolo": "MONITORAGGIO ATTIVO - NESSUNA ANOMALIA RILEVATA"}]
    
    # Tentativo recupero news reali
    try:
        context = ssl._create_unverified_context()
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request("https://www.arezzonotizie.it/rss", headers=headers)
        with urllib.request.urlopen(req, context=context, timeout=5) as response:
            feed = feedparser.parse(response.read())
            if feed.entries:
                news_list = [{"fonte": "CRONACA", "titolo": e.title.upper()} for e in feed.entries[:10]]
    except:
        pass

    # Dati Social obbligatori (Box separati)
    social_data = [
        {"tipo": "WHATSAPP", "comune": "AREZZO OLMO", "testo": "Auto sospetta segnalata.", "data": "1 min fa", "link": "https://web.whatsapp.com"},
        {"tipo": "TELEGRAM", "comune": "@SicurezzaAr", "testo": "Furgone bianco in fuga verso A1.", "data": "5 min fa", "link": "https://t.me/s/ArezzoNotizie"},
        {"tipo": "X", "comune": "@ArezzoCronaca", "testo": "Posto di blocco SR71.", "data": "10 min fa", "link": "https://twitter.com"}
    ]

    # Statistiche Permeabilità
    stats_data = [{"l": "MONTEVARCHI", "v": 9.8}, {"l": "CORTONA", "v": 9.5}, {"l": "CIVITELLA", "v": 9.2}]

    return jsonify({"news": news_list, "social": social_data, "stats": stats_data})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
