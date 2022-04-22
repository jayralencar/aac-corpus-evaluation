from crypt import methods
from flask import Flask
from flask import request,render_template,send_from_directory
from flask_cors import CORS
from flask_ngrok import run_with_ngrok
from flask import send_file, make_response, abort  
import sqlite3

con = sqlite3.connect("./data/database.db",check_same_thread=False)
con.row_factory = sqlite3.Row

app = Flask(__name__,template_folder='template')
run_with_ngrok(app)
CORS(app)

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
  return send_from_directory('./template', path)

@app.route('/')
def hello():
    # return render_template("index.html")
    return make_response(open('./template/index.html').read())


@app.route("/get-sentences", methods=["GET"])
def get_sentences():
    c = con.cursor()
    c.execute("SELECT * FROM sentences ORDER BY RANDOM() LIMIT 10")
    results = [dict(i) for i in c.fetchall()]
    print(results)
    return {"data":results}

def insert(table, data):
    sql = "INSERT INTO {0} ({1}) VALUES ({2})".format(table, ','.join(list(data.keys())),",".join(['?']*len(data.values())))
    print(sql)
    c = con.cursor()
    c.execute(sql, tuple(data.values()))
    insert_id = c.lastrowid
    con.commit()
    c.close()
    return insert_id


@app.route("/save-response",methods=["POST"])
def save_responses():
    json = request.json
    participant_id = insert('participants', json['user'])
    for sentence in json['sentences']:
        d = {
            "sentence_id": sentence['id'],
            "participant_id": participant_id,
            "rate": sentence['response']
        }
        insert("rates",d)
    return {"status":1}
    

if __name__ == "__main__":
    app.run(debug=True)