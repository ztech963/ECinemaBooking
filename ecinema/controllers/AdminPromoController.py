from datetime import datetime
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ecinema.controllers.LoginController import admin_login_required
from ecinema.tools.validation import (
    validate_name, validate_expiration_date, validate_promo_code, validate_unlinked_promo, validate_percentage
)
from ecinema.tools.clean import create_datetime_from_sql

from ecinema.models.Promo import Promo
from ecinema.controllers.AdminShowtimeController import create_datetime

bp = Blueprint('AdminPromosController', __name__, url_prefix='/')

@bp.route('/manage_promos', methods=('GET', 'POST'))
@admin_login_required
def manage_promos():
    promo = Promo()

    if request.method == 'POST':
        delete_promo_id = request.form.get('delete_promo_id')
        edit_promo_id = request.form.get('edit_promo_id')

        if delete_promo_id != None and promo.fetch(delete_promo_id):
            if validate_unlinked_promo(delete_promo_id):
                promo.delete(delete_promo_id)
            else:
                error = "Promo is linked to a booking. Cannot delete right now"
                flash(error)
        elif edit_promo_id != None and promo.fetch(edit_promo_id):
            return redirect(url_for('AdminPromosController.edit_promo', pid=edit_promo_id))

    # get a list of all promos
    promos = promo.get_all_promos()
    return render_template('manage_promos.html', promos=promos)

@bp.route('/edit_promo/<pid>', methods=('GET', 'POST'))
@admin_login_required
def edit_promo(pid):
    promo_id = pid
    promo = Promo()
    print(promo.fetch(promo_id))

    if request.method == 'POST':

        code = request.form.get('code')
        percent = request.form.get('percent')
        expiration = request.form.get('expiration')
        description = request.form.get('description')

        error = None

        if code != '' and not validate_name(code):
            error = "Promotion Code is invalid"
        elif code !='' and not validate_promo_code(code):
            error = "Promotion Code already exists"
        elif code != '':
            promo.set_code(code)

        if description != '':
            promo.set_promo_description(description)

        if validate_percentage(percent):
            promo.set_promo(percent)
        else:
            error = "Invalid percentage"

        if expiration:
            promo_date_dict = expiration.split("-")
            date = datetime(int(promo_date_dict[0]), int(promo_date_dict[1]), int(promo_date_dict[2]))

            print("DAT!!")
            print(date)
            if date != '' and not validate_expiration_date(date):
                error = "Promotion Valid Until Date is invalid"
            elif date != '':
                promo.set_exp_date(expiration)
        else:
            error = "Invalid expiration date"


        promo.save()

        if error is None:
            return redirect(url_for('AdminPromosController.manage_promos'))
        else:
            flash(error)

    info = promo.obj_as_dict(promo_id)
    return render_template('edit_promotion.html', promo=info)

@bp.route('/create_promo', methods=('GET', 'POST'))
@admin_login_required
def create_promo():
    if request.method == 'POST':

        code = request.form['code']
        percent = request.form['percent']
        expiration = request.form['expiration']
        description = request.form.get('description')

        # validate all data, everything must be correct
        error = None

        expiration_date = create_datetime(expiration, "01:00")
        if not expiration_date:
            error = "Invalid expiration date"
        if not validate_name(code):
            error = "Promotion Code is invalid"
        elif not validate_promo_code(code):
            error = "Promotion Code already exists"
        elif not validate_expiration_date(expiration_date, promo=True):
            error = "Promotion Valid Until Date is invalid"
        elif not validate_percentage(percent):
            error = "Promotion percentage is invalid"


        if error is None:
            # if error is None, create a promo
            new_promo = Promo()
            new_promo.create(promo=percent,code=code,promo_description=description, exp_date=expiration)

            # then return to add promo
            return redirect(url_for('AdminPromosController.manage_promos'))

        flash(error)


    return render_template('make_promotion.html')
