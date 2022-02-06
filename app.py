# Flask Setup
import os ,uuid ,random
from flask import Flask, jsonify, redirect, request, abort, render_template, url_for
app = Flask(__name__)
# Google Sheets API Setup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

credential = ServiceAccountCredentials.from_json_keyfile_name("credentials.json",
                                                             ["https://spreadsheets.google.com/feeds",
                                                              "https://www.googleapis.com/auth/spreadsheets",
                                                              "https://www.googleapis.com/auth/drive.file",
                                                              "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credential)


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_form' , methods = ["GET","POST"])
def form():
    gsheet = client.open("Vac").sheet1
    count = gsheet.row_count
    print(count)
    if request.method == "POST":
        age = request.form["age"]
        dis = request.form["chronic"]
        preg = request.form["pregnancy"]
        gen = request.form["sex"]
        vaxed= request.form["vaxed"]


        print(f"{age}:{dis}:{preg}:{gen}:{vaxed}")

        dis_dis = dis

        if dis == "chronic0" and preg == "no":
            dis = 2
        else:
            dis = 1

        vaccine=["Moderna","Pfizer","AstraZeneca","Sinovac","Johnson&Johnson"]
        age=int(age)
        age_dis = age
        arr=[]

        # จัดหมวดหมู่อายุ
        if age>=12 and age<=17:
            age=1
        elif age >=18 and age<=59:
            age=2
        elif  age >= 60:
            age=3
        else:
            arr.append("ยังไม่สามารถฉีดได้")

        # cal
        if len(arr) == 0:
            if age==1:
                arr.append(vaccine[1])
            elif age>1 and dis==1:
                arr.append(random.choice([vaccine[0],vaccine[2]]))
            elif age>2:
                arr.append(random.choice([vaccine[2],vaccine[4]]))
            else:
                arr.append(vaccine[3])

        global arr_str
        arr_str = ''
        for i in arr:
            arr_str += i + " "

        arr_str = arr_str[:-1]
        
        count = gsheet.row_count
        print(count)
        new_row = count+1
        gsheet.resize(new_row)
        gsheet.insert_row([str(uuid.uuid4()),age_dis,gen,dis_dis,preg,vaxed,arr_str],index = count+1)
        gsheet.delete_row(new_row+1)
        return redirect(url_for("result"))

    else:
        return render_template('form.html')

@app.route('/submit', methods = ["GET","POST"])
def result():
    return render_template('result.html',arr = arr_str)

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        usr = request.form["username"]
        pwd = request.form["password"]
        if usr == "admin" and pwd == "1234":
            return redirect(url_for("review_data"))
        else :
            return redirect(url_for("failed"))
    else :
        return render_template('login.html')

@app.route('/failed', methods=["GET","POST"])
def failed():
        return render_template('failed.html')

@app.route('/review_data')
def review_data():
    gsheet = client.open("Vac").sheet1
    data = gsheet.col_values(7)

    pf = data.count("Pfizer")
    aze = data.count("AstraZeneca Johnson&Johnson") + data.count("Moderna AstraZeneca")
    john = data.count("AstraZenecan Johnson&Johnson")
    sin = data.count("Sinovac")
    mod = data.count("Moderna AstraZeneca")

    print(data)
    
    
    # return render_template('review_data.html',pf = pf,aze = aze,john = john,sin = sin,mod = mod)
    return "<h1>{data}</h1>"