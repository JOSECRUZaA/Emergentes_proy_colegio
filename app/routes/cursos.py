from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Curso, Docente, Materia
from functools import wraps

cursos_bp = Blueprint('cursos', __name__, url_prefix='/cursos')

def requiere_admin_o_secretario(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.rol.nombre not in ['Administrador', 'Secretario Académico']:
            flash('Acceso denegado', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@cursos_bp.route('/')
@login_required
@requiere_admin_o_secretario
def lista():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    
    query = Curso.query
    if q:
        query = query.filter(db.or_(
            Curso.nombre.ilike(f'%{q}%'),
            Curso.grado.ilike(f'%{q}%'),
            Curso.seccion.ilike(f'%{q}%')
        ))
        
    cursos = query.paginate(page=page, per_page=10)
    return render_template('cursos/lista.html', cursos=cursos, q=q)

@cursos_bp.route('/<int:id>')
@login_required
def detalle(id):
    curso = Curso.query.get_or_404(id)
    materias = Materia.query.filter_by(curso_id=id).all()
    return render_template('cursos/detalle.html', curso=curso, materias=materias)

@cursos_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@requiere_admin_o_secretario
def nuevo():
    if request.method == 'POST':
        try:
            docente_id = request.form.get('docente_id')
            curso = Curso(
                nombre=request.form.get('nombre'),
                codigo=request.form.get('codigo'),
                grado=request.form.get('grado'),
                seccion=request.form.get('seccion'),
                capacidad=request.form.get('capacidad'),
                docente_id=docente_id,
                activo=True
            )
            db.session.add(curso)
            db.session.commit()
            flash('Curso registrado exitosamente', 'success')
            return redirect(url_for('cursos.lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    docentes = Docente.query.all()
    return render_template('cursos/nuevo.html', docentes=docentes)

@cursos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@requiere_admin_o_secretario
def editar(id):
    curso = Curso.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            curso.nombre = request.form.get('nombre')
            curso.codigo = request.form.get('codigo')
            curso.grado = request.form.get('grado')
            curso.seccion = request.form.get('seccion')
            curso.capacidad = request.form.get('capacidad')
            curso.docente_id = request.form.get('docente_id')
            
            db.session.commit()
            flash('Curso actualizado exitosamente', 'success')
            return redirect(url_for('cursos.detalle', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    docentes = Docente.query.all()
    return render_template('cursos/editar.html', curso=curso, docentes=docentes)

@cursos_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@requiere_admin_o_secretario
def eliminar(id):
    try:
        curso = Curso.query.get_or_404(id)
        db.session.delete(curso)
        db.session.commit()
        flash('Curso eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('cursos.lista'))
