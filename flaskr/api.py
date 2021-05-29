from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from webargs import fields
from webargs.flaskparser import use_args

from .devices import get_device
from .db import get_db
from uuid import uuid4

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/<int:id>/state', methods=('GET',))
@use_args({'token': fields.Str(required=True)}, location="query")
def state(args, id):
    if request.method == 'GET':
        device = get_device(id, False)
        token = args['token']
        print(token)
        print(device['access_token'])
        if (device['access_token'] == token):
            return str(device['state'])
        else:
            abort(403)
    abort(400)