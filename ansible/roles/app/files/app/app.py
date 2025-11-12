# минимальное Flask приложение с Prometheus метриками
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
import psycopg2
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route('/')
def index():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB", "appdb"),
            user=os.getenv("POSTGRES_USER", "appuser"),
            password=os.getenv("POSTGRES_PASSWORD", "app_password"),
            host=os.getenv("DB_HOST", "db"),
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        t = cur.fetchone()
        cur.close()
        conn.close()
        return f"✅ OHUENNO! ZAEBIS!! DB connection OK — {t[0]}"
    except Exception as e:
        return f"❌ KAKAYA-TO HUYNYA!! Database connection failed: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
