#!/usr/bin/env python

from flask import Blueprint, request
from flask import render_template
import subprocess
from subprocess import PIPE

gui_blueprint = Blueprint('ui', __name__)

@gui_blueprint.route('/')
def ui():
    return render_template('ui.html')
