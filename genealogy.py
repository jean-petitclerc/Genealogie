from flask import Flask, render_template, flash, session, redirect, url_for
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
    session['years'] = None
    session['date_naissance_y'] = None
    session['date_deces_y'] = None
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
        session['date_naissance_y'] = date_naissance.year
        session['date_naissance_m'] = date_naissance.month
        session['date_naissance_d'] = date_naissance.day
        session['date_deces_y'] = date_deces.year
        session['date_deces_m'] = date_deces.month
        session['date_deces_d'] = date_deces.day
        if date_deces < date_naissance:
            flash("La date du décès doit être après la date de naissance.")
        else:
            (years, months, days) = calc_age(date_naissance, date_deces)
            session['years'] = years
            session['months'] = months
            session['days'] = days
        return redirect(url_for('calc_age_at'))
    if session.get('date_naissance_y'):
        yr = int(session['date_naissance_y'])
        mn = int(session['date_naissance_m'])
        dy = int(session['date_naissance_d'])
        form.date_naissance.data = date(yr, mn, dy)
    if session.get('date_deces_y'):
        yr = int(session['date_deces_y'])
        mn = int(session['date_deces_m'])
        dy = int(session['date_deces_d'])
        form.date_deces.data = date(yr, mn, dy)
    return render_template('ageat.html', form=form,
                           years=session.get('years'), months=session.get('months'), days=session.get('days'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run()
