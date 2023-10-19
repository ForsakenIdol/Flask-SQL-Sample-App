from flask import Flask, render_template
from mysql import connector
import os
from prometheus_flask_exporter import PrometheusMetrics
from time import sleep

app = Flask(__name__)

retry = 1
connected = False
max_retries = 10
while (retry <= max_retries and not connected):
    try:
        cnx = connector.connect(user=os.environ["DB_USER"],
                                password=os.environ["DB_PASSWORD"],
                                host=os.environ["DB_HOST"],
                                database=os.environ["DB_DATABASE"],
                                port=3306)
        cursor = cnx.cursor()
        connected = True
    except Exception as e:
        print("MySQL connection failed: retry {} of {}. Retrying...".format(retry, max_retries))
        print (e)
        cursor = None
        retry += 1
        sleep(3)
        

if not connected:print("MySQL database connection failed - proceeding without database connection.")
else: print("MySQL connection established.")

flask_metrics = PrometheusMetrics(app, path="/mymetrics")

@app.route("/")
def home():
    print("Hit the root page.")
    return render_template("index.html")

@app.route("/get")
def get():
    global cursor
    if cursor is not None:
        print("Getting database entries.")
        query = "SELECT * FROM {}".format(os.environ["DB_TABLE_NAME"])
        cursor.execute(query)
        return render_template("get.html", db_entries=[entry for entry in cursor])
    else:
        print("Serving /get without database entries.")
        return render_template("get.html", db_entries=[ "No database connection.", "Proceeding without a database connection." ])

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=80)