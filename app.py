from flask import Flask, request, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource


# Init app
app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)
api = Api(app)


# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty



# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')


# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

#class based api for get and post
class ProductList(Resource):
    def get(self):
        products = Product.query.all()
        result = products_schema.dump(products)
        #print(type(jsonify(result)))
        return make_response(jsonify(result))

    def post(self):
        # name = request.json['name']
        # description = request.json['description']
        # price = request.json['price']
        # qty = request.json['qty']
        data = request.json
        new_product = Product(data.get('name'), data.get('description'), data.get('price'), data.get('qty'))
        db.session.add(new_product)
        db.session.commit()
        result = product_schema.dump(new_product)
        # print(type(result))
        # print(type(jsonify(result)))
        return make_response(jsonify(result))

#class based api for retrieve,patch,delete
class ProductView(Resource):
    def get(self,id):
        product = Product.query.get_or_404(id)
        return product_schema.dump(product)

    def put(self,id):
        product = Product.query.get_or_404(id)

        name = request.json['name']
        description = request.json['description']
        price = request.json['price']
        qty = request.json['qty']

        product.name = name
        product.description = description
        product.price = price
        product.qty = qty
        # data = request.json
        # for k,v in data.items():
        #     setattr(product,k,v)
        db.session.commit()
        result = product_schema.dump(product)
        return make_response(jsonify(result))

    def patch(self,id):
        product = Product.query.get_or_404(id)
        data = request.json
        # if data.get('name'):
        #     product.name = data.get('name')
        # if data.get('description'):
        #     product.description = data.get('description')
        # if data.get('price'):
        #     product.price = data.get('price')
        # if data.get('qty'):
        #     product.qty = data.get('qty')
        for k,v in data.items():
            setattr(product,k,v)
        db.session.commit()
        return product_schema.dump(product)

    def delete(self,id):
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()

        return jsonify({"message":"item is deleted"})


# Create a Product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)



# Get All Products
@app.route('/product', methods=['GET'])
def all_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    #print(type(jsonify(result)))
    return jsonify(result)



# Get Single Products
@app.route('/product/<int:id>', methods=['GET'])
def product(id):
    product = Product.query.get_or_404(id)
    return product_schema.jsonify(product)



# Update a Product
@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty
    db.session.commit()

    return product_schema.jsonify(product)

@app.route('/product/<int:id>',methods=['PATCH'])
def partial_update(id):
    product = Product.query.get_or_404(id)
    data = request.json

    if data.get('name'):
        product.name = data.get('name')
    if data.get('description'):
        product.description = data.get('description')
    if data.get('price'):
        product.price = data.get('price')
    if data.get('qty'):
        product.qty = data.get('qty')

    db.session.commit()
    return product_schema.jsonify(product)


# Delete Product
@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()

    return jsonify({"message":"product is deleted"})

api.add_resource(ProductList,'/product_class')
api.add_resource(ProductView,'/product_class/<int:id>')

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
