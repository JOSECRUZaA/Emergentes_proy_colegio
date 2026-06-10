from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Calificacion, Estudiante, Docente, Materia
from functools import wraps

calificaciones_bp = Blueprint('calificaciones', __name__, url_prefix='/calificaciones')

def requiere_docente_o_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.rol.nombre not in ['Administrador', 'Docente']:
            flash('Acceso denegado', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@calificaciones_bp.route('/')
@login_required
@requiere_docente_o_admin
def lista():
    page = request.args.get('page', 1, type=int)
    calificaciones = Calificacion.query.paginate(page=page, per_page=10)
    return render_template('calificaciones/lista.html', calificaciones=calificaciones)

@calificaciones_bp.route('/<int:id>')
@login_required
def detalle(id):
    calificacion = Calificacion.query.get_or_404(id)
    return render_template('calificaciones/detalle.html', calificacion=calificacion)

@calificaciones_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
@requiere_docente_o_admin
def nueva():
    if request.method == 'POST':
        try:
            calificacion = Calificacion(
                estudiante_id=request.form.get('estudiante_id'),
                docente_id=request.form.get('docente_id'),
                materia_id=request.form.get('materia_id'),
                nota_parcial1=request.form.get('nota_parcial1'),
                nota_parcial2=request.form.get('nota_parcial2'),
                nota_parcial3=request.form.get('nota_parcial3'),
                nota_final=request.form.get('nota_final'),
                periodo=request.form.get('periodo')
            )
            db.session.add(calificacion)
            db.session.commit()
            flash('Calificación registrada exitosamente', 'success')
            return redirect(url_for('calificaciones.lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    estudiantes = Estudiante.query.all()
    docentes = Docente.query.all()
    materias = Materia.query.all()
    return render_template('calificaciones/nueva.html', estudiantes=estudiantes, docentes=docentes, materias=materias)

@calificaciones_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@requiere_docente_o_admin
def editar(id):
    calificacion = Calificacion.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            calificacion.nota_parcial1 = request.form.get('nota_parcial1')
            calificacion.nota_parcial2 = request.form.get('nota_parcial2')
            calificacion.nota_parcial3 = request.form.get('nota_parcial3')
            calificacion.nota_final = request.form.get('nota_final')
            calificacion.periodo = request.form.get('periodo')
            
            db.session.commit()
            flash('Calificación actualizada exitosamente', 'success')
            return redirect(url_for('calificaciones.detalle', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    estudiantes = Estudiante.query.all()
    docentes = Docente.query.all()
    materias = Materia.query.all()
    return render_template('calificaciones/editar.html', calificacion=calificacion, estudiantes=estudiantes, docentes=docentes, materias=materias)

@calificaciones_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@requiere_docente_o_admin
def eliminar(id):
    try:
        calificacion = Calificacion.query.get_or_404(id)
        db.session.delete(calificacion)
        db.session.commit()
        flash('Calificación eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('calificaciones.lista'))
