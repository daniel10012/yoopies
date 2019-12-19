a = "CODGEO;LIBGEO;SNHM14;SNHMC14;SNHMP14;SNHME14;SNHMO14;SNHMF14;SNHMFC14;SNHMFP14;SNHMFE14;SNHMFO14;SNHMH14;SNHMHC14;SNHMHP14;SNHMHE14;SNHMHO14;SNHM1814;SNHM2614;SNHM5014;SNHMF1814;SNHMF2614;SNHMF5014;SNHMH1814;SNHMH2614;SNHMH5014;Département;Geo Shape;geo_point_2d"

b = a.replace(";",",")

#[(i['CODGEO'], i['LIBGEO'], i['MED14']) for i in dr]

c = a.split(";")

x = len(c)
print(x)
s = ""
for lib in c:
    s += f"i['{lib}'], "

print(s)

f = 29 * "?, "
print(f)