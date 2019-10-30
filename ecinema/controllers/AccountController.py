import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ecinema.models.Customer import Customer
from ecinema.models.Address import Address

from ecinema.controllers.LoginController import (
    login_required, verify_username_password, get_user
)

from ecinema.tools.validation import (
    validate_name, validate_email, validate_unique_email,
    validate_cvv, validate_cc_number, validate_expiration_date
)

bp = Blueprint('AccountController', __name__, url_prefix='/')


@bp.route('/account', methods=('GET', 'POST'))
@login_required
def account():
    return render_template('account.html')


@bp.route('/editprofile', methods=('GET', 'POST'))
#@login_required
def edit_profile():
    customer = Customer()
    addr = Address()

    user_id = session.get('user_id')
    customer.fetch(user_id)

    info_changed = False

    if(not customer.fetch(user_id)):
        return render_template("index.html")

    if request.method == 'POST':
        first_name = request.form.get('first')
        last_name = request.form.get('last')
        subscribe = request.form.get('subscribe') is not None

        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip')

        error = None
        if first_name != '' and validate_name(first_name):
            customer.set_first_name(first_name)
            info_changed = True

        if last_name != '' and validate_name(last_name):
            customer.set_last_name(last_name)
            info_changed = True

        if customer.get_promo() is not subscribe:
            if customer.get_promo() != subscribe:
                info_changed = True
            customer.set_promo(subscribe)

        if not customer.save():
            error = error + "Issue saving customer details"
            info_changed = False

        # either create, or save addr here
        # get address ID from customer

        addr_id = customer.get_address_id()
        print("addr_id")
        print(addr_id)
        if addr_id is None:
            if (street != '' and city != '' and
                state != '' and zip_code != ''):
                print("About to Create")
                addr.create(street=street, city=city,
                            state=state, zip_code=zip_code)
                customer.set_address_id(addr.get_id())
                customer.save()
                info_changed = True
            else:
                error = "To create a home address, all address information is required"
        else:
            print("about to fetch addr")
            print(addr.fetch(addr_id))

            if street != '':
                print("street")
                print(street)
                addr.set_street(street)
                info_changed = True

            if city != '':
                addr.set_city(city)
                info_changed = True

            if state != '':
                addr.set_state(state)
                info_changed = True

            if zip_code != '':
                addr.set_zip(zip_code)
                info_changed = True

            print("About to save")
            addr.save()

        if error is not None:
            flash(error)

        if info_changed:
            customer.send_profile_change_email()

    address = addr.obj_as_dict(addr.get_id())
    if not address:
        address = {
            'state': 'State (Required)',
            'city': 'City (Required)',
            'street': 'Street (Required)',
            'zip_code': 'ZIP Code (Required)'
        }
    user = customer.obj_as_dict(user_id)
    return render_template('editprofile.html', user=user, address=address)


@bp.route('/manage_payment', methods=('GET', 'POST'))
#@login_required
def manage_payment():
    return render_template('manage_payment.html')


@bp.route('/make_payment', methods=('GET', 'POST'))
#@login_required
def make_payment():
    address = {
        'state': 'State',
        'city': 'City',
        'street': 'Street',
        'zip_code': 'ZIP Code'
    }

    return render_template('make_payment.html', address=address)


@bp.route('/verify_password', methods=('GET', 'POST'))
@login_required
def verify_password():
    # use previous tools to verify the password
    if request.method == 'POST':
        username = session['user_id']
        password = request.form['password']

        user = get_user(username)

        error = None

        if user is not None:
            error = verify_username_password(username, password,
                                             user.get_password())
        if error is None and user is not None:
            return redirect(
                url_for('ResetPasswordController.reset_password')
            )

        flash(error)

    return render_template('verify_password.html')
