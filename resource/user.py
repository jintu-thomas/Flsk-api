from flask_restful import reqparse,Resource
from model.user import UserModel
from flask_jwt_extended import create_access_token,create_refresh_token,get_raw_jwt,jwt_required,get_jwt_claims
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',type=str,required=True,help="This field cannot be blank.")
_user_parser.add_argument('password',type=str,required=True,help="This field cannot be blank.")
                          
                          
class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": f"A user with the same name {data['username']} is already exist "},400
        else:
            user = UserModel(data['username'], data['password'])
            user.save_to_db()
            return {"message": "User created successfully."}, 201 
                               
                          
class User(Resource):
    @jwt_required
    def get(self,id):
        user = UserModel.find_by_id(id)
        if not user:
            return {"message": "user is not found"}
        return user.json()

    @jwt_required
    def delete(self,id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            user = UserModel.find_by_id(id)
            if user:
                user.delete_from_db()
                return{'message': "user deleted"}
            return {"message": "user is not found"},404
        else:
            return {'message': 'you need to admin prevelage to delete user'}

class UserLogin(Resource): 
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password,data['password']):
            access_token = create_access_token(identity = user.id,fresh=True)
            refresh_token = create_refresh_token(identity = user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            },200

        return {'message': 'Invalid credential'},401

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200