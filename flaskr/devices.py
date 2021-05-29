from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from marshmallow.fields import Integer
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db
from uuid import uuid4

bp = Blueprint('devices', __name__)

@bp.route('/')
def index():
    db = get_db()
    if (g.user is not None):
        print(g.user['id'])
        devices = db.execute(
            'SELECT p.id, name, description, author_id, access_token, username, state'
            ' FROM device p JOIN user u ON p.author_id = u.id WHERE u.id = ?'
            ' ORDER BY created DESC ',
            (g.user['id'],)
        ).fetchall()
        return render_template('devices/index.html', devices=devices)
    else:
        return render_template('devices/index.html')
    
    

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        rand_token = uuid4()
        error = None

        if not name:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO device (name, description, access_token, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (name, description, str(rand_token), g.user['id'])
            )
            db.commit()
            return redirect(url_for('devices.index'))

    return render_template('devices/create.html')

def get_device(id, check_author=True):
    device = get_db().execute(
        'SELECT p.id, name, description, author_id, access_token, username, state'
        ' FROM device p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if device is None:
        abort(404, f"Device id {id} doesn't exist.")

    if check_author and device['author_id'] != g.user['id']:
        abort(403)

    return device

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    device = get_device(id)

    if request.method == 'POST':
        name = request.form['title']
        description = request.form['description']
        error = None

        if not name:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE device SET name = ?, description = ?'
                ' WHERE id = ?',
                (name, description, id)
            )
            db.commit()
            return redirect(url_for('devices.index'))

    return render_template('devices/update.html', device=device)

@bp.route('/<int:id>/switch', methods=('POST',))
@login_required
def switch(id):
    get_device(id)
    try:
        if request.method == 'POST':
            switch_val = request.data.decode('UTF-8')
            db = get_db()
            if (switch_val == "true"):
                db.execute('UPDATE device SET state = ? WHERE id = ?', (1, id))
            elif (switch_val == "false"):
                db.execute('UPDATE device SET state = ? WHERE id = ?', (0, id))
            db.commit()
            return "Success"
        else:
            return "Failure"
    except Exception:
        return "Failure"

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_device(id)
    db = get_db()
    db.execute('DELETE FROM device WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('devices.index'))
