from flask import Flask, render_template, url_for, request, flash, \
    session, redirect, abort

from jinja2 import Environment, Template, FunctionLoader, FileSystemLoader
from string import ascii_letters
from random import sample, randint, shuffle


app = Flask(__name__)
app.config['SECRET_KEY'] = sample(ascii_letters, randint(10, 30))
shuffle(app.config['SECRET_KEY'])

data = [{'Name': 'Tec', 'Age': 16, 'Job': 'ML'},
        {'Name': 'Ovad', 'Age': 17, 'Job': 'Physics'},
        {'Name': 'jedoron', 'Age': 14, 'Job': 'friend'}]


@app.route('/greeting')
@app.route('/greeting/<user_name>')
@app.route('/greeting/<user_name>/<int:id>')
def index(user_name='Tec', id=3141):
    print(url_for('index', user_name=user_name, id=id))
    return render_template('user_greeting.html', user_name=user_name, user_id=id)


@app.route('/')
@app.route('/mainpage')
def to_main():
    print(url_for('to_main'))
    return render_template('title_templ.html', title='Main Page')


@app.route('/about')
def to_info():
    print(url_for('to_info'))
    return render_template('title_templ.html', title='Info about site')


@app.route('/info_about')
def user_info():
    print(url_for('user_info'))
    return render_template('Jinja_templ.html', users=data)


@app.route('/register', methods=['POST', 'GET'])
def req():
    if request.method in ['POST', 'GET']:
        print(request.form)
        if 'name' in request.form:
            for i in request.form['name']:
                if i not in ascii_letters:
                    flash('Incorrect name', category='error')
                    break
            else:
                flash('Sent successfully', category='success')
    return render_template('reqister_form.html', title='Register form')


@app.route('/collect', methods=['POST', 'GET'])
def collect():
    if request.method in ['POST', 'GET']:
        print(request.form)
        for i in request.form['name']:
            if i not in ascii_letters:
                flash('Incorrect name', category='error')
                break
        else:
            flash('Sent successfully', category='success')
    return render_template('title_templ.html', title=f'Thanks {request.form["name"]}')


@app.errorhandler(404)
def handle404(error):
    return render_template('404error.html')


@app.route('/login', methods=['POST', "GET"])
def login():
    print(session)
    if 'UserLogged' in session:
        return redirect(url_for('profile', user_name=session['UserLogged']))
    if request.method in ['POST']:
        session['UserLogged'] = request.form['name']
        session['password'] = request.form['password']
        return redirect(url_for('profile', user_name=session['UserLogged']))

    return render_template('login_form.html')

@app.route('/profile/<user_name>')
def profile(user_name):
    if 'UserLogged' not in session or user_name != session['UserLogged']:
        abort(401)
    return render_template('user_greeting.html', user_name=user_name)



if __name__ == '__main__':
    app.run(debug=True)
