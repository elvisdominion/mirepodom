from flask import Flask, Blueprint, render_template, redirect, url_for, session, flash
from modules.ingreso_personal import personal_bp
from modules.ingreso_vehicular import vehicular_bp
from modules.reportes import reportes_bp
from modules.configuracion import configuracion_bp
from modules.admin_login import admin_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

# Registrar Blueprints
app.register_blueprint(personal_bp, url_prefix="/personal")
app.register_blueprint(vehicular_bp, url_prefix="/vehicular")
app.register_blueprint(reportes_bp, url_prefix="/reportes")
app.register_blueprint(configuracion_bp, url_prefix="/configuracion")
app.register_blueprint(admin_bp, url_prefix='/admin')

# Ruta principal: Redirige al login si no hay sesión activa
@app.route('/')
def home():
    if 'usuario' not in session:
        return redirect(url_for('admin.login'))
    return redirect(url_for('personal.personal'))

# Contexto para exponer 'session' en las plantillas
@app.context_processor
def inject_session():
    return dict(session=session)

if __name__ == '__main__':
    app.run(debug=True)

