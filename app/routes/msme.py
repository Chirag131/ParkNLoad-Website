from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from ..models import Order, User, Driver, Warehouse
from .. import db
from flask_login import login_required, current_user
from ..forms import OrderForm, WarehouseForm

msme = Blueprint('msme', __name__)

@msme.route('/')
@login_required
def dashboard():
    # Get warehouse count and recent orders for dashboard
    warehouse_count = Warehouse.query.filter_by(user_id=current_user.id, is_active=True).count()
    recent_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).limit(5).all()
    
    # Get order type statistics
    incoming_orders = Order.query.filter_by(user_id=current_user.id, order_type="incoming").count()
    outgoing_orders = Order.query.filter_by(user_id=current_user.id, order_type="outgoing").count()
    
    # Get user's warehouses for selection
    user_warehouses = Warehouse.query.filter_by(user_id=current_user.id, is_active=True).all()
    
    return render_template('msme/dashboard.html', 
                         warehouse_count=warehouse_count, 
                         recent_orders=recent_orders,
                         incoming_orders=incoming_orders,
                         outgoing_orders=outgoing_orders,
                         user_warehouses=user_warehouses,
                         current_warehouse=current_user.current_warehouse)


@msme.route('/set-warehouse/<int:warehouse_id>')
@login_required
def set_warehouse(warehouse_id):
    """Set the current warehouse for the user"""
    warehouse = Warehouse.query.filter_by(id=warehouse_id, user_id=current_user.id).first_or_404()
    
    current_user.current_warehouse_id = warehouse_id
    db.session.commit()
    
    flash(f"Active warehouse set to: {warehouse.name}", "success")
    return redirect(url_for('msme.dashboard'))


#######################################################################################################################
#################################              WAREHOUSE ROUTES                     #####################################
#######################################################################################################################

@msme.route('/warehouses')
@login_required
def warehouses():
    warehouses = Warehouse.query.filter_by(user_id=current_user.id).order_by(Warehouse.created_at.desc()).all()
    return render_template('msme/warehouses.html', warehouses=warehouses)


@msme.route('/warehouses/add', methods=['GET', 'POST'])
@login_required
def add_warehouse():
    form = WarehouseForm()
    
    if form.validate_on_submit():
        warehouse = Warehouse(
            name=form.name.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            pincode=form.pincode.data,
            contact_person=form.contact_person.data,
            contact_phone=form.contact_phone.data,
            is_active=form.is_active.data,
            user_id=current_user.id
        )
        db.session.add(warehouse)
        db.session.commit()
        
        # If this is the first warehouse, set it as current
        if not current_user.current_warehouse_id:
            current_user.current_warehouse_id = warehouse.id
            db.session.commit()
        
        flash("Warehouse added successfully!", "success")
        return redirect(url_for('msme.warehouses'))
    
    return render_template('msme/add_warehouse.html', form=form)


@msme.route('/warehouses/<int:warehouse_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_warehouse(warehouse_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    
    # Ensure the warehouse belongs to the current user
    if warehouse.user_id != current_user.id:
        flash("You are not authorized to edit this warehouse", "danger")
        return redirect(url_for('msme.warehouses'))
    
    form = WarehouseForm(obj=warehouse)
    
    if form.validate_on_submit():
        warehouse.name = form.name.data
        warehouse.address = form.address.data
        warehouse.city = form.city.data
        warehouse.state = form.state.data
        warehouse.pincode = form.pincode.data
        warehouse.contact_person = form.contact_person.data
        warehouse.contact_phone = form.contact_phone.data
        warehouse.is_active = form.is_active.data
        
        db.session.commit()
        flash("Warehouse updated successfully!", "success")
        return redirect(url_for('msme.warehouses'))
    
    return render_template('msme/edit_warehouse.html', form=form, warehouse=warehouse)


@msme.route('/warehouses/<int:warehouse_id>/delete', methods=['POST'])
@login_required
def delete_warehouse(warehouse_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    
    # Ensure the warehouse belongs to the current user
    if warehouse.user_id != current_user.id:
        flash("You are not authorized to delete this warehouse", "danger")
        return redirect(url_for('msme.warehouses'))
    
    # Check if warehouse has orders
    if warehouse.orders:
        flash("Cannot delete warehouse with existing orders", "danger")
        return redirect(url_for('msme.warehouses'))
    
    # If this was the current warehouse, clear it
    if current_user.current_warehouse_id == warehouse_id:
        current_user.current_warehouse_id = None
        db.session.commit()
    
    db.session.delete(warehouse)
    db.session.commit()
    flash("Warehouse deleted successfully!", "success")
    return redirect(url_for('msme.warehouses'))


#######################################################################################################################
#################################              ORDER ROUTES                       #####################################
#######################################################################################################################

@msme.route('/orders')
@login_required
def orders():
    warehouse_id = request.args.get('warehouse_id', type=int)
    order_type = request.args.get('order_type', type=str)
    
    # Build query
    query = Order.query.filter_by(user_id=current_user.id)
    
    if warehouse_id:
        # Filter orders by specific warehouse
        warehouse = Warehouse.query.filter_by(id=warehouse_id, user_id=current_user.id).first_or_404()
        query = query.filter_by(warehouse_id=warehouse_id)
    else:
        warehouse = None
    
    if order_type and order_type in ['incoming', 'outgoing']:
        # Filter orders by type
        query = query.filter_by(order_type=order_type)
    
    orders = query.order_by(Order.created_at.desc()).all()
    
    return render_template('msme/orders.html', 
                         orders=orders, 
                         selected_warehouse=warehouse,
                         selected_order_type=order_type)


# Add a new order
@msme.route('/orders/add', methods=['GET', 'POST'])
@login_required
def add_order():
    # Check if user has a current warehouse
    if not current_user.current_warehouse_id:
        flash("Please select a warehouse first from your dashboard", "warning")
        return redirect(url_for('msme.dashboard'))
    
    # Check if current warehouse is still active
    current_warehouse = Warehouse.query.filter_by(
        id=current_user.current_warehouse_id, 
        user_id=current_user.id, 
        is_active=True
    ).first()
    
    if not current_warehouse:
        flash("Your selected warehouse is no longer active. Please select another warehouse.", "warning")
        current_user.current_warehouse_id = None
        db.session.commit()
        return redirect(url_for('msme.dashboard'))
    
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

        # 2. Determine order type and auto-fill customer name if needed
        order_type = "outgoing"  # default
        customer_name = form.customer_name.data
        
        # Check if pickup address matches warehouse address (incoming order)
        if form.pickup_address.data.lower().strip() == current_warehouse.address.lower().strip():
            order_type = "incoming"
            # Auto-fill customer name with MSME details if not provided
            if not customer_name:
                customer_name = current_user.name
        
        # 3. Save Order with current warehouse
        order = Order(
            user_id=current_user.id,
            warehouse_id=current_user.current_warehouse_id,
            pickup_address=form.pickup_address.data,
            delivery_address=form.delivery_address.data,
            supplier_name=form.supplier_name.data,
            supplier_phone=form.supplier_phone.data,
            customer_name=customer_name,
            customer_phone=form.customer_phone.data,
            package_name=form.package_name.data,
            package_priority=form.package_priority.data,
            quantity=form.quantity.data,
            package_type=form.package_type.data,
            package_description=form.package_description.data,
            logistic_company=form.logistic_company.data,
            driver_id=driver.id,
            date=form.date.data,
            time_slot=form.time_slot.data,
            order_type=order_type
        )
        db.session.add(order)
        db.session.commit()
        flash("Order created successfully!", "success")
        return redirect(url_for('msme.orders'))
    
    return render_template("msme/add_order.html", form=form, current_warehouse=current_warehouse)


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
