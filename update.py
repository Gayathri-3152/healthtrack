from threading import Timer
import mysql.connector
import requests

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="employee_details"

)
cursor = mydb.cursor()
query = "select * from User"
cursor.execute(query)
record = cursor.fetchall()

def update():
    response = requests.get('http://localhost:5000/api/data')
    data = response.json()
    cursor = mydb.cursor()
    i=0
    for name in record:
        user = name[0]
        bp = str(data[i]["systolic blood pressure"]) + "/" + str(data[i]["diastolic blood pressure"])
        bt = data[i]["body temperature"]
        os = data[i]["oxygen saturation"]
        rr = data[i]["respiration rate"]
        hr = data[i]["heart rate"]
        bg = data[i]["blood glucose"]
        i=i+1
        query = "UPDATE detail set BloodPressure='{}',BodyTemp={},Oxygensat={} ,ResperationRate={} ,HeartRate={} ,BloodGlucose={} WHERE user_name='{}'".format(bp,bt,os,rr,hr,bg,user)

        cursor.execute(query)
        mydb.commit()
    Timer(30,update).start()


update()