from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Tabla de roles
class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))
    
    usuarios = db.relationship('Usuario', backref='rol', lazy='dynamic')
    
    def __repr__(self):
        return f'<Rol {self.nombre}>'

# Tabla de usuarios
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contraseña_hash = db.Column(db.String(255), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, contraseña):
        self.contraseña_hash = generate_password_hash(contraseña)
    
    def check_password(self, contraseña):
        return check_password_hash(self.contraseña_hash, contraseña)
    
    def __repr__(self):
        return f'<Usuario {self.email}>'

# Tabla de estudiantes
class Estudiante(db.Model):
    __tablename__ = 'estudiantes'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    matricula = db.Column(db.String(50), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(255))
    ciudad = db.Column(db.String(100))
    estado_civil = db.Column(db.String(50))
    fecha_ingreso = db.Column(db.DateTime, default=datetime.utcnow)
    
    usuario = db.relationship('Usuario', backref='estudiante')
    inscripciones = db.relationship('Inscripcion', backref='estudiante', lazy='dynamic')
    calificaciones = db.relationship('Calificacion', backref='estudiante', lazy='dynamic')
    asistencias = db.relationship('Asistencia', backref='estudiante', lazy='dynamic')
    
    def __repr__(self):
        return f'<Estudiante {self.matricula}>'

# Tabla de docentes
class Docente(db.Model):
    __tablename__ = 'docentes'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    codigo_empleado = db.Column(db.String(50), unique=True, nullable=False)
    especialidad = db.Column(db.String(120))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(255))
    ciudad = db.Column(db.String(100))
    fecha_ingreso = db.Column(db.DateTime, default=datetime.utcnow)
    
    usuario = db.relationship('Usuario', backref='docente')
    cursos = db.relationship('Curso', backref='docente', lazy='dynamic')
    calificaciones = db.relationship('Calificacion', backref='docente', lazy='dynamic')
    asistencias = db.relationship('Asistencia', backref='docente', lazy='dynamic')
    
    def __repr__(self):
        return f'<Docente {self.codigo_empleado}>'

# Tabla de cursos
class Curso(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    grado = db.Column(db.String(50))
    seccion = db.Column(db.String(10))
    capacidad = db.Column(db.Integer, default=30)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    materias = db.relationship('Materia', backref='curso', lazy='dynamic')
    inscripciones = db.relationship('Inscripcion', backref='curso', lazy='dynamic')
    
    def __repr__(self):
        return f'<Curso {self.codigo}>'

# Tabla de materias
class Materia(db.Model):
    __tablename__ = 'materias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    creditos = db.Column(db.Integer, default=3)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    horas_semana = db.Column(db.Integer, default=4)
    activa = db.Column(db.Boolean, default=True)
    
    calificaciones = db.relationship('Calificacion', backref='materia', lazy='dynamic')
    asistencias = db.relationship('Asistencia', backref='materia', lazy='dynamic')
    
    def __repr__(self):
        return f'<Materia {self.codigo}>'

# Tabla de inscripciones
class Inscripcion(db.Model):
    __tablename__ = 'inscripciones'
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    fecha_inscripcion = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(50), default='Activo')  # Activo, Retirado, Suspendido
    
    def __repr__(self):
        return f'<Inscripcion {self.estudiante_id}-{self.curso_id}>'

# Tabla de calificaciones
class Calificacion(db.Model):
    __tablename__ = 'calificaciones'
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    nota_parcial1 = db.Column(db.Float)
    nota_parcial2 = db.Column(db.Float)
    nota_parcial3 = db.Column(db.Float)
    nota_final = db.Column(db.Float)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    periodo = db.Column(db.String(50))  # 1er Período, 2do Período, etc.
    
    def calcular_promedio(self):
        notas = [n for n in [self.nota_parcial1, self.nota_parcial2, self.nota_parcial3] if n is not None]
        if notas:
            return sum(notas) / len(notas)
        return None
    
    def __repr__(self):
        return f'<Calificacion {self.estudiante_id}-{self.materia_id}>'

# Tabla de asistencias
class Asistencia(db.Model):
    __tablename__ = 'asistencias'
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    presente = db.Column(db.Boolean, default=True)
    observacion = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<Asistencia {self.estudiante_id}-{self.fecha}>'

# Tabla de reportes
class Reporte(db.Model):
    __tablename__ = 'reportes'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)  # promedios, aprobados, reprobados, asistencia
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    datos = db.Column(db.JSON)
    fecha_generacion = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    usuario = db.relationship('Usuario', backref='reportes')
    
    def __repr__(self):
        return f'<Reporte {self.tipo}>'
