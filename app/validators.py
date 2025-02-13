import re

def valid_email(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def strong_password(password: str) -> bool:
    password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_regex, password) is not None

def valid_username(username: str) -> bool:
    username_regex = r'^[a-zA-Z0-9_]{3,20}$'
    return re.match(username_regex, username) is not None