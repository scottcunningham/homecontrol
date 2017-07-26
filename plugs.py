#!/usr/bin/env python3

from flask import Blueprint
from flask import render_template

plugs_blueprint = Blueprint('plugs', __name__)


@plugs_blueprint.route('/')
def view():
    return render_template('plugs.html')
