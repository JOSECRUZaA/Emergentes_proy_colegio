from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Usuario, Rol
from functools import wraps

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

def requiere_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.rol.nombre != 'Administrador':
            flash('Acceso denegado', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@usuarios_bp.route('/')
@login_required
@requiere_admin
def lista():
    page = request.args.get('page', 1, type=int)
    usuarios = Usuario.query.paginate(page=page, per_page=10)
    return render_template('usuarios/lista.html', usuarios=usuarios)

@usuarios_bp.route('/<int:id>')
@login_required
@requiere_admin
def detalle(id):
    usuario = Usuario.query.get_or_404(id)
    return render_template('usuarios/detalle.html', usuario=usuario)

@usuarios_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@requiere_admin
def editar(id):
    usuario = Usuario.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            usuario.nombre = request.form.get('nombre')
            usuario.email = request.form.get('email')
            usuario.rol_id = request.form.get('rol_id')
            usuario.activo = request.form.get('activo') == 'on'
            
            db.session.commit()
            flash('Usuario actualizado exitosamente', 'success')
            return redirect(url_for('usuarios.detalle', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    roles = Rol.query.all()
    return render_template('usuarios/editar.html', usuario=usuario, roles=roles)

@usuarios_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@requiere_admin
def eliminar(id):
    if id == current_user.id:
        flash('No puede eliminar su propia cuenta', 'danger')
        return redirect(url_for('usuarios.lista'))
    
    try:
        usuario = Usuario.query.get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuario eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('usuarios.lista'))
