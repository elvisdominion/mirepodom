from flask import Blueprint, Response, request, jsonify, send_file, render_template
from database import supabase
import pandas as pd
from io import BytesIO
import io

reportes_bp = Blueprint('reportes', __name__)

# Ruta de la página de Reportes
@reportes_bp.route('/')
def reportes():
    return render_template('reportes.html')


# Endpoint para obtener datos del reporte
@reportes_bp.route('/buscar_ingresos', methods=['GET'])
def buscar_ingresos():
    try:
        fecha_desde = request.args.get('desde')
        fecha_hasta = request.args.get('hasta')

        if not fecha_desde or not fecha_hasta:
            return jsonify({"status": "error", "message": "Las fechas son obligatorias."}), 400

        # Consultar datos en Supabase
        response = supabase.table("ingresos") \
            .select("dni, nombres_apellidos, tipo_ingreso, area, nombre_autoriza, sede_id, fecha_hora_ingreso") \
            .gte("fecha_hora_ingreso", f"{fecha_desde} 00:00:00") \
            .lte("fecha_hora_ingreso", f"{fecha_hasta} 23:59:59") \
            .execute()

        if not response.data:
            return jsonify({"status": "error", "message": "No se encontraron registros para el rango de fechas indicado."})

        # Convertir a DataFrame y devolver como JSON
        df = pd.DataFrame(response.data)
        sede_dict = {1: 'Argentina 3090', 2: 'Argentina 4140'}
        df['sede_id'] = df['sede_id'].map(sede_dict)

        return df.to_json(orient="records")

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Endpoint para descargar Excel desde la búsqueda
@reportes_bp.route('/descargar_reporte', methods=['POST'])
def descargar_reporte():
    try:
        data = request.json.get('data')

        if not data:
            return jsonify({"status": "error", "message": "No hay datos para exportar."})

        df = pd.DataFrame(data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Ingresos")
        output.seek(0)

        return Response(
            output.getvalue(),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=Reporte_Ingresos.xlsx"
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@reportes_bp.route('/dashboard_ingresos')
def dashboard_ingresos():
    try:
        # Contar registros manualmente sin 'count('exact')'
        total_personal = len(supabase.table("ingresos").select("id").eq("tipo_ingreso", "PERSONAL").execute().data)
        total_visitas = len(supabase.table("ingresos").select("id").eq("tipo_ingreso", "VISITA").execute().data)

        ingresos_sede1 = len(supabase.table("ingresos").select("id").eq("sede_id", 1).execute().data)
        ingresos_sede2 = len(supabase.table("ingresos").select("id").eq("sede_id", 2).execute().data)

        return jsonify({
            "total_personal": total_personal,
            "total_visitas": total_visitas,
            "ingresos_sede1": ingresos_sede1,
            "ingresos_sede2": ingresos_sede2
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
