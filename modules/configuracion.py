from flask import Blueprint, render_template, request, jsonify
import pandas as pd
from database import supabase
from werkzeug.utils import secure_filename
import os

configuracion_bp = Blueprint('configuracion', __name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@configuracion_bp.route('/')
def configuracion():
    return render_template('configuracion.html')

@configuracion_bp.route('/importar_personal', methods=['POST'])
def importar_personal():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No se envió ningún archivo.'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'El nombre del archivo está vacío.'})

    if file and file.filename.endswith('.xlsx'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        try:
            # Leer el archivo Excel
            df = pd.read_excel(filepath)
            required_columns = ['dni', 'apellidos_nombres', 'cargo', 'ceco']

            # Validar columnas
            for col in required_columns:
                if col not in df.columns:
                    return jsonify({'status': 'error', 'message': f'Falta la columna requerida: {col}'})

            # Insertar registros en Supabase
            registros_insertados = 0
            for _, row in df.iterrows():
                supabase.table('personal').upsert({
                    'dni': str(row['dni']),
                    'apellidos_nombres': row['apellidos_nombres'],
                    'cargo': row['cargo'],
                    'ceco': row['ceco']
                }).execute()
                registros_insertados += 1

            return jsonify({'status': 'success', 'message': f'{registros_insertados} registros importados correctamente.'})

        except Exception as e:
            return jsonify({'status': 'error', 'message': f'Error al procesar el archivo: {str(e)}'})
        finally:
            os.remove(filepath)

    return jsonify({'status': 'error', 'message': 'Formato de archivo no válido. Suba un archivo .xlsx.'})
