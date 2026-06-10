from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import db, Estudiante, Docente, Curso, Calificacion, Asistencia
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/')

@dashboard_bp.route('/')
@login_required
def index():
    total_estudiantes = Estudiante.query.count()
    total_docentes = Docente.query.count()
    cursos_activos = Curso.query.filter_by(activo=True).count()
    
    # Calcular promedio general
    promedio_general = db.session.query(func.avg(Calificacion.nota_final)).scalar()
    promedio_general = round(promedio_general, 2) if promedio_general else 0
    
    estadisticas = {
        'total_estudiantes': total_estudiantes,
        'total_docentes': total_docentes,
        'cursos_activos': cursos_activos,
        'promedio_general': promedio_general,
    }
    
    return render_template('dashboard/index.html', estadisticas=estadisticas, usuario=current_user)
