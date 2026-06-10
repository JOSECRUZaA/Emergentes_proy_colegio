from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Asistencia, Estudiante, Docente, Materia
from functools import wraps

asistencias_bp = Blueprint('asistencias', __name__, url_prefix='/asistencias')

def requiere_docente_o_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.rol.nombre not in ['Administrador', 'Docente']:
            flash('Acceso denegado', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@asistencias_bp.route('/')
@login_required
@requiere_docente_o_admin
def lista():
    page = request.args.get('page', 1, type=int)
    asistencias = Asistencia.query.paginate(page=page, per_page=10)
    return render_template('asistencias/lista.html', asistencias=asistencias)

@asistencias_bp.route('/<int:id>')
@login_required
def detalle(id):
    asistencia = Asistencia.query.get_or_404(id)
    return render_template('asistencias/detalle.html', asistencia=asistencia)

@asistencias_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
@requiere_docente_o_admin
def nueva():
    if request.method == 'POST':
        try:
            asistencia = Asistencia(
                estudiante_id=request.form.get('estudiante_id'),
                docente_id=request.form.get('docente_id'),
                materia_id=request.form.get('materia_id'),
                fecha=request.form.get('fecha'),
                presente=request.form.get('presente') == 'on',
                observacion=request.form.get('observacion')
            )
            db.session.add(asistencia)
            db.session.commit()
            flash('Asistencia registrada exitosamente', 'success')
            return redirect(url_for('asistencias.lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    estudiantes = Estudiante.query.all()
    docentes = Docente.query.all()
    materias = Materia.query.all()
    return render_template('asistencias/nueva.html', estudiantes=estudiantes, docentes=docentes, materias=materias)

@asistencias_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@requiere_docente_o_admin
def editar(id):
    asistencia = Asistencia.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            asistencia.presente = request.form.get('presente') == 'on'
            asistencia.observacion = request.form.get('observacion')
            
            db.session.commit()
            flash('Asistencia actualizada exitosamente', 'success')
            return redirect(url_for('asistencias.detalle', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('asistencias/editar.html', asistencia=asistencia)

@asistencias_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@requiere_docente_o_admin
def eliminar(id):
    try:
        asistencia = Asistencia.query.get_or_404(id)
        db.session.delete(asistencia)
        db.session.commit()
        flash('Asistencia eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('asistencias.lista'))
