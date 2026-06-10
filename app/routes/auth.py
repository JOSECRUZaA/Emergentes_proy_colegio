from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, Usuario, Rol
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(contraseña) and usuario.activo:
            login_user(usuario, remember=request.form.get('recordarme'))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard.index'))
        else:
            flash('Email o contraseña inválidos', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ha cerrado sesión exitosamente', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        
        if Usuario.query.filter_by(email=email).first():
            flash('El email ya existe', 'danger')
        else:
            rol_docente = Rol.query.filter_by(nombre='Docente').first()
            usuario = Usuario(nombre=nombre, email=email, rol_id=rol_docente.id)
            usuario.set_password(contraseña)
            db.session.add(usuario)
            db.session.commit()
            flash('Registro exitoso. Inicie sesión.', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/registro.html')
