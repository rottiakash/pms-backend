from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps,dump
from flask_cors import CORS
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
        query = conn.execute("select * from patient where name like '"+name+"%';")
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
        conn = e.connect()
        cquerry= conn.execute("select pcount from counters")
        id = cquerry.cursor.fetchall()[0][0]
        conn.execute("update counters set pcount=pcount+1")
        values = "('%d','%s','%s',%d,'%s','%s','%s')" %(int(id),name,email,int(phone),gender,dob,addr)
        #Perform query and return JSON data
        query = conn.execute("insert into patient values"+values)
api.add_resource(getpatients,'/getp/<string:name>')
api.add_resource(addPatient,'/addPatient/<string:name>/<string:email>/<string:phone>/<string:gender>/<string:dob>/<string:addr>')
if __name__ == '__main__':
    app.run()