from flask import Blueprint, render_template, redirect, url_for, request, flash
from ..models import Order, User
from .. import db
from flask_login import login_required, current_user

msme = Blueprint('msme', __name__)

@msme.route('/')
@login_required
def dashboard():
    return render_template('msme/dashboard.html')


#######################################################################################################################
#################################              ORDER ROUTES                       #####################################
#######################################################################################################################


@msme.route('/orders')
@login_required
def orders():
    # Fetch orders belonging to the logged-in user only
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('msme/orders.html', orders=orders)


# Add a new order
@msme.route('/orders/add', methods=['GET', 'POST'])
@login_required
def add_order():
    if request.method == 'POST':
        description = request.form.get('description')
        pickup = request.form.get('pickup')
        dropoff = request.form.get('dropoff')
        amount = request.form.get('amount')

        new_order = Order(
            user_id=current_user.id,
            description=description,
            pickup_location=pickup,
            dropoff_location=dropoff,
            amount=float(amount) if amount else None
        )
        db.session.add(new_order)
        db.session.commit()
        flash("Order created successfully!", "success")
        return redirect(url_for('msme.orders'))

    return render_template('msme/add_order.html')


# View order details
@msme.route('/orders/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)

    # Ensure the order belongs to the current user
    if order.user_id != current_user.id:
        flash("You are not authorized to view this order", "danger")
        return redirect(url_for('msme.orders'))

    return render_template('msme/order_detail.html', order=order)
