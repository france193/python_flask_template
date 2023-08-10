from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import jwt
from config import SECRET_KEY, JWT_EXPIRATION_SECONDS
from .models import User
from .utils import generate_random_otp

app = Flask(__name__)
api = Api(app)

# In-memory data store for simplicity (replace with a proper database in production)
users = []


# Helper function to get user by email
def get_user(email):
    for user in users:
        if user.email == email:
            return user
    return None


class Register(Resource):
    @staticmethod
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        full_name = data['full_name']

        # Check if user already exists
        if get_user(email):
            return {'message': 'User already exists'}, 409

        user = User(email=email, password=password, full_name=full_name)
        users.append(user)
        return {'message': 'User registered successfully'}, 201


class Login(Resource):

    @staticmethod
    def post():
        data = request.get_json()
        email = data['email']
        password = data['password']

        user = get_user(email)
        if user and user.password == password:
            payload = {
                'email': user.email,
                'full_name': user.full_name,
                'is_2fa_enabled': user.is_2fa_enabled
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
            return {'token': token}, 200

        return {'message': 'Invalid credentials'}, 401


class TwoFactorAuth(Resource):
    @staticmethod
    def post(self):
        data = request.get_json()
        email = data['email']
        otp = data['otp']

        user = get_user(email)
        if user and user.is_2fa_enabled:
            # You can implement an email sending logic here
            # For simplicity, we will log the OTP to stdout
            random_otp = generate_random_otp()
            print(f'Email OTP for {email}: {random_otp}')

            if otp == random_otp:
                payload = {
                    'email': user.email,
                    'full_name': user.full_name,
                    'is_2fa_enabled': True
                }
                token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
                return {'token': token}, 200

        return {'message': 'Invalid OTP or 2FA not enabled'}, 401


# API endpoints
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(TwoFactorAuth, '/2fa')

if __name__ == '__main__':
    app.run(debug=True)
