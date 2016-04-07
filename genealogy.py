from flask import Flask, render_template, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import SubmitField, DateField
from wtforms.validators import DataRequired

from AgeAt import calc_age
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BlaBlaBla'
manager = Manager(app)
bootstrap = Bootstrap(app)


class AgeAtForm(Form):
    date_naissance = DateField('Date de naissance', format='%Y-%m-%d', validators=[DataRequired()])
    date_deces = DateField('Date du décès', validators=[DataRequired()])
    submit = SubmitField('Calculer')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/AgeAt', methods=['GET', 'POST'])
def calc_age_at():
    years = None
    months = None
    days = None
    form = AgeAtForm()
    if form.validate_on_submit():
        date_naissance = form.date_naissance.data
        date_deces = form.date_deces.data
        if date_deces < date_naissance:
            print("Dates décès avant date de naissance.")
            flash("La date du décès doit être après la date de naissance.")
            years = -1
        else:
            (years, months, days) = calc_age(date_naissance, date_deces)
        return render_template('ageat.html', form=form, years=years, months=months, days=days)
    return render_template('ageat.html', form=form, years=None)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run()
