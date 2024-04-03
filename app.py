from flask import Flask, redirect, request, jsonify, render_template, session
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)
app.secret_key = 'pratiksha1998'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pratiksha1998@localhost/users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

logging.basicConfig(filename='app.log', level=logging.INFO)

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password


with app.app_context():
    db.create_all()
    db.session.commit()


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = UserInfo.query.filter_by(username=username).first()
            if user and user.password == password:
                session['isLoggedIn'] = True
                session['username'] = username.capitalize()
                return redirect('/enter_details')
            else:
                raise Exception("Invalid username or password")
        except Exception as e:
            logging.error(f"Error during login: {str(e)}")
            return render_template('login.html', message="Invalid username or password")


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        try:
            if len(username) < 4 or len(password) < 4:
                raise ValueError("Username and password must be at least 4 characters long")
            existing_user = UserInfo.query.filter_by(username=username).first()
            if existing_user:
                raise ValueError("Username already exists")
            new_user = UserInfo(username, password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('login.html', message="Registration successful. Please login.")
        except ValueError as ve:
            logging.error(f"Error during registration: {str(ve)}")
            return render_template('register.html', message=str(ve))


@app.route('/logout')
def logout():
    session.pop('isLoggedIn', None)
    session.pop('username', None)
    return redirect('/login')


@app.errorhandler(Exception)
def handle_error(error):
    logging.error(f"Unhandled exception: {str(error)}")
    return render_template('error.html', error=error), 500

# Main route
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
