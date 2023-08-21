import os
from flask import Blueprint, jsonify, current_app, request, session
from app.forms import ProductForm
from app.models import Product
from app.extensions import db
from werkzeug.utils import secure_filename

api = Blueprint('api', __name__, url_prefix='/api/v1')

@api.route('/status')
def status():
    return jsonify({ "message": "API Operational" })

@api.route('/products')
def products():
    data = []
    products = Product.query.all()
    for product in products:
        data.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "image": "/images/" + product.image,
            "price": product.price
        })
    return jsonify({ "products": data })

@api.route('/products', methods=["POST"])
def add_product():
    form = ProductForm()
    current_app.logger.debug(request.form)
    current_app.logger.debug(request.files)
    if form.validate_on_submit():
        name = form.name.data
        description =form.description.data
        price = form.price.data
        status = form.status.data
        image = form.image.data
        user_id = form.user_id.data

        filename = secure_filename(image.filename)
        image.save(os.path.join(
            './uploads/', filename
        ))

        product = Product(name, description, price, status, filename, user_id)
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product Added"}), 201
    current_app.logger.debug(form.errors)
    return jsonify({"message": "Product not saved"}), 500

@api.route('/products/<int:id>', methods=["GET"])
def product_details(id):
    product = Product.query.filter_by(id=id).first()
    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "image": "/images/" + product.image,
    })

@api.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'

    response.headers['Access-Control-Allow-Origin'] = '*' #'http://localhost:8100'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Credentials'] = 'true'

    return response