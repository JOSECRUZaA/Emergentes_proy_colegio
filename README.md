# Sistema Administrativo Educativo - Colegio Villa Esperanza

## Descripción
Sistema web desarrollado con Flask para la gestión académica completa del Colegio Villa Esperanza.

## Características
- ✅ Patrón Application Factory
- ✅ Autenticación con roles (Administrador, Secretario Académico, Docente)
- ✅ Gestión de estudiantes, docentes, cursos y materias
- ✅ Sistema de calificaciones y asistencias
- ✅ Reportes académicos (promedios, aprobados, reprobados, asistencia)
- ✅ Dashboard administrativo con estadísticas
- ✅ Interfaz con Bootstrap 5

## Instalación

### 1. Clonar el repositorio
```bash
git clone <url-repositorio>
cd PROYECTO_EMERGENTES_COLEGIO_VILLA_ESPERANZA
```

### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate  # En Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
# Crear archivo .env con:
FLASK_ENV=development
FLASK_APP=run.py
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=sqlite:///colegio.db
```

### 5. Ejecutar la aplicación
```bash
python run.py
```

La aplicación estará disponible en `http://localhost:5000`

## Credenciales de Prueba
- Email: admin@colegio.com
- Contraseña: admin123

## Estructura del Proyecto
```
app/
├── __init__.py              # Application Factory
├── models/
│   └── __init__.py         # Modelos SQLAlchemy (10 tablas)
├── routes/
│   ├── auth.py             # Autenticación
│   ├── dashboard.py        # Dashboard
│   ├── estudiantes.py      # CRUD Estudiantes
│   ├── docentes.py         # CRUD Docentes
│   ├── cursos.py           # CRUD Cursos
│   ├── materias.py         # CRUD Materias
│   ├── inscripciones.py    # CRUD Inscripciones
│   ├── calificaciones.py   # CRUD Calificaciones
│   ├── asistencias.py      # CRUD Asistencias
│   ├── usuarios.py         # Gestión de Usuarios
│   └── reportes.py         # Reportes
├── templates/              # Templates HTML con Bootstrap
└── static/                 # CSS, JS

config.py                   # Configuración
run.py                      # Punto de entrada
requirements.txt            # Dependencias
```

## Módulos del Sistema

### Seguridad
- Login/Logout
- Gestión de Usuarios
- Control de Roles

### Gestión Académica
- Estudiantes (Alta, Baja, Modificación)
- Docentes (Alta, Baja, Modificación)
- Cursos (Alta, Baja, Modificación)
- Materias (Alta, Baja, Modificación)
- Inscripciones

### Seguimiento Académico
- Calificaciones (3 parciales + final)
- Asistencias

### Reportes
- Promedios generales
- Estudiantes aprobados
- Estudiantes reprobados
- Asistencia por estudiante

### Dashboard
- Total de estudiantes
- Total de docentes
- Cursos activos
- Promedio general del colegio

## Tecnologías Utilizadas
- **Backend:** Python 3.x, Flask 2.3.3
- **Base de Datos:** SQLite (desarrollo), PostgreSQL (producción)
- **ORM:** SQLAlchemy
- **Autenticación:** Flask-Login
- **Frontend:** Bootstrap 5, HTML5, CSS3
- **Seguridad:** Werkzeug (password hashing)

## Tablas de Base de Datos
1. usuarios
2. roles
3. estudiantes
4. docentes
5. cursos
6. materias
7. inscripciones
8. calificaciones
9. asistencias
10. reportes

## Próximas Mejoras
- [ ] Envío de emails
- [ ] Generación de reportes en PDF
- [ ] Gráficos de estadísticas
- [ ] Sistema de notificaciones
- [ ] API REST
- [ ] Despliegue en Render/Heroku

## Autor
Equipo de Desarrollo - TEM-742 Tecnologías Emergentes II

## Licencia
Proyecto Académico 2026
