from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/log')
def log():
    return render_template('log.html')

@app.route('/home')
def home_screen():
    data={
        'id': session['user_id']
    }
    return render_template('/home.html', user= User.get_by_id(data))

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email", "login")
        return redirect('/log')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/log')
    session['user_id'] = user.id
    return redirect('/home')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/log')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/home')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

