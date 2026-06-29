import pymysql

from app.core.config import settings

tables = [
    "weather_data",
    "solar_panel",
    "solar_predictions",
    "energy_consumption",
    "battery",
    "battery_status",
    "telemetry",
    "alerts",
    "system_logs",
]

conn = pymysql.connect(
    host=settings.db_host,
    port=settings.db_port,
    user=settings.db_user,
    password=settings.db_password,
    database=settings.db_name,
)
cur = conn.cursor()
for table in tables:
    print(f"=== {table} ===")
    cur.execute(f"DESCRIBE `{table}`")
    for row in cur.fetchall():
        print(row)
conn.close()
