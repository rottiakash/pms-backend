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

class remPatient(Resource):
    def get(self,id):
        conn = e.connect()
        conn.execute("delete from patient where id='"+str(id)+"'")

class addPatient(Resource):
    def get(self,name,email,phone,gender,dob,addr):
        #Connect to databse
        addr = addr.replace("*","/")
        addr = addr.replace("'","\"")
        conn = e.connect()
        cquerry= conn.execute("select pcount from counters where name='Patient'")
        id = cquerry.cursor.fetchall()[0][0]
        values = "('%d','%s','%s',%d,'%s','%s','%s')" %(int(id),name,email,int(phone),gender,dob,addr)
        #Perform query and return JSON data
        query = conn.execute("insert into patient values"+values)
class addTreatment(Resource):
    def get(self,id,title):
        today = datetime.datetime.now()
        tdate = today.strftime('%d-%b-%y')
        ttime = today.strftime('%I:%M %p')
        conn = e.connect()
        cquerry= conn.execute("select pcount from counters where name='Treatment'")
        tid = cquerry.cursor.fetchall()[0][0]
        values= "(%d,%d,'%s','%s','%s',0)" %(int(id),int(tid),tdate,title,ttime)
        query = conn.execute("insert into Treatments values"+values)
        
class getTreatment(Resource):
    def get(self,id):
        result = []
        conn = e.connect()
        query = conn.execute("select * from Treatments where id="+str(id))
        for i in query.cursor.fetchall():
            dict = {
                'id' : i[0],
                'tid' : i[1],
                'tdate' : i[2],
                'title' : i[3],
                'ttime' : i[4],
                'attachment' : i[5]
            }
            result.append(dict)
        return result
class addPresc(Resource):
    def get(self,tid,uid):
        conn = e.connect()
        conn.execute("insert into prescription values("+str(tid)+",'"+uid+"')")
class getPresc(Resource):
    def get(self,tid):
        result = []
        conn = e.connect()
        query = conn.execute("select uid from prescription where tid="+str(tid))
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
    def get(self,tid):
        conn = e.connect()
        conn.execute("delete from Treatments where tid="+str(tid))
class editPatient(Resource):
    def get(self,id,name,email,phone,gender,dob,addr):
        conn = e.connect()
        addr = addr.replace("*","/")
        addr = addr.replace("'","\"")
        querry = "update patient set name='%s', email='%s', phone=%d, gender='%s', dob='%s', address='%s' where id=%d" %(name,email,int(phone),gender,dob,addr,int(id))
        conn.execute(querry)
class addPatientWoP(Resource):
    def get(self,name,email,phone,gender,dob,addr):
        #Connect to databse
        addr = addr.replace("*","/")
        addr = addr.replace("'","\"")
        conn = e.connect()
        cquerry= conn.execute("select pcount from counters where name='Patient'")
        id = cquerry.cursor.fetchall()[0][0]
        values = "('%d','%s','%s',%s,'%s','%s','%s')" %(int(id),name,email,phone,gender,dob,addr)
        #Perform query and return JSON data
        query = conn.execute("insert into patient values"+values)
class editPatientwop(Resource):
    def get(self,id,name,email,phone,gender,dob,addr):
        conn = e.connect()
        addr = addr.replace("*","/")
        addr = addr.replace("'","\"")
        querry = "update patient set name='%s', email='%s', gender='%s', dob='%s', address='%s' where id=%d" %(name,email,gender,dob,addr,int(id))
        conn.execute(querry)
class editTreatment(Resource):
    def get(self,tid,title):
        conn = e.connect()
        querry = "update treatments set title='%s' where tid=%d" %(title,int(tid))
        conn.execute(querry)
class listAll(Resource):
    def get(self):
        result.clear()
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("select * from patient;")
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
api.add_resource(getpatients,'/getp/<string:name>')
api.add_resource(addPatient,'/addPatient/<string:name>/<string:email>/<string:phone>/<string:gender>/<string:dob>/<string:addr>')
api.add_resource(addTreatment,'/addTreatment/<int:id>/<string:title>')
api.add_resource(getTreatment,'/getTreatment/<int:id>')
api.add_resource(addPresc,'/addPresc/<int:tid>/<string:uid>')
api.add_resource(getPresc,'/getPresc/<int:tid>')
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
api.add_resource(remRec,'/remRec/<int:tid>')
api.add_resource(remPatient,'/remPatient/<int:id>')
api.add_resource(editPatient,'/edit/<int:id>/<string:name>/<string:email>/<string:phone>/<string:gender>/<string:dob>/<string:addr>')
api.add_resource(addPatientWoP,'/addPatientwop/<string:name>/<string:email>/<string:phone>/<string:gender>/<string:dob>/<string:addr>')
api.add_resource(editPatientwop,'/editwop/<int:id>/<string:name>/<string:email>/<string:phone>/<string:gender>/<string:dob>/<string:addr>')
api.add_resource(editTreatment,'/editTreat/<int:tid>/<string:title>')
api.add_resource(listAll,'/listall')
if __name__ == '__main__':
    app.run()