from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/")
def index():
    template = jinja_env.get_template('temps.html')
    return template.render()

@app.route("/")
def display_form():
    template = jinja_env.get_template('temps.html')
    return template.render(username = "", username_error = "", password = "", password_error = "", password_confirm = "", passconf_error = "", email = "", email_error = "")

@app.route("/", methods = ['POST'])
def validate_form():
    template = jinja_env.get_template('temps.html')

    username = request.form['username']
    password = request.form['password']
    password_conf = request.form['password_confirm']
    email = request.form['email']

    username_error = ""
    password_error = ""
    passconf_error = ""
    email_error = ""

    if len(username) < 3 or len(username) > 20:
        username_error = "Name must be between 3 and 20 characters in length."
        username = ""

    if len(password) < 3 or len(password) > 20:
        password_error = "Password must be between 3 and 20 characters in length."

    if password != password_conf:
        passconf_error = "Password and confirmation do not match."

    if len(email) > 0:
        if (len(email) < 3 or len(email) > 20):
            email_error = "Email must be between 3 and 20 characters in length."
            email = ""
        elif email.count('@') != 1 or email.count('.') != 1 or email.count(" ") != 0:
            email_error = "Email is not valid.  Must have exactly one '@' and '.' and contain no spaces."
            email = ""

    if not username_error and not password_error and not passconf_error and not email_error:
        return redirect('/welcome-page?username={0}'.format(username))
    else:
        return template.render(username_error = username_error, password_error = password_error,
        passconf_error = passconf_error, email_error = email_error, username = username, email = email)

@app.route('/welcome-page')
def valid_time():
    username = request.args.get('username')
    return '<h1>User profile suscessfully created! Welcome {0}!</h1>'.format(cgi.escape(username))


app.run()