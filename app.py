#Interface for SQLITE
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps,dump
from flask_cors import CORS
import datetime
e = create_engine('sqlite:///app.db')
app = Flask(__name__)
api = Api(app)
CORS(app)
result = []
class getpatients(Resource):
    def get(self,name):
        result.clear()
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("select * from patient where name like '%"+name+"%';")
        for i in query.cursor.fetchall():
            dict = {'id':i[0],
                    'name':i[1],
                    'email':i[2],
                    'phone':i[3],
                    'gender':i[4],
                    'dob':i[5],
                    'address':i[6],
                    }
            result.append(dict)
        return result

class addPatient(Resource):
    def get(self,name,email,phone,gender,dob,addr):
        #Connect to databse
        addr = addr.replace("*","/")
        addr = addr.replace("'","\"")
        conn = e.connect()
        cquerry= conn.execute("select pcount from counters where name='Patient'")
        id = cquerry.cursor.fetchall()[0][0]
        conn.execute("update counters set pcount=pcount+1 where name='Patient'")
        values = "('%d','%s','%s',%d,'%s','%s','%s')" %(int(id),name,email,int(phone),gender,dob,addr)
        #Perform query and return JSON data
        query = conn.execute("insert into patient values"+values)
class addRecord(Resource):
    def get(self,id,title):
        today = datetime.datetime.now()
        tdate = today.strftime('%d-%b-%y')
        ttime = today.strftime('%I:%M %p')
        conn = e.connect()
        cquerry= conn.execute("select pcount from counters where name='Record'")
        rid = cquerry.cursor.fetchall()[0][0]
        conn.execute("update counters set pcount=pcount+1 where name='Record'")
        values= "(%d,%d,'%s','%s','%s')" %(int(id),int(rid),tdate,title,ttime)
        query = conn.execute("insert into Records values"+values)
        
class getRecord(Resource):
    def get(self,id):
        result = []
        conn = e.connect()
        query = conn.execute("select * from Records where id="+str(id))
        for i in query.cursor.fetchall():
            dict = {
                'id' : i[0],
                'rid' : i[1],
                'tdate' : i[2],
                'title' : i[3],
                'ttime' : i[4],
            }
            result.append(dict)
        return result
class addPresc(Resource):
    def get(self,rid,uid):
        conn = e.connect()
        conn.execute("insert into prescription values("+str(rid)+",'"+uid+"')")
class getPresc(Resource):
    def get(self,rid):
        result = []
        conn = e.connect()
        query = conn.execute("select uid from prescription where rid="+str(rid))
        for i in query.cursor.fetchall():
            result.append(i[0])
        return result
class remPresc(Resource):
    def get(self,uid):
        conn = e.connect()
        conn.execute("delete from prescription where uid='"+uid+"'")
class remXray(Resource):
    def get(self,uid):
        conn = e.connect()
        conn.execute("delete from xray where uid='"+uid+"'")
class remReport(Resource):
    def get(self,uid):
        conn = e.connect()
        conn.execute("delete from report where uid='"+uid+"'")
class remMisc(Resource):
    def get(self,uid):
        conn = e.connect()
        conn.execute("delete from misc where uid='"+uid+"'")
class addXray(Resource):
    def get(self,id,uid):
        conn = e.connect()
        conn.execute("insert into xray values("+str(id)+",'"+uid+"')")
class getXray(Resource):
    def get(self,id):
        result = []
        conn = e.connect()
        query = conn.execute("select uid from xray where id="+str(id))
        for i in query.cursor.fetchall():
            result.append(i[0])
        return result
class addReport(Resource):
    def get(self,id,uid):
        conn = e.connect()
        conn.execute("insert into report values("+str(id)+",'"+uid+"')")
class getReport(Resource):
    def get(self,id):
        result = []
        conn = e.connect()
        query = conn.execute("select uid from report where id="+str(id))
        for i in query.cursor.fetchall():
            result.append(i[0])
        return result

class addMisc(Resource):
    def get(self,id,uid):
        conn = e.connect()
        conn.execute("insert into misc values("+str(id)+",'"+uid+"')")
class getMisc(Resource):
    def get(self,id):
        result = []
        conn = e.connect()
        query = conn.execute("select uid from misc where id="+str(id))
        for i in query.cursor.fetchall():
            result.append(i[0])
        return result
class remRec(Resource):
    def get(self,rid):
        conn = e.connect()
        conn.execute("delete from Records where rid="+str(rid))
api.add_resource(getpatients,'/getp/<string:name>')
api.add_resource(addPatient,'/addPatient/<string:name>/<string:email>/<string:phone>/<string:gender>/<string:dob>/<string:addr>')
api.add_resource(addRecord,'/addRecord/<int:id>/<string:title>')
api.add_resource(getRecord,'/getRecord/<int:id>')
api.add_resource(addPresc,'/addPresc/<int:rid>/<string:uid>')
api.add_resource(getPresc,'/getPresc/<int:rid>')
api.add_resource(addXray,'/addXray/<int:id>/<string:uid>')
api.add_resource(getXray,'/getXray/<int:id>')
api.add_resource(addReport,'/addReport/<int:id>/<string:uid>')
api.add_resource(getReport,'/getReport/<int:id>')
api.add_resource(addMisc,'/addMisc/<int:id>/<string:uid>')
api.add_resource(getMisc,'/getMisc/<int:id>')
api.add_resource(remPresc,'/remPresc/<string:uid>')
api.add_resource(remXray,'/remXray/<string:uid>')
api.add_resource(remReport,'/remReport/<string:uid>')
api.add_resource(remMisc,'/remMisc/<string:uid>')
api.add_resource(remRec,'/remRec/<int:rid>')
if __name__ == '__main__':
    app.run()