# Flask Setup
import random, psycopg2, os
from datetime import date, datetime
from flask import Flask, jsonify, redirect, request, abort, render_template, url_for
app = Flask(__name__)

def connection():
    conn = psycopg2.connect(
            host="ec2-3-222-49-168.compute-1.amazonaws.com",
            database="d339viqu0kank6",
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])
            
    cur = conn.cursor()

    return cur
# Google Sheets API Setup
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# credential = ServiceAccountCredentials.from_json_keyfile_name("credentials.json",
#                                                              ["https://spreadsheets.google.com/feeds",
#                                                               "https://www.googleapis.com/auth/spreadsheets",
#                                                               "https://www.googleapis.com/auth/drive.file",
#                                                               "https://www.googleapis.com/auth/drive"])
# client = gspread.authorize(credential)


app = Flask(__name__)

@app.route('/')
def home():
    if connection() is not None :
        print("connect success")
    else :
        print("Error connection")
    return render_template('index.html')

@app.route('/add_form' , methods = ["GET","POST"])
def form():
    # gsheet = client.open("Vac").sheet1
    # count = gsheet.row_count
    # print(count)
    if request.method == "POST":

        global email , arr_str

        email = request.form["email"]
        age = request.form["age"]
        dis = request.form["chronic"]
        preg = request.form["pregnancy"]
        gen = request.form["sex"]
        vaxed= request.form["vaxed"]


        print(f"{email}:{age}:{dis}:{preg}:{gen}:{vaxed}")

        dis_dis = dis

        if dis == "chronic0" and preg == "no":
            dis=2
        else:
            dis=1

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
            arr_str = "ยังไม่สามารถฉีดได้"

        # cal
        if len(arr) == 0:
            if age==1:
                arr_str = vaccine[1]
            elif age>1 and dis==1:
                arr_str = random.choice([vaccine[0],vaccine[2]])
            elif age>2:
                arr_str = random.choice([vaccine[2],vaccine[4]])
            else:
                arr_str = vaccine[3]

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        count = gsheet.row_count
        print(count)
        new_row=count+1
        gsheet.resize(new_row)
        gsheet.insert_row([email,age_dis,gen,dis_dis,preg,vaxed,arr_str,dt_string],index = count+1)
        gsheet.delete_row(new_row+1)
        return redirect(url_for("result"))

    else:
        return render_template('form.html')

@app.route('/submit', methods = ["GET","POST"])
def result():
    global arr_str
    return render_template('result.html',arr = arr_str)

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        usr = request.form["username"]
        pwd = request.form["password"]
        if usr == "admin" and pwd == "1234":
            global key
            key = 'true'
            print (key)
            return redirect(url_for("review_data"))
        else :
            return '<h1>email หรือ password ผิด</h1>'
    else :
        return render_template('login.html')

@app.route('/review_data', methods=["GET","POST"])
def review_data():
    global key
    if key == 'true':
        key = 'false'
        gsheet = client.open("Vac").sheet1
        data = gsheet.col_values(7)

        pf = data.count("Pfizer")
        az = data.count("AstraZeneca")
        jj = data.count("Johnson&Johnson")
        sn = data.count("Sinovac")
        md = data.count("Moderna")

        print(data)
        
        
        return render_template('review_data.html',pf = pf,az = az,jj = jj,sn = sn,md = md)

@app.route('/path', methods=["GET","POST"])
def path():
    gsheet = client.open("Vac").sheet1
    if request.method == "POST":
        email_his = request.form["email_his"]
        global cell_list
        cell_list = gsheet.findall(email_his)
        print(email_his)
        print(cell_list)
        if len(cell_list) != 0:
            return redirect(url_for("find_his"))
        else :
            return '<h1>ไม่พบข้อมูล</h1>'
    else:
        return render_template('path_to_find_his.html')

@app.route('/find_his', methods=["GET","POST"])
def find_his():
    gsheet = client.open("Vac").sheet1
    data_his = []
    row_list=[]

    for i in cell_list:
        row_list.append(i.row)
    
    for i in row_list:
        data_temp = []
        data_temp.append(gsheet.cell(i,8).value)
        data_temp.append(gsheet.cell(i,7).value)
        data_his.append(data_temp)

    print(data_his)

    return render_template('find_his.html',data_his = data_his)