from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import db, Estudiante, Usuario, Rol, Inscripcion
from functools import wraps

estudiantes_bp = Blueprint('estudiantes', __name__, url_prefix='/estudiantes')

def requiere_admin_o_secretario(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.rol.nombre not in ['Administrador', 'Secretario Académico']:
            flash('Acceso denegado', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@estudiantes_bp.route('/')
@login_required
@requiere_admin_o_secretario
def lista():
    page = request.args.get('page', 1, type=int)
    estudiantes = Estudiante.query.paginate(page=page, per_page=10)
    return render_template('estudiantes/lista.html', estudiantes=estudiantes)

@estudiantes_bp.route('/<int:id>')
@login_required
def detalle(id):
    estudiante = Estudiante.query.get_or_404(id)
    inscripciones = Inscripcion.query.filter_by(estudiante_id=id).all()
    return render_template('estudiantes/detalle.html', estudiante=estudiante, inscripciones=inscripciones)

@estudiantes_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@requiere_admin_o_secretario
def nuevo():
    if request.method == 'POST':
        try:
            rol_estudiante = Rol.query.filter_by(nombre='Estudiante').first()
            if not rol_estudiante:
                flash('Rol estudiante no existe', 'danger')
                return redirect(url_for('estudiantes.lista'))
            
            email = request.form.get('email')
            if Usuario.query.filter_by(email=email).first():
                flash('Ese correo electrónico ya está registrado en el sistema. Por favor, usa uno diferente.', 'warning')
                return render_template('estudiantes/nuevo.html')

            usuario = Usuario(
                nombre=request.form.get('nombre'),
                email=email,
                rol_id=rol_estudiante.id
            )
            usuario.set_password(request.form.get('contraseña', 'temporal123'))
            db.session.add(usuario)
            db.session.flush()
            
            estudiante = Estudiante(
                usuario_id=usuario.id,
                matricula=request.form.get('matricula'),
                fecha_nacimiento=request.form.get('fecha_nacimiento'),
                telefono=request.form.get('telefono'),
                direccion=request.form.get('direccion'),
                ciudad=request.form.get('ciudad')
            )
            db.session.add(estudiante)
            db.session.commit()
            flash('Estudiante registrado exitosamente', 'success')
            return redirect(url_for('estudiantes.lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('estudiantes/nuevo.html')

@estudiantes_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@requiere_admin_o_secretario
def editar(id):
    estudiante = Estudiante.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            estudiante.usuario.nombre = request.form.get('nombre')
            estudiante.usuario.email = request.form.get('email')
            estudiante.matricula = request.form.get('matricula')
            estudiante.fecha_nacimiento = request.form.get('fecha_nacimiento')
            estudiante.telefono = request.form.get('telefono')
            estudiante.direccion = request.form.get('direccion')
            estudiante.ciudad = request.form.get('ciudad')
            
            db.session.commit()
            flash('Estudiante actualizado exitosamente', 'success')
            return redirect(url_for('estudiantes.detalle', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('estudiantes/editar.html', estudiante=estudiante)

@estudiantes_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@requiere_admin_o_secretario
def eliminar(id):
    try:
        estudiante = Estudiante.query.get_or_404(id)
        usuario = estudiante.usuario
        
        db.session.delete(estudiante)
        db.session.delete(usuario)
        db.session.commit()
        flash('Estudiante eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('estudiantes.lista'))
