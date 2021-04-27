import random
from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

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
cursor.close()
mydb.close()

def details(username):


    bloodPressure1 = random.randint(80, 180)
    bloodPressuer2 = bloodPressure1 - random.randint(40, 50)
    bodyTemp = random.randint(90, 107)
    oxySat = random.randint(92, 98)
    respireRate = random.randint(10, 30)
    heartRate = random.randint(40, 125)
    bloodGlucose = random.randint(120, 220)

    result ={
            "username":username,
            "systolic blood pressure": bloodPressure1,
            "diastolic blood pressure": bloodPressuer2,
            "body temperature": bodyTemp,
            "oxygen saturation": oxySat,
            "respiration rate": respireRate,
            "heart rate": heartRate,
            "blood glucose": bloodGlucose,
        }
    return result


@app.route('/api/data')
def api():
    result = list()
    for row in record:
        data=details(row[0])
        result.append(data)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

