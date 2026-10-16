# CRM Web Application

A complete Customer Relationship Management (CRM) system built with Flask, SQLAlchemy, and Bootstrap.

## Features
- **User Authentication**: Role-based access (Admin, Manager, Employee).
- **Employee Management**: Admin can add/manage employees.
- **Customer & Contact Management**: Store customer details and multiple contacts.
- **Lead Management**: Track leads through customizable statuses.
- **Sales & Invoices**: Generate invoices and track sales.
- **Task Management**: Assign tasks to employees with due dates.
- **Reports**: Visual analytics for leads and sales.
- **Audit Log**: Track system activities.

## Tech Stack
- Python Flask (Backend)
- SQLite (Database)
- HTML5 / Bootstrap 5 (Frontend)
- Chart.js (Analytics)

## How to Run

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database**
   ```bash
   flask init-db
   ```
   *This creates the `crm.db` file and a default admin user.*

3. **Run Application**
   ```bash
   python app.py
   ```

4. **Login**
   - Open browser at `http://localhost:5000`
   - **Username**: `admin`
   - **Password**: `admin123`

## Project Structure
- `app.py`: Main application controller and routes.
- `models.py`: Database schema definitions.
- `templates/`: HTML files for all modules.
- `static/`: CSS, JS, and images.

## Modules Overview
- **Dashboard**: Quick stats and recent activities.
- **Leads**: Add new leads, change status (New -> Processing -> Closed).
- **Customers**: Manage company profiles.
- **Tasks**: Assign work to employees.
- **Invoices**: Create and print simple invoices.
