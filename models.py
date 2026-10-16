from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

# --------------------
# 1. User Authentication & Authorization
# --------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Admin, Manager, Employee
    
    # Relationships
    employee = db.relationship('Employee', backref='user', uselist=False)

# --------------------
# 2. Employee Management
# --------------------
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100))
    department = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# --------------------
# 3 & 4. Customer & Contact Management
# --------------------
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    contacts = db.relationship('Contact', backref='customer', cascade="all, delete-orphan")
    interactions = db.relationship('CommunicationLog', backref='customer', cascade="all, delete-orphan")
    leads = db.relationship('Lead', backref='customer', cascade="all, delete-orphan")
    deals = db.relationship('Deal', backref='customer', cascade="all, delete-orphan")
    invoices = db.relationship('Invoice', backref='customer', cascade="all, delete-orphan")

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))

# --------------------
# 5. Lead Management
# --------------------
class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True) # Optional link to existing customer
    name_if_new = db.Column(db.String(100)) # If not linked to customer yet
    source = db.Column(db.String(50)) # Website, Referral, Ads
    status = db.Column(db.String(50), default='New') # New, Processing, Follow-up, Closed, Lost
    assigned_to = db.Column(db.Integer, db.ForeignKey('employee.id'))
    interest_level = db.Column(db.String(50)) # High, Medium, Low
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    employee = db.relationship('Employee', backref='leads')

# --------------------
# 6. Opportunity / Deal Management
# --------------------
class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False) # E.g. "Annual Service Contract"
    value = db.Column(db.Float, default=0.0)
    stage = db.Column(db.String(50)) # Qualification, Proposal, Negotiation, Closed Won, Closed Lost
    expected_close_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# --------------------
# 7. Sales & Invoice Management
# --------------------
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    items_json = db.Column(db.Text) # Stored as JSON string [{"item": "X", "qty": 1, "price": 100}]
    tax_rate = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# --------------------
# 8. Task & Activity Management
# --------------------
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    assigned_to = db.Column(db.Integer, db.ForeignKey('employee.id'))
    priority = db.Column(db.String(20), default='Medium') # High, Medium, Low
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='Pending') # Pending, In Progress, Completed
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    employee = db.relationship('Employee', backref='tasks')

# --------------------
# 9. Notification Module
# --------------------
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# --------------------
# 10. Communication Management
# --------------------
class CommunicationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=True)
    type = db.Column(db.String(50)) # Email, Call, Meeting
    notes = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# --------------------
# 13. Audit Log
# --------------------
class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text, nullable=True)

