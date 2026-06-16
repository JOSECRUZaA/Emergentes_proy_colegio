from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Inscripcion, Estudiante, Curso
from functools import wraps

inscripciones_bp = Blueprint('inscripciones', __name__, url_prefix='/inscripciones')

def requiere_admin_o_secretario(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.rol.nombre not in ['Administrador', 'Secretario Académico']:
            flash('Acceso denegado', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@inscripciones_bp.route('/')
@login_required
@requiere_admin_o_secretario
def lista():
    page = request.args.get('page', 1, type=int)
    curso_id = request.args.get('curso_id', type=int)
    
    query = Inscripcion.query
    if curso_id:
        query = query.filter_by(curso_id=curso_id)
        
    inscripciones = query.paginate(page=page, per_page=10)
    cursos = Curso.query.filter_by(activo=True).order_by(Curso.grado, Curso.seccion).all()
    
    return render_template('inscripciones/lista.html', inscripciones=inscripciones, cursos=cursos, curso_actual=curso_id)

@inscripciones_bp.route('/<int:id>')
@login_required
def detalle(id):
    inscripcion = Inscripcion.query.get_or_404(id)
    return render_template('inscripciones/detalle.html', inscripcion=inscripcion)

@inscripciones_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
@requiere_admin_o_secretario
def nueva():
    if request.method == 'POST':
        try:
            inscripcion = Inscripcion(
                estudiante_id=request.form.get('estudiante_id'),
                curso_id=request.form.get('curso_id'),
                estado='Activo'
            )
            db.session.add(inscripcion)
            db.session.commit()
            flash('Inscripción registrada exitosamente', 'success')
            return redirect(url_for('inscripciones.lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    estudiantes = Estudiante.query.all()
    cursos = Curso.query.filter_by(activo=True).all()
    return render_template('inscripciones/nueva.html', estudiantes=estudiantes, cursos=cursos)

@inscripciones_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@requiere_admin_o_secretario
def editar(id):
    inscripcion = Inscripcion.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            inscripcion.estado = request.form.get('estado')
            db.session.commit()
            flash('Inscripción actualizada exitosamente', 'success')
            return redirect(url_for('inscripciones.detalle', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('inscripciones/editar.html', inscripcion=inscripcion)

@inscripciones_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@requiere_admin_o_secretario
def eliminar(id):
    try:
        inscripcion = Inscripcion.query.get_or_404(id)
        db.session.delete(inscripcion)
        db.session.commit()
        flash('Inscripción eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('inscripciones.lista'))
