from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def all_events():
    url = "https://m.investing.com/economic-calendar/"
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X)"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    
    events = []
    for row in soup.select("tr.js-event-item"):
        time_tag = row.select_one(".time, .event-time")
        event_tag = row.select_one(".event")
        country = row.get("data-country", "").strip()
        if time_tag and event_tag:
            events.append({
                "time": time_tag.text.strip(),
                "country": country,
                "event": event_tag.text.strip()
            })
    return jsonify(events)

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
