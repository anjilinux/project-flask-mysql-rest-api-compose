from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import ForeignKey
import datetime

# For seed script
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@db/shipping_01'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Address information model
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postal_code = db.Column(db.String(10))
    state = db.Column(db.String(30), unique=False)
    municipality = db.Column(db.String(100), unique=False)
    city = db.Column(db.String(100), unique=False)
    colony = db.Column(db.String(100), unique=False)
    
    remitent_id = db.Column(db.Integer, db.ForeignKey('remitent.id'))

    def __init__(self, postal_code, state, municipality, city, colony):
        self.postal_code = postal_code
        self.state = state
        self.municipality = municipality
        self.city = city
        self.colony = colony

# Shipping information model
class Shipping(db.Model):
    delivery_number = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.String(100), nullable=False, unique=False)
    product_value = db.Column(db.Float)
    description = db.Column(db.String(100))
    delivered = db.Column(db.Boolean, default=False)
    shipping_price = db.Column(db.Float)
    shipping_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    remitent_id = db.Column(db.Integer, db.ForeignKey('remitent.delivery_number'))

    def __init__(self, contents, product_value, description, delivered, shipping_price, shipping_date):
        self.contents = contents
        self.product_value = product_value
        self.description = description
        self.delivered = delivered
        self.shipping_price = shipping_price
        self.shipping_date = shipping_date

# Remitent information model
class Remitent(db.Model):
    delivery_number = db.Column(db.Integer)
    name = db.Column(db.String(100), unique=False, nullable=False)
    last_name = db.Column(db.String(100), unique=False, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    shippings = db.relationship('Shipping', backref='remitent', lazy=True)
    address = db.relationship('Address', backref='remitent', lazy=True)

    def __init__(self, name, last_name, address, phone):
        self.name = name
        self.last_name = last_name
        self.address = address
        self.phone = phone
        self.shippings = shippings 
        self.address = address
        



# Destinatary information model
class Destinatary(db.Model):
    delivery_number = db.Column(db.Integer, ForeignKey('delivery_number'))
    name = db.Column(db.String(100), unique=False)
    last_name = db.Column(db.String(100), unique=False)
    address = db.Column(db.String(100), unique=False)
    phone = db.Column(db.String(20), unique=False)
    postal_code = db.Column(db.String(10))

    def __init__(self, name, last_name, address, phone, postal_code):
        self.name = name
        self.last_name = last_name
        self.address = address
        self.phone = phone
        self.postal_code = postal_code


db.create_all()


# def import_data(file):
#     with open(str(file)) as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         line_counter = 0
#         for row in csv_reader:
#             if line_counter != 0:
#                 c = Circle(
#                     name=row[0],
#                     slug_name=row[1],
#                     is_public=(False if int(row[2]) == 0 else True),
#                     verified=(False if int(row[3]) == 0 else True),
#                     members_limit=int(row[4])
#                 )
#                 c.save()
#             line_counter += 1

# import_data('puebla.csv')


# class TaskSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'title', 'description')


# task_schema = TaskSchema()
# tasks_schema = TaskSchema(many=True)


# @app.route('/tasks', methods=['Post'])
# def create_task():
#   title = request.json['title']
#   description = request.json['description']

#   new_task= Task(title, description)

#   db.session.add(new_task)
#   db.session.commit()

#   return task_schema.jsonify(new_task)

# @app.route('/tasks', methods=['GET'])
# def get_tasks():
#   all_tasks = Task.query.all()
#   result = tasks_schema.dump(all_tasks)
#   return jsonify(result)

# @app.route('/tasks/<id>', methods=['GET'])
# def get_task(id):
#   task = Task.query.get(id)
#   return task_schema.jsonify(task)

# @app.route('/tasks/<id>', methods=['PUT'])
# def update_task(id):
#   task = Task.query.get(id)

#   title = request.json['title']
#   description = request.json['description']

#   task.title = title
#   task.description = description

#   db.session.commit()

#   return task_schema.jsonify(task)

# @app.route('/tasks/<id>', methods=['DELETE'])
# def delete_task(id):
#   task = Task.query.get(id)
#   db.session.delete(task)
#   db.session.commit()
#   return task_schema.jsonify(task)


# @app.route('/', methods=['GET'])
# def index():
#     return jsonify({'message': 'Welcome to my API'})


if __name__ == "__main__":
    app.run(debug=True)
