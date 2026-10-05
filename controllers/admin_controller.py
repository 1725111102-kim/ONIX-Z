import os
import uuid
from functools import wraps
from werkzeug.utils import secure_filename
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash, current_app
)
from models import db, Product, Admin

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return wrapper


def guardar_imagen(archivo):
    """Guarda el archivo subido y devuelve un nombre de archivo único."""
    if not archivo or not archivo.filename:
        return None
    nombre_seguro = secure_filename(archivo.filename)
    if not nombre_seguro:
        return None
    extension = os.path.splitext(nombre_seguro)[1].lower()
    nombre = f'{uuid.uuid4().hex}{extension}'
    carpeta = current_app.config['UPLOAD_FOLDER']
    os.makedirs(carpeta, exist_ok=True)
    archivo.save(os.path.join(carpeta, nombre))
    return nombre


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        clave = request.form.get('clave')
        admin = Admin.query.filter_by(usuario=usuario, clave=clave).first()
        if admin:
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
        nombre_archivo = guardar_imagen(request.files.get('imagen'))
        nuevo = Product(
            nombre=request.form.get('nombre'),
            precio=float(request.form.get('precio')),
            caracteristicas=request.form.get('caracteristicas'),
            categoria=request.form.get('categoria'),
            imagen=nombre_archivo
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

        nombre_archivo = guardar_imagen(request.files.get('imagen'))
        if nombre_archivo:
            producto.imagen = nombre_archivo  # solo la cambia si subiste una nueva

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


@admin_bp.route('/cambiar-contrasena', methods=['GET', 'POST'])
@login_required
def cambiar_contrasena():
    admin = Admin.query.first()