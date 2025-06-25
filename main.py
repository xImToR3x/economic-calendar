from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def get_events():
    url = "https://www.investing.com/economic-calendar/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    events = []
    rows = soup.select("tr.js-event-item")

    for row in rows:
        time_tag = row.select_one(".first.left.time")
        currency_tag = row.select_one(".left.flagCur.noWrap > span")
        event_tag = row.select_one(".left.event")
        impact_tag = row.select_one(".sentiment > i")

        time = time_tag.get_text(strip=True) if time_tag else ""
        currency = currency_tag.get_text(strip=True) if currency_tag else ""
        event = event_tag.get_text(strip=True) if event_tag else ""
        impact_class = impact_tag.get("class", []) if impact_tag else []
        impact_level = (
            "high" if "high" in impact_class else
            "medium" if "medium" in impact_class else
            "low" if "low" in impact_class else
            "none"
        )

        if time and currency and event:
            events.append({
                "time": time,
                "currency": currency,
                "event": event,
                "impact": impact_level
            })

    return jsonify(events[:10])  # Optional: Begrenze die Anzahl

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
