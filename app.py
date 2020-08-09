from flask import render_template, url_for, Flask, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from server_api import create_app
from server_api.extensions import db
from server_api.models import Key

from datetime import datetime

import hashlib

import functools

import json


app = create_app()


def check_credentials(username, password):
    return username == app.config['ADMIN_USERNAME'] and \
            hashlib.md5(password.encode()).hexdigest() == app.config['ADMIN_PASSWORD']


def login_required(func):
    """Make sure user is logged in before proceeding"""
    @functools.wraps(func)
    def wrapper_login_required(*args, **kwargs):
        if not 'logged_in' in session:
            return redirect(url_for("index", next=request.url))
        return func(*args, **kwargs)
    return wrapper_login_required


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        if check_credentials(request.form.get('username'), \
            request.form.get('password')):
            session['logged_in'] = True
            return redirect(url_for('console'))
            
    return render_template('index.html')


@app.route('/check_key', methods=('POST', ))
def check_key():
    key = request.form.get('key')

    checked_key = Key.query.filter_by(key_string=key).first()

    if not checked_key:
        return json.dumps({
            'error': 'not allowed',
        })

    if checked_key.expiration_date <= datetime.utcnow():
        return json.dumps({
            'error': f'expired {checked_key.expiration_date.strftime("%d %b %Y %H:%M")}'
        })
    
    return json.dumps({
        'status': 'success',
    })


@app.route('/bot_console')
@login_required
def console():
    keys = Key.query.all()

    return render_template('console.html', keys=keys)


@app.route('/generate_keys', methods=('POST', 'DELETE'))
@login_required
def generate_keys():
    if request.method == 'POST':
        i = request.form.get('count', 1, type=int)
        days = request.form.get('days', 1, type=int)
        hours = request.form.get('hours', 1, type=int)

        for i in range(i):
            db.session.add(Key(days=days, hours=hours))
        db.session.commit()
    return redirect(url_for('console'))


@app.route('/delete_expired_keys', methods=('POST', ))
@login_required
def delete_expired_keys():
    if request.method == 'POST':
        if request.form.get('all', False, type=bool):
            Key.query.delete()
        else:
            Key.query.filter(Key.expiration_date < datetime.utcnow()).delete()
        db.session.commit()
    return redirect(url_for('console'))