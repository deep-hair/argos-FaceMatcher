import os,logging

from PIL import Image
from flask import render_template, flash, redirect, url_for, request, Response
from flask_login import current_user, login_user, logout_user, login_required
from torchvision import io
from werkzeug.urls import url_parse

from app import app, db, model
from app.forms import LoginForm, RegistrationForm
from app.frames import gen_frames
from app.models import User

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user is None or not user.check_password(request.form.get('password')):
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
    return redirect('index')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if request.method == "POST":
        print('here')
        user = User(username=request.form.get('username'), email=request.form.get('email'))
        user.set_password(request.form.get('password'))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/live_feed')
def live_feed():

    return render_template('live_feed.html', title='Live Feed')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cam2left')
def cam2left():
    os.system('pyezviz -u lucas.saban@ensae.fr -p lla30360_ camera --serial G81454628 move --direction left --speed 1')
    logging.info('Turned Left')
    return 'nothing'


@app.route('/cam2right')
def cam2right():
    os.system('pyezviz -u lucas.saban@ensae.fr -p lla30360_ camera --serial G81454628 move --direction right --speed 1')
    logging.info('Turned Right')
    return 'nothing'


@app.route('/cam2top')
def cam2top():
    os.system('pyezviz -u lucas.saban@ensae.fr -p lla30360_ camera --serial G81454628 move --direction up --speed 1')
    logging.info('Turned Top')
    return 'nothing'


@app.route('/cam2bottom')
def cam2bottom():
    os.system('pyezviz -u lucas.saban@ensae.fr -p lla30360_ camera --serial G81454628 move --direction down --speed 1')
    logging.info('Turned Bottom')
    return 'nothing'