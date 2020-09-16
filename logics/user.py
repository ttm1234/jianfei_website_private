from flask import render_template, session, redirect, url_for

from expection import BaseError
from models import User, Clock


default_beizhu = '如果有备注写这里'


def template_clock_paging(user_id):
    user = User.get_one(user_id)
    clocks, clock_count = Clock.paging({
        'user_id': user_id,
    })
    return render_template('index.html', user=user, clocks=clocks, clock_count=clock_count, default_beizhu=default_beizhu)


def logic_hello(user_id):
    if user_id is None:
        return render_template('index_auth.html')

    return template_clock_paging(user_id)


def logic_post_login(qq, password):
    user = User.one_from_qq(qq)
    if user is None:
        raise BaseError('没有这个用户')
    if not user.valid_password(password):
        raise BaseError('密码错误')
    session['user_id'] = user.id

    return redirect(url_for('hello'))


def logic_post_clock(user_id, data):
    user = User.get_one(user_id)
    if user is None:
        raise BaseError('没有这个用户')

    if data['msg'] == default_beizhu:
        data['msg'] = ''

    m = Clock.new(user, data)

    return redirect(url_for('hello'))


def logic_get_all():
    class UserInfo(object):

        def __init__(self):
            self.user = None
            self.clocks = clocks
            self.clock_count = None
    # ===========================================
    users, _ = User.paging({})
    all_infos = []
    for user in users:
        clocks, clock_count = Clock.paging({
            'user_id': user.id,
        })

        m = UserInfo()
        m.user = user
        m.clocks = clocks
        m.clock_count = clock_count

        all_infos.append(m)

    return render_template('index2.html', all_infos=all_infos)
