# Tienda Online - Flask + PostgreSQL

## Descripción

Proyecto académico desarrollado con Flask y PostgreSQL.

La aplicación permite gestionar una tienda online con productos físicos, digitales y perecibles. Incluye sistema de usuarios, inicio de sesión, roles, permisos, carrito de compras, gestión de productos e imágenes.

El proyecto fue desarrollado siguiendo las actividades de las Semanas 1, 2 y 3, además de mejoras adicionales de imágenes y diseño.

---

## Funcionalidades

- Registro de usuarios.
- Inicio y cierre de sesión.
- Contraseñas almacenadas de forma segura mediante hash.
- Roles de usuario:
  - Administrador.
  - Cliente.
- Control de permisos.
- Creación de productos físicos.
- Creación de productos digitales.
- Creación de productos perecibles.
- Edición de productos.
- Desactivación de productos.
- Catálogo de productos.
- Vista de detalle de cada producto.
- Carrito de compras.
- Agregar productos al carrito.
- Quitar productos del carrito.
- Cálculo automático de subtotal y total.
- Subida de imágenes de productos.
- Cambio de imágenes mediante edición.
- Diseño responsive con Bootstrap.
- Estilos personalizados con CSS.

---

## Tecnologías utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- pgAdmin
- HTML
- CSS
- Bootstrap
- Werkzeug
- Git
- GitHub

---

## Estructura del proyecto

```text
tienda_online/
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── uploads/
│   │   └── imágenes de productos
│   │
│   └── capturas/
│       ├── catalogo.png
│       ├── detalle.png
│       └── carrito.png
│
├── templates/
│   ├── base.html
│   ├── carrito.html
│   ├── detalle.html
│   ├── editar.html
│   ├── index.html
│   ├── login.html
│   ├── nuevo_digital.html
│   ├── nuevo_fisico.html
│   ├── nuevo_perecible.html
│   └── registro.html
│
├── app.py
├── auth.py
├── config.py
├── init_db.py
├── models.py
├── requirements.txt
├── .gitignore
└── README.md
