# Hackathon2_S2lists

# Plan To Do

Plan To Do is a Django-based web application for managing personal tasks. It allows users to create, update, complete, and delete tasks, with a focus on privacy and usability.

## Table of Contents
- [Features](#features)
- [Project Must Haves](#project-must-haves)
- [Should Haves](#should-haves)
- [Could Haves](#could-haves)
- [Deployment](#deployment)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [License](#license)

## Features
- User registration and authentication
- Private task lists per user
- CRUD operations for tasks (Create, Read, Update, Delete)
- Mark tasks as completed
- Task deadlines
- Search and filter tasks
- Responsive design for mobile and desktop

## Project Must Haves
- Secure user authentication (login, logout, registration)
- Each user can only access their own tasks
- Add, edit, delete, and complete tasks
- Set deadlines for tasks
- Minimum password length of 12 characters

## Should Haves
- Search and filter tasks by keyword or status
- Responsive UI for mobile devices
- Edit task details (title, description)
- Hide completed tasks from active view

## Could Haves
- Task prioritization (e.g., high/medium/low)
- Email notifications for deadlines
- Task categories or tags
- Dark mode UI
- Integration with calendar apps

## Deployment
This project is ready for deployment on platforms like Heroku, Azure, or any server supporting Django. A sample `Procfile` is included for Heroku.

**Basic Deployment Steps:**
1. Install dependencies from `requirements.txt`.
2. Set environment variables for `SECRET_KEY` and allowed hosts.
3. Run database migrations: `python manage.py migrate`
4. Collect static files: `python manage.py collectstatic`
5. Start the server: `gunicorn wsgi:application` (for production)

**Heroku Example:**
```
heroku create
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py collectstatic
heroku open
```

## Setup & Installation
1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Run migrations:
    ```
    python manage.py migrate
    ```
5. Start the development server:
    ```
    python manage.py runserver
    ```

## Usage
Register for an account, log in, and start managing your tasks. Tasks can be added, edited, marked as complete, or deleted. Use the search and filter features to organize your workflow.

## License
This project is for educational and demonstration purposes.

