# Employee Task Management System

A web-based task management application built with **Python** and **Django**, allowing managers/admins to assign tasks to employees and track their progress, while employees can view and update the status of their own tasks.

## Features

- User authentication (signup, login, logout)
- Role-based access (Admin / Manager / Employee)
- Managers/Admins can create, edit, and delete tasks
- Employees can view only their assigned tasks and update task status
- Task filtering by status
- Employee management (add/edit/remove employees, assign roles)
- Responsive, modern UI (dark glassmorphism theme, custom CSS)
- Django Admin panel support for direct data management

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (default, can be swapped for PostgreSQL/MySQL)
- **Frontend:** HTML, CSS (custom, no external framework)

## Project Structure

```
employee_task_management/
├── employee_task_management/   # Project settings, URLs
├── tasks/                      # Main app (models, views, forms, templates)
│   ├── models.py                # Employee & Task models
│   ├── views.py                 # Core logic (dashboard, task/employee CRUD)
│   ├── forms.py                 # Task, Employee, Signup forms
│   ├── urls.py                  # App-level routing
│   └── templates/tasks/         # HTML templates
├── manage.py
└── requirements.txt
```

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/manojpatra-dev1/employee_task_management.git
cd employee_task_management
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # macOS/Linux
```

### 3. Install dependencies
```bash
pip install django
```

### 4. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (admin account)
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

### 7. Open the app
- Main app: `http://127.0.0.1:8000/`
- Django Admin: `http://127.0.0.1:8000/admin/`

## Usage

1. Log in as the superuser (automatically treated as admin/manager).
2. Add employees via the **Employees** section or Django Admin.
3. Create tasks and assign them to employees.
4. Employees log in and see only their assigned tasks, and can update task status (Pending → In Progress → Completed).

## Roles

| Role | Permissions |
|------|-------------|
| Admin / Manager | View all tasks, create/edit/delete tasks, manage employees |
| Employee | View only their own tasks, update task status |

## Future Improvements

- Email notifications for task deadlines
- REST API using Django REST Framework
- Task comments and file attachments
- Analytics dashboard for task completion trends

## License

This project is open-source and available for learning/personal use.
