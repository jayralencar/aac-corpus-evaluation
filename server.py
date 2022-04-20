from flask import Flask
from flask import request,render_template,send_from_directory
from flask_cors import CORS
from flask_ngrok import run_with_ngrok
import sqlite3

con = sqlite3.connect("./data/database.db",check_same_thread=False)
con.row_factory = sqlite3.Row

app = Flask(__name__,template_folder='template')
# run_with_ngrok(app)
CORS(app)

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
  return send_from_directory('./template', path)

@app.route('/')
def hello():
    return render_template("index.html")

@app.route("/get-sentences", methods=["GET"])
def get_sentences():
    c = con.cursor()
    c.execute("SELECT * FROM sentences ORDER BY RANDOM() LIMIT 10")
    results = [dict(i) for i in c.fetchall()]
    print(results)
    return {"data":results}

if __name__ == "__main__":
    app.run(debug=True)