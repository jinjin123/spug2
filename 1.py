a="数据盘:D;容量:4465G;数据盘:E;容量:60G;"
dd = a.split(";")
del dd[-1]
one=[]
two=[]

for x in dd:
    if x.find("数据盘:") == 0:
        one.append(x.split("数据盘:")[1])

    if x.find("容量:") == 0:
        two.append(x.split("容量:")[1])
    #print(x.split("数据盘:")[1] if x.find("数据盘:") == 0 else ""  )
    #e.append({"type":"windata","name":x.split("数据盘:")[1], "size":x.split("容量:")[1]})
    #print(x.split("数据盘:"))
    #print(x.split("容量:"))
    #dd.append({"type":"windata","name":x.split("数据盘:")[1] if x.find("数据盘:")==0 else "" ,
    #                        "size":x.split("容量:")[1] if x.find("容量:")==0 else "" })

#for x in e:
#    c.append({"name":x["name"],"size":x["size"]})

e =[]
for k,v in dict(zip(one,two)).items():
    e.append({"type":"windata","name":k, "size":v})

print(e)
