import sqlite3
import pandas as pd

create_sentences_script = """CREATE TABLE "sentences" (
	"id"	INTEGER,
	"text"	TEXT,
	"source"	INTEGER DEFAULT 1,
	PRIMARY KEY("id" AUTOINCREMENT)
);"""

create_participants_script = """CREATE TABLE "participants" (
	"id"	INTEGER,
	"name"	TEXT,
	"email"	TEXT,
	"profile"	TEXT,
	"experience"	TEXT,
	"token"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);"""

create_rates_script = """CREATE TABLE "rates" (
	"id"	INTEGER,
	"sentence_id"	INTEGER,
	"participant_id"	INTEGER,
	"rate"	INTEGER,
	"datetime"	DATE DEFAULT '(datetime(''now'',''localtime''))',
	PRIMARY KEY("id" AUTOINCREMENT)
);"""

create_complaints_script = """CREATE TABLE "complaints" (
	"id"	INTEGER,
	"sentence_id"	INTEGER,
	"participant_id"	INTEGER,
	"complaint"	INTEGER,
	"datetime"	DATE DEFAULT '(datetime(''now'',''localtime''))',
	PRIMARY KEY("id" AUTOINCREMENT)
);"""

con = sqlite3.connect("./data/database.db")

creations = [create_sentences_script,create_participants_script,create_rates_script,create_complaints_script]

print("Tables creation")

for creation in creations:
	try:
		c = con.cursor()
		c.execute(creation)
		con.commit()
		c.close()
	except sqlite3.Error as er:
		print('SQLite error: %s' % (' '.join(er.args)))

print("Insert sentences")

f = open("./data/shuffled_sentences.txt",'r')
lines = f.readlines()
sentences = []
for l in lines:
	sentences.append((l.rstrip(),1))

df = pd.read_csv("./data/nohuman_7_abr.csv")

for s in df['sentences'].values:
	sentences.append((s.rstrip(),2))

c = con.cursor()

c.executemany('INSERT INTO sentences (text, source) VALUES(?,?);',sentences);

con.commit()
c.close()
con.close()