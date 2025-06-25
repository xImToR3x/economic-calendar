from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Hello from Python on Render!"})

# Optional: weitere Routen z.B. /economic-calendar, /btc-price
