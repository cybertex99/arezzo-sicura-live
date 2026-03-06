from flask import Flask, render_template, jsonify
import feedparser, ssl, os, urllib.request

app = Flask(__name__)

# Fonti Cronaca Arezzo
RSS_SOURCES = [
    "https://www.arezzonotizie.it/rss",
    "https://www.lanazione.it/arezzo/rss",
    "https://www.corrierediarezzo.it/rss"
]

# Parole chiave per il filtro sicurezza
KEYWORDS = ["FURTO", "RAPINA", "RUBATA", "SOSPETTA", "ARRESTATO", "SCIPPO", "COLPO", "LADRI", "TARGHE"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/updates')
def get_updates():
    data = {"ticker": [], "social": []}
    context = ssl._create_unverified_context()
    headers = {'User-Agent': 'Mozilla/5.0'}

    for url in RSS_SOURCES:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=context, timeout=5) as response:
                feed = feedparser.parse(response.read())
                for entry in feed.entries[:10]:
                    titolo = entry.title.upper()
                    # Filtra solo se contiene parole chiave di sicurezza
                    if any(key in titolo for key in KEYWORDS):
                        data["ticker"].append(f"⚠️ ALLERTA: {titolo}")
        except: continue

    # Sezione Social (Telegram/X) - Qui i post che già leggi
    # Inserisco dati di esempio basati sulle tue richieste
    data["social"] = [
        {
            "canale": "TELEGRAM | SEGNALAZIONI",
            "testo": "Avvistata BMW scura targa straniera zona Olmo. Gira con fare sospetto tra le villette.",
            "ora": "5 min fa",
            "tipo": "SOSPETTO"
        },
        {
            "canale": "X | CRONACA AREZZO",
            "testo": "Tentato furto in abitazione a Ceciliano. I malviventi sono fuggiti nei campi verso la ferrovia.",
            "ora": "14 min fa",
            "tipo": "FURTO"
        }
    ]
    
    if not data["ticker"]:
        data["ticker"] = ["✅ NESSUNA NUOVA SEGNALAZIONE DI RILIEVO NELLE ULTIME ORE"]

    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
