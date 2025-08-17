from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField,DateField,TimeField,SelectField
from wtforms.validators import DataRequired, Email,Length,Optional


class BaseProfileForm(FlaskForm):
    name = StringField('Name', render_kw={'readonly': True})
    phone = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email',render_kw={'readonly': True} )


    submit = SubmitField('Save')

class OrderForm(FlaskForm):
    # ------------------------
    # 1. Pickup & Delivery
    # ------------------------
    pickup_address = TextAreaField("Pickup Address", validators=[DataRequired(), Length(max=200)])
    delivery_address = TextAreaField("Delivery Address", validators=[DataRequired(), Length(max=200)])
    
    supplier_name = StringField("Supplier Name", validators=[Optional(), Length(max=100)])
    supplier_phone = StringField("Supplier Phone", validators=[Optional(), Length(max=15)])
    customer_name = StringField("Customer Name", validators=[Optional(), Length(max=100)])
    customer_phone = StringField("Customer Phone", validators=[Optional(), Length(max=15)])
    
    # ------------------------
    # 2. Package Details
    # ------------------------
    package_name = StringField("Package Name", validators=[DataRequired(), Length(max=100)])
    package_priority = SelectField(
        "Package Priority",
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
        validators=[DataRequired()]
    )
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    package_type = SelectField(
        "Package Type",
        choices=[("fragile", "Fragile"), ("liquid", "Liquid"), ("solid", "Solid"), ("other", "Other")],
        validators=[DataRequired()]
    )
    package_description = TextAreaField("Package Description", validators=[Optional(), Length(max=300)])
    
    # ------------------------
    # 3. Logistics Details (Enter driver info directly)
    # ------------------------
    logistic_company = StringField("Logistic Company Name", validators=[DataRequired(), Length(max=100)])
    driver_name = StringField("Driver Name", validators=[DataRequired(), Length(max=100)])
    driver_phone = StringField("Driver Phone", validators=[DataRequired(), Length(max=15)])
    driver_truck_no = StringField("Driver Truck No", validators=[Optional(), Length(max=50)])
    
    # ------------------------
    # 4. Schedule
    # ------------------------
    date = DateField("Date", validators=[DataRequired()])
    time_slot = TimeField("Time Slot", validators=[DataRequired()])
    
    # ------------------------
    # Submit
    # ------------------------
    submit = SubmitField("Create Order")