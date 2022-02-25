import sqlite3
import os
import sqlite3
from string import ascii_letters, digits

from flask import Flask, render_template, url_for, request, session, g, flash, \
    abort, redirect, make_response
from werkzeug.security import generate_password_hash

from TecHeresHub.scripts.Config import Config
from TecHeresHub.scripts.UDataBase import UDataBase
from TecHeresHub.scripts.Forms import LoginForm, RegisterForm

app = Flask(__name__)
app.config.from_object(Config)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'TecHeresHub/tmp/sql/users.db')))
db = None
print(app.config['DATABASE'])


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    database = connect_db()
    with app.open_resource('request', mode='r') as f:
        database.cursor().executescript(f.read().strip())
    database.commit()
    database.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return UDataBase(g.link_db)


@app.before_request
def ret_dbase():
    global db
    db = get_db()


@app.teardown_appcontext
@app.teardown_request
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.errorhandler(404)
def handle404(error):
    return render_template('404error.html')


@app.route('/')
@app.route('/mainpage')
def to_main():
    if 'visited' in session:
        session['visited'] += 1
    else:
        session['visited'] = 1
    return render_template('main_page_posts.html', title='Main Page',
                           posts=db.get_posts(), times=session['visited'], user_name=session.get('logged'))


@app.route('/greeting')
@app.route('/greeting/<user_name>')
@app.route('/greeting/<user_name>/<int:id>')
def index(user_name='Tec', id=3141):
    print(url_for('index', user_name=user_name, id=id))
    return render_template('user_greeting.html', user_name=user_name, user_id=id)


@app.route('/topusers')
def top_users():
    return render_template('top_users.html', users=db.get_users(), title='Top Users')


@app.route('/addpost', methods=['POST', "GET"])
def add_post():
    if request.method == 'POST':
        res = db.add_post(request.form['author'], request.form['title'], request.form['post'])
        if res:
            flash('Post add successfully', category='success')
        else:
            flash('Error while creating post', category='error')
    return render_template('addpost.html')


@app.route('/post/<id>')
def get_post(id):
    db.cur.execute('''UPDATE users_posts 
                    SET visited = visited + 1
                    WHERE id = ?''', id)
    db.db.commit()
    post = db.get_post(id)
    if not post:
        abort(401)
    return render_template('post.html', title=post['title'], post=post)


@app.route('/login', methods=['POST', 'GET'])
def login():

    form = LoginForm()
    print(session.get('logged'))
    if session.get('logged'):
        return redirect(url_for('index', user_name=session['logged']))
    res = make_response(render_template('login_form.html', form=form))
    if form.validate_on_submit():
        print(form.email.data)
        chpass, name = db.check_login(form.email.data,
                                      form.password.data)
        if not chpass:
            flash('Wrong email/password', category='error')
            return res
        else:
            session['logged'] = str(name)
            return redirect(url_for('index', user_name=session['logged']))
    return res


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if session.get('logged'):
        return redirect(url_for('index', user_name=session['logged']))
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            flash("Passwords don't match themselves", category='error')
        else:
            for i in form.name.data:
                if i not in ascii_letters + digits:
                    flash('Incorrect name', category='error')
                    break
            else:
                flash('Sent successfully', category='success')

                res = db.add_user(form.email.data, form.name.data,
                                  generate_password_hash(form.password.data))
                if res:
                    session['logged'] = request.form['name']
                    return redirect(url_for('index', user_name=request.form['name']))
                else:
                    flash('Such user already exists', category='error')

    return render_template('reqister_form.html', title='Register form', form=form)


if __name__ == '__main__':
    app.run(debug=True)
