import csv, sqlite3

con = sqlite3.connect("example.db")
cur = con.cursor()
cur.execute("CREATE TABLE t (CODGEO, LIBGEO, MED14);") # use your column names here

with open('FC2014.csv','r') as fin:
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin,delimiter=";") # comma is default delimiter
    to_db = [(i['CODGEO'], i['LIBGEO'], i['MED14']) for i in dr]

cur.executemany("INSERT INTO t (CODGEO, LIBGEO, MED14) VALUES (?, ?, ?);", to_db)
con.commit()
con.close()