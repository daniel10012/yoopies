import csv, sqlite3

con = sqlite3.connect("sh14.db")
cur = con.cursor()
cur.execute("CREATE TABLE t (CODGEO,LIBGEO,SNHM14,SNHMC14,SNHMP14,SNHME14,SNHMO14,SNHMF14,SNHMFC14,SNHMFP14,SNHMFE14,SNHMFO14,SNHMH14,SNHMHC14,SNHMHP14,SNHMHE14,SNHMHO14,SNHM1814,SNHM2614,SNHM5014,SNHMF1814,SNHMF2614,SNHMF5014,SNHMH1814,SNHMH2614,SNHMH5014,Departement,Geo_Shape,geo_point_2d);") # use your column names here

with open('sh14.csv','r') as fin:
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin,delimiter=";") # comma is default delimiter

    to_db = [(i['CODGEO'], i['LIBGEO'], i['SNHM14'], i['SNHMC14'], i['SNHMP14'], i['SNHME14'], i['SNHMO14'], i['SNHMF14'], i['SNHMFC14'], i['SNHMFP14'], i['SNHMFE14'], i['SNHMFO14'], i['SNHMH14'], i['SNHMHC14'], i['SNHMHP14'], i['SNHMHE14'], i['SNHMHO14'], i['SNHM1814'], i['SNHM2614'], i['SNHM5014'], i['SNHMF1814'], i['SNHMF2614'], i['SNHMF5014'], i['SNHMH1814'], i['SNHMH2614'], i['SNHMH5014'], i['Departement'], i['Geo_Shape'], i['geo_point_2d']) for i in dr]

cur.executemany("INSERT INTO t (CODGEO,LIBGEO,SNHM14,SNHMC14,SNHMP14,SNHME14,SNHMO14,SNHMF14,SNHMFC14,SNHMFP14,SNHMFE14,SNHMFO14,SNHMH14,SNHMHC14,SNHMHP14,SNHMHE14,SNHMHO14,SNHM1814,SNHM2614,SNHM5014,SNHMF1814,SNHMF2614,SNHMF5014,SNHMH1814,SNHMH2614,SNHMH5014,Departement,Geo_Shape,geo_point_2d) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()