"""Routes and views for the Bottle application."""

from bottle import redirect, request, route, view

from active_user_service import (
    build_active_user,
    empty_user_form,
    load_active_users,
    save_active_users,
    validate_active_user,
)
from order_service import build_order, empty_form, load_orders, save_orders, validate_order

@route('/')
@view('index')
def home():
    """render the auth_reg page"""
    return dict()

@route('/main')
@view('./main')
def main():
    return dict()
@route('/reg-auth')
@view('./reg-auth')
def reg_auth():
    return dict()


@route('/orders', method='GET')
@view('orders')
def orders_page():
    """Render the оформленные заказы page with a clean form."""

    return {
        "orders": load_orders(),
        "errors": {},
        "form": empty_form(),
    }


@route('/orders', method='POST')
@view('orders')
def add_order():
    """Validate form input, save a new order, or show errors on the same page."""

    # Bottle keeps submitted values in request.forms. We copy only known fields
    # so unexpected input cannot be written to the JSON file.
    form = {
        "number": (request.forms.getunicode("number") or "").strip(),
        "author": (request.forms.getunicode("author") or "").strip(),
        "text": (request.forms.getunicode("text") or "").strip(),
        "date": (request.forms.getunicode("date") or "").strip(),
        "phone": (request.forms.getunicode("phone") or "").strip(),
    }

    orders = load_orders()
    errors = validate_order(form, orders)

    if errors:
        # The same template receives the previous form values, so the user does
        # not need to type everything again after a validation error.
        return {
            "orders": orders,
            "errors": errors,
            "form": form,
        }

    orders.append(build_order(form))
    save_orders(orders)

    # Redirect after successful POST prevents duplicate submissions and clears
    # the form fields on page reload.
    redirect('/orders')


@route('/active-users', method='GET')
@view('active-users')
def active_users_page():
    """Render the active users page with data loaded from the JSON file."""

    return {
        "users": load_active_users(),
        "errors": {},
        "form": empty_user_form(),
    }


@route('/active-users', method='POST')
@view('active-users')
def add_active_user():
    """Validate and save a new active user or return errors to the same page."""

    # We copy only expected fields from the submitted form. This keeps the JSON
    # structure predictable and prevents accidental extra keys from being saved.
    form = {
        "nick": (request.forms.getunicode("nick") or "").strip(),
        "description": (request.forms.getunicode("description") or "").strip(),
        "active_date": (request.forms.getunicode("active_date") or "").strip(),
        "phone": (request.forms.getunicode("phone") or "").strip(),
    }

    users = load_active_users()
    errors = validate_active_user(form, users)

    if errors:
        # Return the same form values so the user can correct only invalid
        # fields instead of retyping the whole form.
        return {
            "users": users,
            "errors": errors,
            "form": form,
        }

    users.append(build_active_user(form))
    save_active_users(users)

    # Redirect clears fields after successful submit and avoids duplicate POSTs
    # when the browser refreshes the page.
    redirect('/active-users')
