from flask import Flask, render_template, request
import mysql.connector
import requests
import smtplib, ssl


app = Flask(__name__)

def health(i):
    response = requests.get('http://localhost:5000/api/data')
    dataGotFromApi = response.json()
    msg = "Hi " + str(dataGotFromApi[i]["username"]) + ",\n""You may have these following issues, so take care of your health, proper medication is needed\n"

    bp = str(dataGotFromApi[i]["systolic blood pressure"])
    bp1 = str(dataGotFromApi[i]["diastolic blood pressure"])
    btemp = str(dataGotFromApi[i]["body temperature"])
    oxysat = str(dataGotFromApi[i]["oxygen saturation"])
    resrate = str(dataGotFromApi[i]["respiration rate"])
    heartrate = str(dataGotFromApi[i]["heart rate"])
    glucose = str(dataGotFromApi[i]["blood glucose"])

    if (int(glucose) >= 140 and int(glucose) < 200):
        msg = msg+"prediabetes\n"
    elif (int(glucose) >= 200):
        msg = msg + "Diabetes\n"

    if (int(btemp) > 100 and int(resrate) >= 24):
        msg=msg + "Bronchitis\n"

    if (int(oxysat) < 96):
        msg=msg+ "Hypoxemia\n"

    if ((int(oxysat) >= 92 and int(oxysat) <= 95) and int(heartrate) >= 100 and int(resrate) >= 20):
        msg=msg + "Asthma\n"

    if ((int(bp) < 90 or int(bp1) < 60)):
        msg=msg + "Low Blood Pressure\n"
    elif ((int(bp) >= 180 or int(bp1) >= 120)):
        msg=msg + "Severe Blood Pressure\n"
    elif ((int(bp) >= 140 or int(bp1) >= 90)):
        msg = msg + "High Blood Pressure\n"

    if ((int(bp) >= 140 or int(bp1) >= 90) and int(heartrate) >= 100):
        msg = msg + "you are Stressed \n"

    if (msg == "Hi " + str(dataGotFromApi[i]["username"]) + ",\n""You may have these following issues, so take care of your health, proper medication is needed\n"):
        msg ="Hi " + str(dataGotFromApi[i]["username"]) + ",\n" "You are doing great, keep maintaining your health\n"

    msg = msg+"\nblood pressure  : "+bp +"/"+bp1
    msg = msg+"\nbody temperature  : "+btemp+"F"
    msg = msg + "\noxygen saturation  : " + oxysat+"%"
    msg = msg + "\nrespiration rate  : " +resrate +"/min"
    msg = msg + "\nheart rate  : " + heartrate+"/min"
    msg = msg + "\nblood glucose  : " +glucose+"mg/dL"

    return msg


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/dietChart')
def dietChart():
    return render_template("dietchart.html")


@app.route('/login')
def login():
    return render_template("loginPage.html")


@app.route('/login', methods=['POST'])
def logedin():
    loginValue = request.form['Admin/User']
    username=request.form['username']
    password=request.form['password']
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="employee_details"

    )

    cursor = mydb.cursor()
    query = "select * from admin"
    cursor.execute(query)
    admin = cursor.fetchall()
    query = "select * from User"
    cursor.execute(query)
    userData = cursor.fetchall()
    query = "select * from detail"
    cursor.execute(query)
    record = cursor.fetchall()
    cursor.close()
    mydb.close()

    database1 = {}
    for data in userData:
        database1[data[0]] = data[1]

    database2 = {}
    for data in admin:
        database2[data[0]] = data[1]

    if loginValue == 'User' or loginValue=='USER' or loginValue=='user':
        if username not in database1:
            return render_template("loginPage.html", info='"INVALID USERNAME"')
        elif database1[username]!=password:
            return render_template("loginPage.html",info='"INVALID PASSWORD"')
        else:
            return render_template("personal.html", record=record,user=username)
    elif loginValue == 'Admin' or loginValue== 'ADMIN' or loginValue=='admin':
        if username not in database2:
            return render_template("loginPage.html", info='"INVALID USERNAME"')
        elif database2[username]!=password:
            return render_template("loginPage.html",info='"INVALID PASSWORD"')
        else:
            return render_template("table.html", record=record)
    else:
        return render_template("loginPage.html",info='"INVALID LOGIN"')



@app.route('/signup')
def signup():
    return render_template("signUp.html")


@app.route('/signup', methods=['POST'])
def signedup():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="employee_details"

    )

    cursor = mydb.cursor()
    query = "select * from User"
    cursor.execute(query)
    userData = cursor.fetchall()
    cursor.close()
    mydb.close()

    user = request.form['username']
    password = request.form['password']
    mailid = request.form['mailid']
    name = request.form['name']

    check=1
    for data in userData:
        if(data[0]==user):
            check=0
    if check==1:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="employee_details"

        )
        query = "INSERT INTO User(user_name,password,email,name) values('{}','{}','{}','{}')".format(user, password,mailid,name)
        Cursor = mydb.cursor()
        Cursor.execute(query)
        mydb.commit()
        response = requests.get('http://localhost:5000/api/data')
        data = response.json()
        bp = str(data[0]["systolic blood pressure"]) + "/" + str(data[0]["diastolic blood pressure"])
        bt = data[0]["body temperature"]
        os = data[0]["oxygen saturation"]
        rr = data[0]["respiration rate"]
        hr = data[0]["heart rate"]
        bg = data[0]["blood glucose"]

        query = "INSERT INTO detail(user_name,BloodPressure,BodyTemp,Oxygensat ,ResperationRate ,HeartRate ,BloodGlucose) values('{}','{}',{},{},{},{},{})".format(
            user, bp, bt, os, rr, hr, bg)
        Cursor.execute(query)
        mydb.commit()
        Cursor.close()
        mydb.close()
        return render_template("signUp.html",info='"signed up successfully login to view details"')

    else:
        return render_template("signUp.html", info='"invalid user name"')


@app.route('/mail')
def mail():
    return render_template("mail.html")


@app.route('/mail', methods=['POST'])
def mailsent():
     mailid = request.form['email']
     password=request.form['password']
     mydb = mysql.connector.connect(
         host="localhost",
         user="root",
         password="",
         database="employee_details"

     )

     cursor = mydb.cursor()
     query = "select * from User"
     cursor.execute(query)
     userData = cursor.fetchall()
     i=0
     check=0
     for row in userData:
         if row[2]==mailid and row[1]==password:
             check=1
             break
         i=i+1
     if check==1:
         mail = smtplib.SMTP("smtp.gmail.com", 587)
         mail.starttls(context=ssl.create_default_context())
         sender = "sample33022@gmail.com"
         password = "sample2233"
         rec = mailid
         msg = health(i)

         mail.login(sender, password)
         mail.sendmail(sender, rec, msg)
         print("mail send successfully")
         mail.quit()

         return render_template("mail.html", info='"mail sent succesfully"')

     else:
         return render_template("mail.html", info='"mail id does not match password"')


if __name__== "__main__":
    app.run(host='localhost', port=5001, debug=True)



