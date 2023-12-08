from flask import Flask
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/your_database'
db = SQLAlchemy(app)

# Adding Models
class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    department = db.relationship('Department', backref=db.backref('users', lazy=True))

# Schemas
class DepartmentType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()

class UserType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    department = graphene.Field(DepartmentType)

# Querying
class Query(graphene.ObjectType):
    department = graphene.Field(DepartmentType, id=graphene.Int())
    all_departments = graphene.List(DepartmentType)

    user = graphene.Field(UserType, id=graphene.Int())
    all_users = graphene.List(UserType)

    def resolve_department(self, info, id):
        return Department.query.get(id)

    def resolve_all_departments(self, info):
        return Department.query.all()

    def resolve_user(self, info, id):
        return User.query.get(id)

    def resolve_all_users(self, info):
        return User.query.all()

# Mutations
class CreateDepartment(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    department = graphene.Field(lambda: DepartmentType)

    def mutate(self, info, name):
        department = Department(name=name)
        db.session.add(department)
        db.session.commit()
        return CreateDepartment(department=department)

class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        department_id = graphene.Int()

    user = graphene.Field(lambda: UserType)

    def mutate(self, info, name, department_id):
        user = User(name=name, department_id=department_id)
        db.session.add(user)
        db.session.commit()
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_department = CreateDepartment.Field()
    create_user = CreateUser.Field()

# Add the GraphQL endpoint to the Flask app
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=graphene.Schema(query=Query, mutation=Mutation),
        graphiql=True  # Enable GraphiQL for easy testing
    )
)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
