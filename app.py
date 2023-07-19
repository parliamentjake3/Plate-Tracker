from flask import Flask, render_template, request
from flask import session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# home page
@app.route('/')
def home():
    return render_template('home.html')

# Register Page (Expect no POST)
@app.route('/register')
def register_get():
    return render_template('register.html')

# Register Page (Expect POST)
@app.route('/register', methods=['POST'])
def register_post():

    # Declare user input from registry
    username = request.form['username']
    password = request.form['password']
    password_confirmation = request.form['password_confirmation']

    # USERNAME PARAMATERS

    # Username must be at least 5 characters long
    if(len(username) < 5):
        return render_template('register.html', error_message='Username must be 5 characters long')
    
    # Username cannot contain spaces
    if " " in username:
        return render_template('register.html', error_message='Username cannot contain spaces')

    # PASSWORD PARAMATERS

    # Checks password confirmation
    if(password != password_confirmation):
        return render_template('register.html', error_message='Passwords do not match')
    
    #Password cannot contain spaces
    if " " in password:
        return render_template('register.html', error_message='Password cannot contain spaces')
    
    if(len(password) < 8):
        return render_template('register.html', error_message='Password must be 8 characters long')

    # Save new user into database
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return 'Registration successful!'

if __name__ == '__main__':
    app.run()


