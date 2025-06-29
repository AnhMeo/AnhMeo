import sqlite3
import os
import pytest
from datetime import datetime, timedelta
from SecureCatDB import initialize_database, hash_password, save_credentials, validate_password, verify_credentials, log_login_attempt, check_threat, DATABASE_FILE

# Helper function to reset the database before each test
@pytest.fixture(autouse=True)
def setup_database():
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)
    initialize_database()
    yield
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)

def test_initialize_database():
    # Test if the database file is created and tables exist
    assert os.path.exists(DATABASE_FILE), "Database file was not created."

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    users_table = cursor.fetchone()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='login_attempts';")
    attempts_table = cursor.fetchone()
    conn.close()

    assert users_table is not None, "Users table was not created."
    assert attempts_table is not None, "Login attempts table was not created."

def test_hash_password():
    # Test that the hashed password is consistent for the same input and different for different inputs
    password = "TestPassword123!"
    salt = os.urandom(16)
    hash1 = hash_password(password, salt)
    hash2 = hash_password(password, salt)

    assert hash1 == hash2, "Hash function is not consistent with the same input."

    different_password = "AnotherPassword123!"
    hash3 = hash_password(different_password, salt)
    assert hash1 != hash3, "Hash function is not producing unique outputs for different inputs."

def test_save_credentials():
    # Test saving credentials with unique and duplicate usernames
    username = "testuser"
    salt = os.urandom(16)
    password = hash_password("TestPassword123!", salt)

    result = save_credentials(username, salt, password)
    assert result is True, "Failed to save new credentials."

    # Attempt to save a duplicate username
    result = save_credentials(username, salt, password)
    assert result is False, "Duplicate username was saved."

def test_validate_password():
    # Test password validation with various cases
    valid_password = "Valid123!"
    assert validate_password(valid_password) is None, "Valid password was incorrectly rejected."

    short_password = "Short1!"
    assert validate_password(short_password) == "Password must be at least 8 characters long."

    no_uppercase = "lowercase123!"
    assert validate_password(no_uppercase) == "Password must contain at least one uppercase letter."

    no_lowercase = "UPPERCASE123!"
    assert validate_password(no_lowercase) == "Password must contain at least one lowercase letter."

    no_number = "NoNumber!"
    assert validate_password(no_number) == "Password must contain at least one number."

    no_special = "NoSpecial123"
    assert validate_password(no_special) == "Password must contain at least one special character."





if __name__ == "__main__":
    pytest.main(["-v", "--tb=line", "-rN", __file__])