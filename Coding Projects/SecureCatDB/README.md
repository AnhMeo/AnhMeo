# Overview

SecureCatDB is a cybersecurity-focused Python application designed to simulate a real-world login and access management system. This project deepened my understanding of secure user authentication, relational databases, and GUI-based software interfaces. The program integrates directly with an SQLite relational database to log and manage user activity, track login attempts, and enforce role-based access.

The software features a login interface for both standard users and administrators. All login attempts (whether successful or not) are recorded in a dedicated table, including metadata like the IP address, timestamp, and login outcome. Admins are granted access to tools that allow them to manage users, view login logs, and monitor for suspicious behavior such as repeated failed login attempts. Standard users, by contrast, are routed to a basic dashboard showing their account details.

This program was developed to strengthen my skills in secure coding practices, database interaction, and GUI design.

[Software Demo Video](https://youtu.be/NuGWKeA1Si0)

# Relational Database

This application uses an SQLite relational database stored locally as users.db.

The database includes two primary tables:

- users table: Stores user account details such as username, password hash, salt, and whether the account is an admin.

Columns: id, username, salt, password, is_admin

- login_attempts table: Records every login attempt made through the application.

Columns: id, username, password_hash, ip_address, timestamp, success

The system supports SQL operations such as INSERT, SELECT, UPDATE, and DELETE through a Python interface.

# Development Environment

- IDE: Visual Studio Code

- Database: SQLite

- Programming Language: Python 3

- GUI Library: tkinter

- Password Hashing: cryptography.hazmat (PBKDF2HMAC, SHA256)

- Other Libraries: socket, datetime, os

# Useful Websites

- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [Welcome to pyca/cryptography](https://cryptography.io/en/latest/)
- [tkinter — Python interface to Tcl/Tk](https://docs.python.org/3/library/tkinter.html)
- [SQL Tutorial](https://www.w3schools.com/sql/)
- [sqlite3 — DB-API 2.0 interface for SQLite databases](https://docs.python.org/3/library/sqlite3.html)

# Future Work

- Add account lockout feature after repeated failed login attempts

- Enable filtering and exporting of login attempts (e.g., to CSV)

- Enhance UI with better theming and responsiveness

- Implement email notifications for admin alerts

- Add password reset feature with identity verification