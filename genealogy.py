from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from AgeAt import calc_age
from datetime import date

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/AgeAt')
def calc_age_at():
    date_naissance = date(1875, 5, 23)
    date_deces = date(1913, 4, 15)
    (years, months, days) = calc_age(date_naissance, date_deces)
    return render_template('ageat.html', years=years, months=months, days=days)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run()
