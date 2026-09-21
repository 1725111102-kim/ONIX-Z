from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from models import db, Product

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return wrapper


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        clave = request.form.get('clave')
        if usuario == current_app.config['ADMIN_USER'] and clave == current_app.config['ADMIN_PASS']:
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        flash('Usuario o contraseña incorrectos')
    return render_template('admin/login.html')


@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    productos = Product.query.all()
    return render_template('admin/dashboard.html', productos=productos)


@admin_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        nuevo = Product(
            nombre=request.form.get('nombre'),
            precio=float(request.form.get('precio')),
            caracteristicas=request.form.get('caracteristicas'),
            categoria=request.form.get('categoria'),
            imagen=request.form.get('imagen')
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Producto agregado')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_product.html')


@admin_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    producto = Product.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre = request.form.get('nombre')
        producto.precio = float(request.form.get('precio'))
        producto.caracteristicas = request.form.get('caracteristicas')
        producto.categoria = request.form.get('categoria')
        producto.imagen = request.form.get('imagen')
        db.session.commit()
        flash('Producto actualizado')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_product.html', producto=producto)


@admin_bp.route('/delete/<int:id>')
@login_required
def delete_product(id):
    producto = Product.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado')
    return redirect(url_for('admin.dashboard'))