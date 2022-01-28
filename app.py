# Flask Setup
import os
from flask import Flask, jsonify, request, abort, render_template
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
gsheet = client.open("Vac").sheet2


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('index.html', name=name)

# An example GET Route to get all reviews
@app.route('/all_reviews', methods=["GET"])
def all_reviews():
    print(gsheet.get_all_records())
    return jsonify(gsheet.get_all_records())