#!/usr/bin/env python3

from flask import Flask, render_template

from vol import vol_blueprint
from gui import gui_blueprint
from plugs import plugs_blueprint
from tv import tv_blueprint
from new import new_blueprint


app = Flask(__name__)


@app.route('/')
def root():
    return render_template('ugh.html')


def main():
    app.register_blueprint(vol_blueprint, url_prefix='/vol')
    app.register_blueprint(plugs_blueprint, url_prefix='/plugs')
    app.register_blueprint(gui_blueprint, url_prefix='/homecontrol')
    app.register_blueprint(tv_blueprint, url_prefix='/tv')
    app.register_blueprint(new_blueprint, url_prefix='/new')
    app.run(port=1337, debug=True)


if __name__ == '__main__':
    main()
