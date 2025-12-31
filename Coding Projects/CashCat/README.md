# Overview

As a software engineer, I developed CashCat to deepen my expertise in full-stack web development, particularly in building secure, user-friendly applications with Django and Python. This project allowed me to explore user authentication, database management, and dynamic front-end rendering while applying best practices in software design and project management.

CashCat is a web application designed to help users track their income and expenses. It features a login/signup page, a dashboard displaying financial summaries (balance, total income, total expenses, and category breakdowns), and forms to add, edit, or delete transactions. The app uses Django’s authentication system to ensure user-specific data privacy and SQLite as a lightweight database for storing transactions. The front end is styled with Bootstrap for a responsive and modern interface.

To start a test server on your computer:
1. Ensure Python 3.8+ and Django 5.2+ are installed (`pip install django`).
2. Clone or set up the project directory with the provided files.
3. Navigate to the project directory: `cd cashcat_project`.
4. Apply migrations to set up the database: `python manage.py makemigrations` and `python manage.py migrate`.
5. Create a superuser for admin access: `python manage.py createsuperuser`.
6. Run the development server: `python manage.py runserver`.
7. Open `http://localhost:8000` in a web browser to access the login/signup page, which is the first page of the app.

My purpose for writing CashCat was to build a practical, user-focused application that reinforces my skills in Django’s ORM, authentication, and template rendering, while also learning to integrate front-end frameworks like Bootstrap. This project challenged me to manage database migrations, implement secure user authentication, and create a dynamic, interactive user interface, all of which are critical skills for developing scalable web applications.

[Software Demo Video](https://youtu.be/PXb_4TPBAvA)

# Web Pages

CashCat includes four main web pages, each dynamically generated and interconnected through Django’s URL routing and authentication system:

1. **Login/Signup Page (`http://localhost:8000/`)**:
   - **Description**: The entry point of the app, featuring side-by-side forms for users to log in or sign up. It uses Django’s authentication system to validate credentials or create new user accounts. Error messages (e.g., “Invalid username or password”) are dynamically displayed using Django’s messages framework.
   - **Dynamic Content**: Form inputs for username and password, error/success messages, and Bootstrap-styled alerts.
   - **Transitions**: On successful login, users are redirected to the Dashboard (`/dashboard/`). On signup, a success message prompts users to log in. Unauthenticated users accessing other pages are redirected here.

2. **Dashboard (`http://localhost:8000/dashboard/`)**:
   - **Description**: Displays a user’s financial overview, including total balance, income, expenses, a category breakdown table, and a list of recent transactions with edit and delete buttons.
   - **Dynamic Content**: The balance, income, and expense totals are calculated using Django’s ORM (`aggregate(Sum('amount'))`). The category table shows aggregated totals per category, and the transactions table lists user-specific transactions with action buttons. Empty states are handled with “No transactions yet” messages.
   - **Transitions**: Accessible only to authenticated users (via `@login_required`). Links to “Add Transaction” (`/add/`), “Edit Transaction” (`/edit/<id>/`), “Delete Transaction” (`/delete/<id>/`), and “Logout” (`/logout/`).

3. **Add Transaction (`http://localhost:8000/add/`)**:
   - **Description**: A form to add new income or expense transactions, including fields for type, category, amount, and description.
   - **Dynamic Content**: The form is generated using Django’s `TransactionForm`, with validation errors displayed dynamically. On successful submission, users are redirected to the Dashboard.
   - **Transitions**: Accessible from the Dashboard’s “Add Transaction” link. Includes a “Cancel” button to return to the Dashboard.

4. **Edit Transaction (`http://localhost:8000/edit/<id>/`)**:
   - **Description**: A form to edit an existing transaction, pre-filled with the transaction’s current data.
   - **Dynamic Content**: The form is populated using `TransactionForm(instance=transaction)`, ensuring user-specific data. Validation errors are shown if inputs are invalid.
   - **Transitions**: Accessed via the “Edit” button on the Dashboard. “Save Changes” redirects to the Dashboard, and “Cancel” returns to the Dashboard.

**Navigation**: The navbar, defined in `base.html`, dynamically updates based on authentication status, showing “Login/Signup” for unauthenticated users and “Dashboard”, “Add Transaction”, and “Logout” for authenticated users. Delete actions use a POST request with a confirmation prompt to prevent accidental deletions.

# Development Environment

**Tools**:
- **Visual Studio Code**: Used for writing and debugging Python, HTML, and CSS code, with extensions for Python linting and Django template support.
- **Git**: For version control to track changes and manage project iterations.
- **Command Prompt/PowerShell**: For running Django commands (`manage.py`) and managing the development server.
- **Google Chrome**: For testing the web app and using Developer Tools to inspect HTML/CSS and debug JavaScript.

**Programming Language and Libraries**:
- **Python 3.13.4**: The core programming language for the Django backend.
- **Django 5.2.4**: A high-level Python web framework for rapid development, handling URL routing, ORM, authentication, and template rendering.
- **SQLite**: A lightweight, serverless database included with Django for storing user and transaction data.
- **Bootstrap 5.3**: A front-end framework (loaded via CDN) for responsive styling and components like navbars, forms, and tables.
- **Django’s Built-in Libraries**:
  - `django.contrib.auth`: For user authentication and session management.
  - `django.contrib.messages`: For displaying success/error messages.
  - `django.db.models`: For database queries and aggregations.
  - `django.forms`: For form handling and validation.

# Useful Websites

* [Django Documentation](https://docs.djangoproject.com/en/5.2/)
* [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
* [Python Documentation](https://docs.python.org/3.13/)
* [Stack Overflow](https://stackoverflow.com/questions/tagged/django)

# Future Work

* **Enhanced Signup Form**: Add fields like email and password confirmation, with stronger validation (e.g., minimum password length, email format).
* **Category Management**: Allow users to create and manage custom categories for transactions, stored in a separate database model.
* **Data Visualization**: Add charts (e.g., using Chart.js) to the Dashboard for visual representation of category breakdowns and spending trends.
* **Password Recovery**: Implement a password reset feature using Django’s built-in password reset views and email functionality.
* **Mobile Optimization**: Improve responsiveness for smaller screens, adjusting form layouts and table displays.