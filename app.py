from flask import Flask, request, send_file, render_template
from datetime import datetime
import os
import csv
import pandas as pd

app = Flask(__name__)

LOG_FILE = "data/pixel_log.csv"

# Ensure log file exists
os.makedirs("data", exist_ok=True)
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Email", "IP", "User-Agent", "Timestamp"])


@app.route("/pixel")
def pixel():
    """Tracking pixel endpoint"""
    email = request.args.get("email", "unknown")
    ip = request.remote_addr
    ua = request.headers.get("User-Agent", "unknown")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log to CSV
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([email, ip, ua, timestamp])

    # Return 1x1 pixel
    return send_file("pixel.png", mimetype="image/png")


@app.route("/logs")
def logs():
    """View logs in a simple table"""
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        return render_template("logs.html", tables=[df.to_html(classes="table table-striped", index=False)], titles=df.columns.values)
    else:
        return "No logs yet."


@app.route("/")
def home():
    return "<h2>Email Tracker Running 🚀</h2><p>Use /pixel?email=xxx to track and /logs to view results.</p>"


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

