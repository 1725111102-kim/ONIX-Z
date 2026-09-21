from flask import Blueprint, render_template
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