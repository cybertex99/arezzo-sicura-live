from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Endpoint di test per verificare che il server risponda
@app.route('/api/updates')
def get_updates():
    return jsonify({"status": "online"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
