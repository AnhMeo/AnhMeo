import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
import os
import time
import socket
from datetime import datetime

# Database file
DATABASE_FILE = "users.db"

def initialize_database():
    # Initializes the database and creates users and login_attempts tables if they don't exist.
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Users table with admin flag
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            salt BLOB NOT NULL,
            password BLOB NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0
        )
    """)
    
    # Login attempts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password_hash BLOB NOT NULL,
            ip_address TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            success INTEGER NOT NULL
        )
    """)
    
    # Create default admin user if not exists
    cursor.execute("SELECT username FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        salt = os.urandom(16)
        hashed_password = hash_password("Admin123!", salt)
        cursor.execute("INSERT INTO users (username, salt, password, is_admin) VALUES (?, ?, ?, ?)",
                       ("admin", salt, hashed_password, 1))
    
    conn.commit()
    conn.close()

def hash_password(password, salt):
    # Hashes the password using PBKDF2HMAC with a salt.
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def log_login_attempt(username, password, success):
    # Logs a login attempt to the login_attempts table.
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Hash the attempted password
    salt = os.urandom(16)
    password_hash = hash_password(password, salt)
    
    # Get IP address
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
    except:
        ip_address = "127.0.0.1"
    
    # Get timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO login_attempts (username, password_hash, ip_address, timestamp, success)
        VALUES (?, ?, ?, ?, ?)
    """, (username, password_hash, ip_address, timestamp, success))
    
    conn.commit()
    conn.close()

def check_threat(username):
    # Checks for potential threats (e.g., multiple failed login attempts).
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Check for 3 or more failed attempts in the last 5 minutes
    five_minutes_ago = (datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        SELECT COUNT(*) FROM login_attempts
        WHERE username = ? AND success = 0 AND timestamp >= ?
    """, (username, five_minutes_ago))
    
    count = cursor.fetchone()[0]
    conn.close()
    
    return count >= 3

def save_credentials(username, salt, hashed_password, is_admin=0):
    # Saves the username, salt, hashed password, and admin status to the database.
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False  # Username already exists
    cursor.execute("INSERT INTO users (username, salt, password, is_admin) VALUES (?, ?, ?, ?)",
                   (username, salt, hashed_password, is_admin))
    conn.commit()
    conn.close()
    return True

def validate_password(password):
    # Validates the password based on specified criteria.
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return "Password must contain at least one lowercase letter."
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one number."
    if not any(char in "!@#$%^&*()-_=+[]{}|;:',.<>?/~`" for char in password):
        return "Password must contain at least one special character."
    return None

def verify_credentials(username, password):
    # Verifies the username and password against the database.
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT salt, password, is_admin FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        log_login_attempt(username, password, 0)
        return False, False
    
    salt, stored_password, is_admin = row
    try:
        hashed_password = hash_password(password, salt)
        success = hashed_password == stored_password
        log_login_attempt(username, password, 1 if success else 0)
        
        if not success and check_threat(username):
            messagebox.showwarning("Threat Detected", "Multiple failed login attempts detected. Account temporarily locked.")
            return False, False
        
        return success, bool(is_admin)
    except Exception:
        log_login_attempt(username, password, 0)
        return False, False

def open_signup_window(root):
    # Opens the sign-up window.
    def signup():
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        confirm_password = entry_confirm_password.get().strip()

        if not username:
            messagebox.showerror("Error", "Username cannot be empty.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        validation_error = validate_password(password)
        if validation_error:
            messagebox.showerror("Invalid Password", validation_error)
            return

        salt = os.urandom(16)
        hashed_password = hash_password(password, salt)

        if save_credentials(username, salt, hashed_password):
            messagebox.showinfo("Success", f"Account for '{username}' created successfully!")
            signup_window.destroy()
        else:
            messagebox.showerror("Error", f"Username '{username}' is already taken. Please try another.")

    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")

    tk.Label(signup_window, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_username = tk.Entry(signup_window, width=30)
    entry_username.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(signup_window, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_password = tk.Entry(signup_window, width=30, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(signup_window, text="Confirm Password:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    entry_confirm_password = tk.Entry(signup_window, width=30, show="*")
    entry_confirm_password.grid(row=2, column=1, padx=10, pady=10)

    btn_signup = tk.Button(signup_window, text="Sign Up", command=signup)
    btn_signup.grid(row=3, column=0, columnspan=2, pady=10)

def user_dashboard(root, username):
    # Regular user dashboard showing account details.
    dashboard = tk.Toplevel(root)
    dashboard.title(f"User Dashboard - {username}")
    
    tk.Label(dashboard, text=f"Welcome, {username}!", font=("Arial", 14)).pack(pady=10)
    
    # Fetch user details
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE username = ?", (username,))
    user_info = cursor.fetchone()
    conn.close()
    
    tk.Label(dashboard, text=f"User ID: {user_info[0]}").pack(pady=5)
    tk.Label(dashboard, text=f"Username: {user_info[1]}").pack(pady=5)
    
    tk.Button(dashboard, text="Logout", command=dashboard.destroy).pack(pady=10)

def admin_interface(root):
    # Admin interface for managing users and viewing login attempts.
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Interface")
    
    notebook = ttk.Notebook(admin_window)
    notebook.pack(pady=10, expand=True)
    
    # Users management tab
    users_frame = ttk.Frame(notebook)
    notebook.add(users_frame, text="Manage Users")
    
    # Treeview for displaying users
    tree = ttk.Treeview(users_frame, columns=("ID", "Username", "Admin"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("Admin", text="Is Admin")
    tree.pack(pady=10)
    
    def refresh_users():
        for item in tree.get_children():
            tree.delete(item)
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, is_admin FROM users")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()
    
    refresh_users()
    
    # Add user
    tk.Label(users_frame, text="New Username:").pack()
    entry_new_username = tk.Entry(users_frame)
    entry_new_username.pack()
    
    tk.Label(users_frame, text="New Password:").pack()
    entry_new_password = tk.Entry(users_frame, show="*")
    entry_new_password.pack()
    
    def add_user():
        username = entry_new_username.get().strip()
        password = entry_new_password.get().strip()
        
        validation_error = validate_password(password)
        if validation_error:
            messagebox.showerror("Invalid Password", validation_error)
            return
        
        salt = os.urandom(16)
        hashed_password = hash_password(password, salt)
        
        if save_credentials(username, salt, hashed_password):
            messagebox.showinfo("Success", "User added successfully!")
            refresh_users()
        else:
            messagebox.showerror("Error", "Username already exists.")
    
    tk.Button(users_frame, text="Add User", command=add_user).pack(pady=5)
    
    # Delete user
    def delete_user():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user to delete.")
            return
        user_id = tree.item(selected_item)["values"][0]
        if user_id == 1:  # Prevent deleting default admin
            messagebox.showerror("Error", "Cannot delete default admin.")
            return
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        refresh_users()
        messagebox.showinfo("Success", "User deleted successfully!")
    
    tk.Button(users_frame, text="Delete User", command=delete_user).pack(pady=5)
    
    # Toggle admin status
    def toggle_admin():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user to modify.")
            return
        user_id = tree.item(selected_item)["values"][0]
        current_admin = tree.item(selected_item)["values"][2]
        new_admin = 0 if current_admin else 1
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_admin = ? WHERE id = ?", (new_admin, user_id))
        conn.commit()
        conn.close()
        refresh_users()
        messagebox.showinfo("Success", "Admin status updated!")
    
    tk.Button(users_frame, text="Toggle Admin Status", command=toggle_admin).pack(pady=5)
    
    # Login attempts tab
    attempts_frame = ttk.Frame(notebook)
    notebook.add(attempts_frame, text="Login Attempts")
    
    attempts_tree = ttk.Treeview(attempts_frame, columns=("ID", "Username", "IP", "Timestamp", "Success"), show="headings")
    attempts_tree.heading("ID", text="ID")
    attempts_tree.heading("Username", text="Username")
    attempts_tree.heading("IP", text="IP Address")
    attempts_tree.heading("Timestamp", text="Timestamp")
    attempts_tree.heading("Success", text="Success")
    attempts_tree.pack(pady=10)
    
    def refresh_attempts():
        for item in attempts_tree.get_children():
            attempts_tree.delete(item)
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, ip_address, timestamp, success FROM login_attempts")
        for row in cursor.fetchall():
            attempts_tree.insert("", "end", values=row)
        conn.close()
    
    refresh_attempts()
    
    tk.Button(attempts_frame, text="Refresh", command=refresh_attempts).pack(pady=5)
    
    tk.Button(admin_window, text="Logout", command=admin_window.destroy).pack(pady=10)

def main_window():
    # Main login window.
    def login():
        username = entry_username.get().strip()
        password = entry_password.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return

        success, is_admin = verify_credentials(username, password)
        if success:
            if is_admin:
                admin_interface(root)
            else:
                user_dashboard(root, username)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    root = tk.Tk()
    root.title("AccessLogDB Login")
    
    tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_username = tk.Entry(root, width=30)
    entry_username.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_password = tk.Entry(root, width=30, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10)

    btn_login = tk.Button(root, text="Login", command=login)
    btn_login.grid(row=2, column=0, padx=10, pady=10)

    btn_signup = tk.Button(root, text="Sign Up", command=lambda: open_signup_window(root))
    btn_signup.grid(row=2, column=1, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    initialize_database()
    main_window()