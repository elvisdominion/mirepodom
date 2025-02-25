from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import supabase
from datetime import datetime

vehicular_bp = Blueprint('vehicular', __name__)

@vehicular_bp.route('/')
def vehicular():
    return render_template('vehicular.html', title="Ingreso Vehicular")

@vehicular_bp.route('/registrar', methods=['POST'])
def registrar_vehiculo():
    placa = request.form.get('placa')
    if placa:
        # Registrar el ingreso del vehículo en Supabase
        supabase.table("ingresos_vehiculares").insert({
            "placa": placa,
            "fecha_hora_ingreso": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }).execute()
        flash(f"🚗 Ingreso registrado para el vehículo con placa {placa}.", "success")
    else:
        flash("❌ La placa es obligatoria.", "danger")
    return redirect(url_for('vehicular.vehicular'))
