from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape

app = Flask(_name_)

# FIX: correct number of slashes + proper config value
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # FIX: Item not item
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/hello')
@app.route('/hello/')
@app.route('/hello/<user_name>')
def hello(user_name=None):
    return render_template('home.html', user=user_name)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        new_item = Item(name=name)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

# FIX: parameter name must match route
@app.route('/update/<int:item_id>', methods=['GET', "POST"])
def update(item_id):
    # FIX: correct function call
    item = Item.query.get_or_404(item_id)

    if request.method == 'POST':
        item.name = request.form['name']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update.html', item=item)

# FIX: parameter name + delete correct object
@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)  # FIX: delete object, not id
    db.session.commit()
    return redirect(url_for('index'))