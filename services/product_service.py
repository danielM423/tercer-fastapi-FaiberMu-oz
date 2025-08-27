from typing import List, Optional
from datetime import datetime
from models.product_models import ProductCreate, ProductUpdate

# Base de datos simulada (en memoria)
products_db = [
    {
        "id": 1,
        "name": "Laptop Gaming",
        "price": 1500.0,
        "stock": 10,
        "description": "Laptop para gaming de alta gama",
        "created_at": datetime.now()
    },
    {
        "id": 2,
        "name": "Mouse Inalámbrico",
        "price": 45.0,
        "stock": 50,
        "description": "Mouse ergonómico inalámbrico",
        "created_at": datetime.now()
    }
]

class ProductService:

    @staticmethod
    def get_all_products() -> List[dict]:
        return products_db

    @staticmethod
    def get_product_by_id(product_id: int) -> Optional[dict]:
        return next((p for p in products_db if p["id"] == product_id), None)

    @staticmethod
    def create_product(product_data: ProductCreate) -> dict:
        # Evitar duplicados
        if any(p["name"].lower() == product_data.name.lower() for p in products_db):
            raise ValueError(f"Ya existe un producto con el nombre '{product_data.name}'")

        new_id = max([p["id"] for p in products_db], default=0) + 1
        new_product = {
            "id": new_id,
            "name": product_data.name,
            "price": product_data.price,
            "stock": product_data.stock,
            "description": product_data.description,
            "created_at": datetime.now()
        }
        products_db.append(new_product)
        return new_product

    @staticmethod
    def update_product(product_id: int, product_data: ProductUpdate) -> Optional[dict]:
        for i, product in enumerate(products_db):
            if product["id"] == product_id:
                product.update({k: v for k, v in product_data.dict().items() if v is not None})
                products_db[i] = product
                return product
        return None

    @staticmethod
    def delete_product(product_id: int) -> bool:
        for i, product in enumerate(products_db):
            if product["id"] == product_id:
                products_db.pop(i)
                return True
        return False
