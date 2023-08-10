from flask import Blueprint, current_app, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # current_app.logger.debug("Hello World")
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')