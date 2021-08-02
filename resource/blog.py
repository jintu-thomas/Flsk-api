from flask_restful import Resource,reqparse
from model.blog import BlogModel
from flask_jwt_extended import jwt_required,jwt_optional,get_jwt_identity,get_jwt_claims

class Blog(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('heading',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('content',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('desc',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('user_id',type=int,required=True,help="This field cannot be blank.")

    @jwt_required
    def get(self,id):
        blog = BlogModel.find_by_id(id)
        if blog:
            return blog.json()
        return {"message":"blog not found"}
    
    @jwt_required
    def put(self,id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            data =self.parser.parse_args()
            blog = BlogModel.find_by_id(id)
            
            if blog:
                blog.heading = data['heading']
                blog.content = data['content']
                blog.desc = data['desc']
                blog.user_id = data['user_id']
        else:
            return {'mesaage': 'you need to admin previlege to update the blog'}

        blog.save_to_db()
        return blog.json() 

    @jwt_required
    def delete(self,id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        blog = BlogModel.find_by_id(id)
        if blog:
            blog.delete_from_db()
            return {"message": "{} is deleted". format(id)}


class BlogPost(Blog):
   
    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        blog = BlogModel(**data)
        blog.save_to_db()
        return blog.json()

class BlogList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        if user_id:
            blogs = [blog.json() for blog in BlogModel.find_all()]
            return {'blogs':blogs},200
        else:
            blogs = [x.json() for x in BlogModel.query.all()]
            return {
                'blogs': [blog['heading'] for blog in blogs]
            }
