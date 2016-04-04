from flask import Flask, render_template
from flask_script import Manager
from AgeAt import calc_age
from datetime import date

app = Flask(__name__)
manager = Manager(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/AgeAt')
def calc_age_at():
    date_naissance = date(1875, 5, 23)
    date_deces = date(1913, 4, 15)
    (years, months, days) = calc_age(date_naissance, date_deces)
    return render_template('ageat.html', years=years, months=months, days=days)


if __name__ == '__main__':
    manager.run()
