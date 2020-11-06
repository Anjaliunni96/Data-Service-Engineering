# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 17:11:34 2020

@author: Anjali Unni
"""

from flask import Flask
from flask_restplus import Resource, Api , fields , reqparse
from datetime import datetime
import requests
import json
import sqlite3
import pandas as pd


app = Flask(__name__)
api = Api(app)


get_indicator = api.model("get_collections",{"indicator_id":fields.String("indicator_id")})

indicator_parser = reqparse.RequestParser()
indicator_parser.add_argument('indicator_id')


#connection to database
conn = sqlite3.connect('z5275189.db')
cursor = conn.cursor()
cursor.execute("create table collections (uri text, id integer PRIMARY KEY autoincrement, indicator_id text,creation_time text, collection_data text)")
conn.commit()

#creating a data frame
#cnx = sqlite3.connect('z5275189.db')
#df = pd.read_sql_query("SELECT * FROM collections", cnx)

# print(count
############ q1 ##################
@api.route('/collections/')
class put_Collection(Resource):
 @api.expect(indicator_parser)
 def post(self):
     #args = reqparse.RequestParser().parse_args()
     args = indicator_parser.parse_args()
     conn = sqlite3.connect('z5275189.db')
     cursor = conn.cursor()
     if(args["indicator_id"]):
         pass
     elif(args["indicator_id"]==None):
         return "Empty Indicator Id",404

     req = requests.get(" http://api.worldbank.org/v2/countries/all/indicators/"+str(args["indicator_id"])+"?date=2012:2017&format=json&per_page=1000")
     if (req.status_code!=200):
         return "Invalid Parameters",404

     cursor.execute("select max(id) from collections")
     id = cursor.fetchall()[0][0]
     if(id):
         id+=1
     elif(id==None):
             id=1
 
     sql = "INSERT into collections(uri,indicator_id,creation_time,collection_data) values (?,?,?,?)"
     cursor.execute(sql,["collections/"+str(id),str(args["indicator_id"]),str(datetime.now()),str(req.json())])
     conn.commit()
     cursor.execute("select * from collections where id="+str(id))
     data = cursor.fetchall()[0]
     return {'uri':data[0],
                    'id':data[1],
                    'indicator_id':data[2],
                    'creation_time':data[3]} , 201  
 
 ############ q2 ##################
 def delete(self, id):
      cnx = sqlite3.connect('z5275189.db')
      df = pd.read_sql_query("SELECT * FROM collections", cnx)
      df.set_index('id', inplace=True)
      if id not in df.index:
            api.abort(404, "Collection doesn't exist")

      df.drop(id, inplace=True)
      return {"message": "Collection {} was removed from the database!".format(id),
              'id' : id}, 200
 
    ############ q4 ##################
@api.route('/collections/<int:id>')
class get_Collection(Resource):
    def get(self, id): 
      #cnx = sqlite3.connect('z5275189.db')
      #df = pd.read_sql_query("SELECT * FROM collections", cnx)
      args = reqparse.RequestParser().parse_args()
      #df = pd.read_sql_query("SELECT * FROM collections", cnx)
      cursor.execute("select * from collections where id="+str(id))
      data = cursor.fetchall()[0]
      return {
      'id': data[1],
      'indicator': str(args["indicator_id"]),
      'indicator_value': data['indicator_value'],
      'creation_time': data[3],
      'entries': data[4]}, 200
        
    
    
if __name__ == '__main__':
    app.run(debug=True)
    
    