from flask import Blueprint, render_template, request, jsonify, session
from database import supabase
from datetime import datetime

personal_bp = Blueprint('personal', __name__)

@personal_bp.route('/')
def personal():
    return render_template('personal.html')

# Verificar DNI y registrar ingreso
@personal_bp.route('/verificar_dni', methods=['POST'])
@personal_bp.route('/verificar_dni', methods=['POST'])
def verificar_dni():
    dni = request.json.get('dni')
    sede_id = session.get('sede_id')

    # Verificar si ya se registró hoy como personal
    hoy = datetime.now().strftime("%Y-%m-%d")
    existe = supabase.table("ingresos") \
        .select("*") \
        .eq("dni", dni) \
        .eq("tipo_ingreso", "PERSONAL") \
        .gte("fecha_hora_ingreso", f"{hoy} 00:00:00") \
        .lte("fecha_hora_ingreso", f"{hoy} 23:59:59") \
        .execute()

    if existe.data:
        # Mensaje si ya fue registrado
        return jsonify({"status": "ya_registrado", "message": "⚠️ El personal ya fue registrado hoy."})

    # Verificar si el DNI pertenece a un personal registrado
    resultado = supabase.table("personal").select("apellidos_nombres", "cargo", "ceco").eq("dni", dni).execute()

    if resultado.data:
        personal = resultado.data[0]

        # Registrar ingreso para personal
        supabase.table("ingresos").insert({
            "tipo_ingreso": "PERSONAL",
            "dni": dni,
            "nombres_apellidos": personal["apellidos_nombres"],
            "cargo": personal["cargo"],
            "area": personal["ceco"],
            "sede_id": sede_id,
            "fecha_hora_ingreso": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }).execute()
        return jsonify({"status": "personal", "nombre": personal["apellidos_nombres"]})

    # Si no está en la base de datos, preguntar si es visita
    return jsonify({"status": "no_encontrado", "message": "DNI no encontrado. ¿Registrar como visita?"})


# Registrar una visita
@personal_bp.route('/registrar_visita', methods=['POST'])
def registrar_visita():
    dni = request.json.get('dni')
    nombre = request.json.get('nombre')
    autorizador = request.json.get('autorizador')
    sede_id = session.get('sede_id')

    if dni and nombre and autorizador:
        supabase.table("ingresos").insert({
            "tipo_ingreso": "VISITA",
            "dni": dni,
            "nombres_apellidos": nombre,
            "nombre_autoriza": autorizador,
            "area": "Visitante",
            "sede_id": sede_id,
            "fecha_hora_ingreso": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }).execute()
        return jsonify({"status": "visita_registrada"})
    else:
        return jsonify({"status": "error", "message": "Todos los campos son obligatorios."})

# Obtener ingresos para mostrar en el grid
@personal_bp.route('/get_ingresos', methods=['GET'])
def get_ingresos():
    sede_id = session.get('sede_id')
    response = supabase.table("ingresos") \
        .select("dni, nombres_apellidos, tipo_ingreso, area, nombre_autoriza, sede_id, fecha_hora_ingreso") \
        .eq("sede_id", sede_id) \
        .order("fecha_hora_ingreso", desc=True) \
        .execute()
    return jsonify(response.data)

@personal_bp.route('/buscar_autorizador', methods=['GET'])
def buscar_autorizador():
    query = request.args.get('q', '')

    if query:
        # Buscar en la tabla personal por DNI o nombre
        resultado = supabase.table("personal").select("dni, apellidos_nombres") \
            .ilike("apellidos_nombres", f"%{query}%") \
            .execute()

        return jsonify(resultado.data)
    
    return jsonify([])

