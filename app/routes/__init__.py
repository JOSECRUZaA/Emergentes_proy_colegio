# Archivo __init__.py para routes
from .auth import auth_bp
from .dashboard import dashboard_bp
from .estudiantes import estudiantes_bp
from .docentes import docentes_bp
from .cursos import cursos_bp
from .materias import materias_bp
from .inscripciones import inscripciones_bp
from .calificaciones import calificaciones_bp
from .asistencias import asistencias_bp
from .usuarios import usuarios_bp
from .reportes import reportes_bp

__all__ = [
    'auth_bp',
    'dashboard_bp',
    'estudiantes_bp',
    'docentes_bp',
    'cursos_bp',
    'materias_bp',
    'inscripciones_bp',
    'calificaciones_bp',
    'asistencias_bp',
    'usuarios_bp',
    'reportes_bp'
]
