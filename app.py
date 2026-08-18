"""
app.py
──────
Punto de entrada de la aplicación. Aquí se crea la app de Flask,
se conecta con la base de datos, y se definen las rutas (URLs).
"""
import os
from uuid import uuid4
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from config import Config
from models import db, Producto, ProductoFisico, ProductoDigital, ProductoPerecible, Usuario
from auth import login_requerido, rol_requerido


app = Flask(__name__)
app.config.from_object(Config)

# Conecta esta app con la instancia de SQLAlchemy definida en models.py
db.init_app(app)


# ==========================================================
# CONFIGURACIÓN PARA SUBIR IMÁGENES
# ==========================================================

UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

EXTENSIONES_PERMITIDAS = {"png", "jpg", "jpeg", "webp"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def extension_permitida(nombre_archivo):
    return (
        "." in nombre_archivo
        and nombre_archivo.rsplit(".", 1)[1].lower() in EXTENSIONES_PERMITIDAS
    )


def guardar_imagen(archivo):

    if archivo is None or archivo.filename == "":
        return None

    if not extension_permitida(archivo.filename):
        return None

    nombre_seguro = secure_filename(archivo.filename)
    extension = nombre_seguro.rsplit(".", 1)[1].lower()

    nombre_unico = f"{uuid4().hex}.{extension}"

    ruta = os.path.join(
        app.config["UPLOAD_FOLDER"],
        nombre_unico
    )

    archivo.save(ruta)

    return nombre_unico


# ==========================================================
# CATÁLOGO
# ==========================================================

@app.route("/")
def inicio():
    productos = Producto.query.filter_by(activo=True).all()
    return render_template("index.html", productos=productos)


# ==========================================================
# DETALLE DEL PRODUCTO
# ==========================================================

@app.route("/producto/<int:producto_id>")
def detalle_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    return render_template("detalle.html", producto=producto)


# ==========================================================
# CREAR PRODUCTO FÍSICO
# ==========================================================

@app.route("/productos/nuevo/fisico", methods=["GET", "POST"])
@rol_requerido("admin")
def nuevo_producto_fisico():

    if request.method == "POST":

        try:

            imagen = request.files.get("imagen")
            nombre_imagen = guardar_imagen(imagen)

            producto = ProductoFisico(
                codigo=request.form["codigo"],
                nombre=request.form["nombre"],
                precio_base=float(request.form["precio_base"]),
                stock=int(request.form["stock"]),
                peso_kg=float(request.form["peso_kg"]),
                costo_envio_por_kg=float(request.form["costo_envio_por_kg"]),
                imagen=nombre_imagen
            )

            db.session.add(producto)
            db.session.commit()

            flash(
                f"Producto físico '{producto.nombre}' creado correctamente.",
                "success"
            )

            return redirect(url_for("inicio"))

        except ValueError:

            flash(
                "Revisa que los campos numéricos tengan valores válidos.",
                "danger"
            )

        except Exception as error:

            db.session.rollback()
            print(error)

            flash(
                "Ocurrió un error. Verifica que el código no esté repetido.",
                "danger"
            )

    return render_template("nuevo_fisico.html")


# ==========================================================
# CREAR PRODUCTO DIGITAL
# ==========================================================

@app.route("/productos/nuevo/digital", methods=["GET", "POST"])
@rol_requerido("admin")
def nuevo_producto_digital():

    if request.method == "POST":

        try:

            imagen = request.files.get("imagen")
            nombre_imagen = guardar_imagen(imagen)

            producto = ProductoDigital(
                codigo=request.form["codigo"],
                nombre=request.form["nombre"],
                precio_base=float(request.form["precio_base"]),
                stock=int(request.form["stock"]),
                licencia=request.form["licencia"],
                imagen=nombre_imagen
            )

            db.session.add(producto)
            db.session.commit()

            flash(
                f"Producto digital '{producto.nombre}' creado correctamente.",
                "success"
            )

            return redirect(url_for("inicio"))

        except ValueError:

            flash(
                "Revisa que los campos numéricos tengan valores válidos.",
                "danger"
            )

        except Exception as error:

            db.session.rollback()
            print(error)

            flash(
                "Ocurrió un error. Verifica que el código no esté repetido.",
                "danger"
            )

    return render_template("nuevo_digital.html")


# ==========================================================
# CREAR PRODUCTO PERECIBLE
# ==========================================================

@app.route("/productos/nuevo/perecible", methods=["GET", "POST"])
@rol_requerido("admin")
def nuevo_producto_perecible():

    if request.method == "POST":

        try:

            imagen = request.files.get("imagen")
            nombre_imagen = guardar_imagen(imagen)

            producto = ProductoPerecible(
                codigo=request.form["codigo"],
                nombre=request.form["nombre"],
                precio_base=float(request.form["precio_base"]),
                stock=int(request.form["stock"]),
                dias_para_vencer=int(request.form["dias_para_vencer"]),
                imagen=nombre_imagen
            )

            db.session.add(producto)
            db.session.commit()

            flash(
                f"Producto perecible '{producto.nombre}' creado correctamente.",
                "success"
            )

            return redirect(url_for("inicio"))

        except ValueError:

            flash(
                "Revisa que los campos numéricos tengan valores válidos.",
                "danger"
            )

        except Exception as error:

            db.session.rollback()
            print(error)

            flash(
                "Ocurrió un error. Verifica que el código no esté repetido.",
                "danger"
            )

    return render_template("nuevo_perecible.html")


# ==========================================================
# EDITAR PRODUCTO
# ==========================================================

@app.route("/productos/<int:producto_id>/editar", methods=["GET", "POST"])
@rol_requerido("admin")
def editar_producto(producto_id):

    producto = Producto.query.get_or_404(producto_id)

    if request.method == "POST":

        try:

            producto.nombre = request.form["nombre"]
            producto.precio_base = float(request.form["precio_base"])
            producto.stock = int(request.form["stock"])

            imagen = request.files.get("imagen")

            print("ARCHIVO RECIBIDO:", imagen)
            print("NOMBRE:", imagen.filename if imagen else "NINGUNO")

            if imagen and imagen.filename != "":
                nombre_imagen = guardar_imagen(imagen)

                if nombre_imagen:
                    producto.imagen = nombre_imagen

            db.session.commit()

            flash(
                f"Producto '{producto.nombre}' actualizado correctamente.",
                "success"
            )

            return redirect(
                url_for(
                    "detalle_producto",
                    producto_id=producto.id
                )
            )

        except ValueError:

            flash(
                "Revisa que los campos numéricos tengan valores válidos.",
                "danger"
            )

        except Exception as error:

            db.session.rollback()
            print(error)

            flash(
                "Ocurrió un error al actualizar el producto.",
                "danger"
            )

    return render_template(
        "editar.html",
        producto=producto
    )

# ==========================================================
# DESACTIVAR PRODUCTO
# ==========================================================

@app.route("/productos/<int:producto_id>/eliminar", methods=["POST"])
@rol_requerido("admin")
def eliminar_producto(producto_id):

    producto = Producto.query.get_or_404(producto_id)

    producto.activo = False

    db.session.commit()

    flash(
        f"Producto '{producto.nombre}' desactivado del catálogo.",
        "success"
    )

    return redirect(url_for("inicio"))


# ==========================================================
# REGISTRO
# ==========================================================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":

        email = request.form["email"].strip().lower()

        if Usuario.query.filter_by(email=email).first():

            flash(
                "Ya existe una cuenta con ese correo.",
                "danger"
            )

            return render_template("registro.html")

        usuario = Usuario(
            nombre=request.form["nombre"],
            email=email,
            rol="cliente"
        )

        usuario.set_password(
            request.form["password"]
        )

        db.session.add(usuario)
        db.session.commit()

        flash(
            "Cuenta creada correctamente. Ya puedes iniciar sesión.",
            "success"
        )

        return redirect(url_for("login"))

    return render_template("registro.html")


# ==========================================================
# LOGIN
# ==========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        usuario = Usuario.query.filter_by(
            email=email
        ).first()

        if usuario and usuario.check_password(password):

            session["usuario_id"] = usuario.id
            session["usuario_nombre"] = usuario.nombre
            session["usuario_rol"] = usuario.rol

            flash(
                f"¡Bienvenido, {usuario.nombre}!",
                "success"
            )

            return redirect(url_for("inicio"))

        else:

            flash(
                "Correo o contraseña incorrectos.",
                "danger"
            )

    return render_template("login.html")


# ==========================================================
# LOGOUT
# ==========================================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(url_for("inicio"))


# ==========================================================
# AGREGAR PRODUCTO AL CARRITO
# ==========================================================

@app.route("/carrito/agregar/<int:producto_id>", methods=["POST"])
@login_requerido
def agregar_carrito(producto_id):

    producto = Producto.query.get_or_404(producto_id)

    carrito = session.get("carrito", {})

    clave = str(producto_id)

    carrito[clave] = carrito.get(clave, 0) + 1

    session["carrito"] = carrito

    flash(
        f"'{producto.nombre}' agregado al carrito.",
        "success"
    )

    return redirect(
        request.referrer or url_for("inicio")
    )


# ==========================================================
# VER CARRITO
# ==========================================================

@app.route("/carrito")
@login_requerido
def ver_carrito():

    carrito = session.get("carrito", {})

    items = []

    total = 0.0

    for clave, cantidad in carrito.items():

        producto = Producto.query.get(int(clave))

        if producto:

            subtotal = producto.precio_final() * cantidad

            total += subtotal

            items.append(
                {
                    "producto": producto,
                    "cantidad": cantidad,
                    "subtotal": subtotal
                }
            )

    return render_template(
        "carrito.html",
        items=items,
        total=total
    )


# ==========================================================
# ELIMINAR PRODUCTO DEL CARRITO
# ==========================================================

@app.route("/carrito/eliminar/<int:producto_id>", methods=["POST"])
@login_requerido
def eliminar_carrito(producto_id):

    carrito = session.get("carrito", {})

    clave = str(producto_id)

    if clave in carrito:

        del carrito[clave]

        session["carrito"] = carrito

        flash(
            "Producto quitado del carrito.",
            "success"
        )

    return redirect(
        url_for("ver_carrito")
    )


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True)