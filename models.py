from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

#Configuración de la base de datos y definición del modelo de usuario 
db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ ="usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False, default="cliente")
    fecha_registro = db.Column(db.DateTime, default=datetime.now)

    #Método para establecer la contraseña del usuario, generando un hash seguro 
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    #Método para verificar la contraseña del usuario comparando el hash almacenado con el proporciona
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #Método para verificar si el usuario tiene el rol de administrador 
    def es_admin(self):
        return self.rol == "admin"

    #Método para imprimir un objeto dela clase usuario 
    def __repr__(self):
        return f"<Usuario {self.nombre}>"

class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    precio_base = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    imagen = db.Column(db.String(255), nullable=True)

    #Columnas para ProductoFisico
    peso_kg = db.Column(db.Float, nullable=True)
    costo_envio_por_kg = db.Column(db.Float, nullable=True)

    #Columnas para ProductoDigital
    licencia = db.Column(db.String(100), nullable=True)

    #Columnas para ProductoPerecible
    dias_para_vencer = db.Column(db.Integer, nullable=True)

    #Columna que le dice a la base de datos que tipo de productos es, para poder diferenciar entre Prod
    tipo = db.Column(db.String(30))

    #__mapper permite a SQLAl mapear la clase Producto a la tabla productos en las base de datos y 
    __mapper_args__ = {
        'polymorphic_identity': 'producto',
        'polymorphic_on': tipo
    }

    def precio_final(self):
        return self.precio_base

    def ficha(self):
        return f"Producto: {self.nombre}, Precio: {self.precio_final()}, Stock: {self.stock}, Activo: {self.activo}"

    def __repr__(self):
        return f"<Producto {self.nombre}>"

class ProductoFisico(Producto):
    __mapper_args__ = {"polymorphic_identity": "fisico"}

    def precio_final(self):
        envio = (self.peso_kg or 0) * (self.costo_envio_por_kg or 0)
        return self.precio_base + envio


class ProductoDigital(Producto):
    __mapper_args__ = {"polymorphic_identity": "digital"}

    MULTIPLICADORES = {
        "personal": 1.0,
        "comercial": 2.5,
        "educativa": 0.6,
    }

    def precio_final(self):
        multiplicador = self.MULTIPLICADORES.get(self.licencia, 1.0)
        return self.precio_base * multiplicador


class ProductoPerecible(Producto):
    __mapper_args__ = {"polymorphic_identity": "perecible"}

    def precio_final(self):
        dias = self.dias_para_vencer
        if dias is None:
            return self.precio_base
        if dias <= 3:
            return self.precio_base * 0.50
        elif dias <= 7:
            return self.precio_base * 0.80
        return self.precio_base