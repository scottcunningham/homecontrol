#!/usr/bin/env python

from flask import Flask, render_template

from vol import vol_blueprint
from fan import fan_blueprint
from gui import gui_blueprint
from lamp import lamp_blueprint
from plugs import plugs_blueprint


app = Flask(__name__)


@app.route('/')
def root():
    return render_template('ugh.html')


if __name__ == '__main__':
    app.register_blueprint(vol_blueprint, url_prefix='/vol')
    app.register_blueprint(fan_blueprint, url_prefix='/fan')
    app.register_blueprint(lamp_blueprint, url_prefix='/lamp')
    app.register_blueprint(plugs_blueprint, url_prefix='/plugs')
    app.register_blueprint(gui_blueprint, url_prefix='/homecontrol')
    app.run(port=1337, debug=True)
