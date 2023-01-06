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
            
    return conn

def insert(a):
    conn = connection()
    cur = conn.cursor()
    cur.execute(a)

    conn.commit()
    cur.close()
    conn.close()

def select(a):
    conn = connection()
    cur = conn.cursor()
    cur.execute(a)
    result = cur.fetchall()

    cur.close()
    conn.close()

    return result

app = Flask(__name__)

@app.route('/')
def home():
    result = select('SELECT * FROM public."Vac" WHERE "ID" = 1')
    print(result)
    return render_template('index.html')

@app.route('/add_form' , methods = ["GET","POST"])
def form():
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
        dt_string = now.strftime("%Y/%m/%d")


        statement = f'''INSERT INTO public."Vac"(
	"Email", "Age", "Sex", "Chornic", "Pregnancy", "Vaxed", "Vac Reccommend", "Date")
	VALUES ('{email}',{age_dis},'{gen}','{dis_dis}','{preg}','{vaxed}','{arr_str}','{dt_string}')'''
        insert(statement)
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
        statement = '''SELECT "Vac Reccommend" FROM public."Vac"'''
        data = select(statement)

        data_new=[]
        for i in range (len(data)):
            data_new.append(data[i][0])

        pf = data_new.count('Pfizer              ')
        az = data_new.count('AstraZeneca         ')
        jj = data_new.count('Johnson&Johnson     ')
        sn = data_new.count('Sinovac             ')
        md = data_new.count('Moderna             ')

        print(data_new) 
        
        
        return render_template('review_data.html',pf = pf,az = az,jj = jj,sn = sn,md = md)

@app.route('/path', methods=["GET","POST"])
def path():
    if request.method == "POST":
        global email_his
        email_his = request.form["email_his"]
        print(email_his)
        return redirect(url_for("find_his"))
    else:
        return render_template('path_to_find_his.html')

@app.route('/find_his', methods=["GET","POST"])
def find_his():
    global email_his
    data_his = select(f'''SELECT "Date", "Vac Reccommend"
	    FROM public."Vac" WHERE "Email" = '{email_his}' ''')

    print(data_his)

    return render_template('find_his.html',data_his = data_his)