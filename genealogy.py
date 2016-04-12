from flask import Flask, render_template, flash, session, redirect, url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, NumberRange

from AgeAt import calc_age, date_minus_ymd
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BlaBlaBla'
manager = Manager(app)
bootstrap = Bootstrap(app)


class AgeAtForm(Form):
    date_naissance = DateField("Date de naissance (yyyy-mm-dd)", format='%Y-%m-%d', validators=[DataRequired()])
    date_evenement = DateField("Date de l'évènement", validators=[DataRequired()])
    submit = SubmitField('Calculer')


class ReverseAgeForm(Form):
    date_evenement = DateField("Date de l'évènement (yyyy-mm-dd)", format='%Y-%m-%d', validators=[DataRequired()])
    age_years = IntegerField("Nombre d'année(s) à cette date",
                             validators=[NumberRange(0, 150, message="Le nombre d'année est incorrect.")])
    age_months = IntegerField("Nombre de mois",
                              validators=[NumberRange(0, 11, message="Le nombre de mois est invalide.")])
    age_days = IntegerField("Nombre de jour(s)",
                            validators=[NumberRange(0, 30, message="Le nombre de jours est invalide.")])
    submit = SubmitField('Calculer')


@app.route('/')
def index():
    session['age_is_calculated'] = False
    session['date_naissance_y'] = None
    session['date_evenement_y'] = None
    session['age_years'] = None
    session['age_months'] = None
    session['age_days'] = None
    session['reverse_is_calculated'] = False
    return render_template('index.html')


@app.route('/AgeAt', methods=['GET', 'POST'])
def calc_age_at():
    form = AgeAtForm()
    if form.validate_on_submit():
        date_naissance = form.date_naissance.data
        date_evenement = form.date_evenement.data
        session['date_naissance_y'] = date_naissance.year
        session['date_naissance_m'] = date_naissance.month
        session['date_naissance_d'] = date_naissance.day
        session['date_evenement_y'] = date_evenement.year
        session['date_evenement_m'] = date_evenement.month
        session['date_evenement_d'] = date_evenement.day
        if date_evenement < date_naissance:
            flash("La date de l'évènement doit être après la date de naissance.")
            session['age_is_calculated'] = False
        else:
            (years, months, days) = calc_age(date_naissance, date_evenement)
            session['age_is_calculated'] = True
            session['years'] = years
            session['months'] = months
            session['days'] = days
            return redirect(url_for('calc_age_at'))
    if session.get('date_naissance_y'):
        yr = int(session['date_naissance_y'])
        mn = int(session['date_naissance_m'])
        dy = int(session['date_naissance_d'])
        form.date_naissance.data = date(yr, mn, dy)
    if session.get('date_evenement_y'):
        yr = int(session['date_evenement_y'])
        mn = int(session['date_evenement_m'])
        dy = int(session['date_evenement_d'])
        form.date_evenement.data = date(yr, mn, dy)
    return render_template('ageat.html', form=form,
                           years=session.get('years'), months=session.get('months'), days=session.get('days'))


@app.route('/ReverseAge', methods=['GET', 'POST'])
def reverse_age():
    form = ReverseAgeForm()
    date_naissance = None
    if form.validate_on_submit():
        date_evenement = form.date_evenement.data
        session['date_evenement_y'] = date_evenement.year
        session['date_evenement_m'] = date_evenement.month
        session['date_evenement_d'] = date_evenement.day
        session['age_years'] = form.age_years.data
        session['age_months'] = form.age_months.data
        session['age_days'] = form.age_days.data
        date_naissance = date_minus_ymd(date_evenement,
                                        session['age_years'], session['age_months'], session['age_days'])
        session['reverse_is_calculated'] = True
        session['rev_naissance_y'] = date_naissance.year
        session['rev_naissance_m'] = date_naissance.month
        session['rev_naissance_d'] = date_naissance.day
        return redirect(url_for('reverse_age'))
    if session.get('date_evenement_y'):
        yr = int(session['date_evenement_y'])
        mn = int(session['date_evenement_m'])
        dy = int(session['date_evenement_d'])
        form.date_evenement.data = date(yr, mn, dy)
    if session.get('age_years'):
        form.age_years.data = session['age_years']
    else:
        form.age_years.data = 0
    if session.get('age_months'):
        form.age_months.data = session['age_months']
    else:
        form.age_months.data = 0
    if session.get('age_days'):
        form.age_days.data = session['age_days']
    else:
        form.age_days.data = 0
    return render_template('reverseage.html', form=form,
                           naissance_y=session.get('rev_naissance_y'),
                           naissance_m=session.get('rev_naissance_m'),
                           naissance_d=session.get('rev_naissance_d'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run()
