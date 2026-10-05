from flask import Blueprint, current_app, render_template, send_from_directory
from models import Product

store_bp = Blueprint('store', __name__)


@store_bp.route('/')
def index():
    productos = Product.query.all()
    return render_template('index.html', productos=productos)


@store_bp.route('/producto/<int:id>')
def producto_detalle(id):
    producto = Product.query.get_or_404(id)
    return render_template('product_detail.html', producto=producto)


@store_bp.route('/imagenes/<path:filename>')
def imagen_producto(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)