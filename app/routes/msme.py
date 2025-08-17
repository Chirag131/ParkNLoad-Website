from flask import Blueprint, render_template, redirect, url_for, request, flash
from ..models import Order, User ,Driver
from .. import db
from flask_login import login_required, current_user
from ..forms import OrderForm

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
    form = OrderForm()
    
    if form.validate_on_submit():
        # 1. Save Driver first
        driver = Driver(
            name=form.driver_name.data,
            phone=form.driver_phone.data,
            truck_no=form.driver_truck_no.data
        )
        db.session.add(driver)
        db.session.commit()  

        # 2. Save Order with driver_id
        order = Order(
            user_id=current_user.id,
            pickup_address=form.pickup_address.data,
            delivery_address=form.delivery_address.data,
            supplier_name=form.supplier_name.data,
            supplier_phone=form.supplier_phone.data,
            customer_name=form.customer_name.data,
            customer_phone=form.customer_phone.data,
            package_name=form.package_name.data,
            package_priority=form.package_priority.data,
            quantity=form.quantity.data,
            package_type=form.package_type.data,
            package_description=form.package_description.data,
            logistic_company=form.logistic_company.data,
            driver_id=driver.id,
            date=form.date.data,
            time_slot=form.time_slot.data
        )
        db.session.add(order)
        db.session.commit()
        flash("Order created successfully!", "success")
        return redirect(url_for('msme.orders'))
    
    return render_template("msme/add_order.html", form=form)



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
