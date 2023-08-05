#!/usr/bin/python3
import json
import hashlib
from datetime import datetime
class jumpdb(object):
        def __init__(self):
            self.data = []
        def insert(self,data):
            id_=hashlib.sha224(str(datetime.now()).encode()).hexdigest()
            self.data.append({"id_":id_, "data":data})
            return id_
        def enumerate(self,id_):
            for i in self.data:
                    if i["id_"] == id_:
                            for k,v in i["data"].items():
                                    print("{} = {}".format(k,v))
        def find(self,data):
            lst=[]
            keys,values = data.keys(),data.values()
            for i in self.data:
                for k in keys:
                    if k in i["data"].keys():
                        for v in values:
                            if v in i["data"].values():
                                lst.append(i)
            return lst
        def delete(self,id_):
            for i in self.data:
                if i["id_"] == id_:
                    self.data.remove(i)
        def update(self,id_,data):
            for i in self.data:
                if i["id_"] == id_:
                    i["data"].update(data)
                    break
        # =====================================
        def save(self,filepath):
            f=open(filepath,"wb")
            f.write(json.dumps(self.data,indent=4,sort_keys=True).encode())
            f.close()
        def load(self,filepath):
            f=open(filepath,"rb")
            self.data = json.loads(f.read())
            f.close()
        # =====================================

"""
j=jumpdb()
j.load("test.jdb")
#ID=j.insert({44:5,55:8})
#print(ID)
print(j.find({"44":8}))
#j.update(ID,{44:8})
#j.enumerate(ID)
#j.delete(ID)
#print(j.find({44:8}))
#j.save("test.jdb")
"""