from flask import Flask,render_template

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']=['postgres://ojhlnysmrfpdty:8a34eb2d5c3c648cd7260eb9dddfdfcf8aad36d7a5886f736fba60b8cf5592ca@ec2-3-222-49-168.compute-1.amazonaws.com:5432/d339viqu0kank6']

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('index.html', name=name)

@app.route("/bank")
def bank():
    return "<p>จารหล่อจังครับ</p>"