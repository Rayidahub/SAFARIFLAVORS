from models.user.user_model import User

def authenticate_user(username, password):
    user = User.objects(username=username).first()
    if user and user.password == password:
        return user
    return None

