from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from ..models import Order, User, Driver, Warehouse
from .. import db
from flask_login import login_required, current_user
from ..forms import OrderForm, WarehouseForm
from datetime import datetime

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
                         current_warehouse=current_user.current_warehouse,
                         now_date=datetime.now().date())


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
                         selected_order_type=order_type,
                         now_date=datetime.now().date())


# Add a new order
@msme.route('/add_order', methods=['GET', 'POST'])
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
        
        # If pickup address matches the warehouse address, it's an OUTGOING order; otherwise INCOMING
        if form.pickup_address.data.lower().strip() == current_warehouse.address.lower().strip():
            order_type = "outgoing"
        else:
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


#######################################################################################################################
#################################              PROFILE ROUTES                     #####################################
#######################################################################################################################

@msme.route('/profile')
@login_required
def profile():
    """Display user profile page"""
    return render_template('msme/profile.html')


@msme.route('/ltc')
@login_required
def ltc():
    """Display Live Tracking Center page"""
    return render_template('msme/ltc.html')


@msme.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile information"""
    form_type = request.form.get('form_type')
    
    try:
        if form_type == 'personal':
            # Update personal information
            current_user.name = request.form.get('name', current_user.name)
            current_user.phone = request.form.get('phone', current_user.phone)
            
        elif form_type == 'company':
            # Update company information
            current_user.company_name = request.form.get('company_name', current_user.company_name)
            current_user.business_address = request.form.get('business_address', current_user.business_address)
            current_user.gst_number = request.form.get('gst_number', current_user.gst_number)
            current_user.pan_number = request.form.get('pan_number', current_user.pan_number)
            
        elif form_type == 'subscription':
            # Update subscription information
            current_user.subscription_plan = request.form.get('subscription_plan', current_user.subscription_plan)
            current_user.billing_email = request.form.get('billing_email', current_user.billing_email)
            current_user.payment_method = request.form.get('payment_method', current_user.payment_method)
            
        elif form_type == 'preferences':
            # Update preferences
            warehouse_id = request.form.get('current_warehouse_id')
            if warehouse_id:
                # Verify warehouse belongs to user
                warehouse = Warehouse.query.filter_by(id=warehouse_id, user_id=current_user.id).first()
                if warehouse:
                    current_user.current_warehouse_id = int(warehouse_id)
            
            current_user.timezone = request.form.get('timezone', current_user.timezone)
            current_user.language = request.form.get('language', current_user.language)
            current_user.email_notifications = 'email_notifications' in request.form
            current_user.sms_notifications = 'sms_notifications' in request.form
        
        # Update the updated_at timestamp
        current_user.updated_at = datetime.now()
        
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Profile updated successfully!'})
        else:
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('msme.profile'))
            
    except Exception as e:
        db.session.rollback()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': f'Error updating profile: {str(e)}'})
        else:
            flash(f'Error updating profile: {str(e)}', 'error')
            return redirect(url_for('msme.profile'))
