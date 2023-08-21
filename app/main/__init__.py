import os
from flask import Blueprint, current_app, render_template, request, redirect, jsonify, send_from_directory, session, url_for
import stripe
from app.models import Product, User

main = Blueprint('main', __name__)

# YOUR_DOMAIN = 'http://localhost:5000'
YOUR_DOMAIN = 'http://localhost:8100'

@main.route('/')
def index():
    # current_app.logger.debug("Hello World")
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/products')
def products():
    products = Product.query.all()

    return render_template('products.html', products=products)

@main.route('/products/<int:product_id>')
def product(product_id):
    product = Product.query.filter_by(id=product_id).first_or_404()

    return render_template('product.html', product=product)

@main.route('/cart')
def cart():
    if "items" not in session:
        session['items'] = []

    current_app.logger.debug(session['items'])
    return render_template('cart.html', products=session['items'])

@main.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if "items" not in session:
        session['items'] = []

    product_id = request.form['product_id']
    product = Product.query.filter_by(id=product_id).first()
    current_app.logger.debug(product)

    if product != None:
        session['items'].append({"id": product.id, "name": product.name, "price": product.price})

    current_app.logger.debug(session['items'])
    return redirect(url_for('main.cart'))

@main.route('/checkout')
def checkout():
    return render_template('checkout.html')

@main.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    # This is your test secret API key.
    # Ensure the key is kept out of any version control system you might be using.
    stripe.api_key = current_app.config.get('STRIPE_API_KEY')

    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email='jake.peralta@ninenine.com',
            billing_address_collection='required', # or 'auto' so it will collect only when necessary
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    # 'price': '20.00',
                    "price_data":  {
                        "currency": "usd", # Three-letter ISO currency code, e.g. jmd or usd
                        "product_data": {
                            "name": "Stubborn Attachments",
                            "description": "lorem ipsum dolor sit amet",
                            "images": ['https://i.imgur.com/EHyR2nP.png']
                        },
                        # "unit_amount": "000000005899" # A non-negative integer in cents representing how much to charge
                        "unit_amount_decimal": "5899" # A non-negative integer in cents representing how much to charge
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            metadata={
                "order_id": "1",
                "user_id": "2"
            },
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

@main.route("/success")
def success():
    return render_template('success.html')

@main.route("/cancel")
def cancel():
    return render_template('cancel.html')

@main.route('/webhook', methods=['POST'])
def webhook():
    # This is your Stripe CLI webhook secret for testing your endpoint locally.
    # Ensure the key is kept out of any version control system you might be using.
    endpoint_secret = current_app.config.get('STRIPE_WEBHOOK_SECRET')

    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'payment_intent.canceled':
        payment_intent = event['data']['object']
        # update database transaction and order to canceled
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        # update database transaction and order to declined
    elif event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        current_app.logger.debug(payment_intent)
    elif event['type'] == 'checkout.session.completed':
        checkout_details = event['data']['object']
        current_app.logger.debug(checkout_details)
        # update database transaction and order to success
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)

@main.route("/images/<path:filename>")
def image(filename):
    # current_app.logger.debug(os.getcwd())
    return send_from_directory(os.getcwd(), os.path.join('uploads/', filename))

@main.after_request
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
