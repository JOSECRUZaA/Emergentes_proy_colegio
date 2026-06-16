from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Docente, Usuario, Rol, Curso
from functools import wraps

docentes_bp = Blueprint('docentes', __name__, url_prefix='/docentes')

def requiere_admin_o_secretario(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.rol.nombre not in ['Administrador', 'Secretario Académico']:
            flash('Acceso denegado', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@docentes_bp.route('/')
@login_required
@requiere_admin_o_secretario
def lista():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    
    query = Docente.query.join(Usuario)
    if q:
        query = query.filter(db.or_(
            Usuario.nombre.ilike(f'%{q}%'),
            Docente.especialidad.ilike(f'%{q}%')
        ))
        
    docentes = query.paginate(page=page, per_page=10)
    return render_template('docentes/lista.html', docentes=docentes, q=q)

@docentes_bp.route('/<int:id>')
@login_required
def detalle(id):
    docente = Docente.query.get_or_404(id)
    cursos = Curso.query.filter_by(docente_id=id).all()
    return render_template('docentes/detalle.html', docente=docente, cursos=cursos)

@docentes_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@requiere_admin_o_secretario
def nuevo():
    if request.method == 'POST':
        try:
            rol_docente = Rol.query.filter_by(nombre='Docente').first()
            email = request.form.get('email')
            if Usuario.query.filter_by(email=email).first():
                flash('Ese correo electrónico ya está registrado en el sistema. Por favor, usa uno diferente.', 'warning')
                return render_template('docentes/nuevo.html')

            usuario = Usuario(
                nombre=request.form.get('nombre'),
                email=email,
                rol_id=rol_docente.id
            )
            usuario.set_password(request.form.get('contraseña', 'temporal123'))
            db.session.add(usuario)
            db.session.flush()
            
            docente = Docente(
                usuario_id=usuario.id,
                codigo_empleado=request.form.get('codigo_empleado'),
                especialidad=request.form.get('especialidad'),
                telefono=request.form.get('telefono'),
                direccion=request.form.get('direccion'),
                ciudad=request.form.get('ciudad')
            )
            db.session.add(docente)
            db.session.commit()
            flash('Docente registrado exitosamente', 'success')
            return redirect(url_for('docentes.lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('docentes/nuevo.html')

@docentes_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@requiere_admin_o_secretario
def editar(id):
    docente = Docente.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            docente.usuario.nombre = request.form.get('nombre')
            docente.usuario.email = request.form.get('email')
            docente.codigo_empleado = request.form.get('codigo_empleado')
            docente.especialidad = request.form.get('especialidad')
            docente.telefono = request.form.get('telefono')
            docente.direccion = request.form.get('direccion')
            docente.ciudad = request.form.get('ciudad')
            
            db.session.commit()
            flash('Docente actualizado exitosamente', 'success')
            return redirect(url_for('docentes.detalle', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('docentes/editar.html', docente=docente)

@docentes_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@requiere_admin_o_secretario
def eliminar(id):
    try:
        docente = Docente.query.get_or_404(id)
        usuario = docente.usuario
        
        db.session.delete(docente)
        db.session.delete(usuario)
        db.session.commit()
        flash('Docente eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('docentes.lista'))
