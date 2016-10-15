from flask import Blueprint
from flask import g
from flask import flash
from flask import abort
from flask import request
from flask import session
from flask import render_template
from flask import url_for
from flask import redirect
from dock.common import log
from ..model.user import User
from ..model.post import Post
from ..model.scheduler import Scheduler
logger = log.get_logger('ebbinghaus_calendar.view')

blueprint = Blueprint('ebbinghaus_calendar',
                      __name__)


@blueprint.before_request
def before_request():
    g.user = None
    if 'email' in session:
        g.user = User.from_email(session['email'])


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        if not all(
            key in request.form
            for key in ['email', 'password', 'password2']
        ):
            abort(404)
        if request.form['password'] != request.form['password2']:
            abort(404)
        user = User.from_form(request.form.to_dict())
        if not user.registed():
            user.register()
            logger.info('register user', user.email)
        return redirect(url_for('.login'))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        if not all(
            key in request.form
            for key in ['email', 'password']
        ):
            abort(401)
        user = User.from_form(request.form.to_dict())
        if not user.valid():
            logger.info('invalid user',
                        ('email', user.email, 'password', user.password))
            return render_template('login.html')
        logger.info('login usr', user.email)
        session['email'] = request.form['email']
        return redirect(url_for('.edit_post'))


@blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email', None)
    return render_template('login.html')


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/post/edit', methods=['GET', 'POST'])
def edit_post():
    if g.user is None:
        flash('Please Login')
        return redirect(url_for('.login'))
    if request.method == 'GET':
        return render_template('edit_post.html')
    if not all(
        key in request.form
        for key in ['question', 'answer']
    ):
        abort(401)
    data = request.form.to_dict()
    data.update(user_id=g.user.id)
    post = Post.from_form(**data)
    post.dump()
    scheduler = Scheduler()
    scheduler.schedule(post)
    return redirect(url_for('.edit_post'))


@blueprint.route('/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):
    if g.user is None:
        return redirect(url_for('.login'))
    post = Post.from_id(post_id)
    return render_template('post.html', question=post.question,
                           answer=post.answer)


@blueprint.route('/question/<post_id>', methods=['GET', 'POST'])
def question(post_id):
    if g.user is None:
        return redirect(url_for('.login'))
    post = Post.from_id(post_id)
    return render_template('question.html', question=post.question)


@blueprint.route('/answer/<post_id>', methods=['GET', 'POST'])
def anwser(post_id):
    if g.user is None:
        return redirect(url_for('.login'))
    post = Post.from_id(post_id)
    return render_template('answer.html', answer=post.answer)
