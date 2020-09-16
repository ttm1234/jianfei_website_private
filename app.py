import datetime
from flask import Flask, Response, request, render_template, session, redirect, url_for

from expection import BaseError
from extension import conn_init
from config import config
from logics.user import logic_hello, logic_post_login, logic_post_clock


def init_app():
    app = Flask(__name__)
    app.secret_key = config['secret_key']
    app.permanent_session_lifetime = datetime.timedelta(days=200)
    conn_init()
    return app


app = init_app()


@app.route('/')
def hello():
    user_id = session.get('user_id')
    r = logic_hello(user_id)
    return Response(r) if isinstance(r, str) else r


@app.route('/login', methods=['POST'])
def post_login():
    data = request.form.to_dict()
    qq, password = data['qq'], data['password']
    r = logic_post_login(qq, password)
    return Response(r) if isinstance(r, str) else r


@app.route('/quit', methods=['POST'])
def post_quit():
    session.clear()
    return redirect(url_for('hello'))


@app.route('/clock', methods=['POST'])
def post_clock():
    data = request.form.to_dict()
    user_id = session['user_id']
    r = logic_post_clock(user_id, data)
    return Response(r) if isinstance(r, str) else r


@app.errorhandler(BaseError)
def zero_division_error(e):
    return Response(e.msg)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=False)
