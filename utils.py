def login_user(session, user):
    """
    Set session variables for the logged-in user.

    Args:
        session (flask.session): The session object.
        user (dict): A dictionary containing user information.
    """
    session['authenticated'] = 1
    session['user_id'] = user['id']
    session['first_name'] = user['first_name']
    session['last_name'] = user['last_name']
    session['email'] = user['email']
    session['role'] = user['role']
    session['avatar'] = user['avatar']
