from flask import Flask, request, jsonify, send_from_directory
import json
import smtplib
from email.message import EmailMessage
import openai
import time

app = Flask(__name__, static_folder="static")

# Configuración de OpenAI
client = openai.OpenAI(api_key="TU_API_KEY_AQUI")

def generar_respuesta_ia(mensaje):
    try:
        respuesta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": mensaje}]
        )
        return respuesta.choices[0].message.content.strip()
    except Exception as e:
        return "Lo siento, no puedo procesar tu solicitud en este momento."

def clasificar_pqrs(mensaje):
    if "urgente" in mensaje.lower() or "inmediato" in mensaje.lower():
        return "rojo"
    elif "problema" in mensaje.lower() or "revisión" in mensaje.lower():
        return "amarillo"
    else:
        return "verde"

def enviar_correo(nombre, correo, telefono, mensaje, estado):
    email_user = "tu_correo@gmail.com"
    email_password = "tu_contraseña"
    email_send = "williamgaleanoexterno@gmail.com"
    
    subject = "Nueva PQRS Recibida"
    body = f"""
    Nombre del Cliente: {nombre}
    Gmail del Cliente: {correo}
    Número del Cliente: {telefono}
    Datos: {mensaje}
    Estado: {estado.upper()}
    """
    
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = email_user
    msg["To"] = email_send
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_user, email_password)
            server.send_message(msg)
    except Exception as e:
        print("Error al enviar el correo:", e)

@app.route("/pqrs", methods=["POST"])
def procesar_pqrs():
    try:
        data = request.json
        if not all(k in data for k in ["mensaje", "nombre", "correo", "telefono"]):
            return jsonify({"error": "Faltan datos"}), 400
        
        mensaje = data["mensaje"]
        nombre = data["nombre"]
        correo = data["correo"]
        telefono = data["telefono"]
        
        respuesta_ia = generar_respuesta_ia(mensaje)
        estado = clasificar_pqrs(mensaje)
        enviar_correo(nombre, correo, telefono, mensaje, estado)
        
        return jsonify({"mensaje": respuesta_ia, "estado": estado})
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/register")
def register():
    return send_from_directory("static", "register.html")

@app.route("/dashboard")
def dashboard():
    return send_from_directory("static", "dashboard.html")

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(debug=True)
