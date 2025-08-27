from fastapi import FastAPI, HTTPException, Query, Request, status
from models.product_models import Product, ProductCreate
from data.products_data import products
from datetime import datetime
import logging
from fastapi.middleware.cors import CORSMiddleware
from routers.products import router as products_router
from typing import List, Optional
from fastapi.responses import JSONResponse
from app.exceptions import BookNotFoundError, DuplicateISBNError
from app.utils import create_success_response, create_error_response

# ===============================
# Configuración de la aplicación
# ===============================
app = FastAPI(
    title="Mi API Organizada",
    description="API de productos con estructura profesional",
    version="1.0.0"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# Configuración de Logging
# ===============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ===============================
# Manejo de Excepciones Personalizadas
# ===============================
@app.exception_handler(BookNotFoundError)
async def book_not_found_handler(request: Request, exc: BookNotFoundError):
    return JSONResponse(
        status_code=404,
        content=create_error_response(
            message=str(exc),
            status_code=404,
            details={"type": "BookNotFoundError"}
        )
    )

@app.exception_handler(DuplicateISBNError)
async def duplicate_isbn_handler(request: Request, exc: DuplicateISBNError):
    return JSONResponse(
        status_code=400,
        content=create_error_response(
            message=str(exc),
            status_code=400,
            details={"type": "DuplicateISBNError"}
        )
    )

# ===============================
# Rutas base
# ===============================
@app.get("/health")
def health_check():
    return create_success_response("API funcionando correctamente")

@app.get("/")
def read_root():
    return create_success_response("Bienvenido a la API de Productos")

# ===============================
# Rutas de Productos
# ===============================
@app.get("/products")
def list_products(
    skip: int = 0,
    limit: int = Query(10, le=50),
    min_price: float = 0.0,
    max_price: float = 999999.0
):
    logger.info("Listando productos con filtros y paginación")
    filtered = [
        p for p in products
        if p["price"] >= min_price and p["price"] <= max_price
    ]
    return create_success_response(
        message="Lista de productos obtenida exitosamente",
        data={"products": filtered[skip: skip + limit]}
    )

@app.get("/products/{product_id}")
def get_product(product_id: int):
    logger.info(f"Buscando producto con ID: {product_id}")

    if product_id <= 0:
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                message="El ID debe ser mayor a 0",
                status_code=400,
                details={"provided_id": product_id, "min_id": 1}
            )
        )

    for product in products:
        if product["id"] == product_id:
            return create_success_response(
                message="Producto encontrado",
                data={"product": product}
            )

    raise HTTPException(
        status_code=404,
        detail=create_error_response(
            message="Producto no encontrado",
            status_code=404,
            details={"requested_id": product_id}
        )
    )

@app.post("/products")
def create_product(product: ProductCreate):
    for existing in products:
        if existing["name"].lower() == product.name.lower():
            raise HTTPException(
                status_code=400,
                detail=create_error_response(
                    message="El producto ya existe",
                    status_code=400,
                    details={"duplicate_name": product.name}
                )
            )

    new_id = max([p["id"] for p in products], default=0) + 1
    new_product = product.dict()
    new_product["id"] = new_id
    products.append(new_product)

    return create_success_response(
        message="Producto creado exitosamente",
        data={"product": new_product}
    )

@app.put("/products/{product_id}")
def update_product(product_id: int, updated: ProductCreate):
    for product in products:
        if product["id"] == product_id:
            product.update(updated.dict())
            return create_success_response(
                message="Producto actualizado exitosamente",
                data={"product": product}
            )

    raise HTTPException(
        status_code=404,
        detail=create_error_response(
            message="Producto no encontrado",
            status_code=404,
            details={"requested_id": product_id}
        )
    )

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for i, product in enumerate(products):
        if product["id"] == product_id:
            deleted = products.pop(i)
            return create_success_response(
                message="Producto eliminado exitosamente",
                data={"product": deleted}
            )

    raise HTTPException(
        status_code=404,
        detail=create_error_response(
            message="Producto no encontrado",
            status_code=404,
            details={"requested_id": product_id}
        )
    )

@app.get("/products/search")
def search_products(
    name: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
) -> List[dict]:
    """Buscar productos por nombre y rango de precio"""
    try:
        results = products.copy()

        if name:
            name_lower = name.lower().strip()
            if len(name_lower) < 2:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=create_error_response(
                        message="El término de búsqueda debe tener al menos 2 caracteres",
                        status_code=400
                    )
                )
            results = [p for p in results if name_lower in p["name"].lower()]

        if min_price is not None:
            if min_price < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=create_error_response(
                        message="El precio mínimo no puede ser negativo",
                        status_code=400
                    )
                )
            results = [p for p in results if p["price"] >= min_price]

        if max_price is not None:
            if max_price < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=create_error_response(
                        message="El precio máximo no puede ser negativo",
                        status_code=400
                    )
                )
            results = [p for p in results if p["price"] <= max_price]

        if min_price is not None and max_price is not None and min_price > max_price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=create_error_response(
                    message="El precio mínimo no puede ser mayor al máximo",
                    status_code=400,
                    details={"min_price": min_price, "max_price": max_price}
                )
            )

        return create_success_response(
            message="Resultados de búsqueda",
            data={"products": results}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en búsqueda: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_error_response(
                message="Error interno del servidor",
                status_code=500
            )
        )

# ===============================
# Iniciar servidor
# ===============================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
