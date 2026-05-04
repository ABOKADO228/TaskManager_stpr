"""Routes and views for the Bottle application."""

from bottle import redirect, request, route, view

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
