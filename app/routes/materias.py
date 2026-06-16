from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Materia, Curso
from functools import wraps

materias_bp = Blueprint('materias', __name__, url_prefix='/materias')

def requiere_admin_o_secretario(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.rol.nombre not in ['Administrador', 'Secretario Académico']:
            flash('Acceso denegado', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@materias_bp.route('/')
@login_required
@requiere_admin_o_secretario
def lista():
    page = request.args.get('page', 1, type=int)
    curso_id = request.args.get('curso_id', type=int)
    
    query = Materia.query
    if curso_id:
        query = query.filter_by(curso_id=curso_id)
        
    materias = query.paginate(page=page, per_page=10)
    cursos = Curso.query.filter_by(activo=True).order_by(Curso.grado, Curso.seccion).all()
    
    return render_template('materias/lista.html', materias=materias, cursos=cursos, curso_actual=curso_id)

@materias_bp.route('/<int:id>')
@login_required
def detalle(id):
    materia = Materia.query.get_or_404(id)
    return render_template('materias/detalle.html', materia=materia)

@materias_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@requiere_admin_o_secretario
def nuevo():
    if request.method == 'POST':
        try:
            materia = Materia(
                nombre=request.form.get('nombre'),
                codigo=request.form.get('codigo'),
                creditos=request.form.get('creditos'),
                curso_id=request.form.get('curso_id'),
                horas_semana=request.form.get('horas_semana'),
                activa=True
            )
            db.session.add(materia)
            db.session.commit()
            flash('Materia registrada exitosamente', 'success')
            return redirect(url_for('materias.lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    cursos = Curso.query.all()
    return render_template('materias/nuevo.html', cursos=cursos)

@materias_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@requiere_admin_o_secretario
def editar(id):
    materia = Materia.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            materia.nombre = request.form.get('nombre')
            materia.codigo = request.form.get('codigo')
            materia.creditos = request.form.get('creditos')
            materia.curso_id = request.form.get('curso_id')
            materia.horas_semana = request.form.get('horas_semana')
            materia.activa = request.form.get('activa') in ['true', 'on']
            
            db.session.commit()
            flash('Materia actualizada exitosamente', 'success')
            return redirect(url_for('materias.detalle', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    cursos = Curso.query.all()
    return render_template('materias/editar.html', materia=materia, cursos=cursos)

@materias_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@requiere_admin_o_secretario
def eliminar(id):
    try:
        materia = Materia.query.get_or_404(id)
        db.session.delete(materia)
        db.session.commit()
        flash('Materia eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('materias.lista'))
