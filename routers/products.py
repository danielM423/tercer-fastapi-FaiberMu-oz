from fastapi import APIRouter, HTTPException
from models.product_models import ProductCreate, ProductUpdate
from services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/")
def list_products():
    return ProductService.get_all_products()

@router.get("/{product_id}")
def get_product(product_id: int):
    product = ProductService.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.post("/")
def create_product(product: ProductCreate):
    try:
        return ProductService.create_product(product)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{product_id}")
def update_product(product_id: int, product: ProductUpdate):
    updated = ProductService.update_product(product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return updated

@router.delete("/{product_id}")
def delete_product(product_id: int):
    deleted = ProductService.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado correctamente"}
