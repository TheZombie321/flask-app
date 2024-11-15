from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
CORS(app)

# Configuración de PostgreSQL
db_config = {
    'host': 'dpg-csrk5ql6l47c73fgbmeg-a',
    'dbname': 'movilidad_yfoi',  # Nombre de la base de datos
    'user': 'root',  # Ajusta el usuario si es necesario
    'password': 'rZikjEzjEB3j6a6vIFFsyCCgEjSNPger',  # Ajusta la contraseña si es necesario
    'port': 5432  # Puerto por defecto de PostgreSQL
}


# Ruta para confirmar la conexión a la base de datos
@app.route('/conexion', methods=['GET'])
def test_connection():
    try:
        # Intentar conectar a la base de datos
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")  # Consulta simple para verificar la conexión
        cursor.close()
        conn.close()
        return jsonify({"message": "Conexión exitosa a la base de datos!"}), 200
    except Exception as e:
        # Si ocurre un error, devuelve el mensaje de error
        return jsonify({"message": f"Error al conectar a la base de datos: {str(e)}"}), 500

# Ruta para obtener todos los vehículos
@app.route('/vehiculos', methods=['GET'])
def get_vehiculos():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehiculo")  # Consulta todos los registros de la tabla 'vehiculo'
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convierte los resultados en formato JSON
        data = [{"placa": row[0], "color": row[1], "modelo": row[2], "marca": row[3]} for row in rows]
        return jsonify(data)
    except Exception as e:
        return jsonify({"message": f"Error al obtener vehículos: {str(e)}"}), 500

# Ruta para obtener un vehículo por su placa
@app.route('/vehiculo/<string:placa>', methods=['GET'])
def get_vehiculo(placa):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehiculo WHERE placa = %s", (placa,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row:
            data = {"placa": row[0], "color": row[1], "modelo": row[2], "marca": row[3]}
            return jsonify(data)
        else:
            return jsonify({"message": "Vehículo no encontrado"}), 404
    except Exception as e:
        return jsonify({"message": f"Error al obtener vehículo: {str(e)}"}), 500

# Ruta para agregar un nuevo vehículo
@app.route('/vehiculo', methods=['POST'])
def add_vehiculo():
    data = request.get_json()  # Obtiene los datos del JSON
    placa = data['placa']
    color = data['color']
    modelo = data['modelo']
    marca = data['marca']
    
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO vehiculo (placa, color, modelo, marca)
        VALUES (%s, %s, %s, %s)
        """, (placa, color, modelo, marca))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Vehículo agregado correctamente"}), 201
    except Exception as e:
        return jsonify({"message": f"Error al agregar vehículo: {str(e)}"}), 500

# Ruta para actualizar un vehículo existente
@app.route('/vehiculo/<string:placa>', methods=['PUT'])
def update_vehiculo(placa):
    data = request.get_json()  # Obtiene los datos del JSON
    color = data.get('color')
    modelo = data.get('modelo')
    marca = data.get('marca')
    
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE vehiculo
        SET color = %s, modelo = %s, marca = %s
        WHERE placa = %s
        """, (color, modelo, marca, placa))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Vehículo actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"message": f"Error al actualizar vehículo: {str(e)}"}), 500

# Ruta para eliminar un vehículo por su placa
@app.route('/vehiculo/<string:placa>', methods=['DELETE'])
def delete_vehiculo(placa):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vehiculo WHERE placa = %s", (placa,))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Vehículo eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"message": f"Error al eliminar vehículo: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
