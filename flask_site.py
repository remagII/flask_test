from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return "Index Page"

@app.route('/hello')
@app.route('/hello/')
@app.route('/hello/<user_name>')
def hello(user_name=None):
    return render_template('home.html', user=user_name)
    # if user_name:
    #     return f"<h1>Hi {escape(user_name)}! Welcome to my Flask Site</h1>"
    # else:
    #     return "<h1>Hi! Welcome to my Flask Site</h1>"