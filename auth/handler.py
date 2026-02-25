def authenticate(username, password):
    """Authenticate a user and return a session token."""
    user = lookup_user(username)
    if user and user.check_password(password):
        return generate_token(user.id)
    return None
