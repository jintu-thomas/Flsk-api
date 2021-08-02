from blacklist import BLACKLIST
from flask import Flask,jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from db import db
from resource.user import UserLogin, UserLogout,UserRegister,User
from resource.blog import Blog,BlogPost,BlogList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']
api = Api(app)

app.config['JWT_SECRET_KEY'] = 'jose'

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:   # instead of hard-coding, we should read from a config file to get a list of admins instead
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    }),401

@app.before_first_request
def create_tables():
    db.create_all()


#route
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(User, '/user/<int:id>')
api.add_resource(Blog, '/blog/<int:id>')
api.add_resource(BlogPost, '/blog')
api.add_resource(BlogList, '/blogs')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)