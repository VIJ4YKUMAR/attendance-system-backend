from ctypes import sizeof
from sqlite3 import Cursor
from unicodedata import name
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask import request
import psycopg2
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/*/*": {"origins": "*"}})

@app.route('/')
def hello_world():
    return "Hello World!"


@app.route('/student_checkin', methods= ['POST'])
def student_checkin():
    conn = None
    if request.method == 'POST':
        try:
            conn = psycopg2.connect("dbname=Student_attendance user=vijay password=***** host=localhost")
            data = request.get_json()
            roll_no = data['rollNumber']
            name = data['name']
            cur = conn.cursor()
            sql = 'INSERT INTO attendance(roll_no, name, check_in) VALUES(%s, %s, now())'
            cur.execute(sql, (roll_no, name, ))
            conn.commit()
            cur.close()

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
    
        finally:
            if conn is not None:
                conn.close()
                print("connection closed")
            return jsonify([])


@app.route('/student_checkout', methods= ['POST'])
def student_checkout():
    conn = None
    if request.method == 'POST':
        try:
            conn = psycopg2.connect("dbname=Student_attendance user=vijay password=***** host=localhost")
            data = request.get_json()
            roll_no = data['rollNumber']
            name = data['name']
            cur = conn.cursor()
            sql = 'UPDATE attendance SET check_out = now() WHERE roll_no = %s and name = %s'
            cur.execute(sql, (roll_no, name))
            conn.commit()
            cur.close()

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
    
        finally:
            if conn is not None:
                conn.close()
                print("connection closed")
            return jsonify([])


@app.route('/get_students')
def get_students():
    conn = None
    try:
        # conn = psycopg2.connect("dbname=motivational_quotes user=vijay password=x9qbiYEdpMc8FGnVUdpcb4DaO9dYzV19 host=dpg-ceetjc4gqg4b3h9qv1t0-a")
        conn = psycopg2.connect("dbname=Student_attendance user=vijay password=***** host=localhost")
        cursor = conn.cursor()
        sql = "select * from attendance"
        cursor.execute(sql)
        rows = cursor.fetchall()
        rowarray_list = []
        for row in rows:
            t = { 'id': row[0], 'roll_no': row[1], 'name':row[2], 'check_in':str(row[3]), 'check_out':str(row[4])}
            rowarray_list.append(t)
        conn.commit()
        cursor.close()
        return json.dumps(rowarray_list)

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            print("connection closed")

if __name__ == '__main__':
    app.run(debug=True)
