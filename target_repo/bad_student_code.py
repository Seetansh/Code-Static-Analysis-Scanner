import os

# This is a critical security violation we want to catch
FAKE_AWS_SECRET_KEY = "sk_live_892347598273495872398457"

def connect_to_db():
    password = "super_secret_database_password_123"
    print("Connecting...")
    return True

def process_data_poorly():
    print("Starting process...")
    x = 1
    x = x + 1
    x = x + 1
    x = x + 1
    x = x + 1
    x = x + 1
    x = x + 1
    x = x + 1
    x = x + 1
    x = x + 1
    print("Process done.")
    return x