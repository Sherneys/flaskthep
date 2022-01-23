from flask import Flask,render_template

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ["postgres://reuxpjnntrhhin:d25385a061597b190254ebcc134272c8778f53931510104095b94d490b1519ce@ec2-18-234-17-166.compute-1.amazonaws.com:5432/d7qvb8um38c7o"]

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('index.html', name=name)

@app.route("/bank")
def bank():
    return "<p>จารหล่อจังครับ</p>"