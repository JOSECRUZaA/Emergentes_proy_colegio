from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import db, Calificacion, Asistencia, Estudiante, Curso
from sqlalchemy import func

reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')

@reportes_bp.route('/')
@login_required
def index():
    return render_template('reportes/index.html')

@reportes_bp.route('/promedios')
@login_required
def promedios():
    estudiantes = Estudiante.query.all()
    datos = []
    
    for estudiante in estudiantes:
        calificaciones = Calificacion.query.filter_by(estudiante_id=estudiante.id).all()
        if calificaciones:
            promedio = sum([c.nota_final for c in calificaciones if c.nota_final]) / len(calificaciones)
            datos.append({
                'estudiante': estudiante.usuario.nombre,
                'promedio': round(promedio, 2)
            })
    
    return render_template('reportes/promedios.html', datos=datos)

@reportes_bp.route('/aprobados')
@login_required
def aprobados():
    calificaciones = Calificacion.query.filter(Calificacion.nota_final >= 60).all()
    datos = [{
        'estudiante': c.estudiante.usuario.nombre,
        'materia': c.materia.nombre,
        'nota': c.nota_final
    } for c in calificaciones]
    
    return render_template('reportes/aprobados.html', datos=datos)

@reportes_bp.route('/reprobados')
@login_required
def reprobados():
    calificaciones = Calificacion.query.filter(Calificacion.nota_final < 60).all()
    datos = [{
        'estudiante': c.estudiante.usuario.nombre,
        'materia': c.materia.nombre,
        'nota': c.nota_final
    } for c in calificaciones]
    
    return render_template('reportes/reprobados.html', datos=datos)

@reportes_bp.route('/asistencia')
@login_required
def asistencia():
    estudiantes = Estudiante.query.all()
    datos = []
    
    for estudiante in estudiantes:
        asistencias = Asistencia.query.filter_by(estudiante_id=estudiante.id).all()
        if asistencias:
            presentes = len([a for a in asistencias if a.presente])
            porcentaje = (presentes / len(asistencias)) * 100
            datos.append({
                'estudiante': estudiante.usuario.nombre,
                'total': len(asistencias),
                'presentes': presentes,
                'porcentaje': round(porcentaje, 2)
            })
    
    return render_template('reportes/asistencia.html', datos=datos)
