from flask import Flask, render_template, jsonify
import feedparser, ssl, os, urllib.request

app = Flask(__name__)

# Fonti Reali: Arezzo + Guerra
RSS_SOURCES = {
    "AREZZO": "https://www.arezzonotizie.it/rss",
    "GUERRA": "https://www.ansa.it/sito/notizie/mondo/rss.xml" # Feed mondo per aggiornamenti guerra
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/updates')
def get_updates():
    data = {"ticker": [], "social": []}
    context = ssl._create_unverified_context()
    headers = {'User-Agent': 'Mozilla/5.0'}

    # 1. Recupero News (Arezzo + Guerra)
    for tag, url in RSS_SOURCES.items():
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=context, timeout=5) as response:
                feed = feedparser.parse(response.read())
                for entry in feed.entries[:5]:
                    prefix = "🌍 GUERRA" if tag == "GUERRA" else "📍 AREZZO"
                    data["ticker"].append(f"{prefix}: {entry.title.upper()}")
        except: continue

    # 2. Struttura per Post Social (Telegram/X)
    # Se hai già uno script che legge X, i dati verranno iniettati qui
    data["social"] = [
        {
            "piattaforma": "X (TWITTER)",
            "autore": "@Emergenza24",
            "testo": "Aggiornamento fronte: intensificati i controlli nelle zone di confine. Monitoraggio radar attivo.",
            "time": "ORA"
        },
        {
            "piattaforma": "TELEGRAM",
            "autore": "CANALE GUERRA LIVE",
            "testo": "Esplosioni segnalate nel settore Nord. Fonti locali confermano attivazione contraerea.",
            "time": "2 min fa"
        }
    ]
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
