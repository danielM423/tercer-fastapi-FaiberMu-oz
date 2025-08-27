# FastAPI Products API

API REST construida con **FastAPI** para la gestión de productos.  
Incluye operaciones CRUD, búsqueda filtrada y respuestas consistentes con manejo de errores.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-green?logo=fastapi)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Instalación rápida

```bash
git clone https://github.com/tu-usuario/fastapi-products-api.git
cd fastapi-products-api/app
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
 Ejecutar la API
bash
Copiar código
uvicorn main:app --reload
Swagger UI -> http://127.0.0.1:8000/docs

ReDoc -> http://127.0.0.1:8000/redoc

 Organización del proyecto
bash
Copiar código
app/
 ├── main.py            # Punto de entrada
 ├── routers/           # Rutas (ej: products)
 ├── models/            # Modelos Pydantic
 ├── data/              # Datos simulados
 ├── utils.py           # Funciones auxiliares
 └── exceptions.py      # Excepciones personalizadas
 Endpoints principales
Método	Ruta	Descripción
GET	/health	Verificar estado de la API
GET	/products	Listar productos
GET	/products/search	Buscar por nombre/precio
POST	/products	Crear producto
PUT	/products/{id}	Actualizar producto
DELETE	/products/{id}	Eliminar producto

 Respuestas de ejemplo
 Éxito:

json
Copiar código
{
  "success": true,
  "message": "Producto creado exitosamente",
  "data": {
    "id": 1,
    "name": "Zapatos deportivos",
    "price": 120.5
  },
  "timestamp": "2025-08-27T14:30:00"
}
 Error:

json
Copiar código
{
  "success": false,
  "error": {
    "message": "Producto no encontrado",
    "status_code": 404,
    "timestamp": "2025-08-27T14:31:00"
  }
}
 Próximos pasos
 Añadir base de datos real (ej. PostgreSQL, SQLite)

 Tests automatizados con pytest

 Dockerfile para despliegue rápido

 Licencia
Proyecto con fines educativos — puedes usarlo y modificarlo libremente.
