from flask import Flask
from flask_login import LoginManager
from config import config
from app.models import db, Usuario, Rol

login_manager = LoginManager()

def create_app(config_name='development'):
    """Application Factory"""
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicie sesión para continuar.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    # Registrar blueprints
    from app.routes import auth_bp, dashboard_bp, estudiantes_bp, docentes_bp, cursos_bp, materias_bp, inscripciones_bp, calificaciones_bp, asistencias_bp, usuarios_bp, reportes_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(estudiantes_bp)
    app.register_blueprint(docentes_bp)
    app.register_blueprint(cursos_bp)
    app.register_blueprint(materias_bp)
    app.register_blueprint(inscripciones_bp)
    app.register_blueprint(calificaciones_bp)
    app.register_blueprint(asistencias_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(reportes_bp)
    
    # Contexto de aplicación para crear tablas
    with app.app_context():
        db.create_all()
        crear_roles_iniciales()
        crear_usuario_admin()
    
    return app

def crear_roles_iniciales():
    """Crear roles iniciales si no existen"""
    roles = [
        {'nombre': 'Administrador', 'descripcion': 'Acceso total al sistema'},
        {'nombre': 'Secretario Académico', 'descripcion': 'Gestiona académica'},
        {'nombre': 'Docente', 'descripcion': 'Docente del colegio'},
    ]
    
    for rol_data in roles:
        if not Rol.query.filter_by(nombre=rol_data['nombre']).first():
            rol = Rol(**rol_data)
            db.session.add(rol)
    
    db.session.commit()

def crear_usuario_admin():
    """Crear usuario admin si no existe"""
    admin = Usuario.query.filter_by(email='admin@colegio.com').first()
    if not admin:
        rol_admin = Rol.query.filter_by(nombre='Administrador').first()
        admin = Usuario(
            nombre='Administrador',
            email='admin@colegio.com',
            rol_id=rol_admin.id,
            activo=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
