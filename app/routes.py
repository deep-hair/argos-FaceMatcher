from flask import render_template, flash, redirect, url_for, request, Response
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.frames import gen_frames
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Optimus Prime'}
    return render_template('index2.html', user = user)

@app.route('/login', methods=['GET', "POST"])
def login():
    print('test')
    if current_user.is_authenticated:
        print('here')
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == "POST":
        print('wtf')
        print(request.form.get('username'))
        user = User.query.filter_by(username=request.form.get('username')).first()

        if user is None or not user.check_password(request.form.get('password')):
            print('auth error')
            flash('Mot de passe ou login invalide')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        print('auth succes')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        print('auth')
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        print('try')
        user = User(username=form.Username.data, email=form.Email.data)
        user.set_password(form.Password.data)
        db.session.add(user)
        db.session.commit()
        flash("Enregistrement de l'utilisateur réussi.")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/live_feed')
def live_feed():
    return render_template('live_feed.html', title='Live Feed')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')